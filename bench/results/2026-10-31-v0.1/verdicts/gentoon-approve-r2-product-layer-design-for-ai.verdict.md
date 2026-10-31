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
| clarity (per side) | 4 | 3 |

## Defects

**X**
- `storyboard`: "Cancel generation" jumps straight to `brief` with no confirmation and no statement of what is kept or charged. On a paid, minutes-long job this is the one irreversible action and it is the least guarded; the approved plan is also thrown away.
- `plan`: "Not enough balance" is a `by: system` transition to `payment` with no trigger stated, while "Approve and generate" goes directly to `storyboard`. An engineer has to guess when the check runs and which action it hangs on.
- `brief`: length/aspect live under "Adjust" here and again as chips plus `plan-format` on the plan; two places for the same setting on a four-step flow.
- `ready`: "Regenerate a scene" after delivery has no cost stated; the notes only promise no re-pay for assembly retries. "Share link" is unrequested.

**Y**
- `plan-settings`: only a "Done" action; a user who opens the sheet and changes their mind has no Cancel, and Done rewrites scenes when length changed.
- `plan`: scope creep: version badge with compare/restore, scene delete and reorder, a "language" default the brief never mentions. Scene "Rewrite" appears in the loading state but is not an action.
- `brief`: "optional voice input" is unrequested.
- `storyboard`: lyrics stay editable during rendering, with per-scene re-render cost; unrequested and a source of confusion mid-job. "Leave" is modeled as a user action to a notification screen, which is not something the UI offers.
- No payment step anywhere although the brief prices every clip; "Approve and start" goes straight to generation. Honest "(assumption)" tags and the open "is Redo paid?" question partly compensate.
- `ready`: no assembly-failed state (only download-failed); X covers this.

## Winner

**P1: Y. Overall: Y.** Both put the single approval on the plan with price attached, keep the brief to one ask, and make failures per-shot. Y is better on the criteria this project turns on: cancel is confirmed and states what is kept and charged, stopping returns to the plan rather than the blank brief, a whole-run failure has a way out, redo shows its cost first, and the notification has a fallback. X is the more disciplined spec, with tighter scope and a real payment path, but its unguarded cancel to `brief` and the unanchored balance check are exactly the gaps that matter when generation is slow and paid. Y's scope creep (versions, voice, reorder, mid-render lyric edits) and its missing Cancel on the settings sheet keep the margin small.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 5, "handoff": 4, "scope": 3}, "clarity": 3}, "winner": {"P1": "Y", "overall": "Y"}}
```
