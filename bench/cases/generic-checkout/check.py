"""Hidden acceptance check: python check.py P1, run from a copy of the workspace root."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ux import main  # noqa: E402

RULES = {
    "max_steps": {"reorder": 3},  # cart -> checkout -> place order, slot pre-picked; one spare tap
    "states": {"cart": ["empty"], "checkout": ["loading", "error"]},
    "forbid_asks": [r"e-?mail", r"phone", r"address|street|city|country", r"card|expir|billing"],
    "min_actions": {"checkout": 2},  # place order, and a way to change a saved detail or go back
}

if __name__ == "__main__":
    main(RULES)
