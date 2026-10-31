## Scores

| P1 | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|
| X | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 5 | 4 |
| Y | 5 | 4 | 4 | 5 | 5 | 5 | 4 | 4 | 4 |

Both sides land the same core move: digest row at the top of Settings, a three-option sheet, save on pick, Undo toast. 8 steps become 3, no email re-entry, no "Save all changes?". The differences are in the edges.

## X: main defects

- `digest-saved`: Undo goes `to: digest`, i.e. reopens the sheet and makes the user pick again. An undo should revert by system and confirm; as specced it is a second edit, not an undo.
- `export-status`: building and ready are folded into `shows` on one screen with no `by: system` transition. An engineer has to guess how the page moves from building to ready and whether it should poll. The error exit "Request again" goes back to `export`, so recovery costs an extra tap.
- `export`: the `empty` state is "no earlier export", which is not an empty state; the real one (user has no notes) is missing. No expired-download handling.
- `digest`: no `asks` entry even though the format expects one and the sheet does ask the user something (the frequency).
- No `nav` block; the entry from the avatar menu lives only as an assumption in notes.md.
- `delete`: no re-authentication. Two explicit steps and separation from Save make it acceptable, but anyone holding the session can delete the account; the designer flags this as an assumption rather than a decision.
- On the plus side, X is the only one to design the "Undo failed" case and a loading state on the export request.

## Y: main defects

- `digest-saved`: same Undo flaw, `to: digest` instead of a system revert. Its error state is "Not applicable", but undo is a network write and can fail.
- `digest-saved`: "Auto-dismiss after 8 seconds or Close" is one action marked `by: system`, though Close is a user tap.
- `export`: no loading state for the request in flight (X has one). `password`: no loading state.
- `delete`: a `loading` state and a "wrong password" error on the page, but the only forward action is `to: delete-confirm`. It is unclear whether the password is verified on the page or sent with the final delete; the engineer must guess the sequence.
- `profile`: `asks` lumps "name, email, time zone" into one field entry; the format wants one per field. Purpose says "name, email and avatar" while the shows list adds time zone.
- Small scope drift: "ZIP of Markdown files", "Sent at 8:00", contact-support links, Forgot-password links. Sensible defaults, but none were asked for. "Plain text style" and "danger-styled" edge into visual territory.
- Strengths: explicit `nav` block, sheet surface defined per platform, export split into `export-building` -> `export-ready` with a `by: system` hand-off, expired-link state, a real no-notes empty state, Save disabled with a stated reason on `profile`, and the final modal names the account address.

## Winner

**P1: Y. Overall: Y.** Both specs solve the 8-tap problem identically and both share the Undo-reopens-the-sheet mistake, so the call rests on the rest of the brief. Y handles the asynchronous export more honestly (a system transition when the file is ready, expiry, no-notes empty state), makes deletion materially safer with password plus a named-account confirmation, and states the navigation change instead of assuming it. X is tighter in scope and covers a couple of states Y skipped (undo failure, export request pending), but its export-status screen and missing nav leave more for an engineer to guess.

```json
{"X": {"P1": {"success": 4, "flow": 4, "states": 4, "ia": 4, "asks": 4, "fit": 4, "handoff": 4, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 5, "asks": 5, "fit": 5, "handoff": 4, "scope": 4}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
