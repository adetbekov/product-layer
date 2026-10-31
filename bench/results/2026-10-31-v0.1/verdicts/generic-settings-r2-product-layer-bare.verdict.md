# Blind review: settings redesign (P1)

| Criterion | X | Y |
|---|---|---|
| success | 5 | 4 |
| flow | 4 | 3 |
| states | 4 | 4 |
| ia | 5 | 4 |
| asks | 5 | 3 |
| fit | 4 | 4 |
| handoff | 4 | 3 |
| scope | 5 | 4 |
| clarity | 4 | 3 |

## Defects

**X**
- `digest-saved`: Undo goes `to: digest-choice`, i.e. it reopens the sheet instead of restoring the previous value. An undo that makes the user pick again is not an undo; the engineer has to guess whether the revert happens on tap or on re-pick.
- `account-deleted`: the only action is "Back to start" `to: account-deleted` (self-loop) while `shows` promises a sign-up link. Minor, but it is a literal dead end in the spec.
- `export-start`: has an error state but no loading state for the "Request export" call, and no explicit empty state (the "if an export was built in the last 7 days" line implies one but does not design it).
- Reply claims "2 user steps instead of 8"; the honest count from the brief's starting point (nav tap, row, pick) is 3. Small overclaim.
- No empty states anywhere; acceptable for settings, but export is the one place it mattered.

**Y**
- `delete`: confirmation is "type your email", which the app knows and shows one screen earlier in the digest row ("to name@mail"). It is friction, not a safety check; anyone holding the session can copy it. X's password re-auth is the safer answer to "keep deletion safe". Y's own `asks.why` admits the field is known.
- Digest failure is designed twice and differently: `digest.states.error` says the choice stays open and still shows the old value with Retry; `digest-saved.states.error` says the row reverts and the toast says "Not saved" with Retry. The engineer must pick one.
- `export` carries a `loading: Building` state and there is also a separate `export-building` screen for the same thing. Duplicate surface for one state.
- `export-building`: "Try again" is listed as an always-available user action looping to itself, not scoped to the error state, so a user can re-fire a build while one is running.
- `landing`: an out-of-scope stub screen whose only action ("Sign in") loops to itself. `goodbye`, `export-building`, `export-ready` lack the requested moment tags that X applied consistently.
- `settings`: Profile summary ranked equal to Export although export is 15% of visits and profile edits do not appear in the analytics.
- Reply and notes cite rule codes (SR-1, FL-8, IA-3, ST-8) with no glossary; "Notice.error" is an undefined component name. Both read as internal jargon to the recipient.

## Winner

**P1: X. Overall: X.**

Both designers reach the same core shape (digest row first, single-choice sheet that saves on pick, toast with Undo, async export with leave-and-email, delete last as a link). X's spec is tighter and more buildable: every screen has one definition of each state, moments are tagged on every relevant screen, the email and time zone are shown and never asked, and deletion is gated by a password rather than by retyping a visible email. Y covers a few more states (export empty, "Forgot password" recovery, "nothing was removed" wording) and counts steps honestly, but the contradictory digest error, duplicated export loading, self-looping Try again, out-of-scope `landing` stub and rule-code jargon leave more for an engineer to guess, and its delete confirmation asks for data the app already has.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 5, "asks": 5, "fit": 4, "handoff": 4, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 4, "flow": 3, "states": 4, "ia": 4, "asks": 3, "fit": 4, "handoff": 3, "scope": 4}, "clarity": 3}, "winner": {"P1": "X", "overall": "X"}}
```
