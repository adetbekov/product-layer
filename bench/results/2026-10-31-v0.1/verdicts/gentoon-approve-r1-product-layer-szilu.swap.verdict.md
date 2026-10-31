## Scores (P1)

| | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|
| X | 5 | 4 | 4 | 4 | 5 | 4 | 4 | 5 | 5 |
| Y | 5 | 4 | 5 | 4 | 5 | 5 | 5 | 3 | 4 |

## Defects

**X**
- `brief`: action "My clips" points to `brief` itself; the nav names "My clips" but no clips screen exists, so the only path to past clips is a self-loop.
- `brief` / `plan`: the brief's loading state says the user is already moved to `plan`, yet the brief's error state describes the draft failing "with the idea kept in the field" on the brief. Two screens claim the same failure; an engineer must guess which one shows it.
- `storyboard`: "Cancel generation" returns to `plan` with no confirmation and no word on what happens to the price that was charged at approval or to finished shots. For a paid, minutes-long job this is the one place a confirm and a refund rule are needed.
- `storyboard`: "Leave and notify me" is modelled as a user action leading to a notification surface. Leaving should cost nothing; a user-pressed transition to a push message is an odd target.
- `options`: no loading state while the price recomputes; "Done (opened from plan)" is a workaround for a sheet with two callers rather than a stated return-to-caller rule.

**Y**
- `notify`: "Open" always lands on `storyboard`, including for "Your clip is ready"; the user gets an extra hop (or relies on an implicit redirect) to reach `ready`.
- `plan`: scene cards are described as "editable inline" while the only edit action opens the `scene-edit` sheet; and "Change length, aspect or style" also routes to `scene-edit`, so one sheet does two unrelated jobs. The IA of editing is muddier than it needs to be.
- Scope: a credits economy (`credits-sheet`, Credits and Settings in nav), plan versions with compare/restore, clip versions v1/v2, "make a variation", and lyrics editable during rendering were not requested. The payment case is defensible; the versioning and variation features are not.
- `plan`: "lyrics editable while frames render" quietly reopens the approved plan after the approval gate; what a lyric change does to an already-priced, running job is not stated.

## Winner

**P1: Y. Overall: Y.** Both place a single approval on the plan with the price beside the button, ask only for the idea, show per-scene status and let the user fix or skip a failed shot, so the core judgement is a tie. Y is stronger where it matters for a paid, slow pipeline: a confirmed cancel that states what is kept and refunded, insufficient-credit and whole-run-down states with a way out, pending-at-once button copy, range estimates, and explicit priority ranks that an engineer can build from. X is tighter in scope and its reply reads more naturally, but its dangling "My clips", silent cancel on a charged job, and duplicated draft-failure handling are real build-time gaps; Y's faults are mostly extra features, which are easier to cut than to invent.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 5}, "clarity": 5}, "Y": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 5, "handoff": 5, "scope": 3}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
