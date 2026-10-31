# UX bench report

Arms: `product-layer`, `design-for-ai`. Steps recorded: 24. Blind verdicts: 24.

## Objective metrics

| Metric | product-layer | design-for-ai |
|---|---|---|
| Solved, hidden checks | 8/12 | 3/12 |
| check `structure` passed | 12/12 | 8/12 |
| check `dead_ends` passed | 11/12 | 5/8 |
| check `steps` passed | 12/12 | 7/8 |
| check `states` passed | 12/12 | 7/8 |
| check `render` passed | 2/2 | 1/1 |
| check `asks` passed | 10/12 | 7/8 |
| check `nav` passed | 0/2 | 1/1 |
| check `actions` passed | 6/6 | 5/5 |
| User steps, all flows (mean) | 2.8 | 2.9 |
| Asks on the happy path (mean) | 1.8 | 2 |
| Screens (mean) | 10.8 | 9.9 |
| Spec lines (mean) | 236.2 | 176.7 |
| Files out of scope (total) | 0 | 0 |
| Questions in replies (total) | 0 | 0 |
| Tokens per step (mean) | 47149.4 | 35806.1 |
| Tokens per solved step | 70724.1 | 143224.3 |
| Time per step, min (mean) | 1.3 | 0.8 |
| Cost, $ (total) | — | — |

## Per case: hidden checks

| Case | product-layer | design-for-ai |
|---|---|---|
| betke-skin-quiz | 2/2 | 0/2 (dead_ends, structure) |
| generic-checkout | 1/2 (asks) | 1/2 (structure) |
| generic-settings | 1/2 (dead_ends) | 0/2 (dead_ends, states) |
| gentoon-approve | 2/2 | 2/2 |
| stb-split-flow | 2/2 | 0/2 (dead_ends, structure) |
| warmplace-onboarding | 0/2 (asks, nav) | 0/2 (asks, steps, structure) |

## Blind X/Y review (1-5, both orders)

| Criterion | product-layer | design-for-ai |
|---|---|---|
| success | 4.9 | 4.6 |
| flow | 4.2 | 3.5 |
| states | 4.8 | 4.0 |
| ia | 4.3 | 4.0 |
| asks | 4.9 | 4.5 |
| fit | 4.2 | 3.9 |
| handoff | 4.0 | 3.5 |
| scope | 3.7 | 4.5 |
| clarity | 3.8 | 4.2 |
| **overall wins** | 20 | 4 |

Ties: 0.
