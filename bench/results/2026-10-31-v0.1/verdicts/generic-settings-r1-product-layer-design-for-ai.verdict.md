# Blind review: generic-settings-r1 (P1)

| Criterion | X | Y |
|---|---|---|
| success | 4 | 5 |
| flow | 4 | 4 |
| states | 4 | 4 |
| ia | 3 | 5 |
| asks | 5 | 5 |
| fit | 4 | 4 |
| handoff | 3 | 4 |
| scope | 4 | 4 |
| clarity | 4 | 4 |

Both sides land on the same core: a flat settings home with the digest row first, a sheet that saves on pick with a toast and Undo, no Save button, no "Save all changes?" dialog, no email re-entry, and a deletion page that is physically separated, requires typing the email, and has a 14-day grace period. The digest flow is 2 taps from settings in both. The differences are in completeness and modeling.

## X defects

- `settings`: shows a "Profile" row, and `digest` shows a "Change in Profile" link, but there is no `profile` screen and no action pointing anywhere. An engineer has to invent the destination.
- `settings`: the password change (5% of settings visits per the brief) is removed from the spec entirely. `notes.md` even lists "5% password" in the ordering, but `flow.yaml` has no row. "Redesign the settings" does not mean drop a settings function; this hides something people need.
- `delete`: no in-flight state while the deletion request runs (buttons stay live until the error or `deleted` appears).
- `deleted`: the user is signed out, yet the only action goes to `settings`; the restore path from a signed-out state is not actually designed.
- `export-building` -> `export-ready` is `by: system`, but when the user has left, nothing on `settings` carries the export status that "show it here" promises.
- Strengths worth noting: the save spinner on the tapped option, the explicit `export-building` screen, and the empty/expired/failed export states are the best-specified async handling of the two.

## Y defects

- `settings`: the action "Back to notes (nav)" points to `settings` itself, a self-loop; it should leave to Notes.
- `digest`: `loading` is declared "not shown", but the save-in-flight moment between pick and toast is undefined even though a save failure is designed.
- `export`: the transition "Export my notes -> export-ready" is tagged `by: user`; the ready state is reached by the system when the build finishes. The building state lives only inside a `loading` note on a sheet, so the handoff for the background job is thinner than X's.
- `delete-done`: does not say whether the user is signed out or that a confirmation/cancel email is sent; "Restore account" to `settings` is underspecified.
- "rank 1/2/3" and "notice.error" are an undefined vocabulary; readable, but the builder must infer what they map to.

## Winner

**P1: Y. Overall: Y.** The digest flow, the removed asks, and the deletion safety are equivalent. Y's settings home is complete: profile and password have real destinations, the profile form only re-asks the email when it is edited, and page/sheet/notification surfaces are assigned consistently, so a designer and engineer can build the whole settings area without guessing. X models the async export more carefully, but it leaves dangling references (Profile with no screen) and silently drops password change, which fails the "remove steps without hiding things people need" test.

```json
{"X": {"P1": {"success": 4, "flow": 4, "states": 4, "ia": 3, "asks": 5, "fit": 4, "handoff": 3, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 5, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
