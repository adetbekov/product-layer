# Blind review: warmplace onboarding r2 (X vs Y)

## Scores (P1)

| Criterion | X | Y |
|---|---|---|
| success | 5 | 5 |
| flow | 3 | 5 |
| states | 4 | 5 |
| ia | 4 | 5 |
| asks | 5 | 5 |
| fit | 3 | 4 |
| handoff | 4 | 4 |
| scope | 5 | 4 |
| clarity (per side) | 4 | 4 |

## Defects

**X**
- `invite-landing` → `sign-in`: the landing already shows "Continue with Google / email", then sends the user to a second page with the same two buttons. One redundant step on the main student path, and the student commits to an account before seeing a single slot.
- `role-choice` "I want to learn" → `student-home`: lands an unauthenticated visitor on a dashboard with no sign-in in between. Either a dead end or an undefined state for the engineer.
- `lesson-room` Leave → `student-home` only; the tutor (who reaches the room via `tutor-home` → `device-check`) is sent to the student's home. Same for `device-check`, which has no tutor-aware exit.
- Nav: student has "Message tutor" on home and the room has Chat, but neither role has a Messages section; tutor Payments is buried in Settings although it is a core tutor concern. `tutor-profile` has no loading state.
- Device-check error offers "join with audio only" even when the failure is the microphone; the chat fallback saves it, but the wording is wrong for that case.

**Y**
- `device-check` "Done (lesson not started yet)" → `student-home` regardless of role; a tutor who pre-checks devices lands on the wrong home.
- `lesson-reminder` error ("lands on the lesson summary") describes a target but has no corresponding action; engineer has to guess.
- Scope creep: `settings`, `lesson-ended` and `child-sheet` go beyond "invite link to first lesson room" and "sign-up to bookable profile". Small and sensible, but unrequested.
- Tutor nav has 6 items; still named for what people do, but closer to the original clutter than it needs to be.
- `rank` annotations on `shows` are content priority, not visual, but a visual designer could read them as layout instructions.

## Winners

**P1: Y.** Y puts value before commitment: the invited student sees the tutor and slots on the landing page and signs in only to hold a slot, cutting the Google path to four taps with no redundant screen. X's path has a duplicated sign-in step, an unauthenticated jump into the dashboard, and sends tutors to the student home after a lesson. Both infer role from the invite and both put a mandatory device check in front of the room; Y's is better designed (partial states, listen-only vs audio-only, never blocks joining) and the room has a one-tap route back to it. Y also handles both empty dashboards concretely ("Ask your tutor for a link" / "Send your invite link") and gives the tutor a single-screen setup with defaults that is publishable with two taps.

**Overall: Y**, for the same reasons; X is cleaner on scope and asks only the minimum, but its flow defects are the kind an engineer cannot build around without going back to the designer.

```json
{"X": {"P1": {"success": 5, "flow": 3, "states": 4, "ia": 4, "asks": 5, "fit": 3, "handoff": 4, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 5, "states": 5, "ia": 5, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
