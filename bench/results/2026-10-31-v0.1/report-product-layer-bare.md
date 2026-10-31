# UX bench report

Arms: `product-layer`, `bare`. Steps recorded: 24. Blind verdicts: 24.

## Objective metrics

| Metric | product-layer | bare |
|---|---|---|
| Solved, hidden checks | 8/12 | 2/12 |
| check `structure` passed | 12/12 | 8/12 |
| check `dead_ends` passed | 11/12 | 5/8 |
| check `steps` passed | 12/12 | 6/8 |
| check `states` passed | 12/12 | 8/8 |
| check `render` passed | 2/2 | 1/1 |
| check `asks` passed | 10/12 | 6/8 |
| check `nav` passed | 0/2 | 1/2 |
| check `actions` passed | 6/6 | 3/3 |
| User steps, all flows (mean) | 2.8 | 3.6 |
| Asks on the happy path (mean) | 1.8 | 3.1 |
| Screens (mean) | 10.8 | 10.4 |
| Spec lines (mean) | 236.2 | 172.3 |
| Files out of scope (total) | 0 | 0 |
| Questions in replies (total) | 0 | 0 |
| Tokens per step (mean) | 47149.4 | 29644.7 |
| Tokens per solved step | 70724.1 | 177868.0 |
| Time per step, min (mean) | 1.3 | 0.8 |
| Cost, $ (total) | — | — |

## Per case: hidden checks

| Case | product-layer | bare |
|---|---|---|
| betke-skin-quiz | 2/2 | 0/2 (dead_ends, structure) |
| generic-checkout | 1/2 (asks) | 1/2 (structure) |
| generic-settings | 1/2 (dead_ends) | 0/2 (dead_ends, structure) |
| gentoon-approve | 2/2 | 1/2 (structure) |
| stb-split-flow | 2/2 | 0/2 (asks, dead_ends) |
| warmplace-onboarding | 0/2 (asks, nav) | 0/2 (asks, nav, steps) |

## Blind X/Y review (1-5, both orders)

| Criterion | product-layer | bare |
|---|---|---|
| success | 4.7 | 4.8 |
| flow | 4.1 | 3.6 |
| states | 4.7 | 4 |
| ia | 4.2 | 3.7 |
| asks | 4.8 | 4.3 |
| fit | 4.2 | 3.9 |
| handoff | 3.8 | 3.6 |
| scope | 3.6 | 4.4 |
| clarity | 3.7 | 4.1 |
| **overall wins** | 16 | 8 |

Ties: 0.
