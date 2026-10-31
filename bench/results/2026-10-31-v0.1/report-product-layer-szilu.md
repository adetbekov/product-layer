# UX bench report

Arms: `product-layer`, `szilu`. Steps recorded: 24. Blind verdicts: 24.

## Objective metrics

| Metric | product-layer | szilu |
|---|---|---|
| Solved, hidden checks | 8/12 | 8/12 |
| check `structure` passed | 12/12 | 11/12 |
| check `dead_ends` passed | 11/12 | 10/11 |
| check `steps` passed | 12/12 | 9/11 |
| check `states` passed | 12/12 | 11/11 |
| check `render` passed | 2/2 | 2/2 |
| check `asks` passed | 10/12 | 10/11 |
| check `nav` passed | 0/2 | 0/2 |
| check `actions` passed | 6/6 | 6/6 |
| User steps, all flows (mean) | 2.8 | 3.4 |
| Asks on the happy path (mean) | 1.8 | 2.2 |
| Screens (mean) | 10.8 | 9.8 |
| Spec lines (mean) | 236.2 | 187.5 |
| Files out of scope (total) | 0 | 0 |
| Questions in replies (total) | 0 | 0 |
| Tokens per step (mean) | 47149.4 | 38219 |
| Tokens per solved step | 70724.1 | 57328.5 |
| Time per step, min (mean) | 1.3 | 0.9 |
| Cost, $ (total) | — | — |

## Per case: hidden checks

| Case | product-layer | szilu |
|---|---|---|
| betke-skin-quiz | 2/2 | 2/2 |
| generic-checkout | 1/2 (asks) | 2/2 |
| generic-settings | 1/2 (dead_ends) | 1/2 (dead_ends) |
| gentoon-approve | 2/2 | 2/2 |
| stb-split-flow | 2/2 | 1/2 (structure) |
| warmplace-onboarding | 0/2 (asks, nav) | 0/2 (asks, nav, steps) |

## Blind X/Y review (1-5, both orders)

| Criterion | product-layer | szilu |
|---|---|---|
| success | 4.9 | 4.8 |
| flow | 4.0 | 3.8 |
| states | 4.6 | 4.2 |
| ia | 4.1 | 3.8 |
| asks | 4.8 | 4.6 |
| fit | 4.1 | 3.9 |
| handoff | 3.9 | 3.6 |
| scope | 3.8 | 4.3 |
| clarity | 3.8 | 4.3 |
| **overall wins** | 15 | 9 |

Ties: 0.
