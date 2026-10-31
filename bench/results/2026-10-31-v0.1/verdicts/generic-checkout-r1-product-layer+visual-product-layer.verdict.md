# Blind review: checkout for a returning customer (P1)

| Step | Side | success | flow | states | ia | asks | fit | handoff | scope |
|---|---|---|---|---|---|---|---|---|---|
| P1 | X | 5 | 4 | 5 | 4 | 5 | 4 | 4 | 3 |
| P1 | Y | 5 | 4 | 4 | 4 | 4 | 4 | 4 | 4 |

Clarity: X 4, Y 4.

Both specs reach the same shape: `reorder` is two taps (Checkout, Place order/Pay), saved address, slot, card and phone are shown as changeable values, changes open sheets that return to checkout, billing defaults to delivery, the slot defaults to earliest available, 3-D Secure is a system modal, and empty cart plus card decline are handled. The differences are at the edges.

## X defects

- `order-status`: an unrequested extra page (no moment tag) added only to give "Track order" a target. Honest about it in notes, but it is scope the brief did not ask for.
- `cart` -> `sign-in` "Checkout (signed out)": the flow is for a signed-in customer; a signed-out path is out of the stated scope and the sign-in sheet is tagged `cart`, which stretches the moment.
- `payment-failed`: `surface: notice` yet modeled as its own screen "shown on top of the checkout page"; an engineer has to decide whether it is a banner, an overlay, or a route. Y keeps the same recovery inline and is less ambiguous.
- `cart` empty-state action "Order again / Continue shopping" transitions to `cart` itself; the catalogue target is not specced (same gap on Y).

## Y defects

- `confirmed`: "Track order" transitions to `confirmed` — a visible primary-ish action that does nothing. The notes admit tracking is out of scope; the honest spec move is to drop the action or mark the target as external, not wire a self-loop.
- `edit-address` empty: "Not possible, a returning customer has at least one saved address." The brief says 80% have saved data, so 20% of signed-in customers may lack an address or card; `checkout` has no state for a missing saved address/card/phone. X covers this inline (checkout `error` state, sheets open on the add form).
- `edit-address` asks country and city for a new address; a grocery shop knows its service area, so these should be defaulted (X infers them).
- `sign-in` shows a "Continue as guest" link with no transition defined — a dangling action in the spec.
- Reply and notes cite rule codes (SR-1, SR-3...) that appear nowhere in the spec, so a reader cannot follow the reasoning; notes also name an "Apple-style skill" for sheets, a small step toward visual territory.

## Winner

**P1: X. Overall: X.** On the core questions — few taps, changeable address and card, empty cart, payment failure — the two are equivalent. X wins on states and asks: it designs the missing-saved-data case that Y declares impossible, infers country/city instead of asking, and has no no-op action. Y is tighter in scope and has thoughtful engineering details (double-submit block, "never show checkout again" after payment, failure kept inline on the page), but the "Track order" self-loop and the dismissed empty state are concrete holes a builder would hit. X's extra `order-status` page costs it on scope but does not break the flow.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 3}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 4, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
