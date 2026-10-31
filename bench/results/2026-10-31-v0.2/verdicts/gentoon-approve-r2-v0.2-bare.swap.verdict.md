## Scores (P1)

| Criterion | X | Y |
|---|---|---|
| success | 5 | 5 |
| flow | 4 | 3 |
| states | 5 | 4 |
| ia | 4 | 3 |
| asks | 5 | 5 |
| fit | 5 | 4 |
| handoff | 4 | 3 |
| scope | 4 | 4 |
| clarity (per side) | 4 | 3 |

## Defects

**X**
- `storyboard`: "Try again" and "Remove scene" exist only inside the `partial` state text, not in `actions`. An engineer has to infer them; they are the most important per-shot controls in the flow.
- `storyboard`: a failed scene stalls assembly until the user acts ("assembling starts when every scene is ready or removed"). Reasonable, but the spec should say whether the system retries once on its own before asking the user.
- `ready`: the only exit is New clip. A clip with one weak scene cannot be fixed without starting over; a redo path (with its price) would close the loop.
- `plan`: shows "what is kept if the user cancels later" on the approval page, which is noise at the moment of commitment; the error state covers only scene edits, not a failed initial draft (handled on `brief`, so acceptable but split).
- `notification` has no states; fine for a push, but not stated.

**Y**
- `storyboard`: no Cancel. Once approved, a multi-minute paid job has no way out; the user can only wait or close the tab.
- `storyboard`: a failed shot offers only "Regenerate this shot". If it keeps failing there is no "Remove scene" or any other exit, so the clip can never assemble: a loop with no way out, exactly what the brief asked to fix.
- `storyboard` -> `ready` "Leave and get notified, by: system" is mis-modelled: leaving is a user act, and it lands on `ready` before anything is ready. `ready` then carries an "Assembling the MP4" loading state, so one page serves as both the assembly wait and the finished clip. The storyboard stage line and the ready screen blur.
- `ready` "Redo a scene" starts new generation and re-assembly with no price shown and no approval, which breaks the single-gate rule the design itself states; the notes admit pricing is open.
- `brief`: no loading state for the roughly 20 s draft (the plan screen absorbs it, but the button's own pending state is unspecified). `plan` has two separate actions to the same `plan-edit` sheet; `Download MP4 -> ready` is a no-op transition.

## Winner

**P1: X. Overall: X.**

Both put the single approval exactly where the money is spent, replace the JSON with readable scenes and lyrics, and show the price before Start. X is tighter where it matters for an expensive, slow pipeline: cancel on the storyboard that says what is kept, a Remove scene exit for a shot that will not render, a real notification screen for the long wait, and per-edit partial rewrites with a price "updated" marker. Y's opt-in `plan-edit` sheet is a clean idea for control-seekers, but its storyboard has no cancel and no exit from a repeatedly failing shot, and its ready screen takes on assembly and an unpriced redo, so approvals no longer strictly precede costly work.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 5, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 3, "states": 4, "ia": 3, "asks": 5, "fit": 4, "handoff": 3, "scope": 4}, "clarity": 3}, "winner": {"P1": "X", "overall": "X"}}
```
