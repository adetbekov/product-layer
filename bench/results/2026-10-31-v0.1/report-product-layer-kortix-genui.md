# UX bench report

Arms: `product-layer`, `kortix-genui`. Steps recorded: 14. Blind verdicts: 4.

## Objective metrics

| Metric | product-layer | kortix-genui |
|---|---|---|
| Solved, hidden checks | 8/12 | 0/2 |
| check `structure` passed | 12/12 | 0/2 |
| check `dead_ends` passed | 11/12 | — |
| check `steps` passed | 12/12 | — |
| check `states` passed | 12/12 | — |
| check `render` passed | 2/2 | — |
| check `asks` passed | 10/12 | — |
| check `nav` passed | 0/2 | — |
| check `actions` passed | 6/6 | — |
| User steps, all flows (mean) | 2.8 | — |
| Asks on the happy path (mean) | 1.8 | — |
| Screens (mean) | 10.8 | — |
| Spec lines (mean) | 236.2 | 122.5 |
| Files out of scope (total) | 0 | 0 |
| Questions in replies (total) | 0 | 0 |
| Tokens per step (mean) | 47149.4 | 36170 |
| Tokens per solved step | 70724.1 | — |
| Time per step, min (mean) | 1.3 | 0.7 |
| Cost, $ (total) | — | — |

## Per case: hidden checks

| Case | product-layer | kortix-genui |
|---|---|---|
| betke-skin-quiz | 2/2 | 0/2 (structure) |
| generic-checkout | 1/2 (asks) | — |
| generic-settings | 1/2 (dead_ends) | — |
| gentoon-approve | 2/2 | — |
| stb-split-flow | 2/2 | — |
| warmplace-onboarding | 0/2 (asks, nav) | — |

## Blind X/Y review (1-5, both orders)

| Criterion | product-layer | kortix-genui |
|---|---|---|
| success | 5 | 4.8 |
| flow | 4.5 | 4 |
| states | 4.5 | 3.8 |
| ia | 4 | 4 |
| asks | 5 | 4.2 |
| fit | 4.5 | 4.2 |
| handoff | 3.5 | 4.5 |
| scope | 3.8 | 5 |
| clarity | 4 | 4 |
| **overall wins** | 3 | 1 |

Ties: 0.
