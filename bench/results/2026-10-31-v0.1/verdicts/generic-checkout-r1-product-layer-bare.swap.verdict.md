# Blind review: checkout for a returning customer (P1)

| Criterion | X | Y |
|---|---|---|
| success | 5 | 4 |
| flow | 4 | 5 |
| states | 5 | 4 |
| ia | 4 | 4 |
| asks | 5 | 5 |
| fit | 4 | 4 |
| handoff | 4 | 4 |
| scope | 5 | 4 |
| clarity (once) | 4 | 4 |

## Defects

**X**
- `cart`: "Browse the shop" transitions to `cart` itself. The empty-cart exit is a self-loop, so the one state the brief called out has no real way out; "Add items from your last order" is shown but has no action.
- `confirmed`: "Track order" also loops to `confirmed`. Admitted in notes, but still a dead button in the spec.
- `checkout`: uses a `partial` state outside the fixed empty/loading/error vocabulary; an engineer has to guess how it maps. Pay-with-3DS is a `by: system` branch off the same button, which is fine, but there is no explicit processing step between Pay and `confirmed`, only a button label.
- `sign-in` tagged moment `checkout` although nothing is reviewed or paid there. Reply leans on "SR-1 … SR-7" references that mean nothing to the reader.

**Y**
- Moments only on `cart`, `checkout`, `confirmed`; `address-sheet`, `slot-sheet`, `payment-sheet`, `processing`, `three-ds`, `sign-in` carry no moment, so the "where the order is reviewed and paid" moment is incomplete. No `nav` and no `by: user` marks (absent `by` must be assumed to mean user).
- `catalog` screen and the first-order "missing block opens inline as a form" empty state are outside the returning-customer ask.
- `confirmed`: "order status link" is shown but has no action; no loading state for a payment result still being confirmed.
- `sign-in`: "Continue as guest" shown with no transition.
- `checkout` error folds declined card, 3DS timeout, vanished slot and out-of-stock into one message; it does not say "you were not charged", which matters most after a timeout.

## Winners

**P1: X.** Both land the same core design: no sign-in step, one prefilled checkout page, sheets for address/slot/card that return to checkout, billing = delivery, 2 user taps. X answers the request more completely (every screen tagged, nav named, user/system transitions explicit) and designs more states where they bite: slot no longer available, network failure with "you were not charged", confirmed-while-payment-pending, double-submit blocked. Y's flow graph is cleaner (explicit `processing` modal, catalog as a genuine exit from an empty cart, 3DS success routed back through processing), which is why it takes flow, but it under-tags and adds unrequested scope.

**Overall: X**, narrowly. X's self-loops on "Browse the shop" and "Track order" are real defects a builder would have to resolve, but they are declared out-of-scope links rather than missing design, whereas Y's missing moments and untagged actions were the one explicit instruction in the request. Fix for X: point "Browse the shop" at a named catalog screen the way Y did.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 4, "flow": 5, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
