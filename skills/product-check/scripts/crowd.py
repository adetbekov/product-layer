#!/usr/bin/env python3
"""Crowd runs for product-check: many personas, one isolated browser each, funnel and drop-off per variant.

    crowd.py plan --personas personas.json --flow flow.json --variant A=URL --variant B=URL --out DIR \
        [--driver mixed|haiku|sonnet] [--engine playwright|agent-browser] [--no-look]
    crowd.py run --out DIR [--workers 10]                  # over the API: d1-ultra, Claude Haiku / Sonnet on escalation
    crowd.py auto RUN_DIR                                  # agent-driven mixed runs: d1 plays steps until escalation
    crowd.py record --out DIR RUN --input-tokens N --output-tokens N    # agent-driven runs: log what a session used
    crowd.py aggregate --out DIR                           # funnel.md + funnel.json, steps per tier, cost

Each step goes to the cheapest decision maker that can take it (`--driver mixed`, the default):

| tier | decides | when |
|---|---|---|
| d1 | Liquid d1-ultra (`d1.py`): choice / noul / score, text + screenshot | clicks among visible controls, go back, done, quit |
| haiku | Claude Haiku | d1 unsure (confidence < 0.5, yes/no in 0.2-0.8), text input, control on screen but not in tree |
| sonnet | Claude Sonnet | the last action changed nothing, page not recognised (no controls, lost) |

`--driver haiku` / `sonnet` puts every step on that model (the baselines). `plan` writes DIR/runs/<variant>-<persona>/
with `prompt.md` (the persona agent's instructions) and `act` (pc.py bound to that run's browser session, engine,
patience budget and screenshots). Without an API key, run every prompt.md in a fresh session of the driver model, all
in parallel, then `record` its tokens; in mixed runs that session calls `./act auto` and decides only the steps d1
hands over. Funnel stages come from flow.json:

    {"goal": "...", "optimal": 5, "facts": ["..."],
     "stages": [{"id": "cart", "url": "#/cart"}, {"id": "done", "text": "Order placed"}, ...]}

A stage is reached when the page URL (`url`) or the page snapshot (`text`) matches its regex; `"only": ["A"]` limits a
stage to some variants. Completion is the last stage, read from the page, never from the persona's claim.
"""

import argparse
import base64
import json
import os
import random
import re
import shlex
import statistics
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import d1  # noqa: E402

PC = HERE / "pc.py"
PRICES = {"haiku": (0.10, 0.50), "sonnet": (2.0, 10.0)}  # $ per MTok in / out, Claude 5.5 list prices, 2026-10-31
MODELS = {"haiku": os.environ.get("PC_HAIKU_MODEL", "claude-haiku-5-5"),
          "sonnet": os.environ.get("PC_SONNET_MODEL", "claude-sonnet-5-5")}
TIERS = ("d1", "haiku", "sonnet")
ACTIONS = "click <ref> | fill <ref> <text> | select <ref> <option> | check <ref> | press <key> | go-back"

PROMPT = """You are role-playing one user in a usability simulation. Stay in character from start to end.

## Who you are
{card}

{voice}

## What you want
{goal}
{facts}
## How you use the site
You see and touch the site only through `./act` in `{run}` (run every command from that folder):

- `./act open` - once, first. It prints the page as an accessibility tree with refs like `e12`.
- `./act do --note "<what you think right now, first person, one short line>" -- <action>`, where the action is
  one of: {actions}. Put text in quotes. After each action it prints what changed on the page and the path of the
  full page snapshot; read that file when the change is not enough to decide.
- `./act end --outcome done|quit --reason "<one line in your own words>"` - when you reached your goal, or decided
  to leave.
{look}{auto}
Rules:
- Decide as {name} would with what is on the screen now, not as a tester or developer. Do not explore features you
  do not need. If something is confusing, say so in the note.
- You have patience for about {steps} actions. When `./act` says you are out of patience, end with `quit`.
- If {name} would give up (an error, a demand that feels unreasonable, being stuck), end with `quit` and say why.
- Only `./act`. Do not open other files except the snapshot and screen paths it prints; no page source, devtools,
  or URL edits.
- Your final reply is one line: `outcome: done|quit - <reason>`.
"""

