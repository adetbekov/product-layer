# Blind review: tutoring platform onboarding and IA (P1)

| Criterion | X | Y |
|---|---|---|
| success | 5 | 5 |
| flow | 4 | 4 |
| states | 4 | 5 |
| ia | 4 | 5 |
| asks | 4 | 4 |
| fit | 4 | 5 |
| handoff | 4 | 4 |
| scope | 5 | 4 |
| clarity | 5 | 4 |

Both answer every explicit part: two named flows with entry/done, `nav` per role, and `role` / `dashboard` / `room` moments. Both infer student from the invite, kill the 6-page form, cut nav to 4/5 items, put a device check before every room entry, and design the empty dashboard for each role. The differences are in the gaps.

## X defects

- `invite-landing` -> `student-booked`: the booking happens implicitly on sign-in. Nothing says what "Continue with Google" does when no slot is picked, and the landing empty state ("sign in to message the tutor") has no matching action; both buttons still lead to `student-booked`.
- `student-booked` error "This time was just taken. Pick another" has no action back to the slots; `student-home` shows the tutor's open slots but has no booking action. Re-booking is a dead end in the spec.
- The student is never asked a name on the email path, and the parent/child case from the brief is dropped; a tutor can receive an anonymous booking.
- `tutor-preview` shows "Edit details" but only has an "Edit times" action. `tutor-start` and `tutor-setup` have no loading state.
- Reply counts 3 taps to the room, but `student-booked` requires a tap to reach `device-check` (4).

## Y defects

- `check-email-student` "Change address" always returns to `invite-landing`, which is wrong for a student who came from `student-sign-in` without an invite.
- `lesson-room` loading text names a "Test devices link" with no action to `device-check`; there is no "lesson not started yet" state (X has one with a countdown).
- `tutor-sign-up` asks the role although the entry point could set it (as X does with a dedicated tutor start); `student-sign-in` and the "I'm learning" branch are beyond the two requested flows.
- `tutor-profile-preview` offers "Edit" to profile only, not to availability; `tutor-home` carries a stray `terminal: false` field. Shows lists carry no ranking, so "most used first" is left to the builder.

## Winner

P1 and overall: Y, narrowly. X is leaner and its tutor path and nav are as good as Y's, but its student booking path has a real hole (slot taken with no way back, booking implied by the sign-in button) and it ignores the parent-for-child case the brief raised. Y costs one more tap, yet every error names its way out, the booking confirm is correctly a sheet, the parent toggle is where it belongs, and the reminder-to-device-check path plus the 10-minute join window is how students actually reach the room, which is the "I can't hear you" problem the brief asked to solve. Y's scope creep (no-invite sign-in) is the main thing holding its margin down.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 4, "fit": 4, "handoff": 4, "scope": 5}, "clarity": 5}, "Y": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 5, "asks": 4, "fit": 5, "handoff": 4, "scope": 4}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
