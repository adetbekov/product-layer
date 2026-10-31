# Blind review: gentoon-approve r1 (X vs Y)

## Scores (P1)

| criterion | X | Y |
|---|---|---|
| success | 5 | 5 |
| flow | 4 | 4 |
| states | 4 | 5 |
| ia | 4 | 4 |
| asks | 5 | 5 |
| fit | 4 | 5 |
| handoff | 4 | 4 |
| scope | 4 | 3 |
| clarity (per side) | 4 | 4 |

## Defects

**X**
- `ready-notification`: "1 shot needs a retry" opens `ready`, but Regenerate lives on `storyboard`; the user lands on a half-finished clip page and has to find their way back. "Leave and get notified" is also modeled as a user action into a notification screen, which is not a real transition.
- `storyboard`: no way to cancel a paid run once approved, and no whole-run failure state (service down) - only the per-shot error is designed.
- `storyboard` / `ready`: assembly is described twice. The system transition says "All shots done and assembled", yet `ready.loading` is "Clip is being assembled". An engineer cannot tell which screen owns assembly.
- `plan`: length/aspect/style are shown as chips but cannot be changed here; the user must go Edit brief -> Change -> Done -> Create plan again. The `options` sheet also promises a "price effect" before any plan exists, while the brief says price is computed from the plan.
- `plan`: no state for payment or insufficient balance before the paid step.

**Y**
- `plan` -> `scene-edit`: "Change length, aspect or style" reuses the single-scene sheet for global defaults; a sheet named and scoped for one scene now rewrites the whole plan. Lyrics are also editable both "inline" and via the sheet - two paths, one undefined.
- `notify`: Open always lands on `storyboard`, even for "Your clip is ready", adding a hop before the `ready` done screen.
- Scope: `credits-sheet` with purchase options, plan versions with compare/restore, clip v1/v2, Credits and Settings in nav, and a three-step stepper were not requested.
- `ready.partial`: "Retry scene (extra cost shown)" conflicts with the plan's "credit is not charged for scenes not produced" and the brief's single per-clip price.
- `storyboard`: "lyrics remain editable for scenes not yet rendered" has no action or state explaining how, or what happens to an already-rendered shot's audio.

## Winner

**P1: Y. Overall: Y.** Both put the single approval before the paid step, show price at that gate, drop model and seed, and keep a failed shot from sinking the clip. Y goes further on what matters for a slow, paid pipeline: defaults are changed on the plan where the user can actually judge them, the gate shows price and time together, cancel mid-run states what is kept and refunded, a failed scene can be retried or skipped, and whole-run and no-credit failures each have a way out. X is tighter in scope and cleaner to read, but its notification misroute and the missing cancel leave real gaps after the user has committed money. Y wins despite clear scope creep (credits purchase, versioning) that should be trimmed.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 5, "handoff": 4, "scope": 3}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
