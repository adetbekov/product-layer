# Blind review: checkout for a returning customer (P1)

## Scores

| Criterion | X | Y |
|---|---|---|
| success | 5 | 5 |
| flow | 4 | 3 |
| states | 5 | 5 |
| ia | 4 | 5 |
| asks | 5 | 5 |
| fit | 5 | 5 |
| handoff | 5 | 4 |
| scope | 4 | 4 |
| clarity (once) | 5 | 4 |

Both specs hit the core ask: flow `reorder` from `cart` to a confirmed screen, moments `cart` / `checkout` / `confirmed`, two taps on the happy path, every saved field shown as an editable default with a sheet that returns to the same page, billing defaulting to the delivery address, declined card and 3-D Secure timeout keeping the customer on `checkout` with "Try again" / "Use another card", and an empty cart offering the last order.

## Defects

**X**
- `checkout`: the only "Pay and place order" transition goes to `card-verification`, yet that modal's purpose says it is "shown only when the bank requires it". There is no direct `checkout -> order-confirmed` path; the engineer has to infer that the modal auto-passes when 3-DS is not requested.
- `order-confirmed`: "Track order" appears in `shows` but has no action target.
- `catalog`: a full page with its own states was specced although the request was checkout only. It does, however, give the empty cart a real destination.
- `edit-phone` is a fourth sheet for a field most customers never touch; inline edit would be lighter.

**Y**
- `cart`: "Browse the shop" transitions to `cart` itself. The empty-cart way out is a self-loop, acknowledged in notes as a placeholder, but as written the empty state has no exit.
- `confirmed`: "Track order -> confirmed" and "Back to shop -> cart" are both wrong targets; the done screen loops or sends the customer back into an empty cart.
- `sign-in` (session expiry) and `nav` were not requested; the sheet `edit-slot` adds a "Notify me" feature that does not exist in the brief.
- Spec and reply cite "SR-1 … SR-7" and tokens like `notice.warning` that are defined nowhere in the deliverable; a reader without that rulebook must guess what they constrain. Notes also name an "Apple-style skill" for sheets, which edges toward a visual decision.
- Contact phone is "editable inline" with no validation or error state.

**Y's strengths over X**: explicit dual pay routing (`-> confirmed` by user, `-> bank-check` by system), a network-failure message that says "you were not charged", a `partial` state for a slot that filled up, and rank annotations that make section order on `checkout` and `confirmed` unambiguous.

## Winner

**P1: X. Overall: X.** The two are close and both would cut the 7-screen checkout to two taps while keeping address, slot and card changeable. X wins because every exit in its graph lands somewhere real (empty cart -> catalog, confirmed -> shop) and the spec reads in plain language an engineer can build from, whereas Y ships two self-looping actions on exactly the states the brief flagged (empty cart, order done) and leans on undefined rule codes. Y's pay routing and "not charged" messaging are the better detail work, which keeps it within one point.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 5, "handoff": 5, "scope": 4}, "clarity": 5}, "Y": {"P1": {"success": 5, "flow": 3, "states": 5, "ia": 5, "asks": 5, "fit": 5, "handoff": 4, "scope": 4}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
