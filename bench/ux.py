"""Deterministic checks of a flow spec (bench/spec-format.md) against a case's hidden rules.

A case's check.py holds only its RULES and calls `main(RULES)`; it runs from a copy of the workspace root:

    python bench/cases/<case>/check.py P1         # prints one JSON line of per-check results, then "ok" or the failure

RULES keys, each optional:
    max_steps   {flow: n}            user actions on the shortest path entry -> done
    states      {moment: [keys]}     states the moment's screens must describe (each key on at least one of them)
    render      {moment: text|block} reference text-or-block markup of chat messages; render_min = share to match
    forbid_asks [regex] | {flow: [regex]}  fields the happy path (of every flow, or of that flow) must not ask:
                                     the product already knows them
    require_asks [regex]             fields the spec must ask somewhere: only the user knows them
    nav         {roles: [...], max}  top-level navigation per role, at most `max` sections
    min_actions {moment: n}          ways out one screen of the moment must offer (approve and revise, not approve only)
"""

import json
import re
import sys
from collections import deque
from pathlib import Path

import yaml

SPEC = Path("spec/flow.yaml")
MISSING = {"", "n/a", "na", "none", "-", "null"}
DECISION = r"(approv|confirm|consent|agree|accept)"
VALUE = r"\b(enter|type|input|you want|your own|set|choose|pick)\b"  # "confirm the price you want" still asks for it
CHECKS = ("structure", "dead_ends", "steps", "states", "render", "asks", "nav", "actions")


class SpecError(Exception):
    pass


def load(path=SPEC):
    try:
        spec = yaml.safe_load(Path(path).read_text())
    except FileNotFoundError:
        raise SpecError(f"no {path}") from None
    except yaml.YAMLError as exc:
        raise SpecError(f"{path} is not valid YAML: {str(exc).splitlines()[0]}") from None
    if not isinstance(spec, dict):
        raise SpecError(f"{path} is not a mapping")
    screens, flows = spec.get("screens"), spec.get("flows")
    if not isinstance(screens, list) or not screens or not all(isinstance(s, dict) and s.get("id") for s in screens):
        raise SpecError("`screens` must be a non-empty list of mappings with an `id`")
    if not isinstance(flows, list) or not flows or not all(isinstance(f, dict) and f.get("id") for f in flows):
        raise SpecError("`flows` must be a non-empty list of mappings with an `id`")
    ids = [str(s["id"]) for s in screens]
    if dup := sorted({i for i in ids if ids.count(i) > 1}):
        raise SpecError(f"duplicate screen ids {dup}")
    for s in screens:
        s["actions"] = [a for a in s.get("actions") or [] if isinstance(a, dict)]
        s["asks"] = [a if isinstance(a, dict) else {"field": str(a)} for a in s.get("asks") or []]
        s["states"] = s.get("states") if isinstance(s.get("states"), dict) else {}
    return spec


def screens(spec):
    return {str(s["id"]): s for s in spec["screens"]}


def flows(spec):
    return {str(f["id"]): f for f in spec["flows"]}


def path(spec, start, goal):
    """Screens on the cheapest path start -> goal (user action = 1, system transition = 0), or None."""
    by_id = screens(spec)
    cost, prev, queue = {start: 0}, {start: None}, deque([start])
    while queue:
        cur = queue.popleft()
        for a in by_id.get(cur, {}).get("actions", []):
            nxt, w = str(a.get("to")), int(a.get("by", "user") != "system")
            if nxt in by_id and cost[cur] + w < cost.get(nxt, 1 << 30):
                cost[nxt], prev[nxt] = cost[cur] + w, cur
                queue.appendleft(nxt) if w == 0 else queue.append(nxt)
    if goal not in cost:
        return None, None
    out, cur = [], goal
    while cur is not None:
        out.append(cur)
        cur = prev[cur]
    return out[::-1], cost[goal]


def happy(spec, only=None):
    """Screen ids on the shortest path of every flow, or of the flow named `only`."""
    out = set()
    for name, f in flows(spec).items():
        if only in (None, name):
            p, _ = path(spec, str(f.get("entry")), str(f.get("done")))
            out |= set(p or [])
    return out


def by_moment(spec, moment):
    return [s for s in spec["screens"] if str(s.get("moment", "")).lower() == moment.lower()]


def filled(value):
    return value is not None and str(value).strip().lower() not in MISSING


def check_structure(spec, rules):
    by_id, problems = screens(spec), []
    for f in flows(spec).values():
        problems += [
            f"flow {f['id']}: unknown {k} {f.get(k)!r}" for k in ("entry", "done") if str(f.get(k)) not in by_id
        ]
    for s in spec["screens"]:
        problems += [f"{s['id']} -> unknown {a.get('to')!r}" for a in s["actions"] if str(a.get("to")) not in by_id]
    seen, queue = set(), deque(str(f.get("entry")) for f in spec["flows"])
    while queue:
        cur = queue.popleft()
        if cur in by_id and cur not in seen:
            seen.add(cur)
            queue.extend(str(a.get("to")) for a in by_id[cur]["actions"])
    if orphans := sorted(set(by_id) - seen):
        problems.append(f"unreachable {orphans}")
    return problems


