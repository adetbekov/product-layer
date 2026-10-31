# UX bench report

Arms: `v0.2-rc3`, `bare`. Steps recorded: 16. Blind verdicts: 4.

## Objective metrics

| Metric | v0.2-rc3 | bare |
|---|---|---|
| Solved, hidden checks | 4/4 | 3/12 |
| check `structure` passed | 4/4 | 6/12 |
| check `dead_ends` passed | 4/4 | 6/6 |
| check `steps` passed | 4/4 | 6/6 |
| check `states` passed | 4/4 | 6/6 |
| check `render` passed | 2/2 | — |
| check `asks` passed | 4/4 | 3/6 |
| check `nav` passed | — | 1/2 |
| check `actions` passed | 2/2 | 3/3 |
| User steps, all flows (mean) | 1.8 | 4 |
| Asks on the happy path (mean) | 1 | 3.2 |
| Screens (mean) | 7.8 | 10.3 |
| Spec lines (mean) | 143 | 164 |
| Files out of scope (total) | 0 | 0 |
| Questions in replies (total) | 0 | 0 |
| Tokens per step (mean) | 41718 | 30335.8 |
| Tokens per solved step | 41718.0 | 121343.0 |
| Time per step, min (mean) | 0.7 | 0.7 |
| Cost, $ (total) | — | — |

## Per case: hidden checks

| Case | v0.2-rc3 | bare |
|---|---|---|
| betke-skin-quiz | 2/2 | 0/2 (structure) |
| generic-checkout | — | 0/2 (structure) |
| generic-settings | 2/2 | 2/2 |
| gentoon-approve | — | 1/2 (structure) |
| stb-split-flow | — | 0/2 (asks, structure) |
| warmplace-onboarding | — | 0/2 (asks, nav) |

## Blind X/Y review (1-5, both orders)

| Criterion | v0.2-rc3 | bare |
|---|---|---|
| success | 4.8 | 4.2 |
| flow | 4.5 | 3.8 |
| states | 4.5 | 3.8 |
| ia | 4 | 3.8 |
| asks | 4.8 | 4.8 |
| fit | 4.2 | 4.5 |
| handoff | 4 | 3.5 |
| scope | 4.5 | 4.8 |
| clarity | 4 | 3.2 |
| **overall wins** | 4 | 0 |

Ties: 0.
