# UX bench report

Arms: `v0.2`, `bare`. Steps recorded: 24. Blind verdicts: 12.

## Objective metrics

| Metric | v0.2 | bare |
|---|---|---|
| Solved, hidden checks | 9/12 | 3/12 |
| check `structure` passed | 11/12 | 6/12 |
| check `dead_ends` passed | 12/12 | 6/6 |
| check `steps` passed | 12/12 | 6/6 |
| check `states` passed | 11/12 | 6/6 |
| check `render` passed | 2/2 | — |
| check `asks` passed | 10/12 | 3/6 |
| check `nav` passed | 2/2 | 1/2 |
| check `actions` passed | 6/6 | 3/3 |
| User steps, all flows (mean) | 2.7 | 4 |
| Asks on the happy path (mean) | 2.2 | 3.2 |
| Screens (mean) | 8.2 | 10.3 |
| Spec lines (mean) | 159.7 | 164 |
| Files out of scope (total) | 0 | 0 |
| Questions in replies (total) | 0 | 0 |
| Tokens per step (mean) | 43108 | 30335.8 |
| Tokens per solved step | 57477.3 | 121343.0 |
| Time per step, min (mean) | 1.0 | 0.7 |
| Cost, $ (total) | — | — |

## Per case: hidden checks

| Case | v0.2 | bare |
|---|---|---|
| betke-skin-quiz | 2/2 | 0/2 (structure) |
| generic-checkout | 2/2 | 0/2 (structure) |
| generic-settings | 1/2 (states) | 2/2 |
| gentoon-approve | 2/2 | 1/2 (structure) |
| stb-split-flow | 0/2 (asks, structure) | 0/2 (asks, structure) |
| warmplace-onboarding | 2/2 | 0/2 (asks, nav) |

## Blind X/Y review (1-5, both orders)

| Criterion | v0.2 | bare |
|---|---|---|
| success | 4.8 | 4.9 |
| flow | 4.2 | 3.7 |
| states | 4.1 | 4.2 |
| ia | 4 | 3.9 |
| asks | 4.8 | 4.5 |
| fit | 4.2 | 3.8 |
| handoff | 3.8 | 3.7 |
| scope | 4.8 | 4 |
| clarity | 4.2 | 3.9 |
| **overall wins** | 9 | 3 |

Ties: 0.
