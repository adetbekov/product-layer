# Blind review: warmplace-onboarding-r2 (P1)

## Scores

| Step | Side | success | flow | states | ia | asks | fit | handoff | scope |
|---|---|---|---|---|---|---|---|---|---|
| P1 | X | 5 | 4 | 5 | 4 | 5 | 4 | 4 | 4 |
| P1 | Y | 4 | 3 | 4 | 4 | 4 | 4 | 3 | 5 |

Clarity: X 4, Y 4.

## Defects

**X**
- `device-check` — "Done (lesson not started yet)" always goes to `student-home`; a tutor arriving from `tutor-home` → Start lesson is sent to the wrong home.
- `lesson-ended` — a shared screen with two role-suffixed actions ("Go to my home (student/tutor)") pushes the routing decision onto the engineer; a `by: system` branch on role would be cleaner. It also extends past the stated `done: lesson-room`.
- `states` use non-standard keys (`partial`, `success`, `no access`) outside the fixed empty/loading/error format; useful content, but a format deviation.
- `profile-setup` adds a price field that the brief never mentions; it is prefilled and flagged as an assumption, but it is still an unrequested ask.
- Notes and yaml comments cite opaque codes (RL-1, ON-9, FL-4) nobody outside the author can resolve.

**Y**
- `role-choice` — "I want to learn" goes straight to `student-home` with no sign-in; an anonymous visitor lands on an authenticated dashboard.
- `invite-landing` → `sign-in` → `book-slot` — the student must create an account before seeing a single time slot; the slot (the only thing that justifies signing in) is hidden behind auth.
- `lesson-room` — Leave goes only to `student-home`; the tutor who entered via `tutor-home` → Open room exits to the student dashboard.
- `device-check` — the only action is "Join now"; the error state promises "retry, or join with audio only" but there is no exit back to home if the lesson is not starting yet.
- `book-slot` empty state ("Ask <tutor> for a time") describes a message action that appears in no `actions` list, so a student facing zero slots has no modelled way forward.
- `student-home` — "Lesson reminder tapped, by: system" is a modelling hack to make the notification reachable; the reminder should be a system transition from booking, not from the dashboard.
- Tutor flow starts at `role-choice` and then runs two setup pages (`tutor-profile`, `tutor-availability`); 5 user steps versus X's 3, and the role is asked although a tutor entry page could infer it. Name on `tutor-profile` is not stated as prefilled from Google.
- Parent-for-child, named in the brief, is pushed to "later" in notes rather than designed.

## Winner

**P1: X. Overall: X.** Both specs infer role from the invite, kill the 6-page form, split nav by role and put a device check with a no-block fallback before the room. X wins on sequencing and completeness: slots are shown before sign-in so the account is created at the moment of need, the tutor reaches a bookable profile in one defaulted screen with a live preview, and every error state (expired invite, no slots, slot taken, permission denied, connection lost) has a modelled exit. Y is tighter in scope but has three real routing holes (unauthenticated student-home, tutor exiting to the student dashboard, no exit from device-check) and asks students to commit to an account before they can see whether any time suits them.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 4, "flow": 3, "states": 4, "ia": 4, "asks": 4, "fit": 4, "handoff": 3, "scope": 5}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
