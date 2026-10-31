## Scores

| Side | Step | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|---|
| X | P1 | 5 | 4 | 5 | 5 | 5 | 4 | 4 | 4 | 4 |
| Y | P1 | 5 | 3 | 4 | 3 | 3 | 3 | 4 | 4 | 4 |

## Defects

**X**
- `device-check`: "Done (lesson not started yet)" goes to `student-home` for everyone; a tutor arriving from `tutor-home` → Start lesson lands on the wrong role's home. Secondary action, but a real role leak.
- `invite-landing` → "Notify me when times open" → `sign-in-sheet`, whose Google action goes to `booking-confirmed` although no slot exists. The no-slot path needs its own exit (to `student-home` empty state).
- `profile-setup`: no empty state for "no subject chosen"; whether Publish is disabled is left to the engineer.
- Purpose lines carry internal codes (`RL-11`, `IA-3`, `ON-9`) that nobody downstream can resolve; noise in a handoff document.
- Student nav drops Payments entirely (lives in Settings). Defensible for a pay-after model, but the brief lists payments as a core module and the assumption is only stated in notes.

**Y**
- `lesson-room`: the only exit, "Leave lesson", goes to `student-home` for both roles; the tutor's main path ends on the student dashboard. Worse than X's equivalent because it is the primary action.
- `student-details` is a mandatory extra page even on the Google path, and asks "Me / My child" of every student; X makes this a secondary link only parents touch.
- `tutor-profile` requires a bio; `tutor-availability` requires hand-picked hours with Publish disabled until then. Both could default (template hours, bio deferred to the checklist). Tutor path is 5-6 user steps against X's 3.
- `invite-landing` → "Message the tutor (no slots)" → `sign-in` → `student-details` → "Book lesson" with no slot: same dangling no-slot path as X, but it runs one page further before breaking.
- Tutor nav keeps 7 items and adds an unrequested `Materials` section; from 9 to 7 is a thin cut. No surface distinction beyond page/notification, no ordering inside screens.
- Returning students: `sign-in` always routes to `student-details`; there is no returning-user branch (X has `sign-in` with role dispatch and `role-choice`).
- Reminder fires at 15 minutes but Join activates at 10; small inconsistency to resolve.

## Winner

**P1: X. Overall: X.** Both answer every explicit part of the request and both put a device check with audio-only / no-camera fallbacks in front of the room, so the "I can't hear you" problem is handled on each side. X wins on asks and flow: role is inferred with a single fallback screen, sign-in is a sheet over the held slot, parent detail is opt-in, tutor setup is one defaulted screen with a live preview, and device-check distinguishes missing / partial / denied with a way through each. Y is a competent cut of the same idea but keeps more mandatory steps, more required fields, a 7-item tutor nav, and sends the tutor to the student home after every lesson.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 5, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 3, "states": 4, "ia": 3, "asks": 3, "fit": 3, "handoff": 4, "scope": 4}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
