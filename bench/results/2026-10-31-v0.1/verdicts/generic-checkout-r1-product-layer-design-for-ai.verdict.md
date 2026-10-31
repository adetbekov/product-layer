# Blind review: checkout for a returning customer (P1)

| Criterion | X | Y |
|---|---|---|
| success | 5 | 4 |
| flow | 4 | 3 |
| states | 5 | 4 |
| ia | 4 | 4 |
| asks | 5 | 5 |
| fit | 4 | 4 |
| handoff | 4 | 3 |
| scope | 4 | 3 |
| clarity | 4 | 4 |

Both sides make the same core decisions: drop the sign-in/guest step and all forms for signed-in users, merge review and payment into one `checkout` page with prefilled address/slot/card/phone, open "change" sheets that return to the same page, default billing to delivery, preselect the earliest slot. Happy path is two taps (Checkout, Pay) on both. The differences are in edges and precision.

## X defects

- `cart`: "Browse the shop" points to `cart` itself; `confirmed`: "Back to shop" also goes to `cart` and "Track order" loops to `confirmed`. After an order the user lands in an empty cart whose only exit is a self-loop. Notes admit the shop is unspecced, but a placeholder target would have been cleaner than loops.
- `checkout`: phone is "editable inline" with no action or sheet, so the engineer has to invent the edit behaviour.
- `sign-in` (session expiry) is a recovery screen the brief never mentioned; small but unrequested, and its "Continue as guest" link has no transition.
- Reply and notes cite rule codes (SR-1, SR-3...) that mean nothing to the reader.

## Y defects

- `checkout` -> "Pay and place order" transitions only to `card-verification`; there is no direct path to `order-confirmed`. The graph forces the 3-D Secure modal on every order, contradicting the modal's own purpose ("shown only when the bank requires it") and the notes. An engineer must guess which is true.
- `checkout` error state lumps card decline, 3-D Secure timeout, slot filled up and missing saved field into one block; the slot case is a partial/warning, not a failure, and the "Contact support" link has no destination. The timeout message never says whether the customer was charged.
- `edit-slot` empty state ("no slots today, next day preselected") does not cover no slots at all.
- `order-confirmed` shows "Track order" but has no action for it.
- `catalog` is a fully specced out-of-flow screen with its own states; it solves the exit problem but is product surface nobody asked for.
- `by:` tags are mostly missing, and "Cancel or time out" is tagged `by: system` though cancel is a user act.

## Winner

**P1: X. Overall: X.** Both reach a two-tap reorder, keep address/card/slot changes possible without leaving the page, and handle empty cart and payment failure. X is more precise where it counts: a distinct partial state for an unavailable slot, an explicit "you were not charged" on bank timeout, a direct Pay -> confirmed path with the bank check as a system branch, and a no-slots-at-all case. Y's single biggest flaw, routing every payment through the 3-D Secure modal, is a real ambiguity in the happy path; X's flaws are self-loops at the flow's edges that it at least documents.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 4, "flow": 3, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 3, "scope": 3}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
