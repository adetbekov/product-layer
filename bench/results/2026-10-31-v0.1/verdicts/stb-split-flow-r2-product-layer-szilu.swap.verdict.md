# Blind review: stb-split-flow-r2 (X vs Y)

## Scores

| Step | Side | success | flow | states | ia | asks | fit | handoff | scope |
|---|---|---|---|---|---|---|---|---|---|
| P1 | X | 5 | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| P1 | Y | 5 | 4 | 4 | 4 | 5 | 3 | 3 | 3 |

Clarity: X 4, Y 3.

## Defects

**X**
- `split-pay` / `paid-marked`: a friend can only tap "I sent it" after the payer taps "Close picking". That inserts a payer gate the brief did not ask for, and late friends force a "Reopen" that "resets amounts" with no word on what happens to payments already marked.
- `paid-marked` -> `confirm-payments` by system assumes the payer notices an edit. Telegram edits do not notify; nothing mentions the payer when a payment is marked, so the payer may never know money arrived.
- `split-pay` vs `confirm-payments`: both are "the same live message", but a separate user action "Payer opens confirmations" exists. Whether confirm buttons live on the pay table or in a second mode is left to the engineer.
- `parse-failed` -> `fix-item`: "add items by hand" reuses a one-item form, so a wholly unreadable receipt means one round trip per line through `parse-review`. Works, but slow, and `parse-review` empty-state bounces back to `parse-failed` if the first line fails.

**Y**
- `my-share`, `item-claimed`, `payment-marked`: these are callback alerts/toasts, which in Telegram carry no buttons. Yet "I sent the payment", "Send me this in private", "Undo" and "My share" are actions on them. `bill-panel` has no "I sent" button, so the participant's done screen is unreachable as specced unless the engineer re-homes the buttons.
- `parse-progress`: "read with doubts" routes to `parse-error`, contradicting `receipt-check`, which flags unclear items on the card. A mostly-good read would be shown as a failure.
- `bill-panel`: items are a binary toggle with a people count ("Plov x2 - 2 people"); how two portions split among one, two or three claimers is never stated, so amounts are ambiguous on multi-quantity lines.
- `bill-closed`: "final state of the same panel message" while "Close the bill" is tapped in the separate `confirm-payments` message; which message is edited and what happens to the other is unclear.
- Scope creep: voice input of items, deep-linked private copy, currency change, in-message paging, stale-button screen, manual remind — sensible, but unrequested.

## Winner

**P1: X. Overall: X.**

Y has the better ergonomics on paper — two payer taps, friends pay without waiting, a fresh mention when the first payment lands, explicit Skip on payment details — and its asks are the tidiest. But its core participant path rests on buttons inside Telegram alerts, which do not exist, and its doubtful-read routing contradicts its own card. X is slightly heavier for the payer (an explicit "Close picking") and misses payer notification, but every surface it uses behaves as Telegram actually behaves, quantities and shared items are handled precisely, bad photos get reason-specific recovery, and an engineer could build it with fewer guesses. X's final message also reads more like a person; Y leans on opaque rule codes (TG-1, SR-3).

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 4, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 3, "handoff": 3, "scope": 3}, "clarity": 3}, "winner": {"P1": "X", "overall": "X"}}
```
