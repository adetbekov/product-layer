# Blind review: checkout for a returning customer (P1)

## Scores

| Step | Side | success | flow | states | ia | asks | fit | handoff | scope |
|---|---|---|---|---|---|---|---|---|---|
| P1 | X | 5 | 4 | 4 | 4 | 5 | 4 | 4 | 5 |
| P1 | Y | 5 | 4 | 5 | 5 | 5 | 4 | 4 | 4 |

Clarity: X 4, Y 3.

Both deliver the same core: flow `reorder` from `cart` to a confirmed screen, the three moments tagged, sign-in and contact form cut, address/slot/card preselected with a Change sheet, billing checkbox gone, one page to review and pay. Happy path is 2 taps on both sides. The differences are in recovery and edge handling.

## Defects: X

- `payment-failed`: failure is a separate page. "Try again" goes to `checkout`, where the user must tap Place order again, so recovery is two taps and the spec never says whether the retry re-charges or just re-opens the page. An inline error state on `checkout` would keep context and cost one tap.
- `edit-address`, `edit-slot`, `edit-phone`, `edit-card`: each sheet has a single action (Use/Select/Save) and no Close or Cancel. A user who opens Change by mistake has no specified way back.
- `cart` empty state lists "Add items from last order" but there is no action for it; `three-ds` shows Cancel but the only cancel transition is `by: system`. An engineer has to guess both.
- `edit-address` has no empty state (no saved addresses); notes acknowledge this as an assumption rather than designing for it.

## Defects: Y

- `cart`: the empty-state action "Start shopping / Repeat your last order" has `to: cart`. Repeat-last-order correctly refills the cart, but Start shopping loops back to the empty cart; `shop-home` exists and is never reached from here. Empty cart is explicitly in the brief, and as written this is a loop with no exit.
- `checkout` shows "phone ... with edit" but there is no edit action or target screen; whether this is an inline field or a sheet is left to the builder.
- `states` uses `partial` and `stale` beyond the fixed empty/loading/error vocabulary, and the stub `shop-home` carries an "n/a" empty state. Useful thinking, but off-format and slightly beyond scope.
- Final message leans on internal rule codes (SR-1, ST-4, FL-8) the reader cannot decode.

## Winner

P1: Y. Y handles the two failure cases the brief calls out better: payment failure is an inline `checkout` error that keeps every choice and offers Try again / Use another card / Contact support in one tap, with an explicit no-double-charge and no-order-until-paid rule; 3-D Secure has a user Cancel; every sheet has Close; and checkout's `asks` cover the case where a saved detail is missing instead of assuming it away. X is cleaner in scope and its message reads better, but its separate failure page adds a tap and its sheets are dead ends on paper. Y's empty-cart loop is a real defect, yet it is a one-line target fix, while X's gaps are spread across five screens.

Overall: Y.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 5, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 3}, "winner": {"P1": "Y", "overall": "Y"}}
```
