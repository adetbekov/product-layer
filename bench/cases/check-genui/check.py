"""Hidden check for check-genui: which planted bugs does report.md name? Run from the agent's workspace root.

Planted bugs (do not show to agents):
- dead_old_buttons: skin-type chips in the first message still look active after answering, but clicks do nothing.
- slider_no_role: the budget slider is a div without role="slider" / aria-valuenow, not keyboard operable.
- regen_slider: after "Regenerate" on the budget message, the new slider does not move.
- double_submit: "Send routine" can be submitted again and again; each submit posts another "sent" message.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from live import main  # noqa: E402

BUGS = {
    "dead_old_buttons": {"all": [
        r"skin[- ]type|oily|dry|combination|not sure|first message|earlier|previous|old(er)? (message|card|chip|"
        r"button)|scroll(ed|ing)? (back )?up|change (my |her |the )?(mind|answer|skin)",
        r"nothing|no (visible )?(effect|feedback|response|change|reaction)|dead|unresponsive|ignored|silent|"
        r"does ?n[o']t (do|work|respond|change|react)|not (respond|work|disabled)|can(no|'?)t change|look[s]? "
        r"(active|enabled|clickable)",
    ]},
    "slider_no_role": {"all": [
        r"slider|budget",
        r"role|aria|accessib|a11y|keyboard|screen ?reader|focus|arrow key|tab(bing)?\b|not (exposed|in the "
        r"(accessibility|a11y) tree)|accessibility tree|invisible to",
    ]},
    "regen_slider": {"all": [
        r"regenerat",
        r"slider|budget",
        r"not (move|respond|work|change|update|draggable|interactive)|does ?n[o']t (move|respond|work|change|"
        r"update)|stuck|dead|frozen|unresponsive|no longer|broken|lost|ignored",
    ]},
    "double_submit": {"all": [
        r"send routine|routine|e-?mail form|form|submit|send",
        r"twice|duplicate|double|again|repeated(ly)?|multiple|second (time|submit|click)|re-?submi|more than once|"
        r"each (click|submit|time)",
    ]},
}

if __name__ == "__main__":
    main(BUGS)
