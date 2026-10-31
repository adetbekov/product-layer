"""Hidden check for check-visual: which planted bugs does report.md name? Run from the agent's workspace root.

Planted bugs (do not show to agents):
- canvas_seats: the seat map is a <canvas> with no role, label or keyboard access; seats exist only as pixels, so
  "Continue" stays disabled for anyone who cannot click by position (screen readers, keyboard, tree-only agents).
- low_contrast_pay: on Payment the main action "Pay 3 200 ₸" is pale grey on light grey (it looks disabled), while
  the secondary "Change seat" is the dark, bold button.
- offscreen_download: on the confirmation page "Download ticket" is placed outside the screen on the right; it is
  in the accessibility tree but no user can see or reach it.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from live import main  # noqa: E402

BUGS = {
    "canvas_seats": {"all": [
        r"seat",
        r"canvas|not (in|exposed|accessible|announced)|accessib|keyboard|screen ?reader|no (role|label|name)|"
        r"accessibility tree|aria|only (by|with) (the )?(mouse|position|coordinates|pixel)|coordinates|"
        r"(cannot|can'?t) (be )?(select|pick|choose|tab|focus|reach)",
    ]},
    "low_contrast_pay": {"all": [
        r"\bpay\b|payment button|main (action|button)|primary",
        r"contrast|faint|pale|barely (visible|readable|legible)|hard to (see|read|notice)|gr[ae]y(ed)?[- ]out|"
        r"washed|looks? (disabled|inactive)|almost invisible|low visibility|blends",
    ]},
    "offscreen_download": {"all": [
        r"download|ticket",
        r"off[- ]?screen|outside (of )?(the )?(viewport|screen|visible|page)|not visible|cut off|clipped|"
        r"(cannot|can'?t) (see|find|reach|scroll)|out of (view|sight)|beyond (the )?(edge|right|screen|viewport)|"
        r"invisible|hidden|missing on (the )?screen",
    ]},
}

if __name__ == "__main__":
    main(BUGS)
