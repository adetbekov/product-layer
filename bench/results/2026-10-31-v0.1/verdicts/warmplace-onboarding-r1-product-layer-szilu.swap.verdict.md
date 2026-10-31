## Scores (P1)

| | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|
| X | 5 | 5 | 5 | 4 | 5 | 5 | 5 | 4 | 5 |
| Y | 5 | 3 | 4 | 4 | 4 | 4 | 3 | 5 | 4 |

## Defects

**X**
- `lesson-lobby` "Back" and `lesson-room` "Leave lesson" both go to `student-home`, yet `tutor-home` "Start lesson" enters the same lobby. A tutor leaving a lesson lands on the student dashboard.
- `pay-lesson` is entered on every "Book lesson" and then skipped by a system action. The skip belongs on `confirm-booking`; as written the sheet flashes for tutors without prepayment.
- `check-email` "Change email" returns to `sign-in-sheet` (which shows "the chosen time") even when the link was for tutor sign-up.
- Tutor nav is 7 items; `Board` is a tool, not a task, and `Profile` plus `Settings` both sit top-level. `student-home` "See times" assumes the invite link is retained after sign-up (stated only as an assumption).

**Y**
- `tutor-home` "Open room" goes straight to `lesson-room`; `device-check` is reachable only from `student-home`. The tutor half of "I can't hear you" is unsolved, and `profile-live`'s "Test your camera and microphone" link has no action.
- `invite-landing` previews slots but cannot pick one; the student must sign in, fill `student-details`, then `pick-slot`: four user steps to a booking against X's three, and the name is asked before the user has committed to anything. `booking-confirmed`'s only action is "Go to my home"; the room is reachable only via the dashboard.
- `tutor-profile` requires a short bio, price and duration (no defaults) and adds "level" to subjects; more than a bookable profile needs.
- Dangling items in `shows` with no action: "I'm a parent booking for a child" on `invite-landing`, the slots link in `student-home` empty, the camera test on `profile-live`. An engineer guesses the targets. Student nav has no Payments although payment is "deferred until after the lesson".
- No empty state for a tutor with no slots until after sign-in (`pick-slot`); `welcome` "page failed to load" is filler; no loading on `booking-confirmed` or `pick-slot` submit.

## Winner

**P1: X. Overall: X.** X gets the student from invite to a confirmed booking in three taps by showing slots before any account and asking for the account only at commit; the device lobby sits in front of the room for both roles with permission asked at the moment of need and audio-only fallbacks; every screen carries ranked content, asks with reasons, and all three states. Y's nav labels for the tutor (Students, Library) are the better-named sections and its student nav is leaner, but the tutor never passes a device check, the student path adds a form page before the slot pick, and several shown links have no destination, so a builder would have to fill gaps that X already closed.

```json
{"X": {"P1": {"success": 5, "flow": 5, "states": 5, "ia": 4, "asks": 5, "fit": 5, "handoff": 5, "scope": 4}, "clarity": 5}, "Y": {"P1": {"success": 5, "flow": 3, "states": 4, "ia": 4, "asks": 4, "fit": 4, "handoff": 3, "scope": 5}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
