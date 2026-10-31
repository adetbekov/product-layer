# Blind review: Notes app settings redesign (P1)

## Scores

| Criterion | X | Y |
|---|---|---|
| success | 5 | 4 |
| flow | 4 | 3 |
| states | 5 | 4 |
| ia | 4 | 4 |
| asks | 5 | 3 |
| fit | 4 | 4 |
| handoff | 4 | 3 |
| scope | 4 | 4 |
| clarity | 4 | 4 |

## Defects

**X**
- `export-building`: the `empty` state ("account has no notes, button disabled") describes the `export` request page, not the building page. An engineer would wire it to the wrong screen.
- `delete-done`: `Close -> settings, by: system` contradicts the screen itself (user is signed out). The notes patch it in prose, but the yaml says something else; the end state after scheduling deletion should be sign-out, not Settings.
- `digest`: "Change time zone -> profile" from inside a sheet dismisses the sheet mid-task; acceptable, but the return path to the digest is not stated.
- Build failure is only visible on `export-building`; if the user left (which the screen invites), no failure notification is specified, only success.

**Y**
- `settings`: action "Back to notes (nav) -> settings" is a self-loop pointing at the wrong target.
- `digest-saved`: `Undo -> digest` reopens the picker instead of reverting the value; an undo that needs a second pick is not an undo, and it is ambiguous for the engineer whether the revert happens.
- `export`: "Export my notes -> export-ready, by: user" models a tap as landing on a screen that only appears minutes later; the building state is folded into the sheet's `loading`, so a build failure after the user closes the sheet has no surface.
- `delete`: confirmation by typing the account email re-asks data the app already has, the very pattern the brief complains about, and it proves intent but not ownership (anyone at an unlocked device can copy the shown email). X's password check is both safer and not a re-ask.
- `delete-done`: the only action is "Restore account"; a user who really wants to leave has no exit, and sign-out is unspecified.
- Notes cite internal codes (SR-1, FL-8, "no product-type module fits") that mean nothing to the reader.

## Winner

**P1: X. Overall: X.** Both land the same 3-step digest path (Settings, digest row, pick, autosave with toast) and both move delete to the bottom under its own heading with a Keep/Delete pair, Export-first link and 14-day grace. X is more complete and more consistent: a save-in-progress state on the radio, an explicit `export-building` screen with its own error and a system transition to `export-ready`, a password gate on deletion that asks only what the user alone knows, and every action target resolving sensibly. Y has nice touches (rank hierarchy, Undo on the toast, "Weekly, Mondays 9:00" summary), but the self-looping nav action, the Undo that reopens the sheet, the user-tap-to-export-ready shortcut, the dead-end `delete-done` and the email re-entry on delete cost it on flow, asks and handoff.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 4, "flow": 3, "states": 4, "ia": 4, "asks": 3, "fit": 4, "handoff": 3, "scope": 4}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
