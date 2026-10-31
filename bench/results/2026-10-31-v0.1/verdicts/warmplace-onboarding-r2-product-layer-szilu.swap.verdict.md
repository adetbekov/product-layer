## Scores (P1)

| | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|
| X | 5 | 3 | 4 | 4 | 4 | 3 | 4 | 5 | 4 |
| Y | 5 | 4 | 5 | 4 | 5 | 4 | 4 | 3 | 4 |

## Defects

**X**
- `tutor-home` "Open room" goes straight to `lesson-room`, skipping `device-check`. The brief's core complaint ("I can't hear you") is fixed for students only; half the room never gets checked. `lesson-room` also has no action back to a device check.
- `student-who-for` is a forced screen for every student and asks the first name even after Google supplied it. "For me" should be the default with "for my child" as a secondary choice, folded into an existing step.
- Sign-in comes before the student sees any slots (`invite-landing` -> auth -> `pick-slot`). The invited student commits an account before seeing whether a time fits.
- `pick-slot` "Message tutor instead" lands on `student-home`, not on a message thread; `slot-confirmed` adds a full page before home before device check, so the Google path is six taps.
- Editing availability from `tutor-home` routes through `profile-preview` and `profile-live` again, so a slot change requires re-publishing.

**Y**
- `device-check` "Done (lesson not started yet)" exits to `student-home` even when reached from `tutor-home` "Start lesson"; the tutor is dropped on the wrong dashboard. `lesson-ended` has per-role exits, so this is an omission, not a pattern.
- `invite-landing` "Notify me when times open" leads to `sign-in-sheet`, whose actions all go to `booking-confirmed` although nothing was booked; the "then home" path described in the empty state is not wired.
- `student-home` empty copy "Ask your tutor for a link" is wrong for the main case: the student already came from a tutor and simply has no slot yet. The "book action" in shows has no target.
- `profile-setup` publishes a default weekly availability template "accepted untouched". Availability is the one thing only the tutor knows; a prefilled template that becomes bookable slots can sell hours the tutor is not free for. Editable and previewed, but a risky default.
- Payments is dropped from the student nav into Settings; students are the paying side, and `lesson-ended` surfaces payment status, so "where do I pay" has no section.
- Unrequested screens: `lesson-ended` summary, returning-user `sign-in`, `settings` with role switching; reply claims 16 screens, spec has 17; notes cite opaque codes (RL-1, ON-9) an engineer cannot resolve.

## Winner

**P1: Y. Overall: Y.** Y gets each role to its outcome faster and in the right order: the student sees the tutor and picks a time before any account exists, the child question is opt-in, name and email are only asked on the email path, and the tutor is bookable in three taps. Both roles pass the device check and the room has a one-tap route back to it, with partial-failure and no-device states that keep joining possible, which answers the brief's named pain directly. X is tidier in scope and wiring and its tutor flow ends on an honest "profile live with invite link" screen, but it sends tutors into the room unchecked, forces an extra question on every student, and asks for sign-in before showing a single slot. Y's defects are mis-wired exits and scope creep, fixable in a pass; X's are structural.

```json
{"X": {"P1": {"success": 5, "flow": 3, "states": 4, "ia": 4, "asks": 4, "fit": 3, "handoff": 4, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 3}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
