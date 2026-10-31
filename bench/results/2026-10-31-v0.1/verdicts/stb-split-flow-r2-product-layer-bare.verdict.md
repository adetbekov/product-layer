# Blind review: stb-split-flow-r2 (X vs Y)

## Scores (P1)

| Criterion | X | Y |
|---|---|---|
| success | 4 | 5 |
| flow | 3 | 4 |
| states | 3 | 4 |
| ia | 3 | 4 |
| asks | 4 | 5 |
| fit | 4 | 4 |
| handoff | 3 | 4 |
| scope | 5 | 4 |
| clarity (per side) | 4 | 3 |

## Defects

**X**
- `parse-reading`: the 20-second slow state "offers Cancel", but no Cancel action exists on the screen. The payer is stuck watching a spinner with no exit until the bot decides it failed.
- `parse-review` / `parse-failed`: "Fix a row", "Add item" and "Enter items by hand" all loop back to `parse-review` with no mechanism. Inline buttons cannot take text; the engineer has to invent the reply/force-reply interaction.
- `payout-details`: mandatory, no Skip. A payer who does not want to post a card number in the group cannot reach `split-posted`. The form's submit path (how typed text becomes the message) is unspecified.
- `my-share`: surface is a callback alert, yet it carries the "I sent it" and "Change my items" actions. Telegram alerts have only OK; the "I sent" button has no listed home on `split-posted`.
- `confirm-payments`: nothing notifies the payer when a friend marks sent. Edits do not notify, so the payer waits again. Unclaimed items are never addressed.
- `receipt-sent`: a photo without a mention is "ignored by design", a new silent failure for the payer who forgets the mention.

**Y**
- `parse-progress` routes "read with doubts" to `parse-error`, but `receipt-check` shows "unclear items marked" in its partial state and the reply says doubts are flagged on the card. The two contradict; the engineer must pick one.
- `my-share`, `item-claimed`, `payment-marked`: notifications (alerts/toasts) given button actions. Per the message map, the only real "I sent" button lives in `my-share-private` (DM), which undercuts the claim that no private chat is needed. `bill-panel` lists no "I sent" button.
- `payment-marked` Undo goes to `my-share`, an alert to an alert; no surface actually hosts it.
- `receipt-check` shows "Currency: KZT - change" with no change action; "say the items by voice" adds unrequested input mode.
- Rule codes (TG-1, SR-3, FL-7) are cited throughout the spec and reply but never defined for the reader.

## Winner

**P1: Y. Overall: Y.** Y spends the payer's taps better (photo plus "Looks right", payout details deferred and skippable), handles more real Telegram edges (a working Cancel, stale buttons, paging over the keyboard limit, a new mention message because edits do not notify the payer, unclaimed items defaulting to the payer), and ships a message map that tells an engineer which messages exist and which are edited. X is tighter in scope and reads more naturally, but leaves the edit interactions, the Cancel exit and the payout skip undefined. Both share the same fit error of hanging buttons on callback alerts, so it does not separate them.

```json
{"X": {"P1": {"success": 4, "flow": 3, "states": 3, "ia": 3, "asks": 4, "fit": 4, "handoff": 3, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 3}, "winner": {"P1": "Y", "overall": "Y"}}
```
