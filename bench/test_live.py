"""Tests for the live-UI bench and the product-check scripts: python -m pytest bench"""

import importlib.util
import json
import re
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


PW_SNAP = """- banner [ref=e2]:
  - link [ref=e3] [cursor=pointer]:
    - /url: "#/"
    - strong [ref=e4]: Pantry
  - link "Cart (2)" [ref=e6] [cursor=pointer]:
- main [ref=e7]:
  - heading "Your cart" [level=1] [ref=e26]
  - generic [ref=e29]: Oat milk 1 L
  - textbox "Promo code" [ref=e30]
  - button "Checkout" [ref=e31] [cursor=pointer]: Checkout
"""
AB_SNAP = """- link "Pantry" [ref=e1]
- heading "Your cart" [level=1, ref=e2]
  - StaticText "Oat milk 1 L"
- textbox "Promo code" [ref=e5]
- button "Checkout" [ref=e7]
"""


def answers(op="click", op_conf=0.95, click="e31", click_conf=0.9, done=0.01, quit_=0.01, confusion=0.1, **extra):
    return {"op": {"choice": op, "confidence": op_conf, "probabilities": {op: op_conf, "back": 1 - op_conf}},
            "click": {"choice": click, "confidence": click_conf, "probabilities": {click: 1.0}},
            "done": {"noul": done}, "quit": {"noul": quit_}, "confusion": {"score": confusion},
            "why": {"choice": "stuck"}, **extra}


def test_d1_reads_controls_and_text_from_both_engines():
    d1 = load("d1")
    pw, ab = d1.controls(PW_SNAP), d1.controls(AB_SNAP)
    assert [(c["role"], c["name"]) for c in pw] == [("link", "Pantry"), ("link", "Cart (2)"), ("textbox", "Promo code"),
                                                    ("button", "Checkout")]
    assert [c["ref"] for c in ab] == ["e1", "e5", "e7"]
    assert "Your cart" in d1.page_text(PW_SNAP) and "Oat milk 1 L" in d1.page_text(AB_SNAP)
    qs, clicks, types = d1.policy(PW_SNAP, with_image=True)
    assert set(qs["click"]["criteria"]) == {"e3", "e6", "e31"} and [t["ref"] for t in types] == ["e30"]
    assert "type" in qs["op"]["criteria"] and {"unlisted", "screen", "main"} <= set(qs)
    assert "seen_e31" in d1.vision(clicks, each=True) and "seen_e31" not in d1.vision(clicks)


def test_d1_route_escalates_by_rule():
    d1 = load("d1")
    _, clicks, types = d1.policy(PW_SNAP)
    route = lambda a, **k: d1.route(a, clicks, types, **k)  # noqa: E731
    assert route(answers()) == ("d1", {"action": "click", "ref": "e31"})
    assert route(answers(), last_changed=False)[0] == "sonnet"
    assert d1.route(answers(), [], [])[0] == "sonnet"
    assert route(answers(confusion=2.7))[0] == "sonnet"
    assert route(answers(done=0.95)) == ("d1", {"action": "done"})
    assert route(answers(quit_=0.9)) == ("d1", {"action": "quit", "why": "stuck"})
    assert route(answers(quit_=0.5))[0] == "haiku"
    assert route(answers(op_conf=0.4))[0] == "haiku"
    assert route(answers(op="type", op_conf=1.0))[0] == "haiku"
    assert route(answers(click_conf=0.3))[0] == "haiku"
    assert route(answers(unlisted={"noul": 0.9}))[0] == "haiku"
    assert route(answers(screen={"choice": "error", "confidence": 0.9}))[0] == "haiku"


def test_d1_samples_by_probability_not_argmax():
    import random

    d1 = load("d1")
    rng = random.Random(1)
    draws = [d1.sample({"choice": "a", "probabilities": {"a": 0.7, "b": 0.3}}, rng) for _ in range(400)]
    assert 80 < draws.count("b") < 160
    tail = {"choice": "a", "probabilities": {"a": 0.94, "b": 0.05, "c": 0.01}}
    assert {d1.sample(tail, rng) for _ in range(400)} == {"a"}


