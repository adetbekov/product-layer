"""Hidden acceptance check: python check.py P1, run from a copy of the workspace root."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ux import main  # noqa: E402

RULES = {
    "max_steps": {"digest": 3},  # settings -> pick a value (saves itself); 3 leaves room for an extra tap
    "states": {"settings": ["loading", "error"], "export": ["loading", "error"]},
    "forbid_asks": [r"e-?mail[ _]?(address)?$", r"(^|[ _])name$", r"time ?zone|timezone"],  # "email digest" is fine
    "min_actions": {"delete": 2},  # confirm and cancel
}

if __name__ == "__main__":
    main(RULES)
