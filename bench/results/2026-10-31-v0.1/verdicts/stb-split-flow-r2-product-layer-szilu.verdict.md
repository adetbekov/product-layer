# Blind review: stb-split-flow-r2 (P1)

## Scores

| P1 | success | flow | states | ia | asks | fit | handoff | scope | total | clarity |
|---|---|---|---|---|---|---|---|---|---|---|
| X | 5 | 4 | 4 | 4 | 5 | 3 | 4 | 4 | 33 | 4 |
| Y | 5 | 3 | 4 | 3 | 4 | 4 | 3 | 4 | 30 | 4 |

## Defects

**X**
- `my-share`, `item-claimed`, `payment-marked` are `notification` surfaces (callback toast/alert) yet carry actions ("I sent the payment", "Send me this in private", "Undo", "Keep picking"). Telegram alerts have only an OK button. The participant flow's `done` transition literally lives on a surface that cannot hold it; `bill-panel` has no "I sent" button, so the engineer must invent one. Biggest hole in an otherwise platform-literate spec.
- `receipt-check`: payment details can be skipped ("friends see ask <payer>"), but after "Looks right" there is no action anywhere to add them later; `my-share` error state is then a soft dead end.
- `parse-progress` routes "read with doubts" to `parse-error`, while `receipt-check` also defines a partial state with "unclear items marked". Two homes for the same case.
- "Type or say the items" jumps straight to `receipt-check` with no input screen; voice input is unrequested.

**Y**
- `parse-review`: "only the payer checks ... friends see nothing" and "others see '{payer} is checking the receipt'" are impossible in one shared group message; everyone sees the same content. Needs resolving.
- `parse-review` and `split-pay` both `ask` for payment details, but neither has an action or screen for entering them. "Waiting for details" is a dead end for friends with no path out.
- `split-open` shows "who has not picked yet" — the bot only knows members who interacted, so this list is not derivable.
- Pay-to details are withheld until the payer taps "Close picking". Every friend is gated on a payer action the brief did not ask for, and a fast friend waits.
- Payer is not notified when a friend marks sent: `confirm-payments` is an edit of the same message and edits do not notify. "Payer opens confirmations" (user) and "Payer sees a new payment" (system) both lead there, so it is unclear whether it is a state or a view.
- Item buttons carry price plus takers' names; inline button labels truncate fast.

## Winner

**P1: X. Overall: X.**

X gets the structural things right: identity comes from the tap, a friend sees their amount and pay-to instantly without waiting on the payer, the payer's cost is two taps, and X alone noticed that edits do not notify and therefore spawns the confirm message as a new mention. Its one serious error — buttons on alerts — is a fix an engineer will make in one obvious way (put "I sent" on the panel). Y is cleaner on platform mechanics (popups with OK only, throttling, copyable pay line, sum check) but gates every friend on a payer step, promises per-viewer content in a shared message, shows data the bot cannot know, and never says how payment details get entered.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 3, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 3, "states": 4, "ia": 3, "asks": 4, "fit": 4, "handoff": 3, "scope": 4}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