def test_d1_ask_sends_data_url_and_model(monkeypatch):
    d1 = load("d1")
    sent = {}

    class Resp:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return json.dumps({"answers": {"q": {"noul": 0.9}}, "usage": {"input_tokens": 1000}}).encode()

    def fake(req, timeout):
        sent.update(json.loads(req.data))
        return Resp()

    monkeypatch.setenv("LIQUID_AI_API_KEY", "k")
    monkeypatch.setattr(d1.urllib.request, "urlopen", fake)
    ans, usage = d1.ask(None, {"q": {"type": "noul", "instructions": "?"}}, images=[b"\xff\xd8\xff\xe0jpeg"])
    assert sent["model"] == "d1-ultra" and sent["images"][0].startswith("data:image/jpeg;base64,")
    assert ans["q"]["noul"] == 0.9 and usage["cost"] == pytest.approx(1000 / 1e6 * d1.PRICE_IN)


def test_pc_translates_commands_for_agent_browser(monkeypatch):
    pc = load("pc")
    calls = []
    eng = pc.AgentBrowser("s")
    monkeypatch.setattr(eng, "cli", lambda *a, **k: calls.append(a) or (True, {"success": True}))
    eng.act(["click", "e12"])
    eng.act(["go-back"])
    eng.act(["fill", "@e3", "e3 text"])
    assert calls == [("click", "@e12"), ("back",), ("fill", "@e3", "e3 text")]
    pw = pc.Playwright("s")
    monkeypatch.setattr(pw, "cli", lambda *a, **k: calls.append(a) or (True, ""))
    pw.act(["click", "@e12"])
    assert calls[-1] == ("click", "e12")


def test_crowd_plan_mixed_binds_auto_engine_and_look(tmp_path):
    crowd, personas = load("crowd"), load("personas")
    (tmp_path / "p.json").write_text(json.dumps(personas.sample(2, "Buy milk", optimal=5)))
    crowd.main(["plan", "--personas", str(tmp_path / "p.json"), "--flow",
                str(BENCH / "cases" / "check-shop" / "flow.json"), "--variant", "A=http://x/a", "--out",
                str(tmp_path / "c"), "--engine", "agent-browser"])
    run = sorted((tmp_path / "c" / "runs").iterdir())[0]
    act, prompt = (run / "act").read_text(), (run / "prompt.md").read_text()
    assert "PC_ENGINE=agent-browser" in act and "PC_LOOK=1" in act and "crowd.py auto" in act
    assert "./act auto" in prompt and "screen: <path>" in prompt
    crowd.main(["plan", "--personas", str(tmp_path / "p.json"), "--flow",
                str(BENCH / "cases" / "check-shop" / "flow.json"), "--variant", "A=http://x/a", "--out",
                str(tmp_path / "h"), "--driver", "haiku", "--no-look"])
    run = sorted((tmp_path / "h" / "runs").iterdir())[0]
    assert "./act auto" not in (run / "prompt.md").read_text() and "PC_LOOK" not in (run / "act").read_text()


