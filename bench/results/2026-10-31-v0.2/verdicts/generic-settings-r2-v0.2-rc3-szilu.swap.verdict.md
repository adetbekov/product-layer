# Blind review: settings redesign (P1)

| Criterion | X | Y |
|---|---|---|
| success | 4 | 5 |
| flow | 4 | 4 |
| states | 4 | 5 |
| ia | 4 | 4 |
| asks | 4 | 5 |
| fit | 3 | 4 |
| handoff | 4 | 4 |
| scope | 5 | 4 |
| clarity | 4 | 4 |

Both cut the digest path from 8 taps to 2 from the settings home, drop the email re-entry and the "Save all changes?" dialog, and isolate deletion behind a typed email with a path to export first. The differences are in precision.

## X — defects

- `digest`: the flow's `done` screen is the same screen where the pick happens, and the pick action loops to itself. The Undo toast exists only as a `shows` line with no transition, so an engineer must guess where Undo lives and what it returns to.
- `digest`: the time-zone line says digests follow "the time zone from the profile" while the reply says it comes from the device; `profile` lists time zone as an ask even though the app already knows it. Small, but it is the exact kind of re-asking the brief criticised.
- `export`: if the user leaves `export-progress`, there is no way back to a finished file except an assumed notification (flagged as an assumption in notes). No "earlier export available" state on `export`.
- `export-ready`: Download transitions to `settings`, which reads as navigating away on download.
- `account-deleted` carries no `delete` moment and gives no next step after deletion.
- A full page for a three-option radio is heavier than the platform needs on mobile web.

## Y — defects

- `digest-saved`: Undo transitions back to the `digest` sheet instead of reverting the value in place; the user gets the sheet reopened rather than an undo.
- `account`: a "Change password" row sits in `shows` while current/new password sit in `asks` on the same screen, with no target screen. Inline reveal or sub-page is left to guesswork.
- `export-ready`: error state offers "Request a new export" but no action carries that transition.
- `digest`: "Sent at 8:00", "Mondays", and "Almaty" are invented defaults presented as fact rather than flagged as assumptions.
- `delete-confirm` does not say the destructive button stays disabled until the typed email matches (X does).
- Light scope creep: Contact support, 7-day link expiry, confirmation email, sign-in link for a new account were not requested.

## Winner

**P1: Y. Overall: Y.** Y's spec is the more buildable of the two: the flow has an explicit done screen, the digest is a sheet with a named toast, export has an empty state and a recovery path for a previously built file, settings errors degrade per row, and only genuinely user-owned facts are asked. X is tighter in scope and safer on the delete button, but its self-looping digest screen, unspecified Undo, and device-versus-profile time-zone inconsistency would each cost a round of questions before engineering could start.

```json
{"X": {"P1": {"success": 4, "flow": 4, "states": 4, "ia": 4, "asks": 4, "fit": 3, "handoff": 4, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
