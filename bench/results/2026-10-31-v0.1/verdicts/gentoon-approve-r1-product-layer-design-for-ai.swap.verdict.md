# Blind review: gentoon approve, P1

| | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|
| X | 5 | 4 | 4 | 4 | 5 | 4 | 4 | 5 | 5 |
| Y | 5 | 4 | 5 | 4 | 5 | 5 | 4 | 3 | 4 |

## Defects, X

- `cancel-confirm`: "Cancel generation" lands on `brief`, throwing away the approved plan; it should return to `plan` (or the draft in My clips). The modal "shows whether the price is charged or not" without deciding it, so the engineer has to invent the money rule.
- `ready` → "Replace a scene" → `storyboard`: no way to pick which scene, and no price shown before regeneration even though notes admit it may be charged. This is costly work without a gate, which is the one thing the brief asks to guard.
- `plan`: no state for price unavailable or insufficient funds at the approval moment; price failure is handled only inside `length-sheet`.
- `storyboard`: only per-scene failure; no whole-run failure (service down) and no notification when a scene needs a decision while the user is away.
- `plan` shows "thumbnail sketch if available", which hints at image generation before approval; ambiguous and potentially paid.

## Defects, Y

- `plan`: "Change length, aspect or style" is routed into `scene-edit`; a defaults sheet hiding inside a scene editor muddles the IA and makes the engineer build two modes of one sheet.
- `notify` always opens `storyboard`, even for "Your clip is ready"; one extra hop to `ready`.
- `storyboard`: "lyrics remain editable for scenes not yet rendered" changes an approved plan mid-run with no repricing path; unrequested and risky.
- Scope creep: plan versions with compare/restore, clip v1/v2, "Make a variation", `Settings` nav. None asked for.
- Failed shot offers only Retry or Continue without; no edit-and-retry, so the user cannot revise a failing scene prompt (X has `scene-edit-regen`).
- `plan` partial state says other scenes "stay as approved" before anything is approved; reply leans on internal codes (SR-1, AP-4) a reader cannot resolve.

## Winner

**P1 and overall: Y**, narrowly. Both specs put a single approval on the plan with price beside the button, reduce the brief to the idea, and show per-scene progress with retry and skip. Y is more complete exactly where money and long jobs bite: insufficient credit and price-unavailable states on the plan, a priced regenerate from `ready`, a cancel that returns to the plan and states the refund, a whole-run failure state, and a "scene needs a decision" notification. X is tighter in scope and reads better, and its edit-and-retry on a failed shot is a real advantage, but its ungated scene replacement and cancel-to-brief are flow defects on the expensive path.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 5}, "clarity": 5}, "Y": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 5, "handoff": 4, "scope": 3}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
