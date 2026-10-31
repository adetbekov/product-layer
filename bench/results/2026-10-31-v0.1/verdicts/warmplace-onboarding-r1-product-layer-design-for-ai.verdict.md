# Blind review: warmplace onboarding, P1

| Step | Side | success | flow | states | ia | asks | fit | handoff | scope |
|---|---|---|---|---|---|---|---|---|---|
| P1 | X | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 5 |
| P1 | Y | 5 | 5 | 5 | 3 | 5 | 5 | 4 | 4 |

Clarity: X 4, Y 4.

## Defects, X

- `invite-landing`: a pure "Continue" page. The visitor sees the tutor but no slots; the only decision is to proceed to account creation. One click spent, no value shown, account before any reason to commit.
- `start` (moment `role`): shows two choices but only "I teach" has an action. A non-invited student has a dead end.
- `student-sign-in`: the "booking for my child" toggle is asked before anything of value, on the sign-in page. It belongs at booking time (and X's own `slot-pick` already asks the first name there).
- `tutor-room`: not tagged `room`; the request asked to tag the lesson video room, and the tutor's room is one. No loading state while connecting.
- `student-home` empty state says "show the tutor's slots (slot-pick)" but there is no action to `slot-pick`.
- Nav: student has no Payments item while the spec promises "pay after the lesson". Every screen is a `page`; `tutor-device-check` is the lone modal, so the same check is a page for students and a modal for tutors with no stated reason.
- `profile-basics` requires lesson length and price before publishing; a suggested default would do.

## Defects, Y

- Nav: tutor keeps 7 items (adds Board and Profile) against a brief that complains about 9. Profile could live under Settings or Home; "same labels for both roles" is a rule applied at the cost of the "few sections" goal.
- `lesson-lobby` and `lesson-room` are shared by both roles, but "Back" and "Leave lesson" both go to `student-home`. A tutor who presses Back lands on the student dashboard. Role-dependent destinations are not specified.
- `check-email` "Change email" always returns to `sign-in-sheet`, even when the saved choice is tutor sign-up (should return to `tutor-start`).
- `purpose` lines cite rule codes (ON-8, RL-11, IA-4) that are not defined anywhere in the spec; noise for an engineer.
- Scope: `lesson-reminder` and `new-booking-notice` notifications and `ask-time-sent` go beyond onboarding and IA. Useful, but not asked.
- Three stacked sheets in a row (`sign-in-sheet` to `confirm-booking` to `pay-lesson`) on top of the landing; fine as one sheet with steps, but the spec should say so.

## Winner

P1: Y. Overall: Y.

Y shows the tutor's open slots to a signed-out visitor and asks for an account only when a time is picked, so the student reaches value in 3 taps with Google and the only questions are email and a prefilled name. X puts an informational page and an account form ahead of the slots, asks the child toggle too early, and leaves `start` with a dead end for students. Both solve "I can't hear you" with a non-blocking device check with audio-only fallbacks, and both design empty dashboards; Y is more complete on states (notification permission fallback, no-device recovery, resumable tutor setup). X has the better nav (4 and 5 items, role-specific), and Y's 7-item tutor nav and shared-screen back-destinations are real defects, but the student flow is the product's main path and Y's is clearly stronger there.

```json
{"X": {"P1": {"success": 4, "flow": 4, "states": 4, "ia": 4, "asks": 4, "fit": 4, "handoff": 4, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 5, "states": 5, "ia": 3, "asks": 5, "fit": 5, "handoff": 4, "scope": 4}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