def test_crowd_aggregate_counts_tiers_and_d1_cost(tmp_path):
    crowd = load("crowd")
    flow = json.loads((BENCH / "cases" / "check-shop" / "flow.json").read_text())
    (tmp_path / "plan.json").write_text(json.dumps({"variants": {"A": "u"}, "flow": flow, "n": 1, "driver": "mixed"}))
    base = "http://x/check-shop/"
    write_run(tmp_path, "A", "p0", True, [base, base + "#/cart", base + "#/checkout", base + "#/done"],
              ["", "", "", "Order placed"], {"outcome": "done"})
    run = tmp_path / "runs" / "A-p0"
    log = [json.loads(line) for line in (run / "log.jsonl").read_text().splitlines()]
    for e, tier in zip(log, [None, "d1", "d1", "haiku"]):
        e["tier"] = tier
    (run / "log.jsonl").write_text("\n".join(json.dumps(e) for e in log))
    asks = [{"tier": "d1", "decision": {"action": "click"}, "cost_usd": 0.00005},
            {"tier": "sonnet", "decision": {"reason": "x"}, "cost_usd": 0.00005},
            {"tier": "d1", "decision": {"action": "done"}, "cost_usd": 0.00005}]
    (run / "d1.jsonl").write_text("\n".join(json.dumps(a) for a in asks))
    crowd.main(["aggregate", "--out", str(tmp_path)])
    res = json.loads((tmp_path / "funnel.json").read_text())
    assert res["steps_by_tier"] == {"d1": 3, "haiku": 1, "sonnet": 0} and res["d1_asked_for_sonnet"] == 1
    assert res["cost_d1_usd"] == pytest.approx(0.00015)
    assert res["cost_usd"] == pytest.approx(round(0.1 * 0.10 + 0.01 * 0.50 + 0.00015, 4))
    assert "d1 3 (75%)" in (tmp_path / "funnel.md").read_text()


class FakeCDP:
    """Records raw CDP calls of pc.CDP; page expressions answer from `targets`."""

    def __init__(self, targets=None, history=(0, 2)):
        self.calls, self.evals, self.targets, self.history = [], [], targets or {}, history

    def call(self, method, params=None, timeout=60):
        self.calls.append((method, params or {}))
        if method == "Page.getNavigationHistory":
            i, n = self.history
            return {"currentIndex": i, "entries": [{"id": 100 + k} for k in range(n)]}
        return {}

    def eval(self, expr, timeout=60):
        self.evals.append(expr)
        ref = next((r for r in self.targets if f'"{r}"' in expr), None)
        if expr.startswith("(ref =>") and "scrollIntoView" in expr:
            return self.targets.get(ref) or {"error": f"Ref {ref} not found in the current page snapshot."}
        if "values" in expr:
            return {"selected": ["Today"]}
        return True


def fake_cdp(monkeypatch, **kw):
    pc = load("pc")
    eng = pc.CDP("s")
    fake = FakeCDP(**kw)
    monkeypatch.setattr(eng, "call", fake.call)
    monkeypatch.setattr(eng, "eval", fake.eval)
    return pc, eng, fake


BOX = {"x": 50, "y": 20, "w": 80, "h": 30, "top": 5, "left": 10, "disabled": False, "checked": False,
       "editable": False}


def test_cdp_translates_commands_to_devtools_calls(monkeypatch):
    pc, eng, fake = fake_cdp(monkeypatch, targets={"e12": BOX, "e3": {**BOX, "editable": True},
                                                   "e5": {**BOX, "checked": True}})
    assert eng.act(["click", "@e12"])[0]
    assert [(m, p.get("type"), p.get("x")) for m, p in fake.calls] == [
        ("Input.dispatchMouseEvent", "mouseMoved", 50), ("Input.dispatchMouseEvent", "mousePressed", 50),
        ("Input.dispatchMouseEvent", "mouseReleased", 50)]
    fake.calls.clear()
    assert eng.act(["fill", "e3", "aigerim@example.com"])[0]
    assert fake.calls == [("Input.insertText", {"text": "aigerim@example.com"})] and "el.focus()" in fake.evals[-1]
    ok, error, _ = eng.act(["fill", "e12", "x"])
    assert not ok and "not an <input>" in error
    fake.calls.clear()
    eng.act(["check", "e5"])  # already checked: nothing to click
    eng.act(["press", "Enter"])
    assert [p["type"] for _, p in fake.calls] == ["keyDown", "keyUp"] and fake.calls[0][1]["text"] == "\r"
    fake.calls.clear()
    eng.act(["go-back"])  # first history entry: nothing to go back to
    assert [m for m, _ in fake.calls] == ["Page.getNavigationHistory"]
    ok, error, _ = eng.act(["click", "e99"])
    assert not ok and "not found" in error
    ok, error, _ = eng.act(["drag", "e1", "e2"])
    assert not ok and "unknown command" in error
    assert eng.act(["select", "e12", "Today"])[0] and '["Today"]' in fake.evals[-1]


