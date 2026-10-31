# Blind review: settings redesign (X vs Y)

## Scores (P1)

| Criterion | X | Y |
|---|---|---|
| success | 5 | 5 |
| flow | 4 | 4 |
| states | 5 | 4 |
| ia | 5 | 4 |
| asks | 4 | 5 |
| fit | 4 | 4 |
| handoff | 4 | 3 |
| scope | 4 | 5 |
| **P1 total** | **35** | **34** |
| clarity (per side) | 3 | 4 |

Both cut the digest path from 8 to the same real path (Settings, digest row, pick, save-on-pick with Undo), drop the profile form and the email re-entry, move delete to the bottom as a link, and make export asynchronous with leave-and-notify. The differences are in rigor and in the delete confirmation.

## Defects

**X**
- `digest`: error state says "primary recovery is Retry" but no Retry action exists in `actions`; an engineer has to invent the transition.
- `export`: carries a `loading: Building...` state that duplicates the `export-building` screen; two places describe the same wait.
- `digest-saved`: Undo goes back to the sheet instead of reverting directly; an undo should cost one tap, not reopen a choice.
- `delete`: confirmation is "type your email" -- known data, so it proves intent but not identity; anyone at an unlocked device can delete.
- `landing`: stub outside the brief whose only action (Sign in) loops to itself; declared as a placeholder, but still a screen that should not be in this spec.

**Y**
- `account-deleted`: "Back to start" transitions to `account-deleted` itself while `shows` promises a link to sign-up -- a dead end.
- `export-start`: error text offers "Try again and Back" but no Try again action is listed.
- `profile`: `asks` omits time zone although the screen edits it; `shows` are shorthand lists (`[Avatar, name, email, ...]`) with no priority, and most actions lack `by:`.
- `settings-home`: error state only covers the digest subtitle; what the other rows show on a failed load is unspecified.
- `digest-saved`: same Undo-reopens-sheet issue as X.
- Reply opens with runtime noise ("No CLAUDE.md or skills existed").

## Winners

**P1: X.** X is the more complete build document: ranked `shows` on every screen, a success state on the settings home, an empty state for export, an error path for the optimistic toast, rows named as verbs (Export my notes, Change password), and a notes file with a steps-to-value table and explicit assumptions (send time, missing grace period, link expiry). Y is leaner and sharper in places -- saving disables the other options, Cancel is the default on delete, password confirmation is a stronger guard than retyping a visible email -- but it ships an undeclared self-loop on `account-deleted`, thinner screen descriptions, and a one-line notes file.

**Overall: X**, by a narrow margin. Y wins asks and clarity (its reply reads more plainly; X's rule codes like "SR-1, FL-8" mean nothing to a reader), and Y's delete is marginally safer. X wins on states, IA and handoff, which weigh more for a spec that a visual designer and engineer must build from without the author in the room.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 5, "asks": 4, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 3}, "Y": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 3, "scope": 5}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
