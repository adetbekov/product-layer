# Blind review: gentoon-approve-r1 (P1)

| Step | Side | success | flow | states | ia | asks | fit | handoff | scope |
|---|---|---|---|---|---|---|---|---|---|
| P1 | X | 5 | 4 | 5 | 4 | 5 | 5 | 4 | 3 |
| P1 | Y | 5 | 3 | 3 | 4 | 5 | 4 | 3 | 5 |

Clarity: X 4, Y 4.

## Defects, X

- `plan` -> "Change length, aspect or style" routes into `scene-edit`, the same sheet used for rewriting a scene. One sheet with two unrelated jobs; a builder has to invent the switching logic.
- `notify`: the only action is Open -> `storyboard`, even when the message is "Your clip is ready". The ready case should deep-link to `ready`.
- `plan` and `storyboard` both keep lyrics "editable while frames render". The plan is declared the single approval gate, then content that was priced and approved stays mutable mid-run with no stated effect on price, scenes or re-render. This blurs the gate.
- `storyboard` partial state: a failed scene offers only Retry or Continue without; the user cannot change the scene text before retrying, which is the most likely fix for a shot that fails on its prompt.
- Scope creep: plan versions with compare/restore, clip v1/v2, "Make a variation", Share link, and a full credits purchase sheet. Insufficient balance needed a way out; a purchase flow with payment states was not requested.
- Reply cites internal rule codes (SR-1, AP-4) that mean nothing to the reader.

## Defects, Y

- `storyboard`: assembly "waits until every scene is done or skipped", but the only system notification is "clip finished". A user who left (as the screen invites) is never told a scene failed and needs a decision, so the job stalls silently. This is the main failure mode the brief asks to design around.
- `cancel-confirm`: Cancel generation -> `brief`, dumping the user out of their plan; and "whether the price is charged or not" is left for someone else to decide. The modal exists to say exactly that.
- `ready` -> "Replace a scene" -> `storyboard` with no price shown or confirmed, while notes.md admits replacement may be charged. Costly work without an approval in front of it.
- `plan`: no `asks` block (the approval itself is the ask), no insufficient-balance or payment-failed path although per-clip pricing is central to the brief; "Draft a new plan" does not say whether scene edits survive.
- `storyboard`: no whole-run failure state (service down), only per-scene failure.
- `scene-edit`, `scene-edit-regen`: no loading state for a save that triggers a regeneration.

## Winner

P1: X. Overall: X.

Both put the one approval on the plan with price beside the button, strip the brief to the idea, and make failed shots per-scene. Y is tighter in scope and wins on revision at the storyboard (edit-and-retry, live repricing per length option), but it leaves the two moments that matter most under-designed: an away user is never called back for a failed scene, and cancel and scene replacement leave cost undecided or unguarded. X decides those (cancel returns to the plan, states what is kept and refunded, notifies on "scene needs a decision", shows cost before a re-render) and gives ranked content and copy a builder can use, at the price of unrequested versioning and credits features.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 5, "handoff": 4, "scope": 3}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 3, "states": 3, "ia": 4, "asks": 5, "fit": 4, "handoff": 3, "scope": 5}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
