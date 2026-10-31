# Blind review: stb-split-flow-r1 (X vs Y)

| Step | Side | success | flow | states | ia | asks | fit | handoff | scope |
|---|---|---|---|---|---|---|---|---|---|
| P1 | X | 5 | 3 | 5 | 4 | 4 | 4 | 4 | 4 |
| P1 | Y | 5 | 4 | 4 | 4 | 5 | 3 | 3 | 5 |

Clarity: X 3, Y 5.

## Defects, X

- `select-items` / `my-share`: item picking moves to a DM via deep link, so every friend still has to leave the group and tap Start. That is the third pain point of the brief, accepted as "unavoidable" instead of solved; Telegram callbacks on a group message do not need a private chat. Participant path is 3+N (+1 first time) when N+2 is possible.
- `parse-review`: lives in a DM but the group-message button that opens it ("Payer checks 2 items") is only mentioned in a comment; no screen or state covers that intermediate group edit.
- `parse-progress`: user Cancel is routed to the error screen `parse-failed` with a "text variant" — an error screen doubling as a cancel receipt.
- `payer-confirm-person`: "Not received" transitions to `my-share`, which is the friend's screen; the payer's own return state is unspecified.
- `start-needed-group`: claims the bot checks DM availability "before reading"; Telegram only reveals this by attempting a send, so the sequencing is not buildable as written.
- Handoff noise: `shows` items split by a stray comma ("receipt total and currency (KZT" / "change)"), unmatched quotes; the reply is dense with internal codes (TG-1, SR-8, FL-7) that mean nothing to a reader.

## Defects, Y

- `my-share` and `payment-sent` are "callback popups" that carry buttons ("Paid", "Undo", "Change my items", "Close") and tap-to-copy. A callback answer is a plain alert up to 200 characters with only OK; none of those actions can exist there. The intent survives if "My share" and "I paid" sit on the group keyboard, but an engineer has to redesign the share moment.
- `split-post`: "the button shows a checkmark instantly" — the inline keyboard is shared by everyone, so per-person state cannot live on the buttons; only the table rows can show it. No paging for receipts with 15–25 items on one keyboard.
- `bill-closed`: "Confirm all sent" lands here even with people unpaid; its empty state says the bill "stays open and the payer can close it manually", but no close action exists anywhere — a contradiction and a dead end.
- `split-post` "Edit items (payer only)": how the payer fixes a name or price inside a group message is not specified. The payment-details force-reply is a new group message, against the one-message promise.
- Minor: invalid YAML in `parsing.shows` (quoted string followed by bare text inside a flow list).

## Winners

**P1: Y.** Y puts the whole bill in one edited group message, lets friends pick without a private chat, asks only for payment details (once) and manual items (only after two failed photos), and handles the blurry photo with a timeout, a reason and three exits. Its one serious flaw is mechanical — buttons inside a callback popup — and is fixable without changing the shape of the flow. X is the more complete, state-rich spec with sharper Telegram craft (new reply for failures because edits do not notify, paged keyboards, stale-button handling), but it concedes the pain point the brief named, routes every friend through a Start tap and a DM, and leaves cross-actor and cancel transitions muddled.

**Overall: Y**, narrowly — the right product shape with a patchable defect beats a thorough spec built around the wrong room.

```json
{"X": {"P1": {"success": 5, "flow": 3, "states": 5, "ia": 4, "asks": 4, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 3}, "Y": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 3, "handoff": 3, "scope": 5}, "clarity": 5}, "winner": {"P1": "Y", "overall": "Y"}}
```
