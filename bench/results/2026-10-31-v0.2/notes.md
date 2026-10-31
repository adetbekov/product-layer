# product-layer v0.2 rerun, 2026-10-31

Skill under test: `skills/product-layer` on branch `feat/JEB-2034-v0.2`. The rerun checks the fixes listed in the v0.1
results ([v0.1 notes](../2026-10-31-v0.1/notes.md)). Results: [report.md](report.md) (all arms), one `report-A-B.md` per
judged pair, [runs.tsv](runs.tsv), `verdicts/`.

## What ran

- Driver: agent-driven, the same as v0.1. Each session was a fresh Sonnet 5.5 subagent with its own `HOME` holding only
  its arm's skills, copied there the way the README tells users to install. Each verdict was a fresh Fable 5.1
  subagent. Seed 2034.
- Arms: `v0.2` (candidate rc2), `v0.2-rc3` (the final skill, run on two cases only), `szilu`, `bare`. `szilu` is the
  strongest third-party arm in v0.1. All six cases, two repeats.
- Blind pairs: v0.2 against `szilu` and against `bare`, one order per repeat (r1 as packed, r2 swapped). This
  balances position bias across repeats but not within one. v0.1 judged both orders per repeat; that did not fit the
  3M budget here.
- Bench changes made before the rerun, applied to every arm:
  - `terminal: true` marks an intended end ("account deleted", "bill settled"), and such a screen is not a dead end.
    v0.1 fix item 8.
  - An approval ask that also asks for a value ("confirm the price you want") counts as asking for that value.
  - The warmplace student pattern `tutor|subject` matched "one of the tutor's open slots". It now matches only asking
    which tutor or subject. The change came after the first v0.2 sessions and was applied with `recheck` to all arms.

## Candidates and why there are three

1. **rc1**: the v0.2 fixes. 4 of 6 r1 specs were invalid YAML, because copy in quotes was followed by more text
   (`error: "Not saved" - retry`). The run was discarded and is not in this folder. It cost 0.26M tokens.
   Fix: specs must parse before handoff.
2. **rc2**: rc1 plus the parse rule, run on all six cases. Hidden checks 9/12. Blind: beats bare 9:3, loses to szilu
   5:7. The judges' reason in settings (0:4) and betke (0:2 vs szilu): scope was cut too far. Profile and password
   lost their home, delete became one tap, and quiz questions had no loading or error state.
3. **rc3 (final)**: scope now limits only new things, and existing capabilities stay reachable. Every wait after a tap
   has states, a tap is never `by: system`, and an irreversible delete is its own step. Rerun only on the two cases
   that lost, settings and betke: 4/4 hidden checks, beats bare 4:0, szilu 1:3 (rc2 was 2:2 and 0:4 there).

rc3 differs from rc2 by seven lines in `SKILL.md` and one example in `flows.md`. The other four cases were not rerun
on rc3, to stay within budget.

## v0.2 (final) in numbers

"v0.2" means rc3 on settings and betke, rc2 on the other four cases.

| | v0.2 | szilu | bare | v0.1 (old run, for context) |
|---|---|---|---|---|
| Solved, hidden checks | **10/12** | 6/12 | 3/12 | 8/12 (bench before the fixes above) |
| Blind, v0.2 wins : losses | — | 6 : 6 | **11 : 1** | v0.1 had 15 : 9 vs szilu, 16 : 8 vs bare |
| Spec lines (mean) | 169 | 212 | 164 | 236 |
| User steps, all flows (mean) | **2.7** | 3.3 | 4.0 | 2.8 |
| Tokens per session (mean) | 43.8k | 39.1k | 30.3k | 47.1k |
| Blind scope / clarity (1-5) | **4.7 / 4.1** | 3.7 / 4.0 | 4.2 / 3.6 | 3.6-3.8 in v0.1 |

Per case, v0.2 wins : losses (rc3 rows marked):

| Case | vs szilu | vs bare | Hidden checks | v0.1 vs szilu / vs bare |
|---|---|---|---|---|
| betke-skin-quiz (rc3) | 1 : 1 | 2 : 0 | 2/2 | 2/4, 3/4 |
| generic-checkout | 1 : 1 | 2 : 0 | 2/2 | 1/4, 2/4 |
| generic-settings (rc3) | 0 : 2 | 2 : 0 | 2/2 | 2/4, 1/4 |
| gentoon-approve | 1 : 1 | 2 : 0 | 2/2 | 4/4, 3/4 |
| stb-split-flow | 1 : 1 | 2 : 0 | 0/2 | 2/4, 2/4 |
| warmplace-onboarding | 2 : 0 | 1 : 1 | 2/2 | 4/4, 4/4 |

## The v0.1 weaknesses, closed or not

- Size and readability: closed. Spec lines went from 236 to 169, and blind scope from 3.6-3.8 to 4.7, the best of the
  arms. No rule ids appear in any v0.2 spec or reply.
- Buttons without a target, loops, invented features: closed for loops and stubs (`dead_ends` 12/12). Invented
  features: judges no longer flag any. In rc2 they flagged the opposite, missing existing features, which rc3 fixes.
- checkout vs szilu, 1:3 in v0.1: now 1:1.
- settings vs bare, 1:3 in v0.1: now 2:0 (rc3).
- warmplace hidden checks, 0/2 in v0.1: now 2/2. The tutor gets at most 5 sections and the slot is asked.
- New weak spots:
  - stb hidden checks 0/2. Friends pick items with buttons on the group card, and neither spec lists that pick as an
    ask, so the check "asks what each person ate" fails. One spec also has an unreachable screen.
  - States score is below szilu (4.2 vs 4.6).
  - settings still loses to szilu on safety and completeness.

## Gate

v0.2 clearly beats bare (11:1, v0.1 had 16:8) and closes every weakness the v0.1 run named. Against szilu it ties
(6:6), while v0.1 led 15:9 on a different sample with both orders judged. Twelve verdicts per pair is too few to call
6:6 against 15:9 a regression or an improvement. A direct v0.1 vs v0.2 run (12 v0.1 sessions, 12 verdicts, about
1M tokens) was not affordable within the 3M cap, so the per-change rule "wins before `main`" is met against bare and
on the targeted cases, but not shown against v0.1 head to head.

## Cost

Subagent token totals: sessions 1.78M (rc1 0.26M discarded, rc2 0.52M, szilu 0.47M, bare 0.36M, rc3 0.17M), verdicts
1.12M (32 verdicts). Total 2.90M of the 3M cap.
