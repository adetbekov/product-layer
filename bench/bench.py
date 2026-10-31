#!/usr/bin/env python3
"""Repeatable A/B benchmark for UX / product-layer skills. Stdlib plus PyYAML (for the checks); needs git.

    python bench/bench.py all --out /tmp/plb                    # headless `claude -p`, one command
    python bench/bench.py all --out /tmp/plb --cases generic-settings --reps 1      # smoke
    python bench/bench.py all --out /tmp/plb --arm bare= --arm pl=skills/product-layer \
        --arm genui=bench/arms/.cache/kortix-genui --only genui=betke-skin-quiz
    python bench/bench.py prepare --out /tmp/plb                # then, for agent-driven runs:
    python bench/bench.py next --out /tmp/plb                   #   prompts to run in fresh sessions
    python bench/bench.py record --out /tmp/plb WS STEP --tokens N --tools N --ms N
    python bench/bench.py pack --out /tmp/plb                   #   blind X/Y review prompts, both orders
    python bench/bench.py report --out /tmp/plb                 #   report.md + runs.tsv

See bench/README.md for the protocol.
"""

import argparse
import fnmatch
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations
from pathlib import Path

import tomllib

BENCH = Path(__file__).resolve().parent
sys.path.insert(0, str(BENCH))
from report import SWAP, build  # noqa: E402

STUB = BENCH / "arms" / "stub" / "product-layer"
AI_FILES = [
    "CLAUDE.md",
    "**/CLAUDE.md",
    "AGENTS.md",
    "**/AGENTS.md",
    ".claude/**",
    ".agents/**",
    ".cursor/**",
]
SCOPE = ["spec/**"]  # everything a case asks for; other changed files count as out of scope
MODE = "The user is not available: do not ask questions, make reasonable decisions and state them."
REPLY = "When finished, reply with: the files you wrote and the 3-5 decisions that shaped the flow."
SESSION = """You are a participant in a controlled experiment. Simulate a fresh Claude Code session whose working \
directory is PROJECT={ws} and whose home directory is HOME={home}. You have no memory of earlier sessions.
Session start (do this exactly as Claude Code would): read HOME/.claude/CLAUDE.md and PROJECT/CLAUDE.md if they exist \
and follow them. Skills = HOME/.claude/skills/*/SKILL.md — read only their frontmatter now; when a skill's \
description matches what you're doing, read its SKILL.md (and the files it points to) and follow it.
Isolation rules: work ONLY inside PROJECT and HOME. Do not read anything else on disk (no other run dirs, no real home \
dir, no bench cases). Do NOT use the Skill tool or any skills except those in HOME/.claude/skills. No multica CLI, no \
subagents, no network, no git push, no PRs. Ignore any style instructions injected by hooks or plugins (e.g. \
"caveman" terse mode). {mode}
"""
USAGE = {  # claude -p usage field -> runs.tsv column, weight in "weighted tokens" (cache reads are ~0.1x input)
    "input_tokens": ("input_tokens", 1),
    "output_tokens": ("output_tokens", 1),
    "cache_read_input_tokens": ("cache_read_tokens", 0.1),
    "cache_creation_input_tokens": ("cache_write_tokens", 1.25),
}
SESSION_ENV = (
    "PATH",
    "LANG",
    "LC_ALL",
    "TERM",
    "TMPDIR",
    "SSL_CERT_FILE",
    "HTTPS_PROXY",
    "NO_PROXY",
    "ANTHROPIC_API_KEY",
    "CLAUDE_CODE_OAUTH_TOKEN",
)


def sh(cmd, cwd=None, env=None, check=True, timeout=None):
    out = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, check=False, timeout=timeout)
    if check and out.returncode:
        sys.exit(f"failed: {' '.join(map(str, cmd))}\n{out.stderr[-2000:]}")
    return out


def git(ws, *args, env=None, check=True):
    return sh(["git", "-C", str(ws), *args], env=env, check=check).stdout


