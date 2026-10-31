# Blind review: tutoring platform onboarding and IA (P1)

## Scores

| Criterion | X | Y |
|---|---|---|
| success | 5 | 5 |
| flow | 3 | 4 |
| states | 4 | 4 |
| ia | 4 | 5 |
| asks | 3 | 5 |
| fit | 3 | 5 |
| handoff | 4 | 4 |
| scope | 5 | 5 |
| clarity | 4 | 4 |

Both answer every explicit part of the request: two named flows with entry and done screens, nav per role, and the three moments tagged.

## Defects, X

- `tutor-signup`: tagged `role` and asks the role explicitly, yet it is already the tutor door reached via "I am a tutor". The role is inferable from the entry; the question is redundant. Its student option dead-ends in an error message that sends people to `sign-in`, whose "I am a tutor" link sends them back: a loop for any student without an invite.
- `magic-link-sent` has a single system transition to `details`, the student form. A tutor who signs up by email lands in the student flow. The tutor email path is otherwise undefined.
- `sign-in` "Continue with Google" goes straight to `student-dashboard`, skipping `details`, so a new student via the broken-link path never gives a name.
- `device-check` error offers only "Join without camera"; the brief's problem is audio, and there is no path for a denied or missing microphone. `lesson-room` empty state says the device check "is still available" but no action leads there.
- `tutor-basics` asks "subjects and levels" and shows a headline field, while the reply claims level was dropped. Student reaches the room only via the dashboard; no reminder brings them back at lesson time. Seven user steps versus Y's four.

## Defects, Y

- `student-sign-in`: the email path has no "check your inbox" state; after "Email me a link" the sheet's behaviour is unspecified. The two action labels fold two paths and a condition ("time chosen"/"no time chosen") into one line, which an engineer must untangle.
- `tutor-start` "I already have an account" goes to `tutor-home` with no sign-in defined. `invite-landing` error for an expired link deliberately shows no sign-in, so a returning student with a dead link has no door.
- `tutor-home` has no action to edit open times after publishing; the nav has no Calendar, so where availability lives later is left to guessing.
- `terminal: false` on every screen, including done screens, is noise.

## Strengths that decide it

Y asks for a time before asking for an account, puts sign-in in a sheet that holds the chosen slot, and uses a `by: system` reminder notification to deliver one-tap entry to the lobby. Its lobby has a real empty state (permission not yet granted, asked with a reason), an error that keeps "Enter room" available, and the room offers "Check devices" back to the lobby. Settings sits in the avatar menu, leaving 4 and 5 sections named for activities. Priority ranks on `shows` give the visual designer ordering without touching visuals.

X's main contributions (one-page details, slot picking right after sign-in, device check, dashboard with one dominant item) are sound, but Board and Settings as top-level tutor items are tools rather than activities, Payments hidden in Settings is hard to find for paying students, and the redundant role question plus the email misroute undo some of its own simplification.

## Winner

P1: Y. Overall: Y. Y reaches both first outcomes in four user actions with no role question anywhere, handles the camera/microphone failure with a way through, and uses sheets, notifications and system transitions where they fit the web. X is complete and readable but has routing bugs on the email and no-invite paths and asks the one question it could have inferred.

```json
{"X": {"P1": {"success": 5, "flow": 3, "states": 4, "ia": 4, "asks": 3, "fit": 3, "handoff": 4, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 5, "asks": 5, "fit": 5, "handoff": 4, "scope": 5}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
