# Blind review: checkout for a returning customer (P1)

## Scores

| | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|
| X | 5 | 4 | 5 | 4 | 5 | 4 | 3 | 5 | 4 |
| Y | 5 | 5 | 4 | 4 | 5 | 4 | 4 | 4 | 5 |

Both answer the request: flow `reorder` with entry `cart` / done `confirmed`, moments `cart`, `checkout`, `confirmed` tagged, two user taps (Checkout, Place order) with saved address, slot, card and phone preselected and a one-tap "change" sheet for each. Billing checkbox removed on both sides.

## Defects

**X**
- `cart`, empty state: "Start shopping / Repeat your last order" both go `to: cart`. For an empty cart "Start shopping" is a loop back to the empty cart; `shop-home` exists but is not wired here. This is the one empty-cart exit and it is broken.
- `checkout`: phone is shown "with edit" but there is no edit action or target screen; an engineer must invent one.
- `checkout`, error state: "Contact support" has no target.
- No `nav` block; minor, not explicitly asked.
- `partial` and `stale` are not in the fixed state vocabulary (empty/loading/error); useful content, but a builder has to decide how they render.

**Y**
- `sign-in` screen and guest path are outside the signed-in returning-customer flow that was asked for; "Continue as guest -> checkout" also contradicts `checkout`'s "every field pre-filled from the account" (notes admit it is undetailed).
- `checkout` has no `empty` state (cart emptied by stock changes while on the page is only half-covered under `error`).
- `by: user` is omitted on every user action; the format treats `by:` as meaningful, so default must be assumed.
- `cart`, error: "Pick a substitute" has no target. `change-address` has no loading state; `edit-phone` only an error.
- Moment `checkout` is stamped on sheets, `sign-in` and `payment-failed`; tolerable but looser than "where the order is reviewed and paid".

## Winner

**P1 and overall: Y**, narrowly. On the four things the review was asked to check, both let a returning customer order in two taps and keep address/card/slot changeable via sheets that return to the same page; both design payment failure with retry, another card and no order created (X as an in-place checkout error, Y as an explicit `payment-failed` modal that states nothing was charged). The tie breaks on the empty cart: Y routes it to `shop` or "Add items from your last order", while X's only "Start shopping" exit points back at the empty cart. X has the richer state design (stale slot, partial stock, 3-D Secure cancel, confirmed never shows failure for a paid order) and tighter scope, but its three unresolved targets would make an engineer guess; Y's wiring resolves end to end and its message leads with decisions in plain words, at the cost of an unrequested sign-in screen.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 3, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 5, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 5}, "winner": {"P1": "Y", "overall": "Y"}}
```
