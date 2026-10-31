# Blind review: checkout for a returning customer (P1)

## Scores

| | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|
| X | 5 | 4 | 5 | 4 | 4 | 4 | 4 | 4 | 4 |
| Y | 5 | 3 | 4 | 4 | 5 | 4 | 3 | 3 | 3 |

Both deliver the requested `reorder` flow (cart -> confirmed), tag `cart` / `checkout` / `confirmed`, and cut the default path to two taps (Checkout, Place order) with saved address, earliest slot and saved card preselected and changeable through sheets that return to `checkout`. The difference is in the edges.

## Defects: X

- `cart-empty-exit`: a stand-in page doubles as catalog and as order tracking (`confirmed` -> Track order lands on a "Catalog" screen). Honest about being out of scope, but it is an extra screen and the purpose is muddled.
- `checkout`: `empty: Cannot happen; redirects to cart` but no `by: system` action models the redirect. Contact phone is shown with no way to change it.
- `payment-failed`: a full page rather than an inline notice on `checkout`, so recovering from a decline is one screen heavier than it needs to be. Still, Try again, Use another card and Back to checkout make it no dead end.
- `payment-sheet`: "no checkbox unless the customer edits it" is ambiguous.

## Defects: Y

- `cart`: Browse the shop -> `cart` is a self-loop, so the empty cart has no exit inside the spec; "Add items from your last order" has no action at all. `confirmed`: Track order -> `confirmed` is another self-loop, and Back to shop goes to the cart, not the shop.
- `sign-in`: an unrequested session-expiry screen (with a guest link) tagged `moment: checkout`, reached by a `by: system` action labelled "Checkout (session expired)" on the cart. Re-introduces the screen the brief complained about, for a case the brief never raised.
- `checkout` error "Could not place the order, you were not charged" has no idempotency or result-lookup behind it; X ties this to an order key. `edit-address` / `edit-payment` have no loading state. `edit-slot` adds a "Notify me" feature nobody asked for.
- Handoff relies on unexplained tokens (`rank 1/2/3`, `notice.warning`, `SR-1..SR-7`), and notes name an "Apple-style skill" for sheets, which leans into visual decisions.

## Winner

**P1: X. Overall: X.** Y's inline decline handling and editable phone are slightly better product instincts, but its spec has two self-loops where the user must leave the flow, an unrequested sign-in screen, and jargon an engineer cannot resolve. X covers every state it claims (processing modal blocking double-submit, 3-D Secure timeout, slot-hold expiry, network loss resolved by order key) with real transitions, and stays closer to what was asked.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 4, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 3, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 3, "scope": 3}, "clarity": 3}, "winner": {"P1": "X", "overall": "X"}}
```
