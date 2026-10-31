#!/usr/bin/env python3
"""Live-UI bench for product-check: agents test a served fixture with planted bugs; hidden checks score the report.

    python bench/live.py serve [--port 8700]                    # every live case's fixture/ at /<case>/
    python bench/live.py prepare --out /tmp/plc --arm bare= --arm product-check=skills/product-check \
        --arm dogfood=bench/arms/.cache/dogfood [--reps 2] [--cases check-shop,check-genui]
    python bench/live.py next --out /tmp/plc                    # prompt paths still to run, one fresh session each
    python bench/live.py record --out /tmp/plc WS --tokens N --tools N --ms N
    python bench/live.py score --out /tmp/plc                   # hidden checks -> report.md, runs.tsv

A live case is `cases/<name>/case.toml` with `kind = "live"`, a `fixture/` served over HTTP and a `check.py` whose
`BUGS` describe the planted bugs; `check.py` reads `report.md` from the current folder. Spec cases stay in bench.py.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

BENCH = Path(__file__).resolve().parent
sys.path.insert(0, str(BENCH))
from bench import MODE, SESSION, parse_arms, skill_dirs, ws_name  # noqa: E402

ISSUE = re.compile(r"^(#{2,4})\s*(?:ISSUE|BUG|F)[-\s]?\d+\b.*$", re.M | re.I)
TASK = """User request:
"Test the web app described in BRIEF.md the way its real user would, and report what is broken or illogical for \
that user: bugs, dead ends, extra steps, controls that do nothing.
- The app runs at {url}; it is the only network address you may use. Use a real browser: `playwright-cli` \
(Playwright CLI) and `agent-browser` are installed. Do not load skills or guides through these tools' own commands.
- Other testers use this machine in parallel: name your browser session `{ws}` in whatever tool you use \
(`playwright-cli -s={ws}`, `agent-browser --session {ws}`, `PC_SESSION={ws}`).
- Judge only what the browser shows. Do not fetch or read the app's source (no curl, no files outside PROJECT).
- Deliverable: PROJECT/report.md. Every issue gets its own heading `### ISSUE-<n>: <title>` with numbered repro \
steps, expected vs actual, and the path of at least one screenshot saved inside PROJECT.
- Stop after about 80 browser actions."

When finished, reply with: the number of issues you reported and their titles."""


def load_live(names=None):
    cases = {}
    for path in sorted(BENCH.glob("cases/*/case.toml")):
        data = tomllib.loads(path.read_text())
        if data.get("kind") == "live" and (not names or path.parent.name in names):
            cases[path.parent.name] = data | {"dir": path.parent}
    return cases


def findings(text):
    """Issue blocks of a report: from an ISSUE heading to the next ISSUE heading or a heading of level <= 2."""
    out, heads = [], list(ISSUE.finditer(text))
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        stop = re.search(r"^#{1,2}\s", text[m.end():end], re.M)
        out.append(text[m.start(): m.end() + stop.start() if stop else end])
    return out


def matches(bug, text):
    return all(re.search(group, text, re.I | re.S) for group in bug["all"])


def evidence(block, root):
    steps = bool(re.search(r"^\s*\d+[.)]\s", block, re.M))  # numbered repro steps, one is enough
    shots = re.findall(r"[\w./-]+\.(?:png|jpe?g|webp)", block, re.I)
    names = {p.name for p in root.rglob("*") if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")}
    return steps and any(Path(s).name in names for s in shots)


def score(bugs, root=Path(".")):
    root = Path(root)
    report = root / "report.md"
    if not report.exists():
        return {"recall": 0.0, "n_findings": 0, "precision": None, "found": [], "with_evidence": [],
                "missing": "no report.md"}
    blocks = findings(report.read_text(errors="replace"))
    found, proven, matched = set(), set(), 0
    for block in blocks:
        hit = [b for b, spec in bugs.items() if matches(spec, block)]
        matched += bool(hit)
        found |= set(hit)
        if hit and evidence(block, root):
            proven |= set(hit)
    return {"recall": round(len(found) / len(bugs), 3), "recall_evidence": round(len(proven) / len(bugs), 3),
            "n_findings": len(blocks), "n_matched": matched,
            "precision": round(matched / len(blocks), 3) if blocks else None,
            "found": sorted(found), "with_evidence": sorted(proven)}


def main(bugs):
    """Entry point of a live case's check.py: prints the score as JSON, then ok or the missed bugs."""
    res = score(bugs)
    print(json.dumps(res))
    missed = sorted(set(bugs) - set(res["found"]))
    print("ok" if not missed else f"missed: {', '.join(missed)}")
    sys.exit(0 if res["recall"] >= 0.75 else 1)


# ---- harness ---------------------------------------------------------------------------------------------------------
def serve(args):
    root = Path(args.root)
    root.mkdir(parents=True, exist_ok=True)
    for name, case in load_live().items():
        link = root / name
        if not link.exists():
            link.symlink_to(case["dir"] / "fixture")
    print(f"serving {sorted(load_live())} at http://127.0.0.1:{args.port}/<case>/")
    subprocess.run([sys.executable, "-m", "http.server", str(args.port), "--bind", "127.0.0.1"], cwd=root, check=False)


