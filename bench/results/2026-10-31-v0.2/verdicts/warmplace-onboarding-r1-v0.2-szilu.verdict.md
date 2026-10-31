## Scores (P1)

| | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|
| X | 5 | 4 | 4 | 4 | 5 | 4 | 4 | 5 | 4 |
| Y | 5 | 3 | 4 | 3 | 4 | 4 | 4 | 3 | 4 |

Both answer every explicit part: two named flows with entry/done, `role`/`dashboard`/`room` tags, nav per role, and both replace the 6-page form and add a device check before the room.

## X - main defects

- `student-sign-in`: the email path has no "check your email" screen or state. The user is left on the sheet after "Email me a link"; resend and wrong-address paths are undefined, so an engineer must invent them.
- `tutor-start`: "I already have an account" jumps straight to `tutor-home` with no sign-in step in between. Returning tutors have no designed path.
- `tutor-profile-preview`: an extra tap for the tutor that Y avoids by putting a live preview inside the profile form. Defensible, but it makes the tutor path 4 taps where 3 suffice.
- `student-booked` / `student-home`: the device check is reachable only at join time. Y offers it right after booking so "I can't hear you" is caught days before, not minutes before.
- Nav: tutors have no obvious place to edit open hours (no `Edit times` action on `tutor-home`; Settings/profile are in an avatar menu).

## Y - main defects

- `invite-landing`: shows the tutor's free slots but offers only "Continue", so the student sees the times, signs in, then picks the same times again on `booking-slot`. One wasted step; X lets them tap a time immediately.
- `booking-details`: a separate screen asking who the lesson is for, a name, and a goal. The goal is optional but still an unrequested ask on the critical path; the whole screen could fold into the sign-in or the slot pick. Student path is 6 user taps vs X's 4.
- `need-invite`: terminal, with no `actions` block and no sign-in link. A returning student who arrives without a link picks "I'm a student" on `welcome` and dead-ends with no way to sign in.
- `lesson-ended`, `payment-sheet`, waitlist, QR code, share buttons, payout prompts: all beyond what P1 asked (flows end at the room and at a bookable profile). Payments were explicitly out of frame.
- Nav: tutor has 6 items including Settings; student nav has Settings but no Payments even though Y's own design creates unpaid lessons and a "pay later" badge. Settings top-level is not a thing people do.
- `tutor-profile-live`: "share buttons (messenger" / "email)" is a broken list item; `invite-landing` offers "Retry" on an expired link, which cannot help.

## Y - what it does better

`check-email` is fully designed (self-updating when the link opens elsewhere, resend, change address, expired-link exits). `device-check` is reachable from confirmation, reminder and both homes, and separates "no device" from "denied" with audio-only and board-only joins. `tutor-availability` prefills a weekly default so one tap publishes. `lesson-room` degrades to audio-only on reconnect failure.

## Winner

**P1: X. Overall: X.** X gets the student from the invite to the room in 4 taps by letting them pick a time first and signing in only at the moment of booking, asks nothing the product can derive, keeps nav to 4/5 doing-words with no Settings, and stays strictly inside the request; its ranked `shows` also give a visual designer a hierarchy without touching visuals. Y has the better magic-link and device-check coverage and a faster tutor path, but it spends two extra student steps, dead-ends `need-invite`, and adds payment and post-lesson screens nobody asked for.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 3, "states": 4, "ia": 3, "asks": 4, "fit": 4, "handoff": 4, "scope": 3}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
