# UX bench report

Arms: `v0.2-rc3`, `szilu`. Steps recorded: 16. Blind verdicts: 4.

## Objective metrics

| Metric | v0.2-rc3 | szilu |
|---|---|---|
| Solved, hidden checks | 4/4 | 6/12 |
| check `structure` passed | 4/4 | 10/12 |
| check `dead_ends` passed | 4/4 | 8/10 |
| check `steps` passed | 4/4 | 9/10 |
| check `states` passed | 4/4 | 10/10 |
| check `render` passed | 2/2 | 2/2 |
| check `asks` passed | 4/4 | 9/10 |
| check `nav` passed | — | 0/2 |
| check `actions` passed | 2/2 | 5/5 |
| User steps, all flows (mean) | 1.8 | 3.3 |
| Asks on the happy path (mean) | 1 | 2.1 |
| Screens (mean) | 7.8 | 11.1 |
| Spec lines (mean) | 143 | 212.4 |
| Files out of scope (total) | 0 | 0 |
| Questions in replies (total) | 0 | 0 |
| Tokens per step (mean) | 41718 | 39093.8 |
| Tokens per solved step | 41718.0 | 78187.7 |
| Time per step, min (mean) | 0.7 | 0.9 |
| Cost, $ (total) | — | — |

## Per case: hidden checks

| Case | v0.2-rc3 | szilu |
|---|---|---|
| betke-skin-quiz | 2/2 | 0/2 (dead_ends) |
| generic-checkout | — | 2/2 |
| generic-settings | 2/2 | 2/2 |
| gentoon-approve | — | 1/2 (structure) |
| stb-split-flow | — | 1/2 (structure) |
| warmplace-onboarding | — | 0/2 (asks, nav, steps) |

## Blind X/Y review (1-5, both orders)

| Criterion | v0.2-rc3 | szilu |
|---|---|---|
| success | 4.5 | 4.8 |
| flow | 4 | 4 |
| states | 4 | 4.5 |
| ia | 4 | 4.2 |
| asks | 4.2 | 4.8 |
| fit | 3.8 | 4.8 |
| handoff | 4 | 4 |
| scope | 5 | 3.8 |
| clarity | 4 | 4 |
| **overall wins** | 1 | 3 |

Ties: 0.
