#!/usr/bin/env python3
"""Persona sampler and validator for product-check crowd runs. Stdlib only. Schema: references/personas.md.

    personas.py sample --n 20 --goal "Buy oat milk and bread" --optimal 5 [--seed 7] [--hard 0.35] \
        [--langs ru,kk,en] [--device mobile,desktop] [--constraint "budget under 5000 tenge"] > personas.json
    personas.py validate personas.json

Stratified, not random: every axis value appears in proportion, and at least --hard of the personas are hard
(hurried, doubting, ready to quit, or low tech). Build personas from real interviews or analytics
when you have them; this sampler is the fallback.
"""

import argparse
import json
import random
import sys
from itertools import cycle

AXES = {
    "tech": ["low", "mid", "high"],
    "ai_trust": ["low", "mid", "high"],
    "patience": ["hurried", "normal", "patient"],
    "network": ["fast", "slow"],
}
TRAITS = ["hurried", "doubter", "quitter"]
NAMES = {
    "ru": ["Анна", "Дмитрий", "Ольга", "Сергей", "Марина", "Игорь", "Екатерина", "Павел"],
    "kk": ["Айгерим", "Ерлан", "Дана", "Нурлан", "Асель", "Бауыржан", "Жанар", "Арман"],
    "en": ["Sam", "Priya", "Alex", "Maria", "Tom", "Lena", "Omar", "Kate"],
}
VOICE = {
    "hurried": "Has two minutes between tasks; skims, taps the first thing that looks right, leaves when blocked.",
    "doubter": "Reads labels twice, hesitates at anything that asks for data or money, wants to know why.",
    "quitter": "Gives up at the first error or anything that feels like paperwork.",
    None: "Ordinary user: reads headings, follows the obvious button, tolerates one small detour.",
}
REQUIRED = {"id", "name", "goal", "tech", "patience", "ai_trust", "device", "lang", "constraints", "traits", "hard"}


def budget(label, optimal):
    """Action budget: how many actions the persona tolerates for a task whose shortest path is `optimal`."""
    return {"hurried": optimal + 1, "normal": round(optimal * 1.6) + 2, "patient": round(optimal * 2.5) + 3}[label]


def is_hard(p):
    return bool(p["traits"]) or p["tech"] == "low" or p["patience"]["label"] == "hurried"


def sample(n, goal, optimal, seed=7, hard=0.35, langs=("ru", "kk", "en"), devices=("mobile", "desktop"),
           constraints=()):
    rng = random.Random(seed)
    columns = {}
    for axis, values in {**AXES, "lang": list(langs), "device": list(devices)}.items():
        col = [v for v, _ in zip(cycle(values), range(n))]
        rng.shuffle(col)
        columns[axis] = col
    traits = [[t] for t, _ in zip(cycle(TRAITS), range(n))]
    need_hard = max(1, round(n * hard))
    out = []
    for i in range(n):
        lang = columns["lang"][i]
        label = columns["patience"][i]
        trait = traits[i] if i < need_hard else []
        if trait == ["hurried"]:
            label = "hurried"
        p = {
            "id": f"p{i + 1:02d}",
            "name": NAMES[lang][i % len(NAMES[lang])],
            "goal": goal,
            "tech": columns["tech"][i],
            "patience": {"label": label, "steps": budget(label, optimal)},
            "ai_trust": columns["ai_trust"][i],
            "device": {"type": columns["device"][i], "network": columns["network"][i]},
            "lang": lang,
            "constraints": list(constraints),
            "traits": trait,
        }
        p["hard"] = is_hard(p)
        p["voice"] = VOICE[trait[0] if trait else None]
        out.append(p)
    rng.shuffle(out)
    return out


def validate(personas, min_hard=0.3):
    errors = []
    ids = [p.get("id") for p in personas]
    if len(ids) != len(set(ids)):
        errors.append("duplicate ids")
    for p in personas:
        if missing := REQUIRED - set(p):
            errors.append(f"{p.get('id')}: missing {sorted(missing)}")
            continue
        if not isinstance(p["patience"], dict) or not isinstance(p["patience"].get("steps"), int):
            errors.append(f"{p['id']}: patience.steps must be an integer")
        for axis in ("tech", "ai_trust"):
            if p[axis] not in AXES[axis]:
                errors.append(f"{p['id']}: {axis}={p[axis]}")
        if p["lang"] not in NAMES:
            errors.append(f"{p['id']}: lang={p['lang']}")
    if personas and sum(bool(p.get("hard")) for p in personas) < min_hard * len(personas):
        errors.append(f"fewer than {min_hard:.0%} hard personas")
    return errors


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sample")
    s.add_argument("--n", type=int, default=20)
    s.add_argument("--goal", required=True)
    s.add_argument("--optimal", type=int, required=True, help="actions on the shortest path to the goal")
    s.add_argument("--seed", type=int, default=7)
    s.add_argument("--hard", type=float, default=0.35)
    s.add_argument("--langs", default="ru,kk,en")
    s.add_argument("--device", default="mobile,desktop")
    s.add_argument("--constraint", action="append", default=[])
    v = sub.add_parser("validate")
    v.add_argument("file")
    a = ap.parse_args(argv)
    if a.cmd == "sample":
        ps = sample(a.n, a.goal, a.optimal, a.seed, a.hard, a.langs.split(","), a.device.split(","), a.constraint)
        print(json.dumps(ps, ensure_ascii=False, indent=1))
    else:
        errors = validate(json.load(open(a.file)))
        print("\n".join(errors) or "ok")
        sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
