## Scores (P1)

| Criterion | X | Y |
|---|---|---|
| success | 4 | 4 |
| flow | 4 | 3 |
| states | 4 | 4 |
| ia | 4 | 3 |
| asks | 5 | 4 |
| fit | 4 | 4 |
| handoff | 4 | 3 |
| scope | 5 | 3 |
| clarity (once) | 4 | 4 |

Both sides get the returning customer from cart to a placed order in two taps (Checkout, Place order), keep address/slot/card changeable through sheets that return to `checkout`, and handle empty cart, 3-D Secure and declined payment. The difference is in discipline and finish.

## Defects: X

- `checkout`: the only exit from "Place order" is `card-verification`; the "skipped by the system when the bank does not ask" path to `confirmed` exists in prose only, with no `checkout -> confirmed` transition. An engineer can infer it, but it should be modelled.
- `checkout`: uses a non-standard `partial` state (no slot available) instead of folding it into `empty`/`error`; no empty state for "cart emptied meanwhile".
- `change-address`, `change-slot`, `change-card`: no `moment` tag, while `card-verification` has one; inconsistent against the request to tag screens.
- `confirmed`: "Continue shopping" sends the customer back to a now-empty `cart` rather than the catalog.
- `cart` empty state's "Browse products" has no action entry, so it cannot be traced in the graph (acknowledged in notes, still a gap).

## Defects: Y

- `sign-in`: "Continue as guest" leads to a `checkout` whose purpose is "everything is pre-filled from the account" and which asks for nothing — a guest has no saved address or card, so this path is unspecified and effectively a dead end. The screen itself is unrequested.
- `catalog`: a placeholder screen with its own states, outside the request; plus `nav` and a "Buy again" list — scope creep.
- `payment-failed`: the `shows` list is broken YAML — the reason text was split into three items ("reason in plain words (card declined", "verification timed out", "bank unavailable)"). Making a card decline a separate page also moves the customer away from the one screen they need; "Try again" then requires re-pressing Pay, adding a hop that X avoids with an inline error.
- `checkout`: contact phone has "Edit" with no action target. `confirmed` shows "Track order" and "Change or cancel" with no actions (terminal, so they dangle).
- `slot-picker` empty state reads like a note to self ("'Back to cart' is not needed, the customer can close").
- `payment-method` adds a "save this card" ask the brief never raised.

## Winner

**P1: X. Overall: X.** Y is more complete in places (direct `checkout -> confirmed` transition, double-submit lock, checkout empty state, terminal flags) and its reply leads cleanly with decisions. But it pays for that with unrequested screens, a guest path that contradicts its own checkout, a broken list in `payment-failed`, and several affordances with no destination — things a builder would have to guess around. X stays inside the brief, asks only for genuinely new data, keeps payment failure where the customer can fix it in one tap, and its remaining gaps (unmodelled 3-DS skip, odd `partial` state, untagged sheets) are small and easy to close.

```json
{"X": {"P1": {"success": 4, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 4, "flow": 3, "states": 4, "ia": 3, "asks": 4, "fit": 4, "handoff": 3, "scope": 3}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
