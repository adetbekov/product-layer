# Blind review: stb-split-flow-r2

## Scores (P1)

| Criterion | X | Y |
|---|---|---|
| success | 5 | 5 |
| flow | 3 | 4 |
| states | 4 | 5 |
| ia | 4 | 5 |
| asks | 4 | 5 |
| fit | 3 | 4 |
| handoff | 3 | 4 |
| scope | 4 | 3 |
| clarity (per side) | 5 | 4 |

## Defects, X

- `parse-review`: payment details are mandatory (post button disabled with "Add how to pay you") but no screen or action lets the payer enter them. First-time payer is stuck. Dead end.
- `parse-review` -> "Fix an item" goes to `manual-entry`, which asks for every item and the service charge again. Fixing one price costs retyping the whole receipt.
- `bill-card`: [Split the rest equally] is shown but has no action. "Who has not picked yet" assumes a headcount the bot cannot know before people tap.
- `share-popup`: a callback popup has no buttons, yet it carries "I paid" and "Change my items" as actions; "I paid" is said to live on the card, but `bill-card` never shows it. The participant's done step has no defined tap.
- `paid-marked` -> `confirm-payment` says "Payer is notified" by system, but the whole flow is one edited message and Telegram edits do not notify. Mechanism missing.
- `confirm-payment`: a single "Got it" transitions to `settled`; no guard that only the payer can tap "Got it" or "Looks right".

## Defects, Y

- `my-share` is an alert yet lists "I sent the payment", "Send me this in private" and "Back" as actions; `bill-panel` shows only "My share". Same gap as X: the "I sent" tap has no placed button in the group (only the optional DM has one).
- `parse-error` -> "Type or say the items" jumps straight to `receipt-check` with no screen for the typed input or its format; parse timeout is "within the timeout" with no value.
- `payment-details-ask`: the payer types a card number as a reply in the group thread, adding a human message to the chat it is trying to keep quiet.
- Items with quantity above 1 are a plain toggle ("Plov x2 - 2 people"); no way to take one of two portions (X's [-][+] handles this).
- Scope creep: Remind once a day, voice input, currency change, private copy, "Split another receipt". Reply leaks internal rule codes (TG-1, SR-3, FL-7) the reader cannot decode.

## Winner

**P1: Y. Overall: Y.** Both land on the same correct shape (one edited group message, inline toggles, per-tapper popups) and share the alert-buttons flaw, but X has a real dead end (no way to add payment details) and a heavy repair path (retype everything to fix one item), while Y gives the payer a deferred, skippable details screen, in-place item fixes, cancel on every parse step, payer-only taps, stale-button handling and a correct answer to "edits do not notify" with a separate confirm message. Y pays for this with extra unasked features and jargon in the reply; X's message reads better and its portion [-][+] is the sharper selection detail, but the spec underneath has more holes an engineer would have to fill by guessing.

```json
{"X": {"P1": {"success": 5, "flow": 3, "states": 4, "ia": 4, "asks": 4, "fit": 3, "handoff": 3, "scope": 4}, "clarity": 5}, "Y": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 5, "asks": 5, "fit": 4, "handoff": 4, "scope": 3}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
