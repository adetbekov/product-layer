"""Hidden acceptance check: python check.py P1, run from a copy of the workspace root."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ux import main  # noqa: E402

RULES = {
    # payer: send photo (+ one confirm of the parsed items); friend: open, tap items, done, mark paid
    "max_steps": {"payer": 2, "participant": 4},
    "states": {"parse": ["loading", "error"], "select": ["empty"]},
    "forbid_asks": [
        r"price|amount|sum|total|cost|service",
        r"member|participant|people|who (is|are) (in|here)",
        r"\bname\b|username",
    ],
    "require_asks": [r"item|dish|ate|position|order|what"],
}

if __name__ == "__main__":
    main(RULES)