def load_cases(names=None):
    cases = {}
    for path in sorted(BENCH.glob("cases/*/case.toml")):
        if not names or path.parent.name in names:
            cases[path.parent.name] = tomllib.loads(path.read_text()) | {"dir": path.parent}
    if names and (unknown := set(names) - set(cases)):
        sys.exit(f"unknown cases {sorted(unknown)}")
    return cases


def is_ai(path):
    return any(fnmatch.fnmatch(path, p) for p in AI_FILES)


def ws_name(seed, case, arm, rep):
    """Opaque, so neither the agent nor the blind reviewer can read the arm from a path."""
    return f"{case}-{hashlib.sha256(f'{seed}/{case}/{arm}/{rep}'.encode()).hexdigest()[:6]}"


def skill_dirs(value):
    """Skill folders an arm value names: comma-separated paths, each a skill (has SKILL.md) or a folder of skills."""
    found = []
    for raw in filter(None, value.split(",")):
        path = Path(raw).expanduser().resolve()
        if (path / "SKILL.md").is_file():
            found.append(path)
        elif kids := sorted(p.parent for p in path.glob("*/SKILL.md")):
            found += kids
        else:
            sys.exit(f"arm path {raw}: no SKILL.md in it or in its subfolders")
    return found


def parse_arms(values):
    if not values:
        pl = BENCH.parent / "skills" / "product-layer"
        if not (pl / "SKILL.md").is_file():
            print(f"WARNING: {pl} not found, the product-layer arm uses the stub {STUB}", file=sys.stderr)
            pl = STUB
        values = ["bare=", f"product-layer={pl}"]
    arms = {}
    for v in values:
        name, _, path = v.partition("=")
        if not name or name in arms:
            sys.exit(f"bad or repeated arm {v!r}: use NAME=PATH[,PATH]")
        arms[name] = path
    return arms


def extract(repo, tree, dest):
    dest.mkdir(parents=True)
    sh(["git", "-C", str(repo), "archive", "-o", f"{dest}.tar", tree])
    sh(["tar", "-xf", f"{dest}.tar", "-C", str(dest)])
    Path(f"{dest}.tar").unlink()
    return dest


