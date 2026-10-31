# Blind review: bill-splitting Telegram bot, P1

## Scores

| Step | Side | success | flow | states | ia | asks | fit | handoff | scope |
|---|---|---|---|---|---|---|---|---|---|
| P1 | X | 5 | 4 | 4 | 4 | 5 | 4 | 4 | 4 |
| P1 | Y | 4 | 3 | 3 | 3 | 4 | 2 | 3 | 5 |

Clarity: X 4, Y 3.

## Defects: X

- `payer-ping` is unreachable: no action anywhere targets it. `paid-toast` only says "payer is notified" in prose. The engineer has to infer the transition.
- `confirm-payments` "Confirm all sent" has one target (`bill-settled`) but two described outcomes; the "bill stays open" branch should return to `bill-panel`.
- `bill-panel` pagination (4 items, prev/next) lives on a shared message: one friend tapping "next" flips the page for everyone. Same for `payer-tools`, which edits the shared card and locks friends out with "Only Askar can do this" while the payer is inside it. Both are shared-state problems a Telegram inline keyboard does not solve by itself.
- `parse-check` claims to run "before friends see numbers" but its surface is a bot-message in the group thread; where it is shown is not resolved.
- `bill-panel` item button: "tap again to take another portion or remove it" is two opposite behaviours under one gesture; the quantity-1 case is undefined.
- `fix-items` after `parse-check` goes straight to `bill-panel` by system; the payer never gets to re-check the corrected table.
- `pay-details` is typed as a text message in the group: an extra human message in the noisy chat, and nothing says whose text is accepted.

## Defects: Y

- `my-share` is a notification (callback pop-up) that carries "I paid" and "Change my items" buttons. Telegram alert pop-ups are text-only, roughly 200 characters, with no copyable card number. The only path to `payment-marked` runs through this button, so a friend who never opened the bot cannot mark a payment. This recreates pain point 3, the one the brief most wanted solved. `payment-marked` repeats the problem ("tap again with the I paid button" inside a notification).
- `parse-review` is "payer only (private chat or ephemeral reply)". Telegram groups have no ephemeral replies, and the payer may never have started the bot. No fallback is designed; same for `payer-confirm`, which is "sent privately" with no group fallback (X at least specifies one).
- `parse-review` is mandatory on every bill, even a clean read, adding a tap and a private round-trip to the payer's happy path. Approval before posting is defensible, but nothing lets a clean read skip it.
- `group-post` lists a "Done picking" button with no action, and "All paid -> payer-confirm by system" contradicts `payment-marked` already doing that. `payer-confirm` "Got it / Got all" both go to `settled` even when one person is confirmed.
- `payment-marked` has no moment tag (should be `share`). `group-post` uses the "loading" state to describe toast acknowledgment, and `parse-review`'s "error" is an edit instruction, not an error.
- Items toggle on/off only; quantity-2 lines and shared dishes have no model. Where "Remind the unpaid" posts is unspecified.

## Winner

P1: X. Overall: X.

X keeps the payer and every friend on one card in the group with a direct "I sent it", asks for payment details only once and only when unknown, specifies a 30 s timeout into a visible failure, and designs a payer-only check for partial reads, so both bad photos and half-read receipts have a way out. Its flaws (orphan ping, shared-state paging and payer tools, a dual-outcome action) are fixable in the same shape. Y's design depends on pop-ups with buttons and on private chats the payer and friends may not have, which breaks the participant's done condition on the platform as it actually behaves; its clean-read path also costs an extra mandatory review tap.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 4, "flow": 3, "states": 3, "ia": 3, "asks": 4, "fit": 2, "handoff": 3, "scope": 5}, "clarity": 3}, "winner": {"P1": "X", "overall": "X"}}
```
