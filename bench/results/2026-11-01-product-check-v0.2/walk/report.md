# Live bench: product-check

| Case | Arm | Runs | Recall | Recall with steps + screenshot | Precision | Findings | Tokens (mean) |
|---|---|---|---|---|---|---|---|
| check-genui | product-check | 2 | 1.0 | 1.0 | 0.76 | 8.5 | 62856.5 |
| check-shop | product-check | 2 | 1.0 | 1.0 | 0.62 | 6.5 | 55242.5 |
| check-visual | product-check | 2 | 0.83 | 0.83 | 0.55 | 6.5 | 63708.5 |
| check-visual | product-check-v0.1 | 2 | 0.67 | 0.67 | 0.62 | 4.0 | 57679.0 |

Recall: share of planted bugs named by at least one ISSUE block (hidden regexes in check.py). Precision: share of ISSUE blocks that match a planted bug; real but unplanted issues count against it, so read it as focus, not correctness.
