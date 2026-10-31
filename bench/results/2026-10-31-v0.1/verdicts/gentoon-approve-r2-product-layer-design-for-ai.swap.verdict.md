## Scores (P1)

| criterion | X | Y |
|---|---|---|
| success | 4 | 5 |
| flow | 5 | 4 |
| states | 5 | 4 |
| ia | 4 | 4 |
| asks | 5 | 4 |
| fit | 5 | 4 |
| handoff | 4 | 3 |
| scope | 3 | 4 |
| clarity (per side) | 4 | 3 |

## Defects

**X**
- `plan`: payment is never designed. The brief says clips are priced per clip, but "Approve and start" jumps straight to generation; what happens when the user has no balance is left to the engineer.
- `plan`: overloaded. Concept, scene cards with lyric lines, a second "full lyrics" editor, price, cancel policy text, and a version badge with compare/restore all sit on one page. The duplicate lyrics editor and plan versioning were not requested.
- `storyboard`: "Lyrics stay editable" during rendering adds a mid-generation edit path with cost consequences that is underspecified and out of scope.
- `plan-settings`: only a Done action; no Cancel, so a user who opened the sheet by mistake must apply something.
- `ready`: "New clip" and "New clip from this brief" both go to `brief` with no stated difference; "Redo a scene" cost is flagged as open in notes but presented as settled on the screen.

**Y**
- `brief`: shows an "Adjust" link for defaults but the only action is Draft plan; the link has no target (`plan-format` is reachable only from `plan`). It also asks length/aspect on the brief, which the plan screen already handles.
- `storyboard`: "Cancel generation" goes to `brief` with no confirmation, loses the approved plan, and never states what is kept or charged. For a paid, minutes-long job this is the one irreversible action and it is unguarded.
- `storyboard`: "will be told when the clip is ready" has no mechanism; there is no notification or return path, so an engineer must invent it.
- `plan`: "Not enough balance" is a `by: system` transition with no trigger named; readers must guess it fires on Approve. `plan-edit` edits one scene at a time, so whole-song lyric changes take a sheet per scene.
- `ready`: "Share link" is unrequested; "Regenerate a scene" after the clip is finished has no stated cost.

## Winner

**P1: X. Overall: X.** Both put the single approval gate at the plan with price on the button and keep the brief to one field, which is the core of the request. X is more complete on the expensive-step mechanics: cancel is confirmed with what is kept, leaving is a designed notification with a fallback, failed shots have retry plus "assemble without them", and every state has a way out. Y has the better payment handling and a cleaner plan page, but its unconfirmed cancel to `brief`, the dangling Adjust link, and the unspecified notification leave more for the engineer to guess. X loses points for unrequested plan versioning and a cluttered plan screen; Y's final message leaks tooling notes ("the ai-native skill says...") into what should read as a designer's summary.

```json
{"X": {"P1": {"success": 4, "flow": 5, "states": 5, "ia": 4, "asks": 5, "fit": 5, "handoff": 4, "scope": 3}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 4, "fit": 4, "handoff": 3, "scope": 4}, "clarity": 3}, "winner": {"P1": "X", "overall": "X"}}
```
