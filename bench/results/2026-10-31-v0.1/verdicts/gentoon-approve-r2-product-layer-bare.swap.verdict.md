# Blind review: gentoon-approve-r2 (X vs Y)

## Scores (P1)

| criterion | X | Y |
|---|---|---|
| success | 5 | 4 |
| flow | 4 | 4 |
| states | 4 | 5 |
| ia | 4 | 4 |
| asks | 5 | 4 |
| fit | 4 | 4 |
| handoff | 4 | 3 |
| scope | 4 | 3 |
| clarity (per side) | 5 | 3 |

## Defects

**X**
- `storyboard`: the error state offers "Edit scene" on a failed shot, but no action carries it anywhere; an engineer has to guess whether it opens `plan-edit` and what happens to shots already rendered.
- `storyboard`: assembly "waits until every shot is done" and there is no "assemble without this scene" or cancel. A shot that keeps failing stalls the clip indefinitely after the user has paid; the only exits are retry or leave.
- `storyboard`: no way to stop a running, paid generation after approval; the one irreversible costly step cannot be interrupted.
- `ready`: "Regenerate one scene" goes back to `storyboard` with no statement of whether it is charged, while the notes say only failure retries are free.
- `brief`: "honest time estimate" and the drafting state on `plan` are left for the engineer to define; minor.
- nav: `Account` appears with no screen and was not requested.

**Y**
- nav `Clips` is referenced by `brief` (loading), `clip-notice` (error), `ready` (error) and the notes, but no screen is specified. The fallback for a missed notification lands on an undefined page.
- `storyboard` -> "Leave" transitions to `clip-notice`, a notification. A notification is not a destination; the user actually lands somewhere (Clips) and that step is unbuildable as written.
- `storyboard`: "Lyrics stay editable" during rendering with per-scene cost moves paid decisions out of the single gate into the progress screen, which the spec itself argues against.
- `plan`: version badge with compare/restore, and `brief` voice input, are unrequested; "language" appears in the restated goal though the user never set it.
- Retry and "Redo scene" cost is left open ("is Redo scene paid?") while `ready` says "shows cost first"; the pricing rule for re-renders is contradictory within the spec.
- `plan-settings` has no `moment` tag, unlike every other create screen.

## Winners

**P1: X.** Both put the one approval on the plan with the price on the button and keep the brief to a single field. X is the tighter, buildable spec: price is visible from the brief at default length, the options sheet and scene edit are optional sheets, `my-clips` is defined so leaving never dangles, and the reply reads like a designer explaining choices. Y has the better recovery model (assemble without failed scenes, a cancel that says what is kept, partial and stale states) and would be the stronger storyboard if it were finished, but it leaves the `Clips` page undefined, routes "Leave" into a notification, and adds versions, voice input and mid-render lyric edits nobody asked for.

**Overall: X.** Fewer guesses for the builder and the storyboard failure path is the one real hole; Y's extra scope and missing Clips screen cost more than its richer states earn.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 5}, "Y": {"P1": {"success": 4, "flow": 4, "states": 5, "ia": 4, "asks": 4, "fit": 4, "handoff": 3, "scope": 3}, "clarity": 3}, "winner": {"P1": "X", "overall": "X"}}
```
