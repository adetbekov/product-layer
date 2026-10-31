# Blind review: bill-splitting Telegram bot, P1

| P1 | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|
| X | 5 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| Y | 4 | 3 | 4 | 4 | 5 | 3 | 3 | 3 | 3 |

## Defects, X

- `parse-check`: says the payer checks "before the whole group sees it", but the screen is the live group message, so the group does see it. Worse, the "how to pay" ask (card number or phone) is answered by typing into the group chat. This belongs in a DM or a popup, not the shared message.
- `fix-item`: corrections are free-text replies in the group, re-adding the noise the design otherwise removes.
- `split-select` -> `payments-board`: a friend cannot see their share or mark payment until the payer taps "Close picking". Friends who finish early wait on the payer; the payer pays an extra tap every time.
- `paid-marked` error state contradicts itself: "a repeated tap undoes nothing" and "a wrong tap can be reversed from the same button".
- `parse-check` always demands "Looks right" even when items plus service equal the total; the approval could be skipped when the receipt reconciles.

## Defects, Y

- `select-items`, `my-share`, `paid-marked` live in a DM behind a deep link and a Start tap. The brief lists "friends have to open a private chat before they can pick items" as a pain point; Y keeps it and calls it unavoidable, though inline buttons under the group post avoid it entirely.
- `parse-progress` -> `start-needed-group`: a payer who never started the bot is blocked before the photo is even read, adding a gate to the one-step happy path the reply advertises.
- `parse-review` `shows` is corrupted ("receipt total and currency (KZT", "change)", stray quotes around "Publish split"), and the group message's state while the payer reviews in DM is unspecified.
- `payer-confirm-person` "Not received" transitions to `my-share`, a friend's screen; the actor is the payer. The side effect (notify the friend) is not designed.
- `split-panel` shows a "Remind pending" button with no action, and a payer-only "Confirm payments" button visible to everyone with no handling for a non-payer tap.
- Rubric codes (TG-1, SR-8, FL-8) are sprinkled through the spec and the reply; an engineer without that document gains nothing from them.
- Unrequested additions: voice input for items, Cancel during parse, close confirmation dialog, stale-button screen, DM reminders.

## Winner

P1: X. Overall: X.

X answers all three interview pain points with one mechanism that fits Telegram: a single group message edited in place, item buttons under it, and tap-answer popups for private amounts, so no friend ever opens a DM. Its flaws (payer's payment details typed in the group, the close-picking gate) are fixable in a line each. Y shows sharper Telegram knowledge in places (new reply because edits do not notify, stale buttons, deferred and skippable payment details, auto-publish when totals reconcile) and asks the payer less, but it routes every friend into a DM, which the brief named as the problem, adds a Start gate for the payer, and ships a spec with corrupted lines and a wrong-actor transition that an engineer would have to guess around.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 4, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 4, "flow": 3, "states": 4, "ia": 4, "asks": 5, "fit": 3, "handoff": 3, "scope": 3}, "clarity": 3}, "winner": {"P1": "X", "overall": "X"}}
```
