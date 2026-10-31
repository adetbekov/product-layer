# Blind review: Split the Bill, P1

| Step | Criterion | X | Y |
|---|---|---|---|
| P1 | success | 5 | 5 |
| P1 | flow | 4 | 3 |
| P1 | states | 5 | 3 |
| P1 | ia | 4 | 3 |
| P1 | asks | 5 | 3 |
| P1 | fit | 4 | 4 |
| P1 | handoff | 4 | 3 |
| P1 | scope | 4 | 4 |
| — | clarity | 3 | 4 |

## Defects, X

- `select-items` / `split-panel`: friends still leave the group for a DM and first-timers pay a Start tap. The third pain point is conceded, not solved. Participant cost is 3+N (4+N first time) versus Y's N+2.
- `split-panel`: shows "Remind pending" but has no action for it; "Payer: Confirm payments" is a button everyone sees, with no answer for a non-payer tap.
- `parse-review`: malformed `shows` entries ('receipt total and currency (KZT', 'change)', 'Publish split" primary') — a YAML list split on commas; an engineer has to guess.
- `pay-details-ask` → `split-panel`, `payer-confirm-person` "Not received" → `my-share`, `payer-confirm` "Remind pending" → `remind-dm`: transitions jump from one person's DM to another person's screen; the actor change is implied, never stated.
- `close-confirm`: unclaimed items are redistributed to people who may already have marked payment; `paid-marked.partial` patches it after the fact rather than preventing it.

## Defects, Y

- `parse-check`: location is contradictory. The reply says the payer checks "before the group sees anything", but notes say there is one group message edited in place. If it is the group message, the group sees the draft, and "only the payer sees the edit controls" is false for inline buttons.
- `parse-check` / `fix-item`: how-to-pay and item fixes are typed as text replies in the group — new messages in the chat, the exact noise the brief complains about, and a card number typed into a group.
- `split-select`: one toggle per item. No quantity for qty>1 lines, no stated rule for an item several people tap (even split is implied, not written). Button labels carrying name, price and picker names will truncate.
- `payments-board` / `all-settled`: no way for the payer to close while some people have not marked payment ("payer can close anyway" has no action); "way back to reopen picking" has no action; `all-settled` loops to itself.
- `payments-board`: friends cannot see their amount until the payer closes picking — a waiting state nobody designed. "Reminder time reached" has no time, and an "edit plus a single mention" does not exist as a Telegram primitive (edits do not notify).
- `share-view`: a popup is the only carrier of payment details; popup text cannot be copied and is capped at ~200 characters.

## Winner

P1: X. Overall: X.

Y has the better core idea: picking with inline buttons under the single group post removes the private-chat detour and gives the cheapest participant path. But the spec around that idea is too thin to build — shared items and quantities are unspecified, the payer's review screen cannot be both private and the group message, closing with stragglers has no action, and text replies in the group reintroduce the noise. X concedes the DM detour but delivers a flow that reaches each goal with explicit states for every failure (unreadable photo, three-try cap, sender who never started the bot, stale buttons, failed edits), asks the payer only when totals do not reconcile, and defers payment details without blocking the post. X is buildable now; Y needs another round.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 3}, "Y": {"P1": {"success": 5, "flow": 3, "states": 3, "ia": 3, "asks": 3, "fit": 4, "handoff": 3, "scope": 4}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
