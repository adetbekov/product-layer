# Verdict: stb-split-flow-r1 (P1)

| Criterion | X | Y |
|---|---|---|
| success | 5 | 5 |
| flow | 4 | 3 |
| states | 4 | 5 |
| ia | 3 | 4 |
| asks | 4 | 5 |
| fit | 3 | 4 |
| handoff | 3 | 4 |
| scope | 5 | 4 |
| clarity | 5 | 3 |
| **total** | **36** | **37** |

## Defects: X

- `my-share` / `payment-sent` (surface: notification): a Telegram callback popup is plain text, max ~200 characters, no buttons, no text selection. The spec puts "I paid", "Change my items", "Undo" and a "tap to copy" card number inside it. The participant's done screen is therefore unreachable as written; an engineer must invent the real mechanism (a "Paid" button on the group message, or a Mini App).
- `split-post`: one group message carries N item buttons, +/- steppers, Done, My share, payer-only Edit/Set-how-to-pay, and later per-person Confirm, Confirm all, Not received, Remind. Cluttered, role-mixed keyboard; everyone sees payer-only controls. "Edit items" has no described mechanism.
- `split-post` asks: force-reply for payment details posts a new group message, contradicting the one-message rule.
- `parse-failed`: delivered by editing the live message (notes say new message); edits do not notify, so the payer can still wait blind. `receipt-photo` error says "not a receipt - stays silent", which also contradicts "never silent".
- `bill-closed` empty: "payer can close manually" has no action; `parse-failed` Cancel targets the user's own photo message.

## Defects: Y

- `select-items` / `my-share` in DM via deep link: pain point 3 is kept and called "unavoidable", although inline callbacks on the group message or a Mini App button avoid the Start tap entirely. Participant cost is N+3 (N+4 first time) plus a chat switch, vs X's N+2 in place.
- `start-needed-group`: the payer must start the bot before the receipt is even read; an extra gate on the happy path for first-time payers.
- `payer-confirm-person` "Not received" → `my-share`: a payer action transitions to the friend's screen (different user); should return to `payer-confirm` and notify the friend.
- `split-panel`: "Remind pending" appears in shows but not in actions; items and who took what are not visible in the group, so friends decide blind until they open DM.
- `select-items` empty: "Done stays disabled" is not a native inline-keyboard capability.
- `parse-review` shows has a broken string ('receipt total and currency (KZT' / 'change)'); `parse-failed` describes a Cancelled state with no Cancel action. Codes like TG-1/SR-8 cite a checklist the reader does not have.

## Winner

**P1: Y. Overall: Y**, narrowly. X has the better idea for the group context (pick and pay on the live message, no private chat, N+2 taps, zero new messages) and the cleaner reply, but its central share/pay step relies on a popup that cannot hold buttons or copyable text, so the participant flow does not actually close and the handoff would stall there. Y is fully buildable, more Telegram-literate (new reply on failure because edits do not notify, stale-button handling, reconciliation gate so the payer reviews only when totals fail, deferred payment-details ask), and its states are the most complete, at the cost of keeping the DM pain point and heavier, code-laden prose. If X replaced the popup with a group-message "Paid" button or a Mini App sheet, it would win.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 3, "asks": 4, "fit": 3, "handoff": 3, "scope": 5}, "clarity": 5}, "Y": {"P1": {"success": 5, "flow": 3, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 3}, "winner": {"P1": "Y", "overall": "Y"}}
```
