## Scores (P1)

| Criterion | X | Y |
|---|---|---|
| success | 5 | 5 |
| flow | 3 | 4 |
| states | 3 | 4 |
| ia | 4 | 4 |
| asks | 4 | 5 |
| fit | 3 | 4 |
| handoff | 4 | 4 |
| scope | 5 | 4 |
| clarity (per side) | 4 | 4 |

## Defects

**X**
- `tutor-home` "Open room" goes straight to `lesson-room`, bypassing `device-check`. The reply claims the check is required before the room; half the "I can't hear you" problem (the tutor's side) is left unsolved.
- `invite-landing` only previews slots; the student must create an account (`sign-in`) before `pick-slot`. Seven user steps to the room with Google, sign-in before any value.
- `sign-in` has no returning-user path: every exit leads to `student-details` or `tutor-profile`, so a returning user is pushed back into onboarding. "Sign in for returning users" is shown on `invite-landing`/`welcome` with no action.
- `profile-live` shows a "Test your camera and microphone" link with no action; `invite-landing` shows "I'm a parent booking for a child" with no action.
- No loading state on screens that save (`student-details`, `tutor-profile`, `tutor-slots`, `booking-confirmed`, `profile-live`). `invite-landing` error exit ("browse nothing else") is not a real way out.
- `tutor-profile` requires a bio and level; neither is needed to be bookable. Student nav drops Payments although payment is deferred to after the lesson, with no stated place to pay.

**Y**
- `check-email` "Link opened (sign-in)" routes to `sign-in`, a loop (sign-in -> check-email -> sign-in); should land by role. `sign-in` marks "Continue with Google" as `by: system`, which misstates who acts.
- `ask-time-sent` promises "email when the tutor proposes a time" but the anonymous visitor's email was never asked, so the tutor cannot reply.
- `lesson-lobby` Back and `lesson-room` Leave both go to `student-home` even though the screens are shared with the tutor (X has the same room-leave fault).
- Tutor nav is 7 items with `Board` and `Profile` top-level; `Profile` belongs under Settings for a two-role product that wants few sections. Labels stay as nouns rather than what people do.
- `notes.md` cites rule codes (ON-8, RL-11) the reader does not have; noise for handoff.

## Winners

**P1: Y.** Y gets a student from link to room in five taps with the account asked at the moment of commitment, defers payment by a per-tutor setting, and puts the device lobby in front of both roles' room entry, which is the one named pain in the brief. X's nav is leaner and better named (Students, Library), but X forces sign-in before slots, makes the tutor skip the device check, and leaves returning users with no door.

**Overall: Y.** Y's asks are the tightest (email, name, subjects; price and hours prefilled), states cover loading on every network step, and surfaces (page, sheet, notification) tell an engineer what to build. Its defects are routing slips; X's are flow holes in the core promise.

```json
{"X": {"P1": {"success": 5, "flow": 3, "states": 3, "ia": 4, "asks": 4, "fit": 3, "handoff": 4, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
