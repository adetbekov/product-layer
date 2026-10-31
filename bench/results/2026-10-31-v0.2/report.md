# UX bench report

Arms: `v0.2`, `szilu`, `bare`, `v0.2-rc3`. Steps recorded: 40. Blind verdicts: 32.

## Objective metrics

| Metric | v0.2 | szilu | bare | v0.2-rc3 |
|---|---|---|---|---|
| Solved, hidden checks | 9/12 | 6/12 | 3/12 | 4/4 |
| check `structure` passed | 11/12 | 10/12 | 6/12 | 4/4 |
| check `dead_ends` passed | 12/12 | 8/10 | 6/6 | 4/4 |
| check `steps` passed | 12/12 | 9/10 | 6/6 | 4/4 |
| check `states` passed | 11/12 | 10/10 | 6/6 | 4/4 |
| check `render` passed | 2/2 | 2/2 | — | 2/2 |
| check `asks` passed | 10/12 | 9/10 | 3/6 | 4/4 |
| check `nav` passed | 2/2 | 0/2 | 1/2 | — |
| check `actions` passed | 6/6 | 5/5 | 3/3 | 2/2 |
| User steps, all flows (mean) | 2.7 | 3.3 | 4 | 1.8 |
| Asks on the happy path (mean) | 2.2 | 2.1 | 3.2 | 1 |
| Screens (mean) | 8.2 | 11.1 | 10.3 | 7.8 |
| Spec lines (mean) | 159.7 | 212.4 | 164 | 143 |
| Files out of scope (total) | 0 | 0 | 0 | 0 |
| Questions in replies (total) | 0 | 0 | 0 | 0 |
| Tokens per step (mean) | 43108 | 39093.8 | 30335.8 | 41718 |
| Tokens per solved step | 57477.3 | 78187.7 | 121343.0 | 41718.0 |
| Time per step, min (mean) | 1.0 | 0.9 | 0.7 | 0.7 |
| Cost, $ (total) | — | — | — | — |

## Per case: hidden checks

| Case | v0.2 | szilu | bare | v0.2-rc3 |
|---|---|---|---|---|
| betke-skin-quiz | 2/2 | 0/2 (dead_ends) | 0/2 (structure) | 2/2 |
| generic-checkout | 2/2 | 2/2 | 0/2 (structure) | — |
| generic-settings | 1/2 (states) | 2/2 | 2/2 | 2/2 |
| gentoon-approve | 2/2 | 1/2 (structure) | 1/2 (structure) | — |
| stb-split-flow | 0/2 (asks, structure) | 1/2 (structure) | 0/2 (asks, structure) | — |
| warmplace-onboarding | 2/2 | 0/2 (asks, nav, steps) | 0/2 (asks, nav) | — |

## Blind X/Y review (1-5, both orders)

| Criterion | v0.2 | szilu | bare | v0.2-rc3 |
|---|---|---|---|---|
| success | 4.6 | 4.8 | 4.8 | 4.6 |
| flow | 4.0 | 3.9 | 3.7 | 4.2 |
| states | 3.9 | 4.6 | 4.1 | 4.2 |
| ia | 3.9 | 4.1 | 3.9 | 4 |
| asks | 4.8 | 4.6 | 4.6 | 4.5 |
| fit | 4.2 | 4.5 | 3.9 | 4 |
| handoff | 3.8 | 3.9 | 3.6 | 4 |
| scope | 4.8 | 3.8 | 4.2 | 4.8 |
| clarity | 4.1 | 4.1 | 3.8 | 4 |
| **overall wins** | 14 | 10 | 3 | 5 |

Ties: 0.
