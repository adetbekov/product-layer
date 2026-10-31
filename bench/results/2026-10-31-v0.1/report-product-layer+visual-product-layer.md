# UX bench report

Arms: `product-layer+visual`, `product-layer`. Steps recorded: 24. Blind verdicts: 8.

## Objective metrics

| Metric | product-layer+visual | product-layer |
|---|---|---|
| Solved, hidden checks | 8/12 | 8/12 |
| check `structure` passed | 11/12 | 12/12 |
| check `dead_ends` passed | 10/11 | 11/12 |
| check `steps` passed | 11/11 | 12/12 |
| check `states` passed | 11/11 | 12/12 |
| check `render` passed | 2/2 | 2/2 |
| check `asks` passed | 10/11 | 10/12 |
| check `nav` passed | 1/2 | 0/2 |
| check `actions` passed | 5/5 | 6/6 |
| User steps, all flows (mean) | 2.5 | 2.8 |
| Asks on the happy path (mean) | 2.2 | 1.8 |
| Screens (mean) | 10.7 | 10.8 |
| Spec lines (mean) | 220.5 | 236.2 |
| Files out of scope (total) | 0 | 0 |
| Questions in replies (total) | 0 | 0 |
| Tokens per step (mean) | 46116.9 | 47149.4 |
| Tokens per solved step | 69175.4 | 70724.1 |
| Time per step, min (mean) | 1.2 | 1.3 |
| Cost, $ (total) | — | — |

## Per case: hidden checks

| Case | product-layer+visual | product-layer |
|---|---|---|
| betke-skin-quiz | 2/2 | 2/2 |
| generic-checkout | 2/2 | 1/2 (asks) |
| generic-settings | 1/2 (dead_ends) | 1/2 (dead_ends) |
| gentoon-approve | 1/2 (structure) | 2/2 |
| stb-split-flow | 1/2 (asks) | 2/2 |
| warmplace-onboarding | 1/2 (nav) | 0/2 (asks, nav) |

## Blind X/Y review (1-5, both orders)

| Criterion | product-layer+visual | product-layer |
|---|---|---|
| success | 4.9 | 4.9 |
| flow | 4 | 4 |
| states | 4.4 | 4.6 |
| ia | 4.1 | 4 |
| asks | 4.6 | 4.8 |
| fit | 4 | 4.5 |
| handoff | 3.6 | 3.9 |
| scope | 3.9 | 4 |
| clarity | 4.2 | 3.8 |
| **overall wins** | 2 | 6 |

Ties: 0.
