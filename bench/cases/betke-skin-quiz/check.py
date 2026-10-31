"""Hidden acceptance check: python check.py P1, run from a copy of the workspace root."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ux import main  # noqa: E402

RULES = {
    "max_steps": {"onboarding": 4},  # pick skin type, pick concerns (+ confirm), picks arrive
    # Reference markup: few options -> chips, items to compare -> cards, ordered process -> steps, prose -> text.
    "render": {
        "greet": "text",
        "skin-type": "block",
        "concerns": "block",
        "picks": "block",
        "routine": "block",
        "followup": "text",
    },
    "render_min": 5 / 6,
    "states": {"picks": ["loading", "empty", "error"]},
    "forbid_asks": [r"phone", r"e-?mail", r"language"],
    "require_asks": [r"skin"],
}

if __name__ == "__main__":
    main(RULES)
