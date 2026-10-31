"""Hidden check for check-shop: which planted bugs does report.md name? Run from the agent's workspace root.

Planted bugs (do not show to agents):
- extra_step: a signed-in user must re-enter email and password ("Confirm your account") before checkout.
- dead_end: "Delivery terms" opens a page with no header, link or button out of it.
- dead_promo: the promo code "Apply" button does nothing, no message.
- stale_badge: changing quantities in the cart does not update the header "Cart (n)" counter (round trip / reload).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from live import main  # noqa: E402

BUGS = {
    "extra_step": {"all": [
        r"confirm (your )?account|re-?enter|re-?type|enter (it|them|email|password) again|again|already signed|"
        r"signed[- ]in|logged[- ]in|already (known|logged|authenticated)",
        r"e-?mail|password|account|credential",
    ]},
    "dead_end": {"all": [
        r"delivery terms|terms",
        r"dead[- ]end|no (way|link|button|navigation|nav|header|exit|back)|without (any )?(navigation|header|link|"
        r"way)|trap|stuck|only (the )?browser back|cannot (go|get|return|navigate)|can'?t (go|get|return|navigate)|"
        r"(header|navigation|nav)[^.\n]{0,40}(disappear|missing|hidden|gone|vanish)",
    ]},
    "dead_promo": {"all": [
        r"promo|coupon|discount|FRESH10",
        r"nothing|no (visible )?(effect|feedback|response|message|change|error|confirmation)|dead|unresponsive|"
        r"silent|does ?n[o']t (do|work|apply|respond|change)|not (applied|working|respond)|ignored|no-?op",
    ]},
    "stale_badge": {"all": [
        r"badge|counter|header|cart \(|cart count|item count|cart link|nav",
        r"stale|not (update|refresh|reflect|sync)|does ?n[o']t (update|refresh|reflect|change)|out of (date|sync)|"
        r"outdated|old (count|value|number)|mismatch|wrong (count|number)|inconsistent|until (a |the )?(reload|refresh)",
    ]},
}

if __name__ == "__main__":
    main(BUGS)