LOOK = """- Every `./act` call also prints `screen: <path>`, a small screenshot of what is on the screen now. Open it when
  the tree leaves you unsure, when a control seems missing, or when something may look different from what the tree
  says. Judge as {name} sees the page: notice what stands out, as this person would, not everything in the tree.
"""
AUTO = """- Start with `./act auto` instead of `./act open`. A fast assistant plays the steps that are obvious for you and
  stops at `YOUR TURN`, with the reason, the page and the screen. Then decide that one step yourself with
  `./act do --note ... -- <action>` (or `./act end`), and call `./act auto` again. Repeat until the run has ended.
"""

SYSTEM = """You simulate one user of a website in a usability study. Stay in character. Each turn you get the \
page as an accessibility tree with refs (e12) and your memory. Reply with JSON only:
{"think": "<one short first-person line>", "action": "click|fill|select|check|press|go-back|done|quit", \
"ref": "e12", "text": "<text, option or key>"}
"done" only when the goal is visibly reached; "quit" when this person would give up."""


def card(p):
    d = p["device"]
    lines = [
        f"- Name: {p['name']}; language: {p['lang']}",
        f"- Tech skill: {p['tech']}; trust in AI: {p['ai_trust']}",
        f"- Patience: {p['patience']['label']}",
        f"- Device: {d['type']}, {d['network']} network",
    ]
    if p.get("constraints"):
        lines.append(f"- Constraints: {'; '.join(p['constraints'])}")
    return "\n".join(lines)


def runs(out):
    return sorted(p for p in (Path(out) / "runs").iterdir() if (p / "meta.json").exists())


def plan(args):
    out = Path(args.out).resolve()
    personas = json.loads(Path(args.personas).read_text())
    flow = json.loads(Path(args.flow).read_text())
    variants = dict(v.split("=", 1) for v in args.variant)
    for name, url in variants.items():
        for p in personas:
            run = out / "runs" / f"{name}-{p['id']}"
            run.mkdir(parents=True, exist_ok=True)
            flags = (" --mobile" if p["device"]["type"] == "mobile" else "") + (
                " --slow" if p["device"]["network"] == "slow" else "")
            session = f"crowd-{out.name}-{name}-{p['id']}".lower()
            act = run / "act"
            tier = "haiku" if args.driver == "mixed" else args.driver
            act.write_text(
                "#!/bin/sh\n"
                f"export PC_RUN={shlex.quote(str(run))} PC_SESSION={shlex.quote(session)} "
                f"PC_BUDGET={p['patience']['steps']} PC_ENGINE={args.engine} PC_TIER=${{PC_TIER:-{tier}}}"
                f"{'' if args.no_look else ' PC_LOOK=1'}\n"
                f'if [ "$1" = open ]; then exec python3 {shlex.quote(str(PC))} open {shlex.quote(url)}{flags}; fi\n'
                f'if [ "$1" = auto ]; then exec python3 {shlex.quote(str(HERE / "crowd.py"))} auto '
                f'{shlex.quote(str(run))}; fi\n'
                f'exec python3 {shlex.quote(str(PC))} "$@"\n')
            act.chmod(0o755)
            facts = "".join(f"- {f}\n" for f in flow.get("facts", []))
            (run / "prompt.md").write_text(PROMPT.format(
                card=card(p), voice=p.get("voice", ""), goal=p.get("goal") or flow["goal"], run=run,
                actions=ACTIONS, name=p["name"], steps=p["patience"]["steps"],
                facts=f"\nWhat you already know:\n{facts}" if facts else "",
                look="" if args.no_look else LOOK.format(name=p["name"]),
                auto=AUTO if args.driver == "mixed" else ""))
            (run / "meta.json").write_text(json.dumps({"variant": name, "url": url, "persona": p, "driver": args.driver,
                                                       "engine": args.engine, "look": not args.no_look},
                                                      ensure_ascii=False))
    (out / "plan.json").write_text(json.dumps({"variants": variants, "flow": flow, "n": len(personas),
                                               "driver": args.driver, "engine": args.engine}, indent=1))
    for run in runs(out):
        print(run / "prompt.md")


