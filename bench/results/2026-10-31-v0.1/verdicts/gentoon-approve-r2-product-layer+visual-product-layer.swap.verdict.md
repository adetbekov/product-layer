# Blind review: gentoon-approve-r2 (X vs Y)

## Scores (P1)

| criterion | X | Y |
|---|---|---|
| success | 5 | 5 |
| flow | 4 | 4 |
| states | 5 | 4 |
| ia | 4 | 4 |
| asks | 5 | 4 |
| fit | 4 | 4 |
| handoff | 4 | 3 |
| scope | 4 | 3 |
| clarity (once) | 4 | 4 |

Both put the single approval gate on the plan, with system-computed price and time next to the approve action, per-scene badges with reason and own Retry on the storyboard, leave-and-notify, and a cancel modal that states what is kept. The difference is in consistency between what the screens show and what the actions actually define.

## Defects: X

- `plan`: `asks: []` although this is the approval of plan and price; the commitment should be modeled as the screen's ask. The loading state references a per-scene "Rewrite" that appears nowhere in shows or actions, so targeted AI revision exists only by implication (inline edit and whole-plan Regenerate are the defined paths).
- `storyboard`: "Lyrics stay editable" while shots render invites extra paid redo mid-run and was not asked for. The error state offers "Back to plan" but no such action is listed. "Leave" is `by: user` leading to a notification surface, which is really delivered by the system.
- `ready`: "New clip from this brief" and "New clip" both go to `brief` with no stated difference in what is prefilled.

## Defects: Y

- `create-brief` and `create-plan`: length, aspect and style each have a "Change" link, but no sheet or screen is defined as its destination; the reply says defaults are changed on the plan while the yaml puts the link on the brief too. An engineer has to invent this.
- `create-plan`: "Rewrite the plan with a note", "Regenerate plan" and "Top up credits" are named with no actions, no input location and no screen. The spec also invents "clip credits" and a credit shortfall path where the brief says the clip is priced per clip.
- `create-storyboard`: "Leave (we notify you)" is tagged `by: system` although the user leaves; "Retry all failed" and "Skip scene" live only in state text, not in actions, and `create-ready` has no partial state for a clip assembled with skipped scenes (X covers this).
- `create-cancel-confirm`: no loading or error state, though stopping can fail.
- Unrequested: Share link, Account nav item, audience in the summary, last-used prefill.

## Winner

P1: X. Overall: X. Both designs answer the brief's core asks the same way: one gate before the paid render, revise instead of only approve, per-shot failure isolated with its own retry, and a single creative input. X is more buildable: every control it names resolves to a defined screen or state (the settings sheet, assemble-without-failed, the partial ready state), and its ask is strictly the brief. Y has the nicer approval modeling and a stronger scene-edit sheet with "ask AI with a note", but leaves Change, Rewrite-with-note and Top-up as dangling labels and adds credits, sharing and account scope that nobody requested.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 4, "fit": 4, "handoff": 3, "scope": 3}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
