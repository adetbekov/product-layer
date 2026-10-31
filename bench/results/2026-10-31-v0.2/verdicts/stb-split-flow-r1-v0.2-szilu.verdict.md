## Scores

| P1 | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|
| X | 5 | 4 | 5 | 4 | 5 | 5 | 4 | 4 | 4 |
| Y | 5 | 3 | 4 | 3 | 4 | 4 | 3 | 3 | 4 |

Both specs name `payer` and `participant`, tag all four moments, and every `to` resolves. Both keep friends in the group with inline toggles and private callback popups, edit one post in place, and ask for payment details once.

## X: main defects

- `bill-live` / `items-edit`: "payer also sees Edit items and Lock split" implies a per-user keyboard; Telegram shows the same buttons to everyone (X knows this on `payments-live`, so the two screens contradict). `items-edit` says "each editable" with `block: form` but never states the Telegram mechanism (buttons per line? text reply?); only the empty-state hint suggests typed lines. Cancel from the manual path lands on an empty `bill-live`.
- `bill-locked`: the "nobody picked, lock refused" error belongs to the Lock action on `bill-live`, not to the post-lock screen. The unclaimed-items rule (split among pickers) can charge people for food nobody admits to; worth a payer choice.
- Participant flow: a friend cannot mark "sent" until the payer taps Lock; nothing nudges the payer to lock when everyone has tapped "I'm done". No pagination for long receipts (qty expansion makes this likely).
- `payer-requisites` is tagged `parse`; it is not parsing.

## Y: main defects

- `confirm-payments` -> `settled`: "Confirm all marked" is the only confirm path and it ends the bill (terminal, buttons inert). A payer who confirms 3 of 5 strands the other two with no way to mark payment. The `partial` state promises pending friends "stay listed" but the action contradicts it.
- No lock: friends mark "I paid" on provisional amounts; a later tap on a shared item changes what a friend already paid. Not acknowledged anywhere.
- `confirm-payments` edits the one shared card into a payer-only table, so friends still picking lose their buttons until the payer taps Back. Confirmation should not take over the selection surface.
- `payment-details` has no Skip or Cancel; the payer must type a card number into the group to post. `share-popup` then handles "details missing", which cannot happen.
- `parse-failed` "Retake photo" is a button leading to `parsing`; a button cannot take a photo (X correctly routes to the payer's own message). Loading has no timeout or repeat-failure handling ("a few seconds" is not buildable). Most actions omit `by:`. "Next page" oddly opens `share-popup`.
- Scope creep: voice input, currency switcher.

Y's strengths over X: the share popup rides on every item tap (amount for free), payment details are visible in the card text (copyable), friends can pay without waiting, and the always-on check card gives approval before friends see the bill. X's conditional review (only on mismatch) is leaner but exposes an unreviewed read to the group.

## Winner

**P1: X. Overall: X.** X handles the two hard mechanics Y skips: amounts freeze before anyone pays, and the payer is notified when a friend marks "sent" (edits do not notify, so Y's payer has to poll). X's parse handling is concrete (1s ack, 10s hint, 40s timeout, named reason, manual path after a second failure) where Y's is vague. Y is tighter and reads well, but its single terminal "Confirm all marked" is a dead end for late payers, which is the payer's core job.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 5, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 3, "states": 4, "ia": 3, "asks": 4, "fit": 4, "handoff": 3, "scope": 3}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