def decide(client, model, prompt, memory, page, image=None, reason=None):
    """One step by Claude: JSON action from the persona prompt, its memory, the page and the screen."""
    content = []
    if image:
        content.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                                    "data": base64.b64encode(image).decode()}})
    content.append({"type": "text", "text": (f"Why you are asked: {reason}\n\n" if reason else "")
                    + f"Memory:\n{memory or '(start)'}\n\nPage:\n{page[:12000]}"})
    msg = client.messages.create(
        model=model,
        max_tokens=300,
        system=[{"type": "text", "text": SYSTEM + "\n\n" + prompt, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": content}],
    )
    text = "".join(b.text for b in msg.content if b.type == "text")
    return parse_action(text), msg.usage


def parse_action(text):
    m = re.search(r"\{.*\}", text, re.S)
    try:
        data = json.loads(m.group(0)) if m else {}
    except ValueError:
        data = {}
    if data.get("action") not in {"click", "fill", "select", "check", "press", "go-back", "done", "quit"}:
        return {"action": "quit", "think": f"(unreadable decision: {text[:80]})"}
    return data


def to_command(d):
    a = d["action"]
    if a in ("click", "check"):
        return [a, d.get("ref", "")]
    if a in ("fill", "select"):
        return [a, d.get("ref", ""), d.get("text", "")]
    if a == "press":
        return ["press", d.get("text", "Enter")]
    return ["go-back"]


def read_jsonl(path):
    path = Path(path)
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()] if path.exists() else []


def page_now(run):
    """Last snapshot, URL, whether the last action changed the page, and the last screenshot (bytes or None)."""
    log = read_jsonl(run / "log.jsonl")
    last = json.loads((run / "last.json").read_text()) if (run / "last.json").exists() else {"url": "", "snap": ""}
    entry = log[-1] if log else {}
    look = run / entry["look"] if entry.get("look") else None
    return last["snap"], last["url"], entry.get("changed", True) or not entry.get("ok", True), (
        look.read_bytes() if look and look.exists() else None), log


def memory(log):
    return [f"{e.get('note') or ''} -> {' '.join(e['cmd'])}" + ("" if e.get("changed", True) else " (nothing changed)")
            for e in log if e.get("i")]


def d1_step(run, meta, flow):
    """Ask d1 about the current page and route the step. Logs the request to d1.jsonl; returns (tier, decision)."""
    snap, url, changed, image, log = page_now(run)
    p = meta["persona"]
    used = sum(1 for e in log if e.get("i") and e.get("ok"))
    state = d1.state(p, p.get("goal") or flow["goal"], flow.get("facts", []), memory(log), snap, url, used,
                     p["patience"]["steps"])
    questions, clicks, types = d1.policy(snap, with_image=image is not None)
    answers, usage = d1.ask(state, questions, images=[image] if image else ())
    tier, dec = d1.route(answers, clicks, types, last_changed=changed, rng=random.Random(f"{run.name}-{len(log)}"))
    names = {c["ref"]: c["name"] for c in clicks}
    if dec.get("ref"):
        dec["name"] = names.get(dec["ref"], "")
    with open(run / "d1.jsonl", "a") as f:
        f.write(json.dumps({"step": len(log), "tier": tier, "decision": dec, "cost_usd": usage.get("cost"),
                            "input_tokens": usage.get("input_tokens"), "answers": {
                                k: {f: v for f, v in a.items() if f in ("choice", "noul", "score", "confidence")}
                                for k, a in answers.items()}}, ensure_ascii=False) + "\n")
    return tier, dec


WHY = {"asked_again": "it asks for things it already knows", "stuck": "I see no way forward",
       "too_long": "this takes too many steps", "error": "something is broken", "unclear": "I cannot tell what to do",
       "none": "not worth it"}


def play_d1(run, act, dec):
    """Carry out a d1 decision through ./act. Returns False when the run ended."""
    if dec["action"] in ("done", "quit"):
        reason = "(d1) goal reached" if dec["action"] == "done" else f"(d1) {WHY.get(dec.get('why'), 'gave up')}"
        subprocess.run([*act, "end", "--outcome", dec["action"], "--reason", reason], capture_output=True, check=False)
        return False
    cmd = ["click", dec["ref"]] if dec["action"] == "click" else ["go-back"]
    note = f"(d1) {dec['action']} {dec.get('name') or ''}".strip()
    res = subprocess.run([*act, "do", "--tier", "d1", "--note", note, "--", *cmd], capture_output=True, text=True,
                         check=False)
    if res.returncode == 3:  # out of patience
        subprocess.run([*act, "end", "--outcome", "quit", "--reason", "out of patience"], capture_output=True,
                       check=False)
        return False
    return True


def auto(args):
    """Agent-driven mixed run: d1 plays steps until one needs a stronger model, then prints YOUR TURN."""
    run = Path(args.run).resolve()
    meta = json.loads((run / "meta.json").read_text())
    flow = json.loads((run.parent.parent / "plan.json").read_text())["flow"]
    act = [str(run / "act")]
    if not (run / "log.jsonl").exists():
        subprocess.run([*act, "open"], capture_output=True, check=False)
    for _ in range(meta["persona"]["patience"]["steps"] * 2):
        if (run / "end.json").exists():
            end = json.loads((run / "end.json").read_text())
            print(f"run ended: {end['outcome']} - {end.get('reason', '')}. Reply with your one-line outcome.")
            return
        tier, dec = d1_step(run, meta, flow)
        if tier != "d1":
            snap, url, _, _, log = page_now(run)
            look = log[-1].get("look") if log else None
            print(f"YOUR TURN ({tier}): {dec['reason']}\nurl: {url}\n{snap}")
            if look:
                print(f"screen: {run / look}")
            print("Decide one step: ./act do --note \"...\" -- <action>, or ./act end. Then ./act auto again.")
            return
        print(f"d1: {dec['action']} {dec.get('name') or dec.get('ref') or ''}".rstrip())
        if not play_d1(run, act, dec):
            end = json.loads((run / "end.json").read_text())
            print(f"run ended: {end['outcome']} - {end.get('reason', '')}. Reply with your one-line outcome.")
            return
    print("YOUR TURN (haiku): the assistant made too many steps in a row; check where you are.")


def run_one(run, models, router):
    """API run of one persona. router: mixed (d1 first), haiku or sonnet (every step on that model)."""
    import anthropic

    client = anthropic.Anthropic()
    meta = json.loads((run / "meta.json").read_text())
    flow = json.loads((run.parent.parent / "plan.json").read_text())["flow"]
    budget = meta["persona"]["patience"]["steps"]
    prompt = (run / "prompt.md").read_text().split("## How you use the site")[0]
    act = [str(run / "act")]
    subprocess.run([*act, "open"], capture_output=True, text=True, check=False)
    usage = {}
    for _ in range(budget * 2):  # failed refs are free, but never loop forever
        tier, dec = d1_step(run, meta, flow) if router == "mixed" else (router, {"reason": None})
        if tier == "d1":
            if not play_d1(run, act, dec):
                break
            continue
        snap, url, _, image, log = page_now(run)
        model = models[tier]
        d, u = decide(client, model, prompt, "\n".join(memory(log)[-8:]), f"url: {url}\n{snap}", image,
                      dec.get("reason"))
        acc = usage.setdefault(model, {"model": model, "input": 0, "output": 0})
        acc["input"] += u.input_tokens + (u.cache_read_input_tokens or 0) + (u.cache_creation_input_tokens or 0)
        acc["output"] += u.output_tokens
        if d["action"] in ("done", "quit"):
            subprocess.run([*act, "end", "--outcome", d["action"], "--reason", d.get("think", "")], check=False)
            break
        res = subprocess.run([*act, "do", "--tier", tier, "--note", d.get("think", ""), "--", *to_command(d)],
                             capture_output=True, text=True, check=False)
        if res.returncode == 3:
            subprocess.run([*act, "end", "--outcome", "quit", "--reason", "out of patience"], check=False)
            break
    (run / "usage.json").write_text(json.dumps({"models": list(usage.values())}))
    return run.name


def run(args):
    todo = [r for r in runs(args.out) if not (r / "end.json").exists()]
    router = args.router or json.loads((Path(args.out) / "plan.json").read_text()).get("driver", "mixed")
    models = {"haiku": args.haiku, "sonnet": args.sonnet}
    with ThreadPoolExecutor(args.workers) as pool:
        for name in pool.map(lambda r: run_one(r, models, router), todo):
            print("done", name)


def record(args):
    run = Path(args.out) / "runs" / args.run
    (run / "usage.json").write_text(json.dumps({"model": args.model, "input": args.input_tokens,
                                                "output": args.output_tokens}))


def stages_reached(run, stages, variant):
    reached = []
    log = [json.loads(line) for line in (run / "log.jsonl").read_text().splitlines()] if (
        run / "log.jsonl").exists() else []
    for entry in log:
        snap = (run / entry["snapshot"]).read_text() if entry.get("snapshot") and (run / entry["snapshot"]).exists() else ""
        for s in stages:
            if s["id"] in reached or (s.get("only") and variant not in s["only"]):
                continue
            if ("url" in s and re.search(s["url"], entry.get("url", ""))) or (
                    "text" in s and re.search(s["text"], snap)):
                reached.append(s["id"])
    return reached, log


def interval(a, b, reps=2000, seed=1):
    """90% bootstrap interval of mean(b) - mean(a)."""
    rng = random.Random(seed)
    diffs = sorted(statistics.mean(rng.choices(b, k=len(b))) - statistics.mean(rng.choices(a, k=len(a)))
                   for _ in range(reps))
    return diffs[int(reps * 0.05)], diffs[int(reps * 0.95)]


def cost(usages):
    """$ of Claude usage records: {"model", "input", "output"} or {"models": [...]} per session."""
    total = 0.0
    for u in usages:
        for m in u.get("models", [u]):
            price = PRICES["sonnet" if "sonnet" in m.get("model", "") else "haiku"]
            total += m["input"] / 1e6 * price[0] + m["output"] / 1e6 * price[1]
    return total


def tiers(run, driver):
    """Steps per decision maker in one run, d1 requests that asked for Sonnet, and the d1 bill."""
    log, asks = read_jsonl(run / "log.jsonl"), read_jsonl(run / "d1.jsonl")
    count = Counter(e.get("tier") or ("haiku" if driver == "mixed" else driver) for e in log if e.get("i"))
    for e in asks:  # done / quit decided by d1 ends the run without a logged action
        if e["tier"] == "d1" and e["decision"]["action"] in ("done", "quit"):
            count["d1"] += 1
    return count, sum(e["tier"] == "sonnet" for e in asks), sum(e.get("cost_usd") or 0 for e in asks)


def aggregate(args):
    out = Path(args.out)
    plan_ = json.loads((out / "plan.json").read_text())
    flow = plan_["flow"]
    stages, final = flow["stages"], flow["stages"][-1]["id"]
    result = {"goal": flow["goal"], "optimal": flow.get("optimal"), "driver": plan_.get("driver", "haiku"),
              "variants": {}}
    usages, steps, asked_sonnet, d1_cost = [], Counter(), 0, 0.0
    for variant in plan_["variants"]:
        rows = []
        for run in [r for r in runs(out) if json.loads((r / "meta.json").read_text())["variant"] == variant]:
            meta = json.loads((run / "meta.json").read_text())
            reached, log = stages_reached(run, stages, variant)
            end = json.loads((run / "end.json").read_text()) if (run / "end.json").exists() else {"outcome": "none"}
            if (run / "usage.json").exists():
                usages.append(json.loads((run / "usage.json").read_text()))
            count, sonnet, bill = tiers(run, meta.get("driver", result["driver"]))
            steps.update(count)
            asked_sonnet += sonnet
            d1_cost += bill
            actions = [e for e in log if e["i"] and e["ok"]]
            rows.append({
                "persona": meta["persona"]["id"], "hard": meta["persona"]["hard"],
                "patience": meta["persona"]["patience"]["label"], "reached": reached,
                "done": final in reached, "claimed": end["outcome"], "reason": end.get("reason", ""),
                "actions": len(actions), "last_stage": reached[-1] if reached else None,
                "last_url": log[-1]["url"] if log else None,
                "dead_clicks": [" ".join(e["cmd"]) + f" @ {e['url']}" for e in actions if not e["changed"]],
                "notes": [e["note"] for e in log if e.get("note")][-3:],
            })
        funnel = {s["id"]: sum(s["id"] in r["reached"] for r in rows) for s in stages
                  if not s.get("only") or variant in s["only"]}
        drop = Counter(r["last_stage"] for r in rows if not r["done"])
        done_actions = [r["actions"] for r in rows if r["done"]]
        result["variants"][variant] = {
            "n": len(rows), "funnel": funnel, "completed": sum(r["done"] for r in rows),
            "completed_hard": sum(r["done"] for r in rows if r["hard"]), "hard": sum(r["hard"] for r in rows),
            "dropoff": drop.most_common(), "median_actions_done": statistics.median(done_actions) if done_actions else None,
            "dead_clicks": Counter(c.split(" @ ")[0] + " @ " + c.split(" @ ")[1].split("#")[-1]
                                   for r in rows for c in r["dead_clicks"]).most_common(5),
            "claims_vs_page": sum(r["claimed"] == "done" and not r["done"] for r in rows),
            "personas": rows,
        }
    names = list(plan_["variants"])
    if len(names) == 2:
        a, b = (result["variants"][n] for n in names)
        lo, hi = interval([r["done"] for r in a["personas"]], [r["done"] for r in b["personas"]])
        better = names[1] if lo > 0 else names[0] if hi < 0 else None
        result["direction"] = {"better": better, "interval90": [round(lo, 2), round(hi, 2)],
                               "note": "direction only; simulated completion is not a conversion forecast"}
    total = sum(steps.values())
    result["steps_by_tier"] = {t: steps.get(t, 0) for t in TIERS}
    result["share_by_tier"] = {t: round(steps.get(t, 0) / total, 3) if total else 0 for t in TIERS}
    result["d1_asked_for_sonnet"] = asked_sonnet
    result["cost_claude_usd"] = round(cost(usages), 4)
    result["cost_d1_usd"] = round(d1_cost, 5)
    result["cost_usd"] = round(cost(usages) + d1_cost, 4)
    n = sum(v["n"] for v in result["variants"].values())
    result["cost_per_persona_usd"] = round(result["cost_usd"] / n, 5) if n else None
    result["sessions_with_usage"] = len(usages)
    (out / "funnel.json").write_text(json.dumps(result, ensure_ascii=False, indent=1))
    (out / "funnel.md").write_text(markdown(result, stages))
    print((out / "funnel.md").read_text())


def markdown(res, stages):
    names = list(res["variants"])
    lines = [f"# Crowd run: {res['goal']}", "", f"Optimal path: {res['optimal']} actions.", "",
             "| Stage | " + " | ".join(names) + " |", "|---|" + "---|" * len(names)]
    for s in stages:
        cells = []
        for n in names:
            v = res["variants"][n]
            cells.append(f"{v['funnel'][s['id']]} / {v['n']}" if s["id"] in v["funnel"] else "-")
        lines.append(f"| {s['id']} | " + " | ".join(cells) + " |")
    lines += ["", "| | " + " | ".join(names) + " |", "|---|" + "---|" * len(names)]
    rows = [
        ("completed", lambda v: f"{v['completed']} / {v['n']}"),
        ("completed, hard personas", lambda v: f"{v['completed_hard']} / {v['hard']}"),
        ("median actions (completers)", lambda v: v["median_actions_done"]),
        ("top drop-off (last stage reached)", lambda v: ", ".join(f"{k}: {c}" for k, c in v["dropoff"][:3]) or "-"),
        ("clicks that changed nothing", lambda v: "; ".join(f"{k} x{c}" for k, c in v["dead_clicks"][:3]) or "-"),
        ("said done, page disagrees", lambda v: v["claims_vs_page"]),
    ]
    for label, fn in rows:
        lines.append(f"| {label} | " + " | ".join(str(fn(res["variants"][n])) for n in names) + " |")
    if d := res.get("direction"):
        verdict = f"**{d['better']}** completes more often" if d["better"] else "no clear direction"
        lines += ["", f"Direction: {verdict} (90% bootstrap interval of the completion difference "
                      f"{names[1]} - {names[0]}: {d['interval90']}). {d['note']}."]
    share = ", ".join(f"{t} {res['steps_by_tier'][t]} ({res['share_by_tier'][t]:.0%})" for t in TIERS)
    lines += ["", f"Decisions ({res['driver']}): {share}; d1 asked for Sonnet {res['d1_asked_for_sonnet']} times.",
              "", f"Cost: ${res['cost_usd']} (Claude ${res['cost_claude_usd']} over {res['sessions_with_usage']} "
              f"sessions with recorded usage, d1 ${res['cost_d1_usd']}), ${res['cost_per_persona_usd']} per persona.",
              "", "## Drop-off reasons", ""]
    for n in names:
        for r in res["variants"][n]["personas"]:
            if not r["done"]:
                lines.append(f"- {n} {r['persona']} ({r['patience']}{', hard' if r['hard'] else ''}), "
                             f"stopped after `{r['last_stage']}`: {r['reason'] or '(no reason)'}")
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan")
    p.add_argument("--personas", required=True)
    p.add_argument("--flow", required=True)
    p.add_argument("--variant", action="append", required=True, help="NAME=URL, repeat for each variant")
    p.add_argument("--out", required=True)
    p.add_argument("--driver", choices=["mixed", "haiku", "sonnet"], default="mixed")
    p.add_argument("--engine", choices=["playwright", "agent-browser"], default="playwright")
    p.add_argument("--no-look", action="store_true", help="no screenshots: decide from the accessibility tree only")
    r = sub.add_parser("run")
    r.add_argument("--out", required=True)
    r.add_argument("--workers", type=int, default=10)
    r.add_argument("--router", choices=["mixed", "haiku", "sonnet"], help="default: the plan's --driver")
    r.add_argument("--haiku", default=MODELS["haiku"])
    r.add_argument("--sonnet", default=MODELS["sonnet"])
    u = sub.add_parser("auto")
    u.add_argument("run")
    c = sub.add_parser("record")
    c.add_argument("--out", required=True)
    c.add_argument("run")
    c.add_argument("--input-tokens", type=int, required=True)
    c.add_argument("--output-tokens", type=int, required=True)
    c.add_argument("--model", default="claude-haiku-5-5")
    g = sub.add_parser("aggregate")
    g.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "run" and not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set: run each runs/*/prompt.md in a fresh session of the driver model")
    {"plan": plan, "run": run, "auto": auto, "record": record, "aggregate": aggregate}[a.cmd](a)


if __name__ == "__main__":
    main()