def test_cdp_go_back_and_disabled(monkeypatch):
    _, eng, fake = fake_cdp(monkeypatch, targets={"e1": {**BOX, "disabled": True}}, history=(1, 2))
    eng.act(["go-back"])
    assert fake.calls[-1] == ("Page.navigateToHistoryEntry", {"entryId": 100})
    ok, error, _ = eng.act(["click", "e1"])
    assert not ok and error == "element is disabled"
    covered = {**BOX, "covered": '<div class="modal"> intercepts pointer events'}
    _, eng, _ = fake_cdp(monkeypatch, targets={"e2": covered})
    assert "intercepts pointer events" in eng.act(["click", "e2"])[1]


def test_cdp_key_events():
    cdp = load("cdp")
    down, up = cdp.key_events("Control+a")
    assert down["type"] == "rawKeyDown" and "text" not in down and down["modifiers"] == 2 and up["type"] == "keyUp"
    down, _ = cdp.key_events("Shift+Tab")
    assert down["modifiers"] == 8 and down["code"] == "Tab"
    assert cdp.key_events("x")[0]["text"] == "x" and cdp.key_events("Space")[0]["key"] == " "
    with pytest.raises(ValueError):
        cdp.key_events("Hyper")


CDP_NODES = [
    {"d": 0, "role": "generic", "name": "", "ref": "e1", "attrs": []},
    {"d": 1, "role": "banner", "name": "", "ref": "e2", "attrs": []},
    {"d": 2, "role": "link", "name": "Pantry", "ref": "e3", "attrs": [], "url": "#/"},
    {"d": 2, "text": "Hi, Aigerim"},
    {"d": 2, "role": "link", "name": "Cart (2)", "ref": "e7", "attrs": ["active"], "url": "#/cart"},
    {"d": 1, "role": "main", "name": "", "ref": "e8", "attrs": []},
    {"d": 2, "role": "heading", "name": "Your cart", "ref": "e26", "attrs": ["level=1"]},
    {"d": 2, "role": "generic", "name": "", "ref": "e32", "attrs": [], "tail": "1"},
    {"d": 2, "role": "strong", "name": "", "ref": "e43", "attrs": [], "tail": "Total: 1 940 ₸"},
    {"d": 2, "role": "textbox", "name": "Promo code", "ref": "e30", "attrs": [], "placeholder": "e.g. FRESH10"},
    {"d": 2, "role": "textbox", "name": "Say \"hi\"", "ref": "e33", "attrs": [], "tail": "abc"},
    {"d": 2, "role": "combobox", "name": "Delivery time", "ref": "e34", "attrs": []},
    {"d": 3, "role": "option", "name": "As soon as possible", "attrs": ["selected"]},
    {"d": 2, "role": "button", "name": "Add Oat milk to cart", "ref": "e31", "attrs": [], "tail": "Add to cart"},
]


def test_cdp_snapshot_reads_like_playwright():
    cdp, d1, pc = load("cdp"), load("d1"), load("pc")
    snap = cdp.yaml(CDP_NODES)
    assert '    - link "Pantry" [ref=e3]:\n      - /url: "#/"\n' in snap and "    - text: Hi, Aigerim\n" in snap
    assert '- generic [ref=e32]: "1"' in snap and '- strong [ref=e43]: "Total: 1 940 ₸"' in snap
    assert '- textbox "Promo code" [ref=e30]:\n      - /placeholder: e.g. FRESH10' in snap
    assert '- heading "Your cart" [level=1] [ref=e26]\n' in snap and '      - option "As soon as possible" [selected]' in snap
    cs = d1.controls(snap)
    assert [(c["role"], c["name"], c["ref"]) for c in cs] == [
        ("link", "Pantry", "e3"), ("link", "Cart (2)", "e7"), ("textbox", "Promo code", "e30"),
        ("textbox", 'Say "hi"', "e33"), ("combobox", "Delivery time", "e34"), ("button", "Add Oat milk to cart", "e31")]
    assert "Your cart" in d1.page_text(snap)
    _, clicks, types = d1.policy(snap)
    assert {c["ref"] for c in clicks} == {"e3", "e7", "e31"} and {t["ref"] for t in types} == {"e30", "e33", "e34"}
    moved = cdp.yaml([{**n, "ref": n["ref"] + "0"} if n.get("ref") else n for n in CDP_NODES])
    assert pc.norm(snap) == pc.norm(moved) and not pc.changes(snap, moved)  # new refs alone are no change


