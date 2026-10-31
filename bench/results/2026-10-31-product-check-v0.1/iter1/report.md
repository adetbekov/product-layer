# Live bench: product-check

| Case | Arm | Runs | Recall | Recall with steps + screenshot | Precision | Findings | Tokens (mean) |
|---|---|---|---|---|---|---|---|
| check-genui | bare | 2 | 0.62 | 0.62 | 0.53 | 8.5 | 42223.0 |
| check-genui | product-check | 2 | 1.0 | 1.0 | 0.75 | 8.0 | 49980.0 |
| check-genui | dogfood | 2 | 0.38 | 0.38 | 0.58 | 6.0 | 44966.0 |
| check-shop | bare | 2 | 0.62 | 0.62 | 0.38 | 6.5 | 37917.0 |
| check-shop | product-check | 2 | 0.75 | 0.75 | 0.71 | 5.0 | 48080.0 |
| check-shop | dogfood | 2 | 1.0 | 1.0 | 0.75 | 6.0 | 34883.0 |

Recall: share of planted bugs named by at least one ISSUE block (hidden regexes in check.py). Precision: share of ISSUE blocks that match a planted bug; real but unplanted issues count against it, so read it as focus, not correctness.
