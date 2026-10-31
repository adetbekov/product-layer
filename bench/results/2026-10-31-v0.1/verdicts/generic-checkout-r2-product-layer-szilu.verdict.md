# Blind review: checkout for a returning customer (P1)

| Criterion | X | Y |
|---|---|---|
| success | 5 | 4 |
| flow | 5 | 4 |
| states | 4 | 4 |
| ia | 4 | 4 |
| asks | 4 | 5 |
| fit | 4 | 4 |
| handoff | 4 | 3 |
| scope | 4 | 5 |
| clarity (per side) | 4 | 3 |

Both sides reach the same core answer: a two-tap `reorder` (Checkout, Place order), one pre-filled `checkout` page with address, slot, card and phone as defaults, each changeable in a sheet that returns to the same page, billing checkbox removed, 3-D Secure as a system-driven modal, empty cart designed, payment failure keeping every choice with "nothing was charged". The differences are at the edges.

## Defects: X

- `sign-in`: "Continue as guest" leads to `checkout`, which is specified as fully pre-filled from the account. The guest path lands on a page that cannot work as written; notes admit it is undetailed. Either drop the screen or add the missing asks.
- `checkout`: no empty state for a cart that was emptied elsewhere or became fully unavailable; only the out-of-stock error is covered.
- `payment-failed`: "Try again" goes `to: checkout`, so the retry is actually two taps (return, then Place order again). Say whether it re-submits directly. No support exit except in the "unknown failure" sub-case.
- `cart`: the empty-state button "Add items from your last order" has no matching action entry.

## Defects: Y

- `cart`: the action "Start shopping / Repeat your last order" has a single target `to: cart`. "Start shopping" from an empty cart therefore loops back to the empty cart; it should go to `shop-home`. Two different outcomes are also collapsed into one action, which an engineer has to split by guessing.
- `checkout`: payment failure is an `error` state on the page, but the spec never says how it is presented (inline banner, sheet, modal). `partial` and `stale` are useful but non-standard state keys; the fixed format only names empty, loading and error.
- `edit-address`, `edit-slot`, `edit-payment`, `3ds-verify`: no `moment` tag, while they are all part of the checkout moment.
- Reply and notes lean on rule codes (SR-1, ST-4, FL-8) that mean nothing to the reader.

## Winner

**P1: X. Overall: X.** Both specs get the returning customer from cart to placed order in two taps with saved data changeable in place, and both handle empty cart and payment failure. X wins on completeness of exits: every `to` resolves to the right place, payment failure is an explicit surface, and nav is declared. Y's richer checkout states (stale slot, missing-detail asks, partial availability) are the best single piece of either spec, but its empty cart has a broken exit and its message is harder to read without the rulebook.

```json
{"X": {"P1": {"success": 5, "flow": 5, "states": 4, "ia": 4, "asks": 4, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 4, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 3, "scope": 5}, "clarity": 3}, "winner": {"P1": "X", "overall": "X"}}
```
