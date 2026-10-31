## Scores (P1)

| criterion | X | Y |
|---|---|---|
| success | 5 | 4 |
| flow | 4 | 3 |
| states | 4 | 5 |
| ia | 4 | 3 |
| asks | 5 | 4 |
| fit | 4 | 5 |
| handoff | 3 | 3 |
| scope | 4 | 4 |
| clarity (once) | 4 | 4 |

## Defects

**X**
- `payer-ping` is unreachable: no action anywhere points to it (`paid-toast` says "payer is notified" but goes to `bill-panel`). An engineer has to guess when it fires.
- `bill-panel` item button: "tap again to take another portion or remove it" is two contradictory behaviours in one line; the toggle/portion rule is the core interaction and must be unambiguous.
- `confirm-payments` "Confirm all sent" has a conditional target hidden in the label (settles, or confirms some and stays open) while the `to:` says only `bill-settled`.
- `bill-panel` pages items 4 at a time; Telegram keyboards take far more, so a 12-item receipt forces friends through 3 pages for no reason.
- `payer-tools` / `confirm-payments` replace the shared card for everyone while the payer works; the payer-only view should stay a popup or a reply, not the group's picking surface. Mitigated by "Back to the card".
- `parse-progress` 30 s hard timeout is tight for a model reading a long receipt; "Still reading" then failure at the same 30 s mark contradict each other.

**Y**
- `bill-posted` lists an "I sent it" button but has no action for it; the only route to `payment-marked` is from inside the `my-share` popup, which cannot carry a button. The participant's done screen is formally unreachable from the card.
- `payment-marked` transitions `by: system` to `confirm-payments`, i.e. the shared card turns into the payer's confirmation table the moment one friend taps "sent". Friends who have not picked yet lose their buttons until the payer taps "Still waiting". If this is not intended, it is a serious handoff ambiguity.
- `confirm-payments` "Got it from Aida" and "Confirm all" share one transition to `bill-settled`; confirming one person must not close the bill.
- `parse-review` is mandatory on every bill, even a clean read with a matching total, adding a tap to the repeat payer's path; the error text refers to a "Post to the group" button that does not exist (the action is "Looks right").
- `payer-payment-details` uses `block: form`, which a bot message cannot render; and `payment-marked` / `payer-payment-details` carry no moment tag.
- `my-share` error "the bot pings the payer once" has no screen or channel defined.

## Winner

**P1: X. Overall: X.** X reaches the group post with zero taps for a repeat payer when the read is clean, keeps payment details on the card so most friends never need "My share", and the participant path (taps + "I sent it", toast reply, undo) is complete and consistent. Y shows stronger Telegram grain (rate-limit handling, 1 s callback ack, popup length cap, collapsing settled card, specific failure reasons) and the richer state coverage, but its confirm stage is structurally broken: no action marks payment from the card, a single "sent" hijacks the shared card, and one confirmation settles the bill. X's defects are ambiguities an engineer can resolve in a question; Y's are flow errors that would ship wrong.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 3, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 4, "flow": 3, "states": 5, "ia": 3, "asks": 4, "fit": 5, "handoff": 3, "scope": 4}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
