# Blind review: generic-settings-r1 (X vs Y)

## Scores

| Criterion | X | Y |
|---|---|---|
| P1 success | 5 | 5 |
| P1 flow | 4 | 4 |
| P1 states | 4 | 5 |
| P1 ia | 4 | 4 |
| P1 asks | 4 | 5 |
| P1 fit | 4 | 4 |
| P1 handoff | 3 | 4 |
| P1 scope | 4 | 4 |
| clarity | 4 | 4 |

Both hit every explicit ask: flow `digest` with entry/done, all four moments tagged, nav defined, digest cut from 8 user steps to 3 (Settings, Digest row, pick) with no Save button, no "Save all changes?" dialog, no email re-entry. Both move delete away from any save control and add a 14-day grace period.

## Defects

**X**
- `export`: the user action "Export my notes" goes straight `to: export-ready`, yet the file takes minutes and arrives by notice/email. The wait exists only as a `loading` string; there is no system transition, so an engineer has to guess how the sheet becomes the ready notice.
- `settings`: action "Back to notes (nav)" has `to: settings`, a self-loop. Should target Notes.
- `digest-saved`: Undo goes back `to: digest` (reopens the sheet) instead of reverting the value directly; one extra step on the one path the toast exists for.
- `delete`: confirmation is typing the account email. The app shows that email on the Profile row one screen up, so this proves intent but not ownership; the `asks` criterion prefers something only the user knows (password).
- `delete-done`: "Restore account" returns to settings with no mention of the signed-out state or any out-of-band cancel path.
- Minor: "primary-looking", "link-style", "not styled as the main action" lean toward visual language where hierarchy words would do.

**Y**
- `delete-done`: action "Close -> settings, by: system" contradicts the screen (user is signed out). notes.md admits the hack; the spec should model the end state honestly.
- `export-building`: the `empty` state describes behaviour of the `export` page ("button is disabled before the request"); it sits on the wrong screen.
- `digest-saved`: no Undo. Re-picking is one tap away, so it is tolerable, but X's toast-plus-Undo is the better grain for save-on-pick.
- `delete-confirm`: "same size and weight", "far from other buttons" are layout/visual calls; the hierarchy intent (equal weight, Keep is the safe exit) could be stated without them.
- Small scope creep: "Contact support" link, confirmation link on email change (reasonable, but unrequested).

## Winners

**P1: Y.** Both get the headline right, so the difference is rigor. Y models the export as request -> building -> ready with a `by: system` edge, designs loading for the digest pick and the profile, handles sign-out failure after deletion, and confirms deletion with the password rather than an email the app has already displayed. X's spec has two structural slips (the export tap jumping to the ready notice, the settings self-loop) that an engineer would have to resolve by guessing, though X's Undo toast and "Keep my account" as the default exit are genuinely better choices worth borrowing.

**Overall: Y**, for the same reasons; the gap is modest and lives in handoff consistency and deletion safety, not in the core redesign.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 4, "fit": 4, "handoff": 3, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
