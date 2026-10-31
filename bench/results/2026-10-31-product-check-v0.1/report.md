# Live bench: product-check

| Case | Arm | Runs | Recall | Recall with steps + screenshot | Precision | Findings | Tokens (mean) |
|---|---|---|---|---|---|---|---|
| check-genui | bare | 2 | 0.75 | 0.75 | 0.54 | 7.5 | 40360.0 |
| check-genui | product-check | 2 | 0.88 | 0.88 | 0.74 | 7.5 | 47738.0 |
| check-genui | dogfood | 2 | 0.75 | 0.75 | 0.73 | 7.0 | 40580.5 |
| check-shop | bare | 2 | 0.75 | 0.75 | 0.46 | 6.5 | 39384.5 |
| check-shop | product-check | 2 | 0.88 | 0.88 | 0.9 | 5.0 | 51313.0 |
| check-shop | dogfood | 2 | 0.88 | 0.88 | 0.63 | 5.5 | 38603.0 |

Recall: share of planted bugs named by at least one ISSUE block (hidden regexes in check.py). Precision: share of ISSUE blocks that match a planted bug; real but unplanted issues count against it, so read it as focus, not correctness.