@pytest.fixture()
def shop():
    cdp = load("cdp")
    try:
        cdp.find_chrome()
    except RuntimeError:
        pytest.skip("no Chrome")
    port = 8790 + (hash(str(BENCH)) % 50)
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"],
                           cwd=BENCH / "cases" / "check-shop" / "fixture", stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
    yield f"http://127.0.0.1:{port}/"
    srv.terminate()


def test_cdp_engine_live_on_the_shop(shop, tmp_path, monkeypatch):
    import time

    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("PC_CDP_HOME", str(tmp_path / "h"))
    session = f"t{int(time.time() * 1000) % 100000}"
    pc_cmd = [sys.executable, str(SCRIPTS / "pc.py")]
    env_args = ["--engine", "cdp", "--session", session]

    def pc(*args):
        sub, rest = args[0], list(args[1:])
        out = subprocess.run([*pc_cmd, sub, *env_args, *rest], capture_output=True, text=True, timeout=90,
                             env={**__import__("os").environ, "PC_RUN": str(tmp_path / "run")})
        return out.returncode, out.stdout + out.stderr

    for _ in range(50):  # the http server needs a moment
        if pc("open", shop + "?variant=b")[0] == 0:
            break
        time.sleep(0.1)
    try:
        d1 = load("d1")
        snap = (tmp_path / "run" / "last.json").read_text()
        controls = d1.controls(json.loads(snap)["snap"])
        add = next(c["ref"] for c in controls if c["name"] == "Add Oat milk 1 L to cart")
        code, out = pc("do", "--", "click", add)
        assert code == 0 and "Cart (1)" in out and "Added ✓" in out
        cart = next(c["ref"] for c in d1.controls(json.loads((tmp_path / "run" / "last.json").read_text())["snap"])
                    if c["name"].startswith("Cart"))
        code, out = pc("do", "--", "click", cart)
        assert "#/cart  (changed)" in out and 'textbox "Promo code"' in out
        promo = re.search(r'textbox "Promo code" \[ref=(e\d+)\]', out).group(1)
        code, out = pc("do", "--", "fill", promo, "FRESH10")
        assert "FRESH10" in out
        code, out = pc("do", "--", "click", "e1")  # the page body: nothing happens
        assert "changed: false" in out
        code, out = pc("do", "--", "go-back")
        assert "(changed)" in out
        log = [json.loads(line) for line in (tmp_path / "run" / "log.jsonl").read_text().splitlines()]
        assert all(e["engine"] == "cdp" and e["ms"] > 0 for e in log)
        code, out = pc("look")
        assert code == 0 and "screen:" in out
    finally:
        pc("close")


def test_engine_replay_maps_refs_through_controls():
    import engines

    pw = '- button "Add" [ref=e3]\n- button "Add" [ref=e5]\n- link "Cart (1)" [ref=e6]'
    cdp = '- button "Add" [ref=e14]\n- button "Add" [ref=e18]\n- link "Cart (1)" [ref=e7]'
    assert engines.find(cdp, engines.target(pw, "e5")) == "e18"
    assert engines.find(cdp, engines.target(pw, "e6")) == "e7" and engines.target(pw, "e9") is None
