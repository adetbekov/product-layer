## Scores (P1)

| criterion | X | Y |
|---|---|---|
| success | 4 | 4 |
| flow | 3 | 4 |
| states | 4 | 4 |
| ia | 3 | 4 |
| asks | 3 | 5 |
| fit | 3 | 4 |
| handoff | 3 | 4 |
| scope | 4 | 3 |
| clarity (once) | 4 | 3 |

## Defects

**X**
- `pick-items`: specified as a state of the single shared group message with "check mark = mine" toggles and a per-viewer "your share so far". A Telegram group message has one inline keyboard identical for every viewer, so per-person check marks and per-person running totals cannot live there. The engineer must guess whether the buttons mean "add my name to this item" and what the card shows while someone is picking.
- `my-share`: a callback popup (`surface: notification`) carries actions "Back to the card" and "I sent it". Callback alerts are text-only; no buttons, no copyable text. The actual path to `marked-paid` exists only via `split-locked`, which is not what the screen says.
- `split-locked` / `pick-items.error`: once locked, a late friend gets "ask the payer" but there is no unlock action anywhere — a dead end. "I sent it" is also gated on the lock, so friends cannot finish their flow until the payer takes an extra step the payer flow does not include.
- `check-items` is mandatory on every bill even when it shows "items add up to the total"; `payer-details` blocks the post on the first bill. Both are extra steps the system had the information to skip or defer.
- `all-settled` uses `states.empty` for "closed bills are not editable" — a rule, not a state.

**Y**
- `select-items` / `my-share` live in a DM opened by deep link, so the first-time friend still pays the "Start" tap that the brief lists as a pain point; Y names the cost but does not try a group or Mini App alternative.
- `start-needed-group`: the bot refuses to read the photo until the payer has started it, even when the receipt would reconcile and need no DM at all.
- `parse-review`: `shows` has a split line ("receipt total and currency (KZT" / "change)") — YAML artifact; the deep-link button that opens it is not listed as an action on any group screen.
- `split-panel` shows "Remind pending" but has no such action; `payer-confirm-person` "Not received" transitions to another user's screen (`my-share`).
- `parse-failed` gives a generic reason ("may be blurry or cut off") where the model can usually say which.
- Scope: voice input, a Cancel button during a ~10 s parse, a quantity stepper, "Split another receipt" were not asked for. `pay-details-ask` and `bill-closed-stale` carry no moment tag.

## Winner

**P1: Y. Overall: Y.** X has the better instinct — everything in the group, one card edited in place, specific parse failures — but its two central participant screens describe interactions Telegram cannot render (per-viewer toggles on a shared keyboard, buttons in a callback popup), and the lock gate adds a payer step with no way back. Y is buildable as written: it reads the platform correctly (edits do not notify, deep links land on items, stale buttons answered, paging), posts the split with zero payer taps when the totals reconcile, and defers payment details instead of blocking. Y's cost is the one-time Start tap and some unrequested extras; X's cost is a spec an engineer would have to redesign.

```json
{"X": {"P1": {"success": 4, "flow": 3, "states": 4, "ia": 3, "asks": 3, "fit": 3, "handoff": 3, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 4, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 3}, "clarity": 3}, "winner": {"P1": "Y", "overall": "Y"}}
```
