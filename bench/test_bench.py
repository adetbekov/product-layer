"""Tests for the bench and its hidden checks: python -m pytest bench"""

import json
import shutil
import subprocess
import sys
import types
from pathlib import Path

import pytest
import yaml

import bench
import ux
from report import build

BENCH = Path(__file__).resolve().parent
CASES = sorted(p.name for p in (BENCH / "cases").iterdir() if (p / "case.toml").exists())


def run_check(case, tmp_path, spec=None):
    if spec is not None:
        (tmp_path / "spec").mkdir(exist_ok=True)
        (tmp_path / "spec" / "flow.yaml").write_text(spec)
    res = subprocess.run(
        [sys.executable, str(BENCH / "cases" / case / "check.py"), "P1"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    return res.returncode, res.stdout.strip().splitlines()


def test_six_cases():
    assert len(CASES) >= 6
    for case in CASES:
        steps = bench.load_cases([case])[case]["steps"]
        assert [s["kind"] for s in steps] == ["spec"] * len(steps)


@pytest.mark.parametrize("case", CASES)
def test_reference_good_passes(case, tmp_path):
    code, out = run_check(case, tmp_path, (BENCH / "cases" / case / "ref" / "good.yaml").read_text())
    assert (code, out[-1]) == (0, "ok")
    assert all(v is not False for v in json.loads(out[0]).values())


@pytest.mark.parametrize("case", CASES)
def test_reference_bad_fails(case, tmp_path):
    code, out = run_check(case, tmp_path, (BENCH / "cases" / case / "ref" / "bad.yaml").read_text())
    assert code == 1
    assert sum(v is False for v in json.loads(out[0]).values()) >= 2, out  # bad on several axes, not one typo


@pytest.mark.parametrize("case", CASES)
def test_pristine_workspace_fails(case, tmp_path):
    code, out = run_check(case, tmp_path)
    assert code == 1 and "no spec/flow.yaml" in out[-1]


def spec(**over):
    base = {
        "product": "p",
        "flows": [{"id": "f", "entry": "a", "done": "c"}],
        "screens": [
            {"id": "a", "actions": [{"to": "b"}]},
            {"id": "b", "actions": [{"to": "c", "by": "system"}]},
            {"id": "c", "actions": [{"to": "a"}]},
        ],
    }
    return base | over


def check(tmp_path, data, rules):
    path = tmp_path / "flow.yaml"
    path.write_text(yaml.safe_dump(data))
    return ux.run(rules, path)


def test_system_transitions_cost_no_steps(tmp_path):
    assert check(tmp_path, spec(), {"max_steps": {"f": 1}})["steps"] == []
    assert check(tmp_path, spec(), {"max_steps": {"f": 0}})["steps"] == ["f: 1 steps > 0"]
    assert check(tmp_path, spec(), {"max_steps": {"other": 3}})["steps"] == ["no flow `other`"]


def test_dead_ends_and_unknown_targets(tmp_path):
    data = spec()
    data["screens"][2]["actions"] = []
    data["screens"].append({"id": "lost", "actions": [{"to": "nowhere"}]})
    res = check(tmp_path, data, {})
    assert res["dead_ends"] == ["c has no way out"]
    data["screens"][2]["actions"] = [{"to": "c", "by": "system"}]  # a loop onto itself is no way out either
    assert check(tmp_path, data, {})["dead_ends"] == ["c has no way out"]
    assert "lost -> unknown 'nowhere'" in res["structure"] and "unreachable ['lost']" in res["structure"]
    assert res["steps"] is None  # the case does not use it


def test_broken_yaml_fails_structure_only(tmp_path):
    path = tmp_path / "flow.yaml"
    path.write_text("screens: [unclosed")
    res = ux.run({"max_steps": {"f": 1}}, path)
    assert res["structure"][0].startswith(f"{path} is not valid YAML")
    assert all(v is None for k, v in res.items() if k != "structure")


def test_states_need_real_text(tmp_path):
    data = spec()
    data["screens"][1] |= {"moment": "load", "states": {"loading": "Loading...", "error": "n/a"}}
    assert check(tmp_path, data, {"states": {"load": ["loading", "error"]}})["states"] == ["load lacks ['error']"]
    data["screens"][2] |= {"moment": "load", "states": {"error": "Failed. Retry"}}  # the moment spans two screens
    assert check(tmp_path, data, {"states": {"load": ["loading", "error"]}})["states"] == []
    assert check(tmp_path, data, {"states": {"gone": ["empty"]}})["states"] == ["no moment `gone`"]


def test_render_threshold(tmp_path):
    data = spec()
    for s, (m, r) in zip(data["screens"], [("m1", "text"), ("m2", "block"), ("m3", "text")]):
        s |= {"moment": m, "render": r}
    ref = {"m1": "text", "m2": "block", "m3": "block"}
    assert check(tmp_path, data, {"render": ref, "render_min": 2 / 3})["render"] == []
    assert check(tmp_path, data, {"render": ref})["render"] == ["m3: text != block"]


def test_asks_only_on_the_happy_path_and_per_flow(tmp_path):
    data = spec()
    data["flows"].append({"id": "g", "entry": "c", "done": "a"})
    data["screens"][0]["asks"] = [{"field": "Email"}]
    data["screens"].append({"id": "side", "asks": [{"field": "phone"}], "actions": [{"to": "a"}]})
    data["screens"][2]["actions"].append({"to": "side"})
    assert check(tmp_path, data, {"forbid_asks": ["phone"]})["asks"] == []  # off the happy path
    assert check(tmp_path, data, {"forbid_asks": ["e-?mail"]})["asks"] == ["a asks known `email`"]
    assert check(tmp_path, data, {"forbid_asks": {"g": ["e-?mail"]}})["asks"] == ["a asks known `email`"]
    data["flows"][1]["done"] = "c"
    assert check(tmp_path, data, {"forbid_asks": {"g": ["e-?mail"]}})["asks"] == []
    assert check(tmp_path, data, {"require_asks": ["slot"]})["asks"] == ["never asks /slot/"]


def test_nav_and_min_actions(tmp_path):
    data = spec(nav={"a": ["x"], "b": list("123456")})
    data["screens"][0]["moment"] = "plan"
    res = check(tmp_path, data, {"nav": {"roles": ["a", "b", "c"], "max": 5}, "min_actions": {"plan": 2}})
    assert res["nav"] == ["b: 6 top-level sections > 5", "no nav for `c`"]
    assert res["actions"] == ["plan: 1 ways out < 2"]
    data["screens"][1] |= {"moment": "plan", "actions": [{"to": "c"}, {"to": "a"}]}
    assert check(tmp_path, data, {"min_actions": {"plan": 2}})["actions"] == []


def test_ws_name_is_opaque_and_stable():
    a, b = bench.ws_name(1, "c", "product-layer", 1), bench.ws_name(1, "c", "bare", 1)
    assert a == bench.ws_name(1, "c", "product-layer", 1)
    assert a != b and "product" not in a and "bare" not in b


def test_ai_files_are_excluded():
    assert bench.is_ai("CLAUDE.md") and bench.is_ai(".claude/skills/x/SKILL.md")
    assert not bench.is_ai("spec/flow.yaml")


def test_skill_dirs(tmp_path):
    for name in ("one", "pack/a", "pack/b"):
        (tmp_path / name).mkdir(parents=True)
        (tmp_path / name / "SKILL.md").write_text("---\nname: x\n---\n")
    found = bench.skill_dirs(f"{tmp_path / 'one'},{tmp_path / 'pack'}")
    assert [p.name for p in found] == ["one", "a", "b"]
    assert bench.skill_dirs("") == []
    with pytest.raises(SystemExit):
        bench.skill_dirs(str(tmp_path / "missing"))


def test_default_arms_fall_back_to_the_stub(capsys):
    arms = bench.parse_arms(None)
    assert set(arms) == {"bare", "product-layer"} and arms["bare"] == ""
    if not (BENCH.parent / "skills" / "product-layer" / "SKILL.md").exists():
        assert arms["product-layer"] == str(bench.STUB) and "stub" in capsys.readouterr().err
    with pytest.raises(SystemExit):
        bench.parse_arms(["a=x", "a=y"])


def test_session_sees_only_allowed_secrets(monkeypatch, tmp_path):
    seen = {}

    def fake_sh(cmd, cwd=None, env=None, check=True, timeout=None):
        seen.update(env)
        return types.SimpleNamespace(stdout=json.dumps({"result": "ok", "usage": {}}), stderr="")

    monkeypatch.setattr(bench, "sh", fake_sh)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "k")
    monkeypatch.setenv("GITHUB_TOKEN", "secret")
    bench.claude("hi", tmp_path, tmp_path / "home", None)
    assert seen["HOME"] == str(tmp_path / "home") and seen["ANTHROPIC_API_KEY"] == "k"
    assert "GITHUB_TOKEN" not in seen


def test_agent_driven_cycle_writes_report_and_runs(tmp_path, monkeypatch):
    """prepare -> next -> (a fake agent writes the spec) -> record -> pack -> verdicts -> report, no claude needed."""
    out = tmp_path / "out"
    args = types.SimpleNamespace(
        out=str(out), arm=[f"pl={bench.STUB}", "bare="], only=None, reps=1, cases=["generic-settings"], seed=7
    )
    bench.prepare(args)
    b = bench.Bench(out)
    assert sorted(p.name for p in (out / "home").glob("*/.claude/skills/*")) == ["product-layer"]
    todo = list(b.pending())
    assert len(todo) == 2
    refs = BENCH / "cases" / "generic-settings" / "ref"
    for ws, step in todo:
        prompt = b.prompt(ws, step, "agent")
        assert "SPEC-FORMAT.md" in prompt and str(out / "ws" / ws) in prompt
        arm = b.state(ws)["arm"]
        (out / "ws" / ws / "spec").mkdir()
        shutil.copy(refs / ("good.yaml" if arm == "pl" else "bad.yaml"), out / "ws" / ws / "spec" / "flow.yaml")
        (out / "ws" / ws / "notes.txt").write_text("stray file")
        m = b.record(ws, step["id"], 1000, 3, 60_000, "Wrote spec/flow.yaml. Done?")
        assert m["solved"] == (arm == "pl") and m["out_of_scope"] == 1 and m["questions"] == 1
    assert not list(b.pending())
    prompts = b.pack()
    assert len(prompts) == 2 and "spec/flow.yaml" in prompts[0].read_text()
    snap = prompts[0].parent / prompts[0].name.replace(".prompt.md", "") / "X" / "snapshot"
    assert (snap / "spec" / "flow.yaml").exists() and not (snap / "BRIEF.md").exists()
    for p in prompts:
        amap = json.loads(p.with_name(p.name.replace(".prompt.md", ".map.json")).read_text())
        good = next(k for k, v in amap.items() if v == "pl")
        crit = dict.fromkeys(("success", "flow", "states", "ia", "asks", "fit", "handoff", "scope"), 3)
        scores = {k: {"P1": crit | ({"flow": 5} if k == good else {}), "clarity": 4} for k in "XY"}
        scores["winner"] = {"P1": good, "overall": good}
        p.with_name(p.name.replace(".prompt.md", ".verdict.md")).write_text(
            f"text\n```json\n{json.dumps(scores)}\n```\n"
        )
    text = b.report()
    assert (out / "report.md").read_text() == text and (out / "runs.tsv").exists()
    assert "| Solved, hidden checks | 1/1 | 0/1 |" in text
    assert "| flow | 5 | 3 |" in text and "| **overall wins** | 2 | 0 |" in text
    assert len((out / "runs.tsv").read_text().splitlines()) == 3


def test_only_limits_an_arm_to_its_cases(tmp_path):
    out = tmp_path / "out"
    args = types.SimpleNamespace(
        out=str(out),
        arm=["bare=", f"genui={bench.STUB}"],
        only=["genui=betke-skin-quiz"],
        reps=1,
        cases=["generic-settings", "betke-skin-quiz"],
        seed=7,
    )
    bench.prepare(args)
    b = bench.Bench(out)
    got = sorted((b.state(ws)["case"], b.state(ws)["arm"]) for ws in b.workspaces())
    assert got == [("betke-skin-quiz", "bare"), ("betke-skin-quiz", "genui"), ("generic-settings", "bare")]


def test_report_without_verdicts():
    rows = [
        {
            "ws": "w",
            "case": "c",
            "arm": "a",
            "rep": 1,
            "step": "P1",
            "solved": True,
            "c_steps": True,
            "tokens": 10,
            "ms": 60000,
            "n_steps": 3,
        }
    ]
    text, tsv = build(rows, {}, ["a", "b"])
    assert "No verdicts yet." in text and "| Solved, hidden checks | 1/1 | 0/0 |" in text
    assert tsv.splitlines()[1].split("\t")[:5] == ["w", "c", "a", "1", "P1"]
