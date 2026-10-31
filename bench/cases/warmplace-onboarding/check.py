"""Hidden acceptance check: python check.py P1, run from a copy of the workspace root."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ux import main  # noqa: E402

RULES = {
    # student: accept invite, sign in, book the offered slot, join; tutor: sign up, subjects/price, slots, publish
    "max_steps": {"student": 4, "tutor": 5},
    "states": {"dashboard": ["empty"], "room": ["loading", "error"]},
    "forbid_asks": {
        "student": [r"time ?zone|timezone", r"country|language", r"\brole\b", r"tutor|subject"],  # from the invite
        "tutor": [r"time ?zone|timezone", r"country|language", r"\brole\b"],
    },
    "require_asks": [r"slot|availab|time|schedule"],
    "nav": {"roles": ["student", "tutor"], "max": 5},
}

if __name__ == "__main__":
    main(RULES)
