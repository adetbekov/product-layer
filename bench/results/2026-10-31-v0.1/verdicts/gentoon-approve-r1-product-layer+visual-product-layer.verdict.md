## Scores

| Step | Side | success | flow | states | ia | asks | fit | handoff | scope |
|---|---|---|---|---|---|---|---|---|---|
| P1 | X | 5 | 4 | 4 | 4 | 5 | 4 | 4 | 5 |
| P1 | Y | 5 | 5 | 5 | 4 | 5 | 5 | 4 | 3 |

Clarity: X 5, Y 3.

## Defects

**X**
- `storyboard`: a failed shot can only be regenerated or the whole run cancelled. There is no "continue without this scene", so a shot that keeps failing blocks assembly forever; the only exit (`cancel-confirm` -> `plan`) throws away every finished shot. Cost of a regenerate is not shown at the point of action (notes admit the policy is open).
- `ready` -> "Replace a shot" jumps to `storyboard` with no way stated to pick which shot, and no price shown before committing to a paid regeneration.
- `edit-plan`: no loading state, yet it reprices live and may need an LLM rewrite of a scene; no statement of whether a text edit regenerates anything.
- `cancel-confirm`: no loading or error state for a stop that can fail while shots are mid-render.
- `plan` shows no time estimate beside the price, although minutes-per-shot waits are the brief's main pain.

**Y**
- Scope: `credits-sheet` with purchase options, `Credits` and `Settings` in nav, share link, "make a variation", plan and clip versioning, lyric/track upload. None was requested. The insufficient-credits exit is defensible; the rest is invention.
- `scene-edit` is also the sheet for length, aspect and style; the id and purpose mislead a builder, and a defaults change is not a "scene" edit.
- `notify` -> Open always lands on `storyboard`, even for "Your clip is ready", contradicting its own "deep link to the right place".
- Drafting is described twice (`brief` loading and `plan` loading); which screen the user is on during the 20 s draft is ambiguous.
- `storyboard` lets lyrics be edited after approval "for scenes not yet rendered", which quietly reopens the plan after the single gate.
- Reply and notes cite rule codes (SR-1, AP-4, AP-10) no reader can resolve, and leak an internal project id.

## Winner

**P1: Y. Overall: Y.** Both put the one approval exactly before the paid step, show the price there, hide model and seed, and make a failed shot local to its scene. Y does the judged things more completely: a time range next to the price, a per-scene retry *or* "continue without", a cancel that says what credit comes back, a route back for a user who left, and a per-scene regenerate on the plan instead of only redrafting everything. X is tighter in scope and far better written, but its storyboard can deadlock on one bad shot and its only escape destroys finished work, which is the one failure the brief named. Y's scope creep costs it points but not the decision.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 5}, "clarity": 5}, "Y": {"P1": {"success": 5, "flow": 5, "states": 5, "ia": 4, "asks": 5, "fit": 5, "handoff": 4, "scope": 3}, "clarity": 3}, "winner": {"P1": "Y", "overall": "Y"}}
```
