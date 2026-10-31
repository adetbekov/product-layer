# Verdict: stb-split-flow-r2 (X vs Y)

## Scores (P1)

| Criterion | X | Y |
|---|---|---|
| success | 5 | 5 |
| flow | 4 | 2 |
| states | 5 | 3 |
| ia | 4 | 4 |
| asks | 5 | 3 |
| fit | 4 | 3 |
| handoff | 4 | 3 |
| scope | 4 | 4 |
| clarity (per side) | 4 | 4 |

## Defects

**X**
- `my-share`, `item-claimed`, `payment-marked` (surface: notification) carry actions ("I sent the payment", "Send me this in private", "Keep picking"). Telegram callback alerts/toasts have no buttons; these must be buttons on `bill-panel`, yet the panel's `shows` lists only items and "My share". An engineer has to guess where "I sent" and the deep-link button live.
- `parse-error` → "Type or say the items" jumps straight to `receipt-check` with no screen or format for typed items; only the fix-an-item error hints at "the water, 500". Manual entry is under-specified.
- Quantities: "Plov x2 - 2 people" does not say how one friend claims two portions.
- Minor scope creep: `my-share-private`, daily `Remind`, `stale-button`, paging. All defensible for Telegram, but unrequested.

**Y**
- `parse-review`: the error state disables the post button until payment details are added, but there is no action, screen or transition for entering them, and Telegram inline buttons cannot be disabled. A first-time payer is stuck; the payer flow cannot complete.
- `confirm-payment`: "Got it / Confirm all sent" goes to `settled` after a single confirm; there is no loop back to a partial state, no way to close a bill when one friend never pays, no remind. `Not received` → `bill-card` muddles the card's state.
- `parse-review` "Fix an item" → `manual-entry`, which re-asks all items line by line; one wrong price costs a full retype.
- No Cancel anywhere during parse; `paid-marked` tagged `share` though it is the end of participant flow (acceptable but loose).
- Payer "mentioned" on first payment is only in notes; since confirm lives on the edited card and edits do not notify, the mechanism is unspecified. "Who has not picked yet" assumes the bot knows all group members, which the brief says it does not.

## Winner

**P1: X. Overall: X.** Both sides land on the right skeleton (one edited group message, inline picking, popup share, loud parse failure, review before post). X's version actually closes every path: payment details are asked once and skippable, the payer can close a bill without waiting for everyone, confirmation is a separate new message precisely because edits do not notify, and the states (long lists, stale taps, 10-second "still reading") are designed rather than mentioned. Y has a hard dead end for a first-time payer with no saved details and a confirmation transition that cannot represent "two of four confirmed"; its flow and states fail where it matters most. X's mistake, putting actions on alerts, is a modelling slip an engineer can resolve by moving buttons to the panel; Y's gaps change the product.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 2, "states": 3, "ia": 4, "asks": 3, "fit": 3, "handoff": 3, "scope": 4}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
