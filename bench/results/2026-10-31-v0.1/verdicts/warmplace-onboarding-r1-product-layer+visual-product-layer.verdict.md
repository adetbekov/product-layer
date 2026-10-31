# Blind review: warmplace onboarding r1 (X vs Y)

## Scores (P1)

| Criterion | X | Y |
|---|---|---|
| success | 5 | 5 |
| flow | 4 | 3 |
| states | 5 | 5 |
| ia | 5 | 4 |
| asks | 5 | 4 |
| fit | 4 | 5 |
| handoff | 4 | 4 |
| scope | 5 | 4 |
| clarity (once) | 5 | 4 |

## Defects

**X**
- `sign-in`: "Continue with Google" is marked `by: system`, but the Google tap is a user step; the step count and an engineer's reading of the transition are both off.
- `invite-landing` → "Request a time" lands on `sign-in`, which only shows "the chosen slot" and exits to `booked`. The request path has no confirmation screen and no way to deliver a tutor's reply; it quietly turns into a booking.
- `invite-expired`: "Ask for a new link" goes to `student-home`, a page that needs an account the visitor does not have. No contact channel is collected either.
- `invite-landing` asks "for me / for my child" but never asks the child's name, although the stated reason is "changes whose name the tutor sees".
- `student-home` empty state offers "Request a time" and `tutor-start` offers "Sign in", neither with an action target. Returning users have no door at all.

**Y**
- `check-email`: "Link opened (sign-in)" returns to `sign-in`, which sends email users back to `check-email`. A loop with no exit for the email path of a returning user; it should branch to the role's home.
- Student path is 5 user steps (pick slot, Google, Book, Open room, Join) against X's 4; `confirm-booking` exists mostly to confirm a name Google already supplies. Tutor path is 4 steps because the preview is its own page rather than live next to the fields.
- Tutor nav has 7 items (Board, Profile and Payments all top level); the brief's complaint was 9 items, and Profile belongs with Settings. "Same labels for all roles" is stated but the lists differ.
- `profile-live`: "Copy invite link" navigates to `tutor-home`; copying should not move the user.
- `ask-time-sent` promises "email when the tutor proposes a time" but no email was asked before the request was sent.
- Rule codes (ON-8, RL-11) sprinkled in the spec are not resolvable by a builder.

## Winner

**P1: X. Overall: X.** Both specs answer every explicit part, infer the role from the entry, delay the account to slot commit, put a device-check lobby with denied-permission and no-device fallbacks before the room, and give each role an empty home that fits it. X gets each role to its outcome in fewer steps (4 and 3 vs 5 and 4), with a tighter nav (4/5 vs 5/7) and nothing unrequested. Y is stronger on grain (per-tutor prepayment, tutor booking notice, a role fallback for sign-ins with no entry) and its states are a touch more thorough, but the sign-in loop, the extra confirm and preview pages, and a 7-item tutor nav outweigh that for this request.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 5, "asks": 5, "fit": 4, "handoff": 4, "scope": 5}, "clarity": 5}, "Y": {"P1": {"success": 5, "flow": 3, "states": 5, "ia": 4, "asks": 4, "fit": 5, "handoff": 4, "scope": 4}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
