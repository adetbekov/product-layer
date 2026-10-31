# Blind review: settings redesign (P1)

| Side | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|
| X | 5 | 4 | 5 | 4 | 4 | 4 | 4 | 4 | 4 |
| Y | 5 | 4 | 4 | 5 | 5 | 4 | 4 | 3 | 4 |

## Defects

**X**
- `profile`: shows "Change email" as a guarded step but no screen or action targets it; the engineer has to invent the email-change flow.
- `export`: adds a format choice (Markdown zip default) that nobody asked for; it is defaulted, so no extra tap, but it is unrequested surface.
- `export-building`: error offers "contact support" with no target or definition.
- `digest-saved`: Undo goes back to the `digest` sheet instead of reverting the value directly, so undo costs two taps (reopen, re-pick); ambiguous whether the revert happens on tap.
- `account-deleted`: `actions: []` with the sign-up link only in `shows`; acceptable after sign-out, but the exit should be an action.

**Y**
- `settings`: action "Back to notes (nav)" points `to: settings`, a self-loop; the nav exit to Notes is unreachable in the spec.
- `export`: "Export my notes" goes `to: export-ready, by: user`, but the file takes minutes; the ready notification should be a `by: system` transition after the build. As written an engineer would read it as a synchronous download.
- `digest`: `loading: "Not shown"` ignores the save-in-flight moment; the pick must round-trip before the toast, and there is no state for that or for disabling the other options meanwhile.
- `delete-done` / `delete`: a 14-day grace period and "Restore account" is a new retention policy, flagged as an assumption but out of scope for a settings redesign and it changes what "Delete" means for the backend.
- `delete`: "primary-looking rank 1 action" leans into visual styling; `profile` and `password` have no loading state for Save.
- `notes.md` cites "SR-1, IA-3/IA-6, FL-8, ST-8" without explaining them.

## Winner

**P1: X.** Both land the digest at 3 taps with save-on-pick, undo instead of a confirm dialog, no email re-entry, and delete moved to an isolated, plain-styled row at the bottom with typed-email confirmation. Y has the cleaner home (ranked rows, export as a sheet, "Keep my account" as the default exit) and asks less, but it carries two spec errors an engineer would trip on (the `settings` self-loop and the export transition that pretends the build is instant), skips the digest save-in-flight state, and spends scope on a grace-period policy that was not requested. X covers loading and error on every screen where they can happen, including a dedicated building state for export and a locked form while deleting, which is exactly what the brief asked to be judged. The gap is narrow; X wins on completeness of states and on staying inside the request.

**Overall: X**, for the same reasons; one step only.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 4, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 5, "asks": 5, "fit": 4, "handoff": 4, "scope": 3}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
