"""Step time of the product-check browser engines on the same actions (JEB-2059).

Replays the actions of a finished crowd run (crowd.py plan + sessions) on each engine with no decision maker in the
loop: same URL, device flags, screenshots on (PC_LOOK=1), one fresh browser per persona. Refs differ between
engines, so each ref is mapped through the control it pointed at (role, name, occurrence) in the source snapshot.

    python bench/engines.py --crowd CROWD_DIR --engine playwright --engine cdp --out DIR [--workers 4]

Writes DIR/steps.tsv (one row per command: engine, run, step, command, ms inside pc.py, wall ms of the process,
stage reached) and DIR/engines.md (median and p90 step time, time per persona, replay agreement with the source).
"""

import argparse
import json
import os
import statistics
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "skills" / "product-check" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import crowd  # noqa: E402
import d1  # noqa: E402


def target(snap, ref):
    """(role, name, occurrence) of the control `ref` in a snapshot, or None."""
    cs = d1.controls(snap)
    for c in cs:
        if c["ref"] == ref:
            same = [x for x in cs if (x["role"], x["name"]) == (c["role"], c["name"])]
            return c["role"], c["name"], same.index(c)
    return None


def find(snap, key):
    role, name, k = key
    same = [c for c in d1.controls(snap) if (c["role"], c["name"]) == (role, name)]
    return same[k]["ref"] if k < len(same) else None


def replay(src, engine, out):
    """Replay one source run on `engine`; returns rows for steps.tsv."""
    meta = json.loads((src / "meta.json").read_text())
    log = crowd.read_jsonl(src / "log.jsonl")
    run = out / "runs" / engine / src.name
    run.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "PC_RUN": str(run), "PC_SESSION": f"eng-{engine}-{out.name}-{src.name}".lower(),
           "PC_ENGINE": engine, "PC_LOOK": "1"}
    env.pop("PC_BUDGET", None)
    pc = [sys.executable, str(SCRIPTS / "pc.py")]
    flags = (["--mobile"] if meta["persona"]["device"]["type"] == "mobile" else []) + (
        ["--slow"] if meta["persona"]["device"]["network"] == "slow" else [])
    rows = []

    def call(args):
        t = time.time()
        subprocess.run(pc + args, env=env, capture_output=True, text=True, check=False, timeout=300)
        return round((time.time() - t) * 1000)

    wall = call(["open", meta["url"], *flags])
    rows.append((engine, src.name, 0, "open", crowd.read_jsonl(run / "log.jsonl")[-1]["ms"], wall))
    for prev, e in zip(log, log[1:]):
        if not e.get("ok"):
            continue
        cmd = list(e["cmd"])
        if len(cmd) > 1 and d1.REF.fullmatch(f"[ref={cmd[1]}]"):
            key = target((src / prev["snapshot"]).read_text(), cmd[1])
            now = json.loads((run / "last.json").read_text())["snap"]
            ref = key and find(now, key)
            if not ref:
                rows.append((engine, src.name, e["i"], " ".join(cmd) + " (unmapped)", None, None))
                break
            cmd[1] = ref
        wall = call(["do", "--", *cmd])
        rows.append((engine, src.name, e["i"], " ".join(e["cmd"]), crowd.read_jsonl(run / "log.jsonl")[-1]["ms"], wall))
    call(["close"])
    return rows


def stage(run_dir, flow, variant):
    reached, _ = crowd.stages_reached(run_dir, flow["stages"], variant)
    return reached[-1] if reached else None


def pct(xs, q):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(q * len(xs)))]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--crowd", required=True)
    ap.add_argument("--engine", action="append", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args(argv)
    src, out = Path(a.crowd).resolve(), Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    flow = json.loads((src / "plan.json").read_text())["flow"]
    runs = crowd.runs(src)
    rows = []
    for engine in a.engine:
        t = time.time()
        with ThreadPoolExecutor(a.workers) as pool:
            for r in pool.map(lambda s: replay(s, engine, out), runs):
                rows += r
        print(f"{engine}: {len(runs)} runs in {time.time() - t:.0f} s", file=sys.stderr)
    with open(out / "steps.tsv", "w") as f:
        f.write("engine\trun\tstep\tcommand\tms\twall_ms\n")
        for r in rows:
            f.write("\t".join("" if v is None else str(v) for v in r) + "\n")
    lines = ["| | " + " | ".join(a.engine) + " |", "|---|" + "---|" * len(a.engine)]
    stats = {}
    for engine in a.engine:
        steps = [r for r in rows if r[0] == engine and r[3] != "open" and r[4] is not None]
        opens = [r for r in rows if r[0] == engine and r[3] == "open"]
        per = {}
        for r in rows:
            if r[0] == engine and r[5] is not None:
                per[r[1]] = per.get(r[1], 0) + r[5]
        same = sum(stage(out / "runs" / engine / s.name, flow, json.loads((s / "meta.json").read_text())["variant"])
                   == stage(s, flow, json.loads((s / "meta.json").read_text())["variant"]) for s in runs)
        stats[engine] = {
            "steps": len(steps), "unmapped": sum(r[4] is None for r in rows if r[0] == engine),
            "step median ms (pc.py)": statistics.median(r[4] for r in steps),
            "step p90 ms (pc.py)": pct([r[4] for r in steps], 0.9),
            "step median ms (process wall)": statistics.median(r[5] for r in steps),
            "open median ms (process wall)": statistics.median(r[5] for r in opens),
            "browser time per persona, median s": round(statistics.median(per.values()) / 1000, 1),
            "last stage same as the source run": f"{same} / {len(runs)}",
        }
    for key in stats[a.engine[0]]:
        lines.append(f"| {key} | " + " | ".join(str(stats[e][key]) for e in a.engine) + " |")
    (out / "engines.json").write_text(json.dumps(stats, indent=1))
    (out / "engines.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
