## Scores (P1)

| | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|
| X | 5 | 3 | 5 | 4 | 4 | 3 | 3 | 4 | 3 |
| Y | 4 | 4 | 4 | 4 | 4 | 4 | 3 | 4 | 4 |

## Defects

**X**
- `select-items`, `my-share`, `paid-marked`: the whole participant flow runs in a private chat via deep link. The brief names "friends must open a private chat" as a pain point; X calls the Start tap "unavoidable" instead of solving it. Participant cost is 3+N taps plus a context switch (4+N first time).
- `start-needed-group` / `parse-progress`: the bot refuses to read the photo until a first-time payer starts it ("checked before reading"). Reading and posting in the group need no DM; only `parse-review` and `pay-details-ask` do. The advertised one-step payer path is false for new payers.
- `my-share` / `paid-marked`: amounts are never frozen, so a friend can mark 4 200 KZT as sent and then see "the amount changed to X" when someone else picks a shared item. Handled as a state, not prevented.
- `parse-progress`: "Cancel" routes to `parse-failed`, a failure screen reused for a user cancel.
- `payer-confirm-person`: "Not received" transitions to `my-share`, a screen belonging to a different actor; what the payer sees next is unspecified.
- `parse-review`, `start-needed-group`: `shows` lines are corrupted by YAML splitting (`'receipt total and currency (KZT'`, `'change)'`, unclosed quotes). Codes TG-1/SR-3/FL-8 are cited throughout but never defined, so the builder cannot follow them.

**Y**
- `pick-items`: "check mark = mine" and "your share so far" are written as content of the shared group message. A Telegram inline keyboard is identical for every viewer, so per-user marks are impossible there; the names-on-items approach of `split-posted` and the callback popup of `my-share` are the only ways, and the spec should say so. No paging and no quantity handling for items with qty > 1.
- `split-locked`: "I sent it" is a button on each person's line; nothing says what happens when Dana taps Askar's button (contrast `payments-tracker`, which does guard the payer's buttons).
- `my-share`: a callback popup is capped at about 200 characters and its text is not copyable on mobile; "payment details, copyable" is not achievable as written.
- `check-items`: "Fix the numbers" has no target; there is no path to a new photo from here, only from `parse-failed`.
- `parse-failed` is an edit of `parsing`; Telegram edits send no notification, so "tagged payer so the message reaches them" is weaker than it sounds. Most actions omit `by:`, and `all-settled` misuses `empty` for "not editable".
- `payer-details`, `edit-item`, `manual-entry` expect free-text replies in a group chat without saying how the reply is bound to the question (reply-to / force reply).

## Winner

**P1: Y. Overall: Y.** The brief gives three pain points; Y solves all three with one live card, callback popups and in-group taps (2+N taps for a friend, no Start, no context switch), and never needs the bot to DM anyone, which also removes the "never started the bot" dead end that X spends two screens on. X is the more careful spec: richer states, deferred and skippable asks, correct notes about edits not notifying, stale-button handling, paging. But it declares the private-chat pain point unsolvable and gates a new payer's parse on starting the bot, which are design errors that need a redesign; Y's defects are rendering and guard details an engineer can fix without changing the flow.

```json
{"X": {"P1": {"success": 5, "flow": 3, "states": 5, "ia": 4, "asks": 4, "fit": 3, "handoff": 3, "scope": 4}, "clarity": 3}, "Y": {"P1": {"success": 4, "flow": 4, "states": 4, "ia": 4, "asks": 4, "fit": 4, "handoff": 3, "scope": 4}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
