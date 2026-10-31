# Blind review: generic-settings-r1 (X vs Y)

## Scores

| Step | Side | success | flow | states | ia | asks | fit | handoff | scope |
|---|---|---|---|---|---|---|---|---|---|
| P1 | X | 5 | 4 | 4 | 5 | 4 | 4 | 4 | 5 |
| P1 | Y | 4 | 3 | 4 | 4 | 5 | 4 | 3 | 5 |

Clarity: X 4, Y 4.

## Defects

**X**
- `settings`: action "Back to notes (nav)" targets `settings` itself, a self-loop; the nav exit is not actually specified.
- `digest`: loading is "not shown", so the in-flight save has no state; a slow network leaves the user unsure whether the pick landed before the toast appears. No `asks` block even though the screen asks for the frequency.
- `digest-saved`: Undo transitions to `digest` (reopens the sheet) instead of reverting the value in place; an undo should cost zero taps.
- `export`: the user action goes straight to `export-ready` while the waiting is folded into the sheet's loading state; the async model works but the transition graph hides the "building" period an engineer must implement.
- `delete-done`: no mention of sign-out or a confirmation email; "Restore account" leads back to `settings` as if nothing happened.

**Y**
- `settings`: "Profile" row is shown but has no action and there is no profile screen anywhere, a dead end. Password change (5% of visits in the brief, and listed in Y's own notes ordering) is absent entirely, so a settings redesign has no path for it.
- `digest`: "Change in Profile" link points at a screen that does not exist.
- `export-building`: error offers "Try again" and "Contact support" with no action targets; the export screen also has no in-app surface for the ready state despite promising "we will show it here".
- `digest-saved`: auto-close after ~4 s is too short for an Undo to be reliably reachable.
- `delete`: no loading state while the deletion request runs; `deleted` has no states at all.

## Winner

**P1: X. Overall: X.**

Both specs collapse the digest change to a row plus a pick with autosave, drop the email re-entry and the global Save/confirm, make export asynchronous, and isolate deletion with typed-email confirmation and a grace period, so the core request is well answered on both sides. Y's digest sheet is the more carefully stated (explicit ask, saving spinner, specific copy) and its `deleted` screen (signed out, emailed cancel link) is the safer ending. But Y leaves a dead Profile row, two dangling links, unresolved error exits, and no password path, while X covers the whole settings surface (profile, password, delete loading) with every action resolved except one trivial nav self-loop. An engineer can build X without guessing; Y needs a follow-up round.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 5, "asks": 4, "fit": 4, "handoff": 4, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 4, "flow": 3, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 3, "scope": 5}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
