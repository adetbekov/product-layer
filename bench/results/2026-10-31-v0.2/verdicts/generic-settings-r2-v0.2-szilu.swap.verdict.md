## Scores

| P1 | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|
| X | 3 | 4 | 3 | 4 | 5 | 4 | 4 | 5 | 4 |
| Y | 5 | 4 | 4 | 5 | 5 | 4 | 4 | 4 | 4 |

## Defects

**X**
- `settings`: the home has only digest, export and delete. Name, email, time zone and password change (5% of visits per the brief) have no entry point at all. The brief asked to redesign the settings; X removed the old path and left nothing in its place, so the redesign hides something people need. Deferring it to notes.md does not make the spec buildable.
- `export`: "Request export" is tagged `by: system`, but it is a user tap. An engineer reading the fixed format would conclude the export starts without the user and the user is never charged a step. The request, the building wait and the failure are also folded into one screen while `export-ready` is a second screen, so the model is inconsistent.
- `digest-saved`: a separate sheet that requires a "Done" tap. Save-on-pick then a mandatory dismissal is a softer version of the confirm dialog the brief wanted gone; the true path is avatar, Settings, row, pick, Done.
- `settings`: no loading or error state although it displays the current digest value, which must be fetched.
- `export`: the user "may leave", but nothing tells them when the file is ready; they must come back and check.

**Y**
- `digest-saved`: "Undo" transitions to the `digest` sheet instead of reverting the value by system. As written, Undo makes the user re-pick, which is not an undo.
- `export-building` and `export-ready`: the error states name "Try again", "Contact support" and "Request a new export", but none of these appear in `actions`, so the way out of each error is described in prose only.
- `export`: if the user leaves during the build and returns, the page covers "no earlier export" and "earlier export available" but not "build in progress", so the return path is a guess.
- `digest`: "Sent at 8:00 ... on Mondays" and the 7-day link expiry invent product behaviour the brief did not give.
- Several visual hints ("plain text style, not a button", "destructive-styled", "small spinner", "indeterminate progress") drift past where this spec should stop.

## Winner

**P1: Y. Overall: Y.** Both specs land the core move (digest first on the home, sheet that saves on pick, email and time zone shown rather than re-asked, delete pulled away from any save control with a typed email and an export offer). Y goes one step further on the headline metric, 3 taps with a self-dismissing toast versus X's 4 plus a Done tap, and it keeps the account and password path reachable instead of dropping it, which is the "without hiding things people need" half of the test. Y also designs loading and error on the settings home and tells the user when the export is ready. X is cleaner on scope and asks, but the mislabelled `by: system` export action and the missing account section are the more serious handoff problems.

```json
{"X": {"P1": {"success": 3, "flow": 4, "states": 3, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 5, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
