# Blind review: checkout for a returning customer (P1)

## Scores

| Criterion | X | Y |
|---|---|---|
| success | 5 | 5 |
| flow | 4 | 3 |
| states | 5 | 4 |
| ia | 5 | 4 |
| asks | 5 | 4 |
| fit | 4 | 4 |
| handoff | 5 | 4 |
| scope | 4 | 4 |
| clarity | 4 | 4 |

Both answer the request: flow `reorder` with cart entry and confirmed done, moments `cart` / `checkout` / `confirmed` tagged, happy path cut to two user taps (Checkout, Place order), sign-in prompt and contact form gone, saved address / slot / card shown as defaults with a one-tap change sheet, billing checkbox removed.

## Defects

**X**
- `cart`: the empty-state action "Start shopping / Repeat your last order" targets `cart` itself. "Repeat last order" refilling the cart is fine, but "Start shopping" should go to `shop-home`, which exists but is unreachable from the empty cart. Small loop, not a dead end.
- `checkout`: payment-failure handling is an `error` state, but the retry actions ("Try again", "Use another card", "Contact support") are only described in prose; "Contact support" has no `to`. An engineer would have to guess where support lives.
- Notes reference rule codes (SR-1, ST-4, FL-8) the reader cannot resolve; the reply would read better without them.

**Y**
- `payment-failed`: a full page for a failure costs an extra step. "Try again" returns to `checkout`, where the user must tap "Place order" again, so retry is two taps versus X's one, and the user leaves the page that holds their choices.
- `cart` empty state lists "Add items from last order" as an action but no transition is defined for it; only "Start shopping" resolves.
- `three-ds`: shows a Cancel control but has no `by: user` action; user cancel is folded into a `by: system` "Timed out or cancelled" transition, which misstates who pays the step.
- Missing-data case is unhandled: `checkout` assumes a saved address, card and phone exist (stated as an assumption). The brief says 80% of orders have them, so the other signed-in customers hit a page with nothing to change from. X asks for each only when missing.
- `edit-address` has no empty or loading state; `edit-card` has no empty state (no saved cards). `edit-address` re-asks country, which the account already knows.
- `payment-failed` promises a 10-minute slot hold with no state for what happens when it expires.
- `order-confirmed` error covers only receipt delivery, not failure to load the order details after a successful charge.

## Winner

**P1: X. Overall: X.** Both land the two-tap happy path and keep address, slot and card editable from one checkout page. X is tighter where the brief's hard cases live: payment failure stays on `checkout` with every choice kept and a one-tap retry, missing saved data is asked for only when absent, and partial/stale states (out-of-stock line, slot filled while open) are designed. Y's separate `payment-failed` page adds a step to the exact moment the user is most likely to abandon, and its spec leaves several listed controls and the missing-saved-data path without transitions.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 5, "asks": 5, "fit": 4, "handoff": 5, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 3, "states": 4, "ia": 4, "asks": 4, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
