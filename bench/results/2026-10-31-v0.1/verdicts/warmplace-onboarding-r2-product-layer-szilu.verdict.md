## Scores (P1)

| Criterion | X | Y |
|---|---|---|
| success | 5 | 5 |
| flow | 4 | 3 |
| states | 5 | 4 |
| ia | 5 | 3 |
| asks | 5 | 3 |
| fit | 4 | 4 |
| handoff | 4 | 3 |
| scope | 4 | 4 |
| clarity (once) | 4 | 4 |

## Defects

**X**
- `sign-in-sheet`: the "Notify me when times open" path (from the empty invite landing) enters a sheet whose only exits are `booking-confirmed` / check-email; a student with no slot lands on a booking confirmation for a booking that does not exist. Needs a no-slot exit to `student-home`.
- `device-check`: shared by both roles (tutor arrives via `tutor-home` → Start lesson, and mid-lesson via "Audio and video settings") but its only non-join exit is `student-home`. Whether the mid-lesson entry is a modal over the room or a page replacing it is left to guess.
- `student-home`: shows "tutor's next free slots with a book action" but no action with a `to`; the only booking path in the spec is the invite link.
- `lesson-ended`, `settings`, `sign-in`: useful but beyond the request; the pair of "Go to my home (student/tutor)" actions is a workaround for role-specific exits from shared screens.

**Y**
- `invite-landing`: the student must create an account before seeing a single time slot; the value (tutor's times) sits behind sign-in. Google path is 6 user steps to the room vs X's 4.
- `student-who-for`: asks the name even on the Google path, and forces "for me / for my child" on every student instead of making the parent case a secondary choice.
- `slot-confirmed` → `student-home`: no reminder or system transition toward the room; Join only activates 10 minutes before, so the flow "invite link to being in the room" has an unaddressed gap where the student must remember to return.
- `tutor-home`: "Open room" goes straight to `lesson-room`, bypassing `device-check` — the tutor keeps the "I can't hear you" problem. `lesson-room` "Leave" sends both roles to `student-home`.
- `nav.tutor`: 7 top-level items, including Documents, while notes.md says documents live inside the room and lessons. Everything is a `page`; no sheet or notification surfaces, so page-vs-sheet is undecided.
- `pick-slot`: "Message tutor instead" goes to `student-home`, not to a message.
- `profile-preview`: a separate preview step after `set-availability`; X folds the live preview into the single setup screen and ships in 3 taps vs 5.

## Winner

**P1: X. Overall: X.** X puts the slot before the account, defaults price and availability, skips name on Google, and treats the device check as a no-block gate with partial-failure states and a reminder that lands one tap from the room — the brief's three pains (same dashboard, 6-page form, "I can't hear you") are each closed with a concrete mechanism. Y's spec is clean and complete, but it asks for the account before showing value, keeps 7 tutor nav items, leaves the tutor without a device check, and has no path from booking to the room beyond "come back later". X's own gaps (the notify-me dead end, the shared device-check exit) are smaller and local.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 5, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 3, "states": 4, "ia": 3, "asks": 3, "fit": 4, "handoff": 3, "scope": 4}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
