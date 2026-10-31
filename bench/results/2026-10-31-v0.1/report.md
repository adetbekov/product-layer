# product-layer v0.1: full bench, 2026-10-31

Six cases, two repeats, six arms (`kortix-genui` on `betke-skin-quiz` only): 62 agent sessions, 84 blind verdicts.
What was run and why it deviates from the plan: [notes.md](notes.md).

Arms: `bare`, `product-layer`, `szilu`, `design-for-ai`, `kortix-genui`, `product-layer+visual`. Steps recorded: 62. Blind verdicts: 84.

## Objective metrics

| Metric | bare | product-layer | szilu | design-for-ai | kortix-genui | product-layer+visual |
|---|---|---|---|---|---|---|
| Solved, hidden checks | 2/12 | 8/12 | 8/12 | 3/12 | 0/2 | 8/12 |
| check `structure` passed | 8/12 | 12/12 | 11/12 | 8/12 | 0/2 | 11/12 |
| check `dead_ends` passed | 5/8 | 11/12 | 10/11 | 5/8 | — | 10/11 |
| check `steps` passed | 6/8 | 12/12 | 9/11 | 7/8 | — | 11/11 |
| check `states` passed | 8/8 | 12/12 | 11/11 | 7/8 | — | 11/11 |
| check `render` passed | 1/1 | 2/2 | 2/2 | 1/1 | — | 2/2 |
| check `asks` passed | 6/8 | 10/12 | 10/11 | 7/8 | — | 10/11 |
| check `nav` passed | 1/2 | 0/2 | 0/2 | 1/1 | — | 1/2 |
| check `actions` passed | 3/3 | 6/6 | 6/6 | 5/5 | — | 5/5 |
| User steps, all flows (mean) | 3.6 | 2.8 | 3.4 | 2.9 | — | 2.5 |
| Asks on the happy path (mean) | 3.1 | 1.8 | 2.2 | 2 | — | 2.2 |
| Screens (mean) | 10.4 | 10.8 | 9.8 | 9.9 | — | 10.7 |
| Spec lines (mean) | 172.3 | 236.2 | 187.5 | 176.7 | 122.5 | 220.5 |
| Files out of scope (total) | 0 | 0 | 0 | 0 | 0 | 0 |
| Questions in replies (total) | 0 | 0 | 0 | 0 | 0 | 0 |
| Tokens per step (mean) | 29644.7 | 47149.4 | 38219 | 35806.1 | 36170 | 46116.9 |
| Tokens per solved step | 177868.0 | 70724.1 | 57328.5 | 143224.3 | — | 69175.4 |
| Time per step, min (mean) | 0.8 | 1.3 | 0.9 | 0.8 | 0.7 | 1.2 |
| Cost, $ (total) | — | — | — | — | — | — |

## Per case: hidden checks

| Case | bare | product-layer | szilu | design-for-ai | kortix-genui | product-layer+visual |
|---|---|---|---|---|---|---|
| betke-skin-quiz | 0/2 (dead_ends, structure) | 2/2 | 2/2 | 0/2 (dead_ends, structure) | 0/2 (structure) | 2/2 |
| generic-checkout | 1/2 (structure) | 1/2 (asks) | 2/2 | 1/2 (structure) | — | 2/2 |
| generic-settings | 0/2 (dead_ends, structure) | 1/2 (dead_ends) | 1/2 (dead_ends) | 0/2 (dead_ends, states) | — | 1/2 (dead_ends) |
| gentoon-approve | 1/2 (structure) | 2/2 | 2/2 | 2/2 | — | 1/2 (structure) |
| stb-split-flow | 0/2 (asks, dead_ends) | 2/2 | 1/2 (structure) | 0/2 (dead_ends, structure) | — | 1/2 (asks) |
| warmplace-onboarding | 0/2 (asks, nav, steps) | 0/2 (asks, nav) | 0/2 (asks, nav, steps) | 0/2 (asks, steps, structure) | — | 1/2 (nav) |

## Blind X/Y verdicts by pair

Judge: Fable 5.1, one fresh session per verdict, workspaces under opaque names. Wins are "overall" winners.

| Pair (A vs B) | Verdicts | A wins | B wins | Orders | Full report |
|---|---|---|---|---|---|
| product-layer vs bare | 24 | 16 | 8 | both | [report-product-layer-bare.md](report-product-layer-bare.md) |
| product-layer vs szilu | 24 | 15 | 9 | both | [report-product-layer-szilu.md](report-product-layer-szilu.md) |
| product-layer vs design-for-ai | 24 | 20 | 4 | both | [report-product-layer-design-for-ai.md](report-product-layer-design-for-ai.md) |
| product-layer vs kortix-genui (betke only) | 4 | 3 | 1 | both | [report-product-layer-kortix-genui.md](report-product-layer-kortix-genui.md) |
| product-layer+visual vs product-layer | 8 | 2 | 6 | one per repeat, alternating | [report-product-layer+visual-product-layer.md](report-product-layer+visual-product-layer.md) |

Per case, product-layer wins / verdicts:

| Case | vs bare | vs szilu | vs design-for-ai | vs kortix-genui |
|---|---|---|---|---|
| betke-skin-quiz | 3/4 | 2/4 | 3/4 | 3/4 |
| generic-checkout | 2/4 | 1/4 | 3/4 | — |
| generic-settings | 1/4 | 2/4 | 3/4 | — |
| gentoon-approve | 3/4 | 4/4 | 4/4 | — |
| stb-split-flow | 3/4 | 2/4 | 3/4 | — |
| warmplace-onboarding | 4/4 | 4/4 | 4/4 | — |

## Blind X/Y review, mean scores per arm over all its verdicts (1-5, both orders)

| Criterion | bare | product-layer | szilu | design-for-ai | kortix-genui | product-layer+visual |
|---|---|---|---|---|---|---|
| success | 4.8 | 4.8 | 4.8 | 4.6 | 4.8 | 4.9 |
| flow | 3.6 | 4.1 | 3.8 | 3.5 | 4 | 4 |
| states | 4 | 4.7 | 4.2 | 4.0 | 3.8 | 4.4 |
| ia | 3.7 | 4.2 | 3.8 | 4.0 | 4 | 4.1 |
| asks | 4.3 | 4.8 | 4.6 | 4.5 | 4.2 | 4.6 |
| fit | 3.9 | 4.2 | 3.9 | 3.9 | 4.2 | 4 |
| handoff | 3.6 | 3.9 | 3.6 | 3.5 | 4.5 | 3.6 |
| scope | 4.4 | 3.7 | 4.3 | 4.5 | 5 | 3.9 |
| clarity | 4.1 | 3.8 | 4.3 | 4.2 | 4 | 4.2 |
| **overall wins** | 8 | 60 | 9 | 4 | 1 | 2 |

Ties: 0.