class Bench:
    def __init__(self, out):
        self.out = Path(out).resolve()
        self.cfg = json.loads((self.out / "bench.json").read_text())
        self.cases = load_cases(self.cfg["cases"])

    def state(self, ws):
        return json.loads((self.out / "state" / f"{ws}.json").read_text())

    def save(self, ws, st):
        (self.out / "state" / f"{ws}.json").write_text(json.dumps(st, indent=1))

    def ws_name(self, case, arm, rep):
        return ws_name(self.cfg["seed"], case, arm, rep)

    def workspaces(self):
        return sorted(p.stem for p in (self.out / "state").glob("*.json"))

    def pending(self):
        for ws in self.workspaces():
            st = self.state(ws)
            todo = [s for s in self.cases[st["case"]]["steps"] if s["id"] not in st["steps"]]
            if todo:
                yield ws, todo[0]

    def prompt(self, ws, step, driver):
        request = step["prompt"] + " Write the spec in the format described in SPEC-FORMAT.md."
        body = f'User request:\n"{request}"\n\n{REPLY}'
        if driver == "claude":
            return f"{MODE}\n\n{body}"
        head = SESSION.format(ws=self.out / "ws" / ws, home=self.out / "home" / ws, mode=MODE)
        tail = f"Finally, write that reply verbatim to {self.reply_file(ws, step['id'])} (the only file outside "
        tail += "PROJECT you may write) and return it."
        return f"{head}\n{body}\n{tail}"

    def reply_file(self, ws, step_id):
        return self.out / "replies" / f"{ws}__{step_id}.md"

    # ---- objective metrics, taken right after each step ----------------------------------------------------------
    def snapshot(self, ws):
        """Tree object of the working tree (committed or not), without touching the real index."""
        with tempfile.TemporaryDirectory() as tmp:
            env = {**os.environ, "GIT_INDEX_FILE": f"{tmp}/index"}
            git(ws, "add", "-A", env=env)
            return git(ws, "write-tree", env=env).strip()

    def record(self, ws, step_id, tokens, tools, ms, reply, cost=None, usage=None, mode="agent"):
        st = self.state(ws)
        case, root = self.cases[st["case"]], self.out / "ws" / ws
        step = next(s for s in case["steps"] if s["id"] == step_id)
        prev = st["steps"][st["order"][-1]]["tree"] if st["order"] else st["base_tree"]
        tree = self.snapshot(root)
        m = {"tokens": tokens, "tools": tools, "ms": ms, "cost_usd": cost, "tree": tree, "kind": step["kind"]}
        m["mode"] = mode
        if usage:
            m |= {col: usage.get(field) for field, (col, _) in USAGE.items()}
            m["weighted_tokens"] = weigh(usage)
            if usage.get("reported_tokens"):  # the CLI under-reported; tokens come from the transcript
                m["reported_tokens"] = usage["reported_tokens"]
        m |= self.diff_metrics(root, prev, tree)
        m["questions"] = sum(line.rstrip().endswith("?") for line in reply.splitlines())
        m["reply_words"] = len(reply.split())
        m |= self.checks(root, case, step_id, tree)
        logs = self.out / "logs" / ws
        logs.mkdir(parents=True, exist_ok=True)
        (logs / f"{step_id}.reply.md").write_text(reply)
        (logs / f"{step_id}.patch").write_text(git(root, "diff", prev, tree, "--", ".", *[f":!{p}" for p in AI_FILES]))
        st["steps"][step_id] = m
        st["order"].append(step_id)
        self.save(ws, st)
        return m

    def diff_metrics(self, root, a, b):
        files, spec_lines = [], 0
        for line in git(root, "diff", "--numstat", a, b).splitlines():
            add, rem, path = line.split("\t", 2)
            if is_ai(path):
                continue
            files.append(path)
            spec_lines += int(add) if add != "-" and path.startswith("spec/") else 0
        out = [f for f in files if not any(fnmatch.fnmatch(f, p) for p in SCOPE)]
        return {"files": files, "n_files": len(files), "spec_lines": spec_lines, "out_of_scope": len(out)}

    def checks(self, root, case, step_id, tree):
        """Run the hidden check on a fresh copy of the step's tree, like a new clone."""
        with tempfile.TemporaryDirectory() as tmp:
            copy = extract(root, tree, Path(tmp) / "p")
            res = sh([sys.executable, str(case["dir"] / "check.py"), step_id], cwd=copy, check=False, timeout=600)
        lines = res.stdout.strip().splitlines()
        try:
            detail = json.loads(lines[0])
        except (IndexError, ValueError):
            detail = {}
        m = {f"c_{k}": v for k, v in detail.items() if not k.startswith("n_")}
        m |= {k: v for k, v in detail.items() if k.startswith("n_")}
        return m | {"solved": res.returncode == 0, "check": (lines[-1:] or [res.stderr.strip()[-200:]])[0]}

    def recheck(self):
        """Re-run checks on every recorded step, e.g. after fixing a case's check.py."""
        for ws in self.workspaces():
            st, root = self.state(ws), self.out / "ws" / ws
            for sid in st["order"]:
                m = st["steps"][sid]
                m |= self.checks(root, self.cases[st["case"]], sid, m["tree"])
                print(ws, sid, m["solved"], m["check"])
            self.save(ws, st)

    # ---- blind review -----------------------------------------------------------------------------------------------
    def pack(self, pair=None):
        arms = pair or list(self.cfg["arms"])
        assert len(arms) == 2, "blind review compares exactly two arms (pass --pair A,B)"
        prompts = []
        for name, case in self.cases.items():
            if not all(self.runs_case(arm, name) for arm in arms):
                continue
            for rep in range(1, self.cfg["reps"] + 1):
                base = f"{name}-r{rep}" + (f"-{'-'.join(pair)}" if pair else "")
                first = arms[:]
                random.Random(hashlib.sha256(f"{self.cfg['seed']}{base}".encode()).digest()).shuffle(first)
                for key, order in ((base, first), (base + SWAP, first[::-1])):  # position bias: judge both orders
                    prompts.append(self.pack_one(key, name, case, rep, order))
        return prompts

    def runs_case(self, arm, case):
        only = self.cfg.get("only", {}).get(arm)
        return only is None or case in only

    def pack_one(self, key, name, case, rep, order):
        rdir = self.out / "review" / key
        shutil.rmtree(rdir, ignore_errors=True)
        for label, arm in zip("XY", order):
            ws = self.ws_name(name, arm, rep)
            st, root, side = self.state(ws), self.out / "ws" / ws, rdir / label
            side.mkdir(parents=True)
            for s in case["steps"]:
                shutil.copy(self.out / "logs" / ws / f"{s['id']}.reply.md", side / f"{s['id']}.reply.md")
            snap = extract(root, st["steps"][case["steps"][-1]["id"]]["tree"], side / "snapshot")
            for p in sorted(snap.rglob("*"), reverse=True):
                rel = str(p.relative_to(snap))
                if is_ai(rel) or rel in ("BRIEF.md", "SPEC-FORMAT.md"):
                    shutil.rmtree(p) if p.is_dir() else p.unlink()
        (rdir.parent / f"{key}.map.json").write_text(json.dumps(dict(zip("XY", order))))
        text = (
            (BENCH / "rubric.md")
            .read_text()
            .format(
                dir=rdir,
                title=case["title"],
                review=case["review"],
                brief=case["brief"].strip(),
                requests="\n".join(f'- {s["id"]}: "{s["prompt"]}"' for s in case["steps"]),
                steps=", ".join(s["id"] for s in case["steps"]),
            )
        )
        (rdir.parent / f"{key}.prompt.md").write_text(text)
        return rdir.parent / f"{key}.prompt.md"

    # ---- report -----------------------------------------------------------------------------------------------------
    def report(self, pair=None):
        arms = pair or list(self.cfg["arms"])
        rows = []
        for ws in self.workspaces():
            st = self.state(ws)
            if st["arm"] in arms:
                for sid in st["order"]:
                    rows.append(
                        {"ws": ws, "case": st["case"], "arm": st["arm"], "rep": st["rep"], "step": sid}
                        | st["steps"][sid]
                    )
        reviews = {}
        for path in (self.out / "review").glob("*.verdict.md"):
            key = path.name.removesuffix(".verdict.md")
            amap = json.loads((self.out / "review" / f"{key}.map.json").read_text())
            if (scores := verdict(path)) and set(amap.values()) <= set(arms):
                reviews[key] = {"map": amap, "scores": scores}
        text, tsv = build(rows, reviews, arms)
        suffix = f"-{'-'.join(pair)}" if pair else ""
        (self.out / f"report{suffix}.md").write_text(text)
        (self.out / f"runs{suffix}.tsv").write_text(tsv)
        return text


