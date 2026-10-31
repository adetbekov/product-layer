# Blind review: checkout for a returning customer (P1)

## Scores

| Step | Side | success | flow | states | ia | asks | fit | handoff | scope |
|---|---|---|---|---|---|---|---|---|---|
| P1 | X | 5 | 4 | 5 | 4 | 4 | 4 | 4 | 4 |
| P1 | Y | 4 | 4 | 5 | 4 | 5 | 4 | 3 | 4 |

Clarity: X 4, Y 3.

## Defects

**X**
- `edit-address`, `edit-slot`, `edit-phone`, `edit-payment`: the only action is "Use this / Save". A user who opens "Change address" just to look has no Cancel or Close; the sheet is a soft dead end unless the engineer invents one.
- `edit-address`: when adding an address it asks country, city, street, flat, entrance. Country is derivable from the account or the shop; asking it is a leftover from the old form.
- `payment-failed`: "Try again" goes back to `checkout`, so a retry costs two taps (dismiss, then pay again) instead of one.
- `sign-in` sheet and session-expiry handling were not requested; defensible, but it widens the spec beyond the reorder flow.

**Y**
- `cart`: the empty-state action "Start shopping / Repeat your last order" has `to: cart`. Start shopping loops the user back onto the empty cart while `shop-home` exists and is not targeted.
- `checkout`: the phone block shows "edit" but there is no action and no edit-phone screen, so an engineer has to guess. "Contact support" is named in the error state with no action or destination either.
- `edit-address`, `edit-slot`, `edit-payment`, `3ds-verify`: no `moment` tag, although the request asked for the checkout moment to cover where the order is reviewed and paid; X tagged all of them.
- `notes.md` and the reply lean on rule codes (SR-1, ST-4, FL-8) that are never explained, which reads like an internal checklist rather than a person's reasoning.

## Both sides got right
Two-tap happy path (Checkout, Pay), one prefilled page instead of a wizard, saved address/slot/card with a one-tap change sheet, billing defaulted to the delivery address, empty cart with a repeat-order shortcut, 3-D Secure as a system modal with a timeout, payment failure that keeps the cart and offers retry or another card, and a confirmation page that never shows failure for a paid order. Neither touches colors, fonts or motion.

## Winners

**P1: X.** Both specs answer the brief with the same shape and the same two-tap path, so the decision comes down to internal consistency. X's spec has no mis-wired transitions and tags every checkout surface with its moment; its weakness (sheets without Cancel) is a single pattern fix. Y has the better asks (country from account, explicit conditional asks) and tidier in-place payment retry, but it ships a self-looping empty-cart action, a phone "edit" affordance with nowhere to go, and a support exit with no target, which are exactly the gaps an engineer would have to guess at.

**Overall: X**, by a narrow margin, for a spec that builds without guessing and a final message that reads as plain reasoning rather than rule codes.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 4, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 4, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 3, "scope": 4}, "clarity": 3}, "winner": {"P1": "X", "overall": "X"}}
```
