"""Tests for the live-UI bench and the product-check scripts: python -m pytest bench"""

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import bench
import live

BENCH = Path(__file__).resolve().parent
SCRIPTS = BENCH.parent / "skills" / "product-check" / "scripts"
LIVE = sorted(live.load_live())


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_check(case, ws):
    res = subprocess.run([sys.executable, str(BENCH / "cases" / case / "check.py")], cwd=ws, capture_output=True,
                         text=True, check=False)
    return res.returncode, json.loads(res.stdout.splitlines()[0])


def test_live_cases_exist_and_stay_out_of_spec_bench():
    assert len(LIVE) >= 2
    assert not set(LIVE) & set(bench.load_cases())
    for case in LIVE:
        assert (BENCH / "cases" / case / "fixture" / "index.html").exists()


@pytest.mark.parametrize("case", LIVE)
def test_good_report_finds_all_with_evidence(case, tmp_path):
    shutil.copy(BENCH / "cases" / case / "ref" / "good.md", tmp_path / "report.md")
    (tmp_path / "shots").mkdir()
    for i in range(1, 5):
        (tmp_path / "shots" / f"issue-{i}.png").write_bytes(b"png")
    code, res = run_check(case, tmp_path)
    assert code == 0 and res["recall"] == 1.0 and res["recall_evidence"] == 1.0 and res["precision"] == 1.0


@pytest.mark.parametrize("case", LIVE)
def test_good_report_without_screenshots_has_no_evidence(case, tmp_path):
    shutil.copy(BENCH / "cases" / case / "ref" / "good.md", tmp_path / "report.md")
    code, res = run_check(case, tmp_path)
    assert res["recall"] == 1.0 and res["recall_evidence"] == 0.0


@pytest.mark.parametrize("case", LIVE)
def test_bad_report_finds_nothing(case, tmp_path):
    shutil.copy(BENCH / "cases" / case / "ref" / "bad.md", tmp_path / "report.md")
    code, res = run_check(case, tmp_path)
    assert code == 1 and res["recall"] == 0 and res["n_findings"] == 2


@pytest.mark.parametrize("case", LIVE)
def test_empty_workspace_fails(case, tmp_path):
    code, res = run_check(case, tmp_path)
    assert code == 1 and res["missing"] == "no report.md"


def test_findings_split_at_issue_and_top_headings():
    text = "# R\n### ISSUE-1: a\nx\n### ISSUE-2: b\ny\n## Not tested\nz\n## ISSUE-3 c\nw\n"
    blocks = live.findings(text)
    assert len(blocks) == 3 and "Not tested" not in blocks[1] and blocks[2].startswith("## ISSUE-3")


def test_personas_stratified_with_hard_share():
    personas = load("personas")
    ps = personas.sample(20, "Buy milk", optimal=5)
    assert personas.validate(ps) == []
    assert sum(p["hard"] for p in ps) >= 7
    assert {p["lang"] for p in ps} == {"ru", "kk", "en"}
    assert {p["patience"]["label"] for p in ps} == {"hurried", "normal", "patient"}
    hurried = [p for p in ps if p["patience"]["label"] == "hurried"]
    assert all(p["patience"]["steps"] == 6 for p in hurried)
    assert personas.validate([{**ps[0], "hard": False}] * 2) == ["duplicate ids", "fewer than 30% hard personas"]


def write_run(out, variant, pid, hard, urls, texts, end):
    run = out / "runs" / f"{variant}-{pid}"
    (run / "snaps").mkdir(parents=True)
    persona = {"id": pid, "hard": hard, "patience": {"label": "hurried", "steps": 6}}
    (run / "meta.json").write_text(json.dumps({"variant": variant, "persona": persona}))
    lines = []
    for i, (url, text) in enumerate(zip(urls, texts)):
        (run / "snaps" / f"{i:03d}.yml").write_text(text)
        lines.append(json.dumps({"i": i, "cmd": ["click", "e1"], "url": url, "ok": True, "changed": i != 2,
                                 "snapshot": f"snaps/{i:03d}.yml", "note": f"n{i}"}))
    (run / "log.jsonl").write_text("\n".join(lines))
    (run / "end.json").write_text(json.dumps(end))
    (run / "usage.json").write_text(json.dumps({"model": "claude-haiku-5-5", "input": 100000, "output": 10000}))


