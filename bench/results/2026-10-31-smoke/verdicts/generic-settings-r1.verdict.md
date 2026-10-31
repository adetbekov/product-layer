## Scores

| Step | Criterion | X | Y |
|---|---|---|---|
| P1 | success | 5 | 4 |
| P1 | flow | 4 | 3 |
| P1 | states | 5 | 4 |
| P1 | ia | 5 | 4 |
| P1 | asks | 5 | 4 |
| P1 | fit | 4 | 3 |
| P1 | handoff | 4 | 3 |
| P1 | scope | 4 | 4 |
| — | clarity | 4 | 4 |

## Defects

**X**
- `digest-saved`: Undo routes back to the `digest` sheet instead of reverting in place. Undo should restore the previous value with one tap; reopening the sheet adds a step and a chance to pick wrong again.
- `deleted`: the only action is a `by: system` self-loop. The notes admit it is a placeholder; the spec should say "session ends, user lands on sign-up" rather than model a loop.
- `export-ready` is reachable only through the `by: system` transition from `export-building`. If the user left (which the page encourages), the spec names an email and an "in-app message" but defines no screen or entry point for that message, so the return path is a guess.
- `profile`: shows Email and Time zone as editable fields but `asks` lists only name; either the fields are read-only (say so) or email/time zone belong in `asks` with a reason.
- `delete-confirm` Cancel goes to `settings`, skipping the `delete` page the user came from; minor, but inconsistent with Back semantics elsewhere.

**Y**
- `settings-home`: rows "Password" and "Profile" have no actions and no target screens. Two of the five rows are dead ends; 5% of visits (password) have nowhere to go.
- `export-start`: "Export my notes" transitions to itself and readiness is a bullet under `shows`, not a `by: system` transition. There is no `export` done state, no way the engineer can tell what triggers the Download button, and no path back if the user closed the sheet other than "we'll email you the link".
- `delete-confirm`: "Delete my account" returns to `settings-home` of a deleted account. The grace period mentioned in `shows` is not designed anywhere (no state, no screen, no way to restore). Delete is also one tap from the home list straight into the confirm page; typed email keeps it safe, but there is no explanation screen before the input.
- `digest-sheet`: lists `frequency` under `asks` with "the product cannot guess" — correct, but the same spec says nothing about what the digest contains beyond "what is sent", so the line of copy is vague for handoff.
- `settings-home` error: banner says settings failed to load yet rows "stay tappable"; export and delete would open on unknown account state.

## Winners

**P1: X.** Both designers cut the digest path to settings -> row -> pick with autosave and Undo, stop re-asking email and time zone, and move delete into its own zone with typed confirmation. X is more complete: export is modelled as three screens with a real `by: system` ready transition, password and profile have screens, delete has an explain page before the typed confirmation, and every error has a named exit. Y's spec leaves two home rows pointing nowhere and models export readiness as prose rather than a transition, which an engineer cannot build from without guessing. Y's single-page delete and sheet-based export are reasonable choices, but the dead rows and placeholder deletion outcome cost it the flow and handoff scores.

**Overall: X.**

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 5, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 4, "flow": 3, "states": 4, "ia": 4, "asks": 4, "fit": 3, "handoff": 3, "scope": 4}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
