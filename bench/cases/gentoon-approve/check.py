"""Hidden acceptance check: python check.py P1, run from a copy of the workspace root."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ux import main  # noqa: E402

RULES = {
    "max_steps": {"create": 3},  # submit brief, approve plan (price shown), generation runs by itself; one spare
    "states": {"plan": ["loading", "error"], "storyboard": ["loading", "error"]},
    "min_actions": {"plan": 2},  # approve and revise
    "forbid_asks": [r"price|cost|credit", r"seed|model", r"e-?mail"],
    "require_asks": [r"brief|idea|prompt|story|song|description|concept"],
}

if __name__ == "__main__":
    main(RULES)
