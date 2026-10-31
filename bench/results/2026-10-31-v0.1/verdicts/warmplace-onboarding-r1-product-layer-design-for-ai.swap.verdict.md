## Scores

| Step | Side | success | flow | states | ia | asks | fit | handoff | scope |
|---|---|---|---|---|---|---|---|---|---|
| P1 | X | 5 | 5 | 5 | 4 | 5 | 4 | 4 | 4 |
| P1 | Y | 4 | 3 | 4 | 4 | 4 | 3 | 3 | 4 |

Clarity: X 4, Y 4.

## Defects

**X**
- `lesson-lobby` / `lesson-room`: declared shared by both roles, but the only exits (`Back`, `Leave lesson`) go to `student-home`. A tutor leaving a lesson lands on the student dashboard.
- `profile-live`: `Copy invite link` is modelled as a navigation to `tutor-home`; copying should not leave the screen.
- `new-booking-notice`: "Open lesson" goes to `tutor-home`, not to the booking it announces.
- `confirm-booking` always routes through `pay-lesson` and relies on a `by: system` skip. Acceptable, but the sheet-then-sheet chain should be stated as conditional at the action, not in a comment.
- Tutor nav has 7 items; `Profile` and `Board` could live under Settings and Lessons. Rule codes (ON-8, RL-11) leak into `purpose` text and mean nothing to an engineer.

**Y**
- `start`: shows "I'm looking for a tutor" but has no action for it. Dead end for every uninvited student.
- `invite-landing`: a pure "Continue" screen with no slots shown; the student must create an account before seeing whether the tutor has a time that fits. No `empty` state for a tutor with no open slots until after sign-in (`slot-pick`).
- `slot-pick` empty: "Message {tutor}" and "leave an email reminder" have no target screens.
- `tutor-room` lacks the `room` moment and a loading state; `tutor-device-check` has no audio-only fallback and no loading/permission-prompt state, so a tutor with a dead mic has only "Enter without camera".
- Student nav has no Payments although the product bills "after the lesson"; nowhere to pay.
- `student-sign-in` asks the child toggle before it matters; `profile-basics` asks price with no default and shows photo during onboarding; `availability` adds an unrequested Google Calendar connect.

## Winner

**P1: X. Overall: X.**

X puts the tutor's open slots in front of the invited visitor before any account, asks for sign-in only at the moment of commitment, and reaches the room in about five user steps with device check, permission timing and fallbacks fully stated. Its surfaces are differentiated (sheet for commit moments, notification for the reminder) and every screen carries all three states with a way out. Y's shape is sound and its nav labels ("Students") are the better set, but it front-loads account creation, leaves a dead end on `start`, and specs the tutor side thinly. X's role-exit bugs on the shared room are real but cheaper to fix than Y's ordering problem.

```json
{"X": {"P1": {"success": 5, "flow": 5, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 4, "flow": 3, "states": 4, "ia": 4, "asks": 4, "fit": 3, "handoff": 3, "scope": 4}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
