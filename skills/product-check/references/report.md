# report - findings people can act on

One `report.md` per run, screenshots in `shots/` next to it. The reader is the
team that fixes the product and the product-layer author who owns the flow.

## Layout

```markdown
# product-check: <product> - <date>

Verdict: pass | conditional | fail | incomplete
Persona: <three-line card, or "crowd: N personas, see funnel">
Mode: walk | crowd    Engine: Playwright CLI <version>    URL: <url>

## Tasks
| Task | Optimum | Actions | Messages (chat) | Result |

## Findings
### ISSUE-1: <what breaks, in user words>
...

## Not tested
- <area> - <why>
```

Verdict: **fail** if any critical finding is confirmed; **conditional** for
high ones only; **incomplete** if a top task has no artifact; else **pass**.

## Finding format

```markdown
### ISSUE-3: Promo code "Apply" does nothing
Severity: high    Confidence: confirmed (2/2 repros)    Rule: WK-2, ST-4
Where: /cart, mobile    Affected: 7 of 20 personas (crowd) | walk persona
Steps:
1. Open /, add any product, open Cart.
2. Type FRESH10 in Promo code, press Apply.
Expected: the total changes, or a message says the code is invalid.
Actual: nothing changes; no message; console clean.
Evidence: shots/issue-3-before.png, shots/issue-3-after.png
```

- **Severity**: critical (blocks a top task, loses data or money), high
  (task done with a detour or a wrong result), medium (friction, extra step),
  low (polish).
- **Confidence**: confirmed (reproduced twice from a clean start), likely
  (seen twice, one path), seen once. Only confirmed findings count for the
  verdict.
- **Rule**: product-check id (`WK-2`, `GW-1`) plus a product-layer id when one
  fits (`FL-2`, `SR-4`, `GC-7`, `ST-4`), so the spec owner sees which rule the
  build broke.
- **Affected**: share of personas that hit it (crowd), or the walk persona.
- Describe what happened, not how to fix the code. One suggested product
  change is fine when obvious.

## RP-1 · Every finding has steps and a screenshot · CRITICAL

**Check.** Numbered steps from a real entry point, expected vs actual, and at
least one screenshot path that exists.
**Why.** A finding nobody can reproduce gets closed.
**Bug if.** (In the report.) A finding lacks steps or evidence.

## RP-2 · Noise filter for persona complaints · HIGH

**Check.** Tag every persona complaint before it becomes a finding:
- **RED** - a problem for any user, even a busy competent one: blocked task,
  silent control, data loss, extra step with no reason. Becomes a finding.
- **YELLOW** - valid but minor or limited to some users. Finding with low or
  medium severity.
- **WHITE** - persona noise: a taste, a misreading only this persona would
  make. Dropped; count them.
- **GREEN** - an idea for a feature, not a defect. Listed under ideas.
Test: would a busy, competent adult complain about this too?
**Why.** Hard personas are useful because they complain; most of their
complaints are not bugs.
**Bug if.** WHITE items appear as findings, or RED items are lost.

## RP-3 · Dedup with a fresh subagent · HIGH

**Check.** Before the verdict, give the findings list (titles, steps, rule)
to a fresh subagent that has not seen the walk. It labels each one:
- **KEEP** - distinct and specific;
- **GENERIC** - true of any product ("could be faster"), drop or make
  specific;
- **DUPLICATE of ISSUE-n** - merge, keep the better evidence.
No subagents available: after the walk, reread the list cold, title by title,
and apply the same labels.
**Why.** The walker is attached to its findings; a fresh reader catches
duplicates and vague items.
**Bug if.** Two findings describe the same root cause.

## Crowd section

Paste `funnel.md` from `crowd.py aggregate`, then:

- clusters of drop-off reasons and dead clicks, each with the variant, stage
  and share of personas, tagged RED / YELLOW / WHITE / GREEN;
- the direction line with its interval and the sentence: "Direction only:
  simulated completion is not a conversion forecast";
- the run cost (tokens and dollars) and the model;
- for the top RED cluster, a walk-mode repro with steps and a screenshot.

## Handing on

- To the product-layer author: findings grouped by product-layer rule id.
- To engineering: confirmed critical and high findings; for each, one
  Playwright check that would have caught it (a few lines) is a welcome
  extra.
- To people: what the simulation cannot answer (trust, emotions, price,
  accessibility with real assistive tech).
