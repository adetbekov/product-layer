# UX bench report

Arms: `bare`, `product-layer`. Steps recorded: 2. Blind verdicts: 2.

## Objective metrics

| Metric | bare | product-layer |
|---|---|---|
| Solved, hidden checks | 0/1 | 1/1 |
| check `structure` passed | 1/1 | 1/1 |
| check `dead_ends` passed | 0/1 | 1/1 |
| check `steps` passed | 1/1 | 1/1 |
| check `states` passed | 1/1 | 1/1 |
| check `render` passed | — | — |
| check `asks` passed | 1/1 | 1/1 |
| check `nav` passed | — | — |
| check `actions` passed | 1/1 | 1/1 |
| User steps, all flows (mean) | 2 | 2 |
| Asks on the happy path (mean) | 0 | 1 |
| Screens (mean) | 11 | 5 |
| Spec lines (mean) | 190 | 108 |
| Files out of scope (total) | 0 | 0 |
| Questions in replies (total) | 0 | 0 |
| Tokens per step (mean) | 29855 | 28855 |
| Tokens per solved step | — | 28855.0 |
| Time per step, min (mean) | 0.6 | 0.5 |
| Cost, $ (total) | — | — |

## Per case: hidden checks

| Case | bare | product-layer |
|---|---|---|
| generic-settings | 0/1 (dead_ends) | 1/1 |

## Blind X/Y review (1-5, both orders)

| Criterion | bare | product-layer |
|---|---|---|
| success | 5 | 4 |
| flow | 4 | 3.5 |
| states | 4.5 | 4 |
| ia | 5 | 4 |
| asks | 5 | 4.5 |
| fit | 4 | 3.5 |
| handoff | 4 | 3 |
| scope | 4.5 | 4.5 |
| clarity | 4 | 4 |
| **overall wins** | 2 | 0 |

Ties: 0.