def verdict(path):
    block = re.findall(r"^```json\s*(\{.*?\})\s*^```", path.read_text(), re.DOTALL | re.MULTILINE)  # fences only
    try:
        return json.loads(block[-1]) if block else None
    except ValueError:
        return None


def prepare(args):
    out = Path(args.out).resolve()
    arms = parse_arms(args.arm)
    only = {k: v.split(",") for k, v in (a.split("=", 1) for a in args.only or [])}
    if unknown := set(only) - set(arms):
        sys.exit(f"--only names unknown arms {sorted(unknown)}")
    for name, value in arms.items():  # frozen copies, outside every workspace
        dest = out / "skills" / name
        shutil.rmtree(dest, ignore_errors=True)
        dest.mkdir(parents=True)
        for skill in skill_dirs(value):
            shutil.copytree(skill, dest / skill.name, ignore=shutil.ignore_patterns(".git"))
    cases = load_cases(args.cases)
    out.mkdir(parents=True, exist_ok=True)
    (out / "state").mkdir(exist_ok=True)
    cfg = {"arms": arms, "only": only, "reps": args.reps, "seed": args.seed, "cases": list(cases)}
    (out / "bench.json").write_text(json.dumps(cfg, indent=1))
    for name, case in cases.items():
        for arm in arms:
            if arm in only and name not in only[arm]:
                continue
            for rep in range(1, args.reps + 1):
                ws = ws_name(args.seed, name, arm, rep)
                root, home = out / "ws" / ws, out / "home" / ws
                if (out / "state" / f"{ws}.json").exists():
                    continue
                shutil.rmtree(root, ignore_errors=True)
                shutil.rmtree(home, ignore_errors=True)
                shutil.copytree(out / "skills" / arm, home / ".claude" / "skills")
                root.mkdir(parents=True)
                (root / "BRIEF.md").write_text(case["brief"].lstrip())
                shutil.copy(BENCH / "spec-format.md", root / "SPEC-FORMAT.md")
                git(root, "init", "-q", "-b", "main")
                git(root, "add", "-A")
                git(root, "-c", "user.name=bench", "-c", "user.email=bench@example.com", "commit", "-qm", "init")
                st = {"case": name, "arm": arm, "rep": rep, "order": [], "steps": {}}
                st["base_tree"] = git(root, "rev-parse", "HEAD^{tree}").strip()
                (out / "state" / f"{ws}.json").write_text(json.dumps(st, indent=1))
                print("prepared", ws)


