# Blind review: checkout for a returning customer (P1)

| Criterion | X | Y |
|---|---|---|
| success | 5 | 4 |
| flow | 4 | 4 |
| states | 5 | 5 |
| ia | 4 | 3 |
| asks | 5 | 5 |
| fit | 4 | 4 |
| handoff | 4 | 4 |
| scope | 4 | 4 |
| clarity | 4 | 4 |

Both sides get the core right: `reorder` runs cart -> checkout -> confirmed in two taps, nothing saved is re-asked, review and pay are one page, address / slot / card are editable in sheets that return to `checkout`, billing defaults to delivery, empty cart offers catalog plus "add from last order", and a declined card or 3-DS timeout leaves the customer with Try again / Use another card and a "you were not charged" message.

## Defects: X

- `cart`: "Browse the shop" targets `cart` itself, and `confirmed`: "Track order" targets `confirmed`. Self-loops instead of an explicit out-of-scope exit; the notes admit it, but an engineer still has to guess where these go.
- `sign-in`: a session-expiry re-auth page is not in the request and is tagged `checkout`, which muddies the moment. Small scope creep.
- `checkout`: uses a `partial` state key outside the fixed empty / loading / error set; the content (slot no longer available) is good, the slot is just nonstandard.
- `edit-address`: asks country and city for a new address while the same line says they are inferred. Decide one.

## Defects: Y

- `cart-empty-exit`: one placeholder page stands in for both the catalog and order tracking. `confirmed` -> "Track order" therefore lands on the catalog. Wrong target and a confusing id for handoff.
- Moments are tagged on only three screens; `payment-processing`, `three-ds` and `payment-failed` are where the order is paid but carry no `checkout` tag, which the request asked for.
- `payment-failed` is a full page rather than a notice on `checkout`, so a decline swaps the whole context away even though the data is kept. Workable, but one more place for the same choices.
- No `nav` block; the checkout page is otherwise well placed.

## Where Y is stronger

`payment-processing` with an idempotency key and result lookup after network loss, slot hold with remaining time, the 10 s "still working" message, and the 5-minute 3-DS timeout are concrete engineering details X leaves implicit. Y's `checkout` also designs "some items changed" with a diff.

## Winner

P1: X. Overall: X.

X answers every explicit part of the request (flow, all screens tagged, nav), keeps payment failure on the checkout page where the customer's choices are visible, and handles the 3-DS modal with a Cancel that returns safely. Y's failure handling is more thoroughly engineered, but the `cart-empty-exit` stand-in, the mis-targeted Track order and the untagged payment screens cost it on IA and completeness. It is a close call on substance; X is the cleaner handoff.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 4, "flow": 4, "states": 5, "ia": 3, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
