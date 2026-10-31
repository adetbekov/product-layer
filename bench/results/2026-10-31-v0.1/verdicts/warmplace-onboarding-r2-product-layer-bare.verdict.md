# Blind review: tutoring platform onboarding and IA (P1)

## Scores

| Criterion | X | Y |
|---|---|---|
| success | 5 | 5 |
| flow | 3 | 5 |
| states | 4 | 5 |
| ia | 4 | 5 |
| asks | 4 | 5 |
| fit | 4 | 5 |
| handoff | 3 | 4 |
| scope | 5 | 4 |
| clarity (once) | 4 | 4 |

## Defects

**X**
- `lesson-room`: the only exit, "Leave lesson", goes to `student-home`. A tutor who joins from `tutor-home` lands on the student dashboard. The room is shared but the leave target is not role-split.
- `device-check`: the only action is "Join lesson". The dashboard offers "Test camera and mic" well before the lesson, but the tester cannot go back; the only way out is into the room.
- `invite-landing` no-slot path: "Message the tutor" goes to `sign-in`, then `student-details`, whose only action is "Book lesson" with a slot summary that does not exist. The no-slot student has no coherent path to a message or to home.
- `student-details`: a mandatory extra screen for every student, including Google users whose name is already known; "me or my child" is asked of everyone though most invitees are students themselves.
- `tutor-profile`: bio is a required field. Students can book without it; it belongs in the deferred list with avatar and payouts.
- Nav: tutor has 7 items, Payments sits in the student nav; still much better than 9, but not pared to the role matrix.

**Y**
- `device-check`: "Done (lesson not started yet)" always goes to `student-home`; a tutor testing devices from `tutor-home` has no return.
- `sign-in`: the error says "No account for this email, offers Start" with no target, while a system action sends role-less accounts to `role-choice`. Which happens for a fresh Google sign-in is left to the engineer.
- Scope: `settings` (with "Also teach / Also learn" dual roles) and `lesson-ended` were not requested; the spec and notes cite rule codes (RL-1, ON-9, FL-4) that a reader cannot resolve.
- Student nav drops Payments entirely into Settings; students do pay per lesson, so this is defensible but debatable.

## Winner

**P1: Y. Overall: Y.** Y gets a Google student from invite to room in four taps (slot, Google, reminder, Join) and a tutor to a bookable profile in three, by holding the slot in a sheet over the landing, making the child case an optional link rather than a universal question, and prefilling price and a weekly availability template behind a live preview. Its device check covers no-device, partial, denied and success with join never blocked, and the room has one-tap settings back to it. X is clean and well-stated, but it costs every student an extra form screen, requires a tutor bio and a separate hours step, and leaves three real gaps an engineer must guess at: the tutor's leave target, the device-check exit, and the no-slot booking path. Y's extras (settings, lesson-ended) are mild scope creep but do not undo its lead.

```json
{"X": {"P1": {"success": 5, "flow": 3, "states": 4, "ia": 4, "asks": 4, "fit": 4, "handoff": 3, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 5, "states": 5, "ia": 5, "asks": 5, "fit": 5, "handoff": 4, "scope": 4}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
