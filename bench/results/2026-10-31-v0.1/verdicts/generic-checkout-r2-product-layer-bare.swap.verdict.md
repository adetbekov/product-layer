# Blind review: checkout for a returning customer (P1)

| P1 | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|
| X | 5 | 5 | 5 | 5 | 5 | 4 | 4 | 4 | 4 |
| Y | 5 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 3 |

Both answer the request fully: flow `reorder` from cart to a placed order, moments `cart` / `checkout` / `confirmed` tagged, happy path cut to two user taps (Checkout, Pay), saved address, slot, phone and card shown as defaults with a one-tap "Change" sheet, empty cart and payment failure designed. The differences are in the edges.

## Defects: X
- `cart`: the action "Start shopping / Repeat your last order" targets `cart` itself. "Repeat last order" refilling the cart is fine; "Start shopping" should go to `shop-home`, otherwise the empty state loops.
- `checkout`: shows "phone ... with edit" but there is no action or screen for changing the phone; an engineer has to guess.
- `edit-slot` empty state offers "Notify me" with no target or behaviour.
- Reply and notes lean on internal rule codes (SR-1, ST-4, FL-8) that mean nothing to the reader.
- `order-tracking` and `shop-home` are stubs beyond the ask, though clearly labelled out of scope.

## Defects: Y
- `edit-address`, `edit-slot`, `edit-phone`, `edit-payment`, `sign-in`: no Close or Cancel action. In `edit-slot`'s empty state ("no slots available") the only action is "Select slot", which cannot be taken, so the spec has a dead end; X gives every sheet an explicit Close.
- `edit-address` asks for country when adding an address; the account already knows it (X derives it).
- `payment-failed` modal: "Try again" returns to `checkout`, where the user must tap Pay again, so a retry costs two taps where X's in-page retry costs one. The modal does add the useful "No money was charged" line.
- `order-confirmed`: the only next action is "Continue shopping"; no "Track order" or link to the order, which is the thing a grocery customer wants after paying. Notes admit it was deferred.
- `sign-in` (session expired) is unrequested and its "Reset password" has no target.
- Reply opens with a runtime absolute path and "No CLAUDE.md or skills existed", which is tooling noise, not a decision.

## Winner
P1: X. Both reach the same two-tap happy path and both keep address and card changeable, but X's spec is tighter where it counts for the brief: each sheet has a way out, payment failure keeps the user on the page with a one-tap retry and a stated no-double-charge guarantee, the confirmation offers the real next action, and `asks` on `checkout` state precisely when a missing phone, address or card is requested. Y is close and has good additions (unavailable items in cart, 120 s 3-D Secure countdown, masked card example) but the missing sheet dismissals and the deferred confirmation action are gaps a builder would have to fill.

Overall: X.

```json
{"X": {"P1": {"success": 5, "flow": 5, "states": 5, "ia": 5, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 4, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 3}, "winner": {"P1": "X", "overall": "X"}}
```