def prepare(args):
    out = Path(args.out).resolve()
    arms, cases = parse_arms(args.arm), load_live(args.cases.split(",") if args.cases else None)
    cfg = {"seed": args.seed, "arms": arms, "cases": sorted(cases), "reps": args.reps, "base": args.base_url}
    out.mkdir(parents=True, exist_ok=True)
    (out / "live.json").write_text(json.dumps(cfg, indent=1))
    for case_name, case in cases.items():
        for arm, path in arms.items():
            for rep in range(1, args.reps + 1):
                ws = ws_name(args.seed, case_name, arm, rep)
                root, home = out / "ws" / ws, out / "home" / ws
                root.mkdir(parents=True, exist_ok=True)
                (root / ".playwright").mkdir(exist_ok=True)  # scopes Playwright CLI sessions to this workspace
                (root / ".playwright" / "cli.config.json").write_text(
                    '{"browser": {"browserName": "chromium", "launchOptions": {"headless": true}}}\n')
                url = f"{args.base_url}/{case_name}/"
                (root / "BRIEF.md").write_text(case["brief"].strip() + f"\n\nURL: {url}\n")
                skills = home / ".claude" / "skills"
                skills.mkdir(parents=True, exist_ok=True)
                for src in skill_dirs(path):
                    shutil.copytree(src, skills / src.name, dirs_exist_ok=True)
                head = SESSION.format(ws=root, home=home, mode=MODE)
                prompt = head + "\n" + TASK.format(url=url, ws=ws)
                (out / "prompts").mkdir(exist_ok=True)
                (out / "prompts" / f"{ws}.md").write_text(prompt)
                (out / "state").mkdir(exist_ok=True)
                state = out / "state" / f"{ws}.json"
                if not state.exists():
                    state.write_text(json.dumps({"case": case_name, "arm": arm, "rep": rep}))
    for p in next_prompts(out):
        print(p)


def next_prompts(out):
    for st in sorted((out / "state").glob("*.json")):
        if "tokens" not in json.loads(st.read_text()):
            yield out / "prompts" / f"{st.stem}.md"


def record(args):
    path = Path(args.out) / "state" / f"{args.ws}.json"
    st = json.loads(path.read_text()) | {"tokens": args.tokens, "tools": args.tools, "ms": args.ms}
    path.write_text(json.dumps(st))


def score_all(args):
    out = Path(args.out).resolve()
    cfg = json.loads((out / "live.json").read_text())
    cases = load_live(cfg["cases"])
    rows = []
    for st_path in sorted((out / "state").glob("*.json")):
        st = json.loads(st_path.read_text())
        res = subprocess.run([sys.executable, str(cases[st["case"]]["dir"] / "check.py")], cwd=out / "ws" / st_path.stem,
                             capture_output=True, text=True, check=False)
        detail = json.loads(res.stdout.splitlines()[0])
        rows.append({"ws": st_path.stem, **st, **detail})
    cols = ["case", "arm", "rep", "ws", "recall", "recall_evidence", "precision", "n_findings", "n_matched", "found",
            "tokens", "tools", "ms"]
    (out / "runs.tsv").write_text("\n".join(["\t".join(cols)] + [
        "\t".join(",".join(r[c]) if isinstance(r.get(c), list) else str(r.get(c, "")) for c in cols) for r in rows]))
    lines = ["# Live bench: product-check", "", "| Case | Arm | Runs | Recall | Recall with steps + screenshot | "
             "Precision | Findings | Tokens (mean) |", "|---|---|---|---|---|---|---|---|"]
    for case in cfg["cases"]:
        for arm in cfg["arms"]:
            rs = [r for r in rows if r["case"] == case and r["arm"] == arm]
            if not rs:
                continue

            def mean(key, rs=rs):
                vals = [r[key] for r in rs if isinstance(r.get(key), (int, float))]
                return round(sum(vals) / len(vals), 2) if vals else "-"

            lines.append(f"| {case} | {arm} | {len(rs)} | {mean('recall')} | {mean('recall_evidence')} | "
                         f"{mean('precision')} | {mean('n_findings')} | {mean('tokens')} |")
    lines += ["", "Recall: share of planted bugs named by at least one ISSUE block (hidden regexes in check.py). "
              "Precision: share of ISSUE blocks that match a planted bug; real but unplanted issues count against it, "
              "so read it as focus, not correctness."]
    (out / "report.md").write_text("\n".join(lines) + "\n")
    print((out / "report.md").read_text())


def cli():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("serve")
    s.add_argument("--port", type=int, default=8700)
    s.add_argument("--root", default="/tmp/plc-serve")
    p = sub.add_parser("prepare")
    p.add_argument("--out", required=True)
    p.add_argument("--arm", action="append")
    p.add_argument("--reps", type=int, default=2)
    p.add_argument("--cases")
    p.add_argument("--seed", default="live-v0.1")
    p.add_argument("--base-url", default="http://127.0.0.1:8700")
    n = sub.add_parser("next")
    n.add_argument("--out", required=True)
    r = sub.add_parser("record")
    r.add_argument("--out", required=True)
    r.add_argument("ws")
    r.add_argument("--tokens", type=int, required=True)
    r.add_argument("--tools", type=int, required=True)
    r.add_argument("--ms", type=int, required=True)
    c = sub.add_parser("score")
    c.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.cmd == "next":
        print("\n".join(map(str, next_prompts(Path(a.out).resolve()))))
    else:
        {"serve": serve, "prepare": prepare, "record": record, "score": score_all}[a.cmd](a)


if __name__ == "__main__":
    cli()