def transcript_usage(path):
    """USAGE fields summed over a session transcript's model calls, and the number of calls.

    `claude -p` reports only the last stretch of a session that a background task resumed; the transcript
    has every call. Streamed blocks of one call repeat its usage, so each message id counts once.
    """
    calls = {}
    for line in Path(path).read_text().splitlines():
        rec = json.loads(line)
        msg = rec.get("message") or {}
        if rec.get("type") == "assistant" and msg.get("usage"):
            calls[msg.get("id")] = msg["usage"]
    return {k: sum(u.get(k) or 0 for u in calls.values()) for k in USAGE}, len(calls)


def weigh(usage):
    return sum(w * (usage.get(field) or 0) for field, (_, w) in USAGE.items())


def honest(usage, turns, path):
    """The transcript's usage when the CLI under-reports it. Returns (usage, tokens, turns, reported or None)."""
    tokens = sum(v or 0 for v in usage.values())
    if not path:
        return usage, tokens, turns, None
    full, calls = transcript_usage(path)
    if sum(full.values()) <= tokens:
        return usage, tokens, turns, None
    return full, sum(full.values()), max(turns, calls), tokens


def claude(prompt, cwd, home, model, timeout=3600):
    """One fresh headless session. Auth comes from ANTHROPIC_API_KEY or CLAUDE_CODE_OAUTH_TOKEN.

    The session sees only SESSION_ENV and its own HOME, so user-level skills and rules never leak in.
    """
    env = {k: os.environ[k] for k in SESSION_ENV if k in os.environ} | {"HOME": str(home)}
    cmd = ["claude", "-p", prompt, "--output-format", "json", "--permission-mode", "bypassPermissions"]
    cmd += ["--model", model] if model else []
    res = sh(cmd, cwd=cwd, env=env, check=False, timeout=timeout)
    try:
        data = json.loads(res.stdout)
    except ValueError:
        sys.exit(f"claude failed in {cwd}: {res.stderr[-500:] or res.stdout[-500:]}")
    if data.get("is_error"):
        sys.exit(f"claude error in {cwd}: {data.get('result')}")
    usage = {k: data.get("usage", {}).get(k) for k in USAGE}
    found = sorted(Path(home, ".claude", "projects").glob(f"*/{data.get('session_id')}.jsonl"))
    usage, tokens, turns, reported = honest(usage, data.get("num_turns", 0), found[0] if found else None)
    if reported:
        usage["reported_tokens"] = reported
    return data.get("result", ""), tokens, turns, data.get("duration_ms", 0), data.get("total_cost_usd"), usage


