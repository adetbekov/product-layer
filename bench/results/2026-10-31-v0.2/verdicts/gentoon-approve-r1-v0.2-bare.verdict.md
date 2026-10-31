## Scores (P1)

| criterion | X | Y |
|---|---|---|
| success | 5 | 5 |
| flow | 4 | 5 |
| states | 4 | 4 |
| ia | 4 | 4 |
| asks | 5 | 5 |
| fit | 4 | 5 |
| handoff | 4 | 3 |
| scope | 3 | 4 |
| clarity | 4 | 4 |

## Defects

**X**
- `brief` -> "Change defaults" opens `plan-edit`, whose only exits (Save, Cancel) go to `plan`. No plan has been drafted yet, so the user lands on an empty plan screen with a price that cannot exist. Broken path on the entry screen.
- `ready` -> "Regenerate a scene" jumps straight to `storyboard`. Price is computed per clip before generation, yet this rework starts paid generation with no cost shown and no approval. Contradicts the project's own rule that approvals guard the expensive steps.
- `storyboard` error state promises "Replace scene" and "Skip scene" after repeated failures; neither exists as an action, and "Replace" implies new generation with unstated cost. `drafting` error mentions "Retry" with no action either.
- `download-done` sheet adds share/copy-link and a confirmation step nobody asked for; `nav` (My clips, Settings) was not requested. Scope drift.
- `ready` is the `done` screen but its loading state is "assembling the MP4", so the ready moment is entered before the clip is ready.

**Y**
- `plan` lists "regenerate the whole plan, or one scene" under shows, but actions are only Approve and Edit brief. Engineer has to invent the transition and the loading behaviour.
- `storyboard` "Retry for that scene alone" and `ready` "Download MP4 (primary action)" / "Retry for missing scene" are described but not wired as actions. The spec format exists to avoid exactly this guessing.
- No assembly-failure state anywhere: the stepper names assembly, `ready` only covers download failing.
- `storyboard` Cancel goes to `plan` with no confirmation after minutes of paid work; "finished shots are kept" softens it, but one tap still ends a job.
- `brief` says defaults have "a way to change each" without saying where (inline, sheet). "Last clips as starting points" and email notification are small unrequested additions.

## Winner

**P1: Y. Overall: Y.** Both ask for one thing (the idea), both put the single approval with price before generation, both show per-shot failure on its own tile with a scoped retry. Y is tighter where the brief hurts most: four screens, four user steps, in-place plan editing with delete/reorder, playable results as they arrive, and rework from `ready` routed back through `plan` so cost is seen again before spending. X has richer safeguards (stop-confirm modal, assembly error, Replace/Skip) and a clearer page/sheet/modal split, but a broken `brief -> plan-edit -> plan` path, an unpriced regenerate from `ready`, and unrequested nav and share features cost it more than Y's unwired secondary actions cost Y.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 3}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 5, "states": 4, "ia": 4, "asks": 5, "fit": 5, "handoff": 3, "scope": 4}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
