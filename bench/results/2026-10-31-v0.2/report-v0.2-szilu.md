# UX bench report

Arms: `v0.2`, `szilu`. Steps recorded: 24. Blind verdicts: 12.

## Objective metrics

| Metric | v0.2 | szilu |
|---|---|---|
| Solved, hidden checks | 9/12 | 6/12 |
| check `structure` passed | 11/12 | 10/12 |
| check `dead_ends` passed | 12/12 | 8/10 |
| check `steps` passed | 12/12 | 9/10 |
| check `states` passed | 11/12 | 10/10 |
| check `render` passed | 2/2 | 2/2 |
| check `asks` passed | 10/12 | 9/10 |
| check `nav` passed | 2/2 | 0/2 |
| check `actions` passed | 6/6 | 5/5 |
| User steps, all flows (mean) | 2.7 | 3.3 |
| Asks on the happy path (mean) | 2.2 | 2.1 |
| Screens (mean) | 8.2 | 11.1 |
| Spec lines (mean) | 159.7 | 212.4 |
| Files out of scope (total) | 0 | 0 |
| Questions in replies (total) | 0 | 0 |
| Tokens per step (mean) | 43108 | 39093.8 |
| Tokens per solved step | 57477.3 | 78187.7 |
| Time per step, min (mean) | 1.0 | 0.9 |
| Cost, $ (total) | — | — |

## Per case: hidden checks

| Case | v0.2 | szilu |
|---|---|---|
| betke-skin-quiz | 2/2 | 0/2 (dead_ends) |
| generic-checkout | 2/2 | 2/2 |
| generic-settings | 1/2 (states) | 2/2 |
| gentoon-approve | 2/2 | 1/2 (structure) |
| stb-split-flow | 0/2 (asks, structure) | 1/2 (structure) |
| warmplace-onboarding | 2/2 | 0/2 (asks, nav, steps) |

## Blind X/Y review (1-5, both orders)

| Criterion | v0.2 | szilu |
|---|---|---|
| success | 4.4 | 4.8 |
| flow | 3.9 | 3.8 |
| states | 3.8 | 4.7 |
| ia | 3.8 | 4.1 |
| asks | 4.8 | 4.5 |
| fit | 4.1 | 4.4 |
| handoff | 3.7 | 3.8 |
| scope | 4.8 | 3.8 |
| clarity | 4 | 4.1 |
| **overall wins** | 5 | 7 |

Ties: 0.
