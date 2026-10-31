# Blind review: settings redesign (P1)

## Scores

| Step | Side | success | flow | states | ia | asks | fit | handoff | scope |
|---|---|---|---|---|---|---|---|---|---|
| P1 | X | 5 | 4 | 4 | 5 | 4 | 4 | 4 | 5 |
| P1 | Y | 5 | 4 | 4 | 4 | 5 | 4 | 3 | 4 |

Clarity: X 5, Y 4.

## Defects

**X**
- `account`: "Change password" asks only for the new password; no current-password check. A password change without re-authentication is a security hole, even if the screen is outside the tagged moments. No loading state on the page either.
- `deleted`: `shows` lists a sign-up link but `actions: []`, so the spec contradicts itself at the terminal screen.
- `export-ready`: "Download" transitions to `settings`; a download should not navigate away. Also no loading state for the download itself.
- `digest`: the save is blocking (spinner, other options disabled) rather than optimistic. Consistent and safe, but slower than it needs to be for a 3-option toggle.
- `delete`: no states at all; acceptable for a static page but thin.

**Y**
- `digest` / `digest-saved`: the save path is contradictory. The sheet is optimistic ("shows selected at once while it saves") yet its error state says "choice stays open", while `digest-saved` adds a toast error "Not saved with Retry" that has no action target. An engineer cannot tell where a failed save surfaces or where Retry goes.
- `export`: its `loading` state describes "Building: progress notice... user may leave", which duplicates the whole `export-building` screen. Two homes for the same state.
- `landing`: a stub outside the brief, with "Sign in -> landing" self-loop. Unrequested and a dead end on paper.
- `settings`: error is whole-page ("Could not load your settings. Retry") where X degrades per row; the profile summary (avatar, name, email, tz) on the home adds weight to the 70% path.
- Reply and notes cite rule codes (SR-1, FL-8, ST-3) nobody outside the author can decode.

## Where each is stronger

Y asks for the current password when changing it, offers "Forgot password" as a recovery, tells the user "your notes are untouched" on export failure, and adds "Contact support" on a failed deletion. Y's typed-email confirmation is reasonable friction, though a password (X) is a stronger proof of ownership. X's settings home is leaner (four rows, Account collapsed with the email as subtitle), its error handling on the home is per-row, and its delete path (page -> modal with password or DELETE, export offered first, delete visually quiet and far from any save) is the safest of the two.

## Winner

**P1: X. Overall: X.** Both specs cut the digest to 3 taps, stop asking for email and time zone, make the digest the first row, and separate deletion with an export-first offer. X wins on consistency: its digest save path has exactly one error surface, its scope stops at what was asked, and its reply reads like a designer explaining decisions rather than a rules checklist. Y covers slightly more states and gets the password ask right, but its optimistic-save contradiction and the out-of-brief `landing` stub would force an engineer to guess.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 5, "asks": 4, "fit": 4, "handoff": 4, "scope": 5}, "clarity": 5}, "Y": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 3, "scope": 4}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
