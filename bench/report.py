"""Aggregate per-step metrics and blind verdicts into report.md and runs.tsv."""

from collections import Counter, defaultdict
from statistics import mean

SWAP = ".swap"  # review key suffix: the same pair judged with X and Y swapped
CHECKS = ("structure", "dead_ends", "steps", "states", "render", "asks", "nav", "actions")
CRITERIA = ("success", "flow", "states", "ia", "asks", "fit", "handoff", "scope")
TSV = (
    "ws",
    "case",
    "arm",
    "rep",
    "step",
    "mode",
    "tokens",
    "weighted_tokens",
    "reported_tokens",
    "input_tokens",
    "output_tokens",
    "cache_read_tokens",
    "cache_write_tokens",
    "tools",
    "ms",
    "cost_usd",
    "solved",
    "check",
    *(f"c_{c}" for c in CHECKS),
    "n_screens",
    "n_steps",
    "n_asks",
    "spec_lines",
    "n_files",
    "out_of_scope",
    "questions",
    "reply_words",
)


def fmt(v, digits=1):
    if v is None:
        return "—"
    return f"{v:.{digits}f}" if isinstance(v, float) else str(v)


def table(head, rows):
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    return "\n".join(lines + ["| " + " | ".join(fmt(c) for c in r) + " |" for r in rows])


def avg(vals):
    vals = [v for v in vals if v is not None]
    return mean(vals) if vals else None


def rate(vals):
    vals = [v for v in vals if v is not None]
    return f"{sum(map(bool, vals))}/{len(vals)}" if vals else "—"


def objective(rows, arm):
    mine = [r for r in rows if r["arm"] == arm]
    solved = sum(bool(r.get("solved")) for r in mine)
    tokens = [r.get("tokens") for r in mine]
    out = {"Solved, hidden checks": f"{solved}/{len(mine)}"}
    out |= {f"check `{c}` passed": rate(r.get(f"c_{c}") for r in mine) for c in CHECKS}
    out |= {
        "User steps, all flows (mean)": avg(r.get("n_steps") for r in mine),
        "Asks on the happy path (mean)": avg(r.get("n_asks") for r in mine),
        "Screens (mean)": avg(r.get("n_screens") for r in mine),
        "Spec lines (mean)": avg(r.get("spec_lines") for r in mine),
        "Files out of scope (total)": sum(r.get("out_of_scope") or 0 for r in mine),
        "Questions in replies (total)": sum(r.get("questions") or 0 for r in mine),
        "Tokens per step (mean)": avg(tokens),
        "Tokens per solved step": sum(t or 0 for t in tokens) / solved if solved and None not in tokens else None,
        "Time per step, min (mean)": avg((r.get("ms") or 0) / 60000 for r in mine) if mine else None,
        "Cost, $ (total)": sum(c for r in mine if (c := r.get("cost_usd")) is not None) or None,
    }
    return out


def blind(reviews, arms):
    """Mean blind score per criterion and arm, and overall wins per arm (each order counts once)."""
    scores, wins = defaultdict(lambda: defaultdict(list)), Counter()
    for rev in reviews.values():
        amap, s = rev["map"], rev["scores"]
        for label, arm in amap.items():
            side = s.get(label) or {}
            for step, vals in side.items():
                if isinstance(vals, dict):
                    for crit, v in vals.items():
                        if isinstance(v, (int, float)):
                            scores[arm][crit].append(v)
                elif isinstance(vals, (int, float)):
                    scores[arm][step].append(vals)
        won = (s.get("winner") or {}).get("overall")
        wins[amap.get(won, "tie")] += 1
    crits = [c for c in (*CRITERIA, "clarity") if any(scores[a][c] for a in arms)]
    rows = [[c, *(avg(scores[a][c]) for a in arms)] for c in crits]
    rows.append(["**overall wins**", *(wins[a] for a in arms)])
    return rows, wins["tie"]


def build(rows, reviews, arms):
    obj = {a: objective(rows, a) for a in arms}
    keys = list(next(iter(obj.values())))
    parts = [
        "# UX bench report",
        f"Arms: {', '.join(f'`{a}`' for a in arms)}. Steps recorded: {len(rows)}. Blind verdicts: {len(reviews)}.",
        "## Objective metrics",
        table(["Metric", *arms], [[k, *(obj[a][k] for a in arms)] for k in keys]),
        "## Per case: hidden checks",
    ]
    cases = sorted({r["case"] for r in rows})
    per_case = []
    for case in cases:
        cell = []
        for a in arms:
            mine = [r for r in rows if r["case"] == case and r["arm"] == a]
            fails = sorted({c for r in mine for c in CHECKS if r.get(f"c_{c}") is False})
            cell.append(
                f"{sum(bool(r.get('solved')) for r in mine)}/{len(mine)}" + (f" ({', '.join(fails)})" * bool(fails))
                if mine
                else "—"
            )
        per_case.append([case, *cell])
    parts.append(table(["Case", *arms], per_case))
    parts.append("## Blind X/Y review (1-5, both orders)")
    if reviews:
        brows, ties = blind(reviews, arms)
        parts.append(table(["Criterion", *arms], brows))
        parts.append(f"Ties: {ties}.")
    else:
        parts.append("No verdicts yet.")
    tsv = ["\t".join(TSV)]
    tsv += ["\t".join(fmt(r.get(c)).replace("\t", " ") for c in TSV) for r in rows]
    return "\n\n".join(parts) + "\n", "\n".join(tsv) + "\n"