def test_crowd_aggregate_funnel_direction_and_claims(tmp_path):
    crowd = load("crowd")
    flow = json.loads((BENCH / "cases" / "check-shop" / "flow.json").read_text())
    (tmp_path / "plan.json").write_text(json.dumps({"variants": {"A": "u", "B": "u"}, "flow": flow, "n": 6}))
    base = "http://x/check-shop/"
    for k in range(6):
        write_run(tmp_path, "A", f"p{k}", k % 2 == 0, [base, base + "#/cart", base + "#/confirm"],
                  ["", "", "Confirm your account"], {"outcome": "done" if k == 0 else "quit", "reason": "asked again"})
        write_run(tmp_path, "B", f"p{k}", k % 2 == 0, [base + "?variant=b", base + "?variant=b#/cart",
                  base + "?variant=b#/checkout", base + "?variant=b#/done"], ["", "", "", "Order placed"],
                  {"outcome": "done"})
    crowd.main(["aggregate", "--out", str(tmp_path)])
    res = json.loads((tmp_path / "funnel.json").read_text())
    a, b = res["variants"]["A"], res["variants"]["B"]
    assert a["funnel"] == {"catalog": 6, "cart": 6, "confirm_account": 6, "checkout": 0, "done": 0}
    assert "confirm_account" not in b["funnel"] and b["completed"] == 6
    assert a["dropoff"][0] == ["confirm_account", 6] and a["claims_vs_page"] == 1
    assert res["direction"]["better"] == "B"
    assert res["cost_usd"] == pytest.approx(12 * (0.1 * 0.10 + 0.01 * 0.50))
    assert "| confirm_account | 6 / 6 | - |" in (tmp_path / "funnel.md").read_text()


def test_crowd_plan_writes_prompt_and_bound_act(tmp_path):
    crowd, personas = load("crowd"), load("personas")
    (tmp_path / "p.json").write_text(json.dumps(personas.sample(3, "Buy milk", optimal=5)))
    crowd.main(["plan", "--personas", str(tmp_path / "p.json"), "--flow",
                str(BENCH / "cases" / "check-shop" / "flow.json"), "--variant", "A=http://x/a", "--variant",
                "B=http://x/b", "--out", str(tmp_path / "c")])
    runs = sorted((tmp_path / "c" / "runs").iterdir())
    assert len(runs) == 6
    act = (runs[0] / "act").read_text()
    assert "PC_BUDGET=" in act and "http://x/a" in act and "PC_SESSION=" in act
    prompt = (runs[0] / "prompt.md").read_text()
    assert "oatmilk42" in prompt and "./act end" in prompt


def test_crowd_parse_action_falls_back_to_quit():
    crowd = load("crowd")
    assert crowd.parse_action('ok {"action": "click", "ref": "e3", "think": "go"}')["ref"] == "e3"
    assert crowd.parse_action("I am not sure")["action"] == "quit"
    assert crowd.to_command({"action": "fill", "ref": "e2", "text": "a b"}) == ["fill", "e2", "a b"]


def test_pc_normalises_refs_and_focus():
    pc = load("pc")
    a = '- button "Go" [active] [ref=e3] [cursor=pointer]\n- slider [ref=e4]'
    b = '- button "Go" [ref=e9]\n- slider [ref=e10]'
    assert pc.norm(a) == pc.norm(b)
    assert pc.result("### Result\n42\n### Ran Playwright code\nx") == "42"