def check_dead_ends(spec, rules):
    """Screens with no action, or whose every action leads back to the same screen.

    A screen marked `terminal: true` ends the journey on purpose ("account deleted", "bill settled") and needs no exit.
    """
    return [
        f"{s['id']} has no way out"
        for s in spec["screens"]
        if s.get("terminal") is not True and all(str(a.get("to")) == str(s["id"]) for a in s["actions"])
    ]


def check_steps(spec, rules):
    problems = []
    for name, limit in rules.get("max_steps", {}).items():
        f = flows(spec).get(name)
        if f is None:
            problems.append(f"no flow `{name}`")
            continue
        p, cost = path(spec, str(f.get("entry")), str(f.get("done")))
        if p is None:
            problems.append(f"{name}: done unreachable from entry")
        elif cost > limit:
            problems.append(f"{name}: {cost} steps > {limit}")
    return problems


def check_states(spec, rules):
    problems = []
    for moment, keys in rules.get("states", {}).items():
        found = by_moment(spec, moment)  # a moment may span screens (start, building, ready): any of them counts
        if not found:
            problems.append(f"no moment `{moment}`")
        elif lacking := [k for k in keys if not any(filled(s["states"].get(k)) for s in found)]:
            problems.append(f"{moment} lacks {lacking}")
    return problems


def check_render(spec, rules):
    ref = rules.get("render", {})
    misses = []
    for moment, want in ref.items():
        found = by_moment(spec, moment)
        got = str(found[0].get("render", "")).lower() if found else "missing"
        if got != want:
            misses.append(f"{moment}: {got} != {want}")
    need = rules.get("render_min", 1.0)
    return misses if ref and (len(ref) - len(misses)) / len(ref) < need else []


def check_asks(spec, rules):
    problems = []
    asked = [(str(s["id"]), str(a.get("field", "")).lower()) for s in spec["screens"] for a in s["asks"]]
    # "approve the plan and price" is a decision on a value the product shows, not a request for that value
    decisions = [(sid, f) for sid, f in asked if re.match(DECISION, f) and not re.search(VALUE, f)]
    forbid = rules.get("forbid_asks", [])
    for flow, patterns in forbid.items() if isinstance(forbid, dict) else [(None, forbid)]:
        path_ids = happy(spec, flow)
        for pattern in patterns:
            problems += [
                f"{sid} asks known `{f}`"
                for sid, f in asked
                if sid in path_ids and re.search(pattern, f) and (sid, f) not in decisions
            ]
    for pattern in rules.get("require_asks", []):
        if not any(re.search(pattern, f) for _, f in asked):
            problems.append(f"never asks /{pattern}/")
    return problems


def check_nav(spec, rules):
    want, nav = rules.get("nav", {}), spec.get("nav") if isinstance(spec.get("nav"), dict) else {}
    problems = []
    for role in want.get("roles", []):
        items = nav.get(role)
        if not isinstance(items, list) or not items:
            problems.append(f"no nav for `{role}`")
        elif len(items) > want.get("max", 99):
            problems.append(f"{role}: {len(items)} top-level sections > {want['max']}")
    return problems


def check_actions(spec, rules):
    problems = []
    for moment, n in rules.get("min_actions", {}).items():
        found = by_moment(spec, moment)
        if not found:
            problems.append(f"no moment `{moment}`")
        elif (most := max(len(s["actions"]) for s in found)) < n:
            problems.append(f"{moment}: {most} ways out < {n}")
    return problems


KEYS = {"steps": "max_steps", "states": "states", "render": "render", "asks": ("forbid_asks", "require_asks")}
KEYS |= {"nav": "nav", "actions": "min_actions"}


def run(rules, spec_path=SPEC):
    """{check: problems list, or None when the case does not use it}; a broken spec fails `structure` only."""
    try:
        spec = load(spec_path)
    except SpecError as exc:
        return {"structure": [str(exc)]} | {c: None for c in CHECKS[1:]}
    out = {}
    for name in CHECKS:
        keys = KEYS.get(name)
        used = keys is None or any(k in rules for k in ((keys,) if isinstance(keys, str) else keys))
        out[name] = globals()[f"check_{name}"](spec, rules) if used else None
    return out


def summary(spec_path=SPEC):
    """Shape metrics for the report: screens, user steps per flow, asks on the happy path."""
    try:
        spec = load(spec_path)
    except SpecError:
        return {}
    steps = {name: path(spec, str(f.get("entry")), str(f.get("done")))[1] for name, f in flows(spec).items()}
    on_path = happy(spec)
    return {
        "n_screens": len(spec["screens"]),
        "n_steps": sum(v for v in steps.values() if v is not None),
        "n_asks": sum(len(s["asks"]) for s in spec["screens"] if str(s["id"]) in on_path),
    }


def main(rules):
    res = run(rules)
    failed = [f"{k}: {'; '.join(v[:3])}" for k, v in res.items() if v]
    print(json.dumps({k: (None if v is None else not v) for k, v in res.items()} | summary()))
    print(" | ".join(failed) or "ok")
    sys.exit(1 if failed else 0)
