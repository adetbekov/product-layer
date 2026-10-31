# Verdict: stb-split-flow-r2 (X vs Y)

## Scores

| Step | Side | success | flow | states | ia | asks | fit | handoff | scope |
|---|---|---|---|---|---|---|---|---|---|
| P1 | X | 5 | 4 | 5 | 4 | 5 | 4 | 4 | 4 |
| P1 | Y | 4 | 3 | 4 | 3 | 4 | 3 | 3 | 4 |

Clarity: X 4, Y 4.

## Defects

**X**
- `my-share` (notification) carries "I sent the payment", "Send me this in private" and "Back" as actions. A Telegram callback alert has only OK; it cannot host buttons. "I sent" is never placed on `bill-panel`, so the engineer must guess where the participant's key action lives. Same problem with "Undo" on `payment-marked` and "Keep picking" on `item-claimed`.
- `bill-panel` item buttons show "Plov x2 - 2 people" but the spec does not say how a quantity of 2 splits among 3 tappers; shared-item rule is implied, not stated.
- `parse-error` "Type or say the items" jumps straight to `receipt-check`; the text-entry moment itself has no screen or format hint, though the receipt-check error state partially covers it.
- Reply leans on internal rule codes (TG-1, SR-3, FL-7) a reader cannot decode.

**Y**
- `confirm-payments` "Confirm all who sent" goes to `bill-closed`, which shows "all rows confirmed"; people still at "not sent" vanish. `bill-closed` mentions "Close anyway" but no screen offers that action. "Remind unpaid" lands on `split-posted`, an odd target.
- `pick-items` is a duplicate of `split-posted` ("the same group message"); it adds a screen without adding a state, and no toast shows the running share.
- No notification path for the payer: a friend marking "sent" only edits the message, and edits do not notify. The payer has to "open payments" by noticing.
- `parse-review` "tap a row to edit" and `payout-details` as `block: form` do not exist in bot messages; the correction mechanic (reply text? per-row buttons?) is left to guesswork.
- Unclaimed items have no owner ("stays highlighted"); the shares of everyone else are undefined until the bill closes.
- `my-share` has the same alert-with-buttons problem as X, and its fallback posts a reply mentioning the friend into the group, re-creating the noise pain point.
- No `nav` key and `by:` missing on most actions, so system vs user steps are ambiguous.
- `parse-reading` sends "no items found" to `parse-failed`, while `parse-review` also defines an empty "no items" state; two homes for one condition.

## Winners

**P1: X.** Both converge on the right skeleton: one group message edited in place, item picks via inline buttons, share via private alert, payer review before posting. X is more complete and more Telegram-literate: it answers the parse failure with a 10-second heartbeat, flags doubtful items instead of claiming success, defaults unclaimed items to the payer, and sends the confirm tracker as a new message precisely because edits do not notify. Y has good details (batched edits, deleted-message repost, mismatch warning) but its confirmation logic is broken, the payer is never told a payment arrived, and several blocks and gestures do not map to the platform.

**Overall: X.** X's one real flaw, buttons on alerts, is shared by Y, while Y adds a redundant screen, an extra payer step, and dead logic in the close path. X's steps-to-value and message map give an engineer what they need; Y's spec would need a second pass before building.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 4, "flow": 3, "states": 4, "ia": 3, "asks": 4, "fit": 3, "handoff": 3, "scope": 4}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
