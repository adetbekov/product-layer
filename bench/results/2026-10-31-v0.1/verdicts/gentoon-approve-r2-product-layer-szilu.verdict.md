## Scores (P1)

| criterion | X | Y |
|---|---|---|
| success | 4 | 5 |
| flow | 4 | 4 |
| states | 4 | 5 |
| ia | 4 | 4 |
| asks | 5 | 5 |
| fit | 4 | 5 |
| handoff | 4 | 4 |
| scope | 4 | 3 |
| **clarity (per side)** | 5 | 4 |

## Defects

**X**
- `confirm-cancel`: "Stop generation" lands on `brief`, throwing away the approved plan. A user who cancels usually wants to adjust the plan, not retype the brief.
- `ready`: "Regenerate one shot" has no cost statement and no note on re-assembly; the brief says clips are priced before generation, so a paid re-render with no price shown breaks the gate the rest of the spec protects.
- `brief`: "link to past clips" points to nothing; there is no nav or clips screen.
- `storyboard` vs reply: the message says a failed shot is "regenerated on its own", the spec requires a user tap ("Regenerate this shot"). An engineer cannot tell which is intended.
- `ready`: no error state for a failed download; only assembly failure is covered.

**Y**
- `plan`: per-scene "Rewrite" appears in the loading/partial states but is not an action; "compare/restore earlier versions" has no screen; "language" is shown in the summary but is never set or derived anywhere.
- `storyboard`: "Assemble without failed scenes" transitions back to `storyboard` rather than to an assembly/ready path; keeping lyrics editable mid-render puts a paid edit on the progress page, where it was not asked for.
- `plan-settings`: only "Done", no way to dismiss without applying.
- `ready`: "New clip from this brief" and "New clip" both go to `brief` with no stated difference.
- Reply and notes leak internal codes (SR-1, AP-4, FL-8) that mean nothing to the reader.
- Scope: nav, voice input, plan versioning, stage stepper, assemble-without-failed are all unrequested additions.

## Winner

**P1: Y.** Both put the single approval before any paid work, strip the brief to one field, and show per-scene status with per-shot retry. Y goes further on the points the brief stresses: cancel returns to the plan instead of discarding it, price and time sit on the approve action and recompute while edits are pending, every paid re-do (redo scene, length change rewriting scenes) names its cost before it runs, and leaving mid-job has a modelled return path through the notification. X is tighter and cleaner to read but leaves the post-approval cost gaps (regenerate from ready, cancel destination) that matter most in a pay-per-clip product.

**Overall: Y**, narrowly. X wins on scope discipline and a plainer message; Y wins on state coverage and cost transparency after the gate, which the request weights more heavily. Y's extra features would need trimming before build, but its core is more buildable without guessing about money.

```json
{"X": {"P1": {"success": 4, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 5}, "Y": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 5, "handoff": 4, "scope": 3}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