def run(args):
    b = Bench(args.out)
    while todo := list(b.pending()):

        def one(item):
            ws, step = item
            reply, tok, turns, ms, cost, usage = claude(
                b.prompt(ws, step, "claude"), b.out / "ws" / ws, b.out / "home" / ws, args.model
            )
            b.record(ws, step["id"], tok, turns, ms, reply, cost, usage, mode="headless")
            print(ws, step["id"], tok, "tokens")

        with ThreadPoolExecutor(args.jobs) as pool:
            list(pool.map(one, todo))
    arms = list(b.cfg["arms"])
    pairs = [None] if len(arms) == 2 else args.pair or [list(p) for p in combinations(arms, 2)]

    def judge(prompt):
        out = prompt.with_name(prompt.name.replace(".prompt.md", ".verdict.md"))
        if out.exists() and verdict(out):  # a resumed run keeps the verdicts it already has
            return
        out.write_text(claude(prompt.read_text(), prompt.parent, b.out / "home" / "judge", args.judge_model)[0])

    for pair in pairs:
        with ThreadPoolExecutor(args.judge_jobs) as pool:
            list(pool.map(judge, b.pack(pair)))
        b.report(pair)
    print(b.report())


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("all", "prepare", "run", "next", "record", "recheck", "pack", "report"):
        s = sub.add_parser(name)
        s.add_argument("--out", required=True)
        if name in ("all", "prepare"):
            s.add_argument(
                "--arm",
                action="append",
                help="NAME=PATH[,PATH]: skill folders or folders of skills, empty = bare agent "
                "(default: bare= and product-layer=skills/product-layer, or the stub when it does not exist yet)",
            )
            s.add_argument("--only", action="append", help="ARM=CASE[,CASE]: run that arm on these cases only")
            s.add_argument("--reps", type=int, default=3)
            s.add_argument("--cases", nargs="*")
            s.add_argument("--seed", type=int, default=1877)
        if name in ("all", "run"):
            s.add_argument("--model", default=None)
            s.add_argument("--judge-model", default="claude-fable-5-1", help="another model line than the agents'")
            s.add_argument("--jobs", type=int, default=4)
            s.add_argument("--judge-jobs", type=int, default=1, help="blind verdicts run in parallel")
            s.add_argument(
                "--pair", action="append", type=lambda v: v.split(","), help="A,B: judge only these pairs (3+ arms)"
            )
        if name in ("pack", "report"):
            s.add_argument("--pair", type=lambda v: v.split(","), help="A,B: the two arms to compare")
        if name == "record":
            s.add_argument("ws")
            s.add_argument("step")
            s.add_argument("--tokens", type=int, required=True)
            s.add_argument("--tools", type=int, default=0)
            s.add_argument("--ms", type=int, default=0)
            s.add_argument("--reply", help="file with the agent's final message (default: the one the prompt names)")
            s.add_argument("--cost", type=float, help="session cost, $, if the driver reports it")
            for field, (col, _) in USAGE.items():
                s.add_argument(f"--{col.replace('_', '-')}", dest=field, type=int, help=f"usage.{field}")
    args = p.parse_args()
    if args.cmd in ("all", "prepare"):
        prepare(args)
    if args.cmd in ("all", "run"):
        run(args)
    elif args.cmd == "next":
        b = Bench(args.out)
        (b.out / "prompts").mkdir(exist_ok=True)
        (b.out / "replies").mkdir(exist_ok=True)
        for ws, step in b.pending():
            path = b.out / "prompts" / f"{ws}__{step['id']}.md"
            path.write_text(b.prompt(ws, step, "agent"))
            print(json.dumps({"ws": ws, "step": step["id"], "prompt": str(path)}))
    elif args.cmd == "record":
        b = Bench(args.out)
        reply = Path(args.reply or b.reply_file(args.ws, args.step)).read_text()
        usage = {k: getattr(args, k) for k in USAGE}
        usage = usage if any(v is not None for v in usage.values()) else None
        m = b.record(args.ws, args.step, args.tokens, args.tools, args.ms, reply, args.cost, usage)
        print(json.dumps({k: v for k, v in m.items() if k not in ("files", "tree")}))
    elif args.cmd == "recheck":
        Bench(args.out).recheck()
    elif args.cmd == "pack":
        print("\n".join(map(str, Bench(args.out).pack(args.pair))))
    elif args.cmd == "report":
        print(Bench(args.out).report(args.pair))


if __name__ == "__main__":
    main()
