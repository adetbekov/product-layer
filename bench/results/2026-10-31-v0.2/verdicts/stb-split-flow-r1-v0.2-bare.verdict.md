# Blind review: bill-splitting Telegram bot, P1

| Step P1 | success | flow | states | ia | asks | fit | handoff | scope |
|---|---|---|---|---|---|---|---|---|
| X | 5 | 4 | 4 | 4 | 4 | 4 | 4 | 5 |
| Y | 5 | 3 | 4 | 3 | 4 | 3 | 3 | 4 |

Clarity (once per side): X 4, Y 4.

## X: main defects

- `payment-details`: the only action is "Send details (typed reply)". No Skip, no Cancel. A payer who does not want to type a card number into the group has no way forward; the bill is stuck before posting.
- `confirm-payments`: it is "the same group card switched to a payer-only confirm view". A Telegram message is shared, so while the payer is in this view every friend loses the item buttons and "I paid". Then `settled` is terminal and the payer may close with people pending, so a late friend gets only "already settled" and has no path to mark payment.
- `check-receipt` is always shown, even on a clean parse: one extra tap on every bill. Defensible as an approval gate, but not the fewest steps.
- Mapping oddities an engineer will trip on: "Next page of items" transitions to `share-popup`; two user actions "Post split (details known)" / "Post split (first time)" model what is one tap plus a system branch; `payment-details` is tagged `parse`.
- Corrections are "free text or voice" in the group, but nothing says how the bot tells a correction from chatter (reply-to the card?).

## Y: main defects

- `payout-details` is reachable only from `parse-check`. On a confident parse `parsing` goes straight to `split-posted`, so a first-time payer is never asked how to be paid and every friend's `my-share` degrades to "Ask {payer}". Flow bug on the most common path.
- `my-share` is `surface: notification` yet renders a card with a Copy action and buttons "I paid", "Change my items", "Close". A Telegram callback alert is plain text with one OK. As specced it cannot be built; the private-chat copy is optional, so the engineer must guess where "I paid" actually lives.
- `pick-items` is `surface: sheet` but "is the same group message". A per-friend running "Your part: X", a quantity stepper and a disabled Done cannot exist on one shared message with shared inline buttons. It duplicates `split-posted` and muddles the IA.
- After "Close picking" the message becomes `payments-tracking`, which has no friend-side action: a friend who picked but has not yet marked paid cannot reach `my-share`. Settlement is only the system "Everyone confirmed", so one silent friend keeps the bill open forever; there is no manual close.
- No correction path once a confident parse is posted; cancel after posting is declared out of scope. A misread price has no way out.

## Good in both

Both keep one edited group message, pick by inline buttons (no private chat), handle the blurry photo with an immediate reason plus retake / type-items / cancel, and ask payment details once. Y's parse states (1 s ack, 15 s "still reading", re-post if the message is deleted, merged edit bursts) and Skip on payment details are better than X's. X knows that edits do not notify and makes the reminder the only new message, puts "I paid" on the card where a button can actually be, and admits the popup-copy limitation instead of inventing a Copy action.

## Winner

P1: X. Overall: X. X's spec is buildable as written on Telegram's actual surfaces and gets a friend to "I paid" in N+1 taps; its defects (no skip on payment details, the confirm view hijacking the shared card, the always-on review) are fixable without restructuring. Y has the richer states and a leaner happy path on paper, but its two central participant screens are described as things Telegram cannot render, and the first-time payer never gets asked for payment details on the common path, so the flow fails its own goal.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 4, "fit": 4, "handoff": 4, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 3, "states": 4, "ia": 3, "asks": 4, "fit": 3, "handoff": 3, "scope": 4}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
