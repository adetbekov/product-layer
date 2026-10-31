# Blind review: checkout for a returning customer (P1)

| Step | Criterion | X | Y |
|---|---|---|---|
| P1 | success | 4 | 5 |
| P1 | flow | 4 | 4 |
| P1 | states | 5 | 4 |
| P1 | ia | 4 | 4 |
| P1 | asks | 5 | 4 |
| P1 | fit | 4 | 4 |
| P1 | handoff | 4 | 3 |
| P1 | scope | 4 | 4 |
| — | clarity | 3 | 4 |

Both answer the core ask the same way: sign-in step and contact form cut, saved address / soonest slot / saved card shown as defaults with "change" sheets, review and pay merged into one `checkout` page, 2 user taps from cart to placed order, payment failure returns to `checkout` with everything kept, empty cart designed. The differences are in the edges.

## Defects: X

- `cart`: the empty-state action "Start shopping / Repeat your last order" has `to: cart`. "Repeat your last order" staying on the cart is right, but "Start shopping" pointing back at the cart is a loop; it should go to `shop-home`. The only real routing error in the spec.
- `checkout`: two transitions hang off the same button ("Place order and pay" -> `confirmed` by user, and -> `3ds-verify` by system). The intent (bank decides) is readable, but an engineer has to infer the branching rule from the action labels.
- No `nav` block; the brief does not demand one, but Y shows it is cheap.
- Reply leans on rule codes (SR-1, ST-4, FL-8) that mean nothing to a reader without the skill; the file list comes before the decisions.

## Defects: Y

- `checkout`: the only path to `confirmed` is `Place order -> three-ds (by: user)`, then `Payment accepted -> confirmed (by: system)`. The sheet's own purpose says "only when the bank requires it", so the spec contradicts itself: as written, every order shows a 3-D Secure sheet. An engineer would have to guess whether the sheet is conditional.
- `checkout`: no `asks` block and no empty state. Notes say a customer without a saved card "lands in the picker sheet empty state", but no transition opens it; and a cart that empties while checkout is open (items removed in another tab, stock gone) is not covered beyond "back to cart with that item marked".
- `address-picker`, `card-picker`: no loading state although both save or verify server-side; the payment error has no support exit.
- `cart` empty: "Buy again" sends the user to `shop-home` instead of filling the cart in place.

## Strengths worth noting

- Y puts the next 3-5 slots inline on `checkout`, so the most common slot change costs one tap with no sheet; Y also defines `nav`.
- X covers more of what can go wrong: conditional `asks` for a missing phone, address or card; `stale` slot and `partial` stock states on checkout; "Contact support" on a declined card; country taken from the account; loading on every sheet.

## Winner

**P1: X. Overall: X.** Both reach a 2-tap reorder with saved data editable and failures recoverable, so the call rests on the edges. X's one routing slip ("Start shopping" -> cart) is a one-line fix, while Y's model routes every payment through a 3-D Secure sheet that it also says is conditional, and leaves missing-default and emptied-cart cases unhandled on the checkout page. X's richer states and conditional asks make it the safer spec to build from, even though Y's reply reads more cleanly and its inline slot chips are the nicer single idea.

```json
{"X": {"P1": {"success": 4, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 3}, "Y": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 4, "fit": 4, "handoff": 3, "scope": 4}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
