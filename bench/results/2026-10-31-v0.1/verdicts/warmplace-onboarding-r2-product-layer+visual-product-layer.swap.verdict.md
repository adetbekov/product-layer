# Blind review: tutoring platform onboarding + IA (P1)

## Scores

| Side | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|
| X | 5 | 4 | 4 | 4 | 4 | 4 | 3 | 4 | 4 |
| Y | 5 | 4 | 5 | 4 | 5 | 4 | 4 | 3 | 4 |

Both answer every explicit part: two named flows, `nav` per role, `role` / `dashboard` / `room` tags. Both infer role from the entry door, put sign-in after the slot pick, and put a device check in front of the room. Student path is 4 taps with Google on both sides; tutor path is 4 (X) vs 3 (Y).

## Defects: X

- `invite-landing` / `tutor-start` / `invite-unavailable`: "Sign in" jumps straight to `student-home` / `tutor-home`. There is no sign-in screen for returning users; an engineer must invent it. `invite-unavailable` also mentions "Contact support" with no action.
- `slot-request-sent` -> `student-sign-in` -> `booking-confirmed`: the sign-in sheet assumes a chosen slot and lands on a booking that does not exist on the "ask for another time" path.
- `booking-confirmed` error "slot taken: show nearest free slots" has no edge back to the slot list.
- `student-sign-in` asks "me / my child" of every student, and `booking-confirmed` adds a browser-notification permission ask; both are small but not strictly needed to reach the first lesson.
- `tutor-preview` is a separate page; a live preview on `tutor-profile-setup` would remove a step.
- `student-home` empty state wording ("Copy-free action") is unclear; reply claims 21 screens, the spec has 17.

## Defects: Y

- `device-check` "Done (lesson not started yet)" -> `student-home` only; a tutor arriving via `tutor-home` "Start lesson" is sent to the wrong home. Shared screens elsewhere label role edges; this one does not.
- `invite-landing` empty state "Notify me when times open" -> `sign-in-sheet` -> `booking-confirmed`: same incoherence as X, a confirmation with nothing booked (prose says "then home", the edges say otherwise).
- Student nav hides Payments inside Settings; students pay for lessons, so a due payment is one level deeper than it should be. Tutor "Calendar" vs student "Lessons" is an inconsistent name for the same kind of section.
- `settings` and `lesson-ended` are unrequested screens; `profile-setup` lets a tutor publish an untouched availability template, which risks false open slots.
- Extra state names (`partial`, `success`, `no access`) sit outside the fixed empty/loading/error format, though they are clear.

## Winner

P1: Y. Overall: Y.

Y handles the two named risks better: the device check has empty, partial and denied states with join never blocked, is reachable right after booking (so "I can't hear you" is caught days early, not at lesson start), and the room links back to it; both empty dashboards point to the one useful action. Y also asks less (child name optional, no notification prompt, tutor publishes in one screen) and includes the returning-user door and the no-role fallback that X leaves implicit. X is solid and slightly tighter in scope, but its missing sign-in screen, the orphan support/slot-taken exits and the extra preview step leave more guessing for the build.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 4, "fit": 4, "handoff": 3, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 3}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
