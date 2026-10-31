# Blind review: checkout for a returning customer (P1)

## Scores

| Criterion | X | Y |
|---|---|---|
| success | 5 | 4 |
| flow | 4 | 3 |
| states | 4 | 5 |
| ia | 4 | 4 |
| asks | 4 | 4 |
| fit | 4 | 4 |
| handoff | 4 | 4 |
| scope | 3 | 4 |
| **P1 total** | **32** | **32** |
| clarity (per side) | 5 | 4 |

Both deliver the core ask: `reorder` runs cart -> checkout -> confirmed in two taps, saved address/slot/card are visible with a Change sheet that returns to checkout, billing defaults to delivery, and the sign-in/guest step is gone for signed-in users.

## Defects

**X**
- `checkout`: the `empty` state is used for "no saved address or card (first order)". That is not an empty state and the first-time customer was not requested; it muddles the states contract.
- `checkout` / `processing` error: no "you were not charged" reassurance after a decline or 3-DS timeout, which is the first thing a customer wants to know.
- `three-ds`: Verified -> `processing` -> `confirmed` is a two-hop system path; harmless but unexplained. `sign-in` shows "Continue as guest" yet its only action is Sign in -> checkout, so the guest link is a dead end.
- `catalog`: a full unrequested screen (categories, search, states) specced only to give the empty cart an exit.
- `confirmed`: no loading state for a payment still being confirmed.

**Y**
- `cart`: "Browse the shop" -> `cart` is a self-loop. The empty-cart state promises "Browse the shop" and "Add items from your last order", but neither has a real target, so an empty cart has no way out inside the spec (the notes admit this).
- `confirmed`: "Track order" -> `confirmed` is another self-loop and "Back to shop" -> `cart` sends the user to the basket they just emptied.
- `sign-in`, all sheets and `bank-check` are tagged `moment: checkout`; the request defined `checkout` as "where the order is reviewed and paid", so `sign-in` at least is mis-tagged.
- `nav` block and `edit-address` asking for country (with a hedge) are small unrequested additions; the reply leans on opaque codes (SR-1...SR-7) the reader cannot resolve.
- `notes.md` names an "Apple-style skill" for sheets, brushing against the visual layer it should stay out of.

## Winner

**P1: X. Overall: X.** On raw points this is a tie, and Y is clearly stronger on states: it designs the partial "slot vanished" case, network failure with "you were not charged", a cart emptied in another tab, and a "confirming your payment" state on `confirmed`. But the review was asked to judge whether empty cart and failure are handled, and Y's empty cart has no exit: both promised actions resolve to the same screen, while X spends scope on a `catalog` page so the exit is real. X also keeps the moment tags to the three screens the request defined, has no dead-end loops, and its reply is shorter and reads more like a person. Y would win if the self-loops were resolved and X's stronger error copy were absent; as submitted, X is the one an engineer can build without an unanswered "where does this go".

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 4, "fit": 4, "handoff": 4, "scope": 3}, "clarity": 5}, "Y": {"P1": {"success": 4, "flow": 3, "states": 5, "ia": 4, "asks": 4, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
