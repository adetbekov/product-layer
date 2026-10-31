# Blind review: settings redesign (P1)

## Scores

| Step | Side | success | flow | states | ia | asks | fit | handoff | scope |
|---|---|---|---|---|---|---|---|---|---|
| P1 | X | 5 | 5 | 5 | 5 | 5 | 4 | 5 | 4 |
| P1 | Y | 4 | 3 | 4 | 4 | 5 | 4 | 3 | 4 |

Clarity (final message): X 5, Y 4.

## Defects

**X**
- `export` / `export-building`: the building state is specified twice (as a `loading` state on `export` and as its own screen). Harmless but an engineer has to pick one.
- `digest-saved`: Undo goes back to the `digest` sheet instead of reverting in place; one extra tap for the rare undo. Defensible, but reverting directly would be tighter.
- `landing`: a stub outside the brief with a self-looping "Sign in" action. Documented as placeholder in notes, so not misleading, but it is unrequested surface.
- "Delete account (link, not a button)" edges toward a visual call; acceptable as hierarchy, but phrase it as weight, not component.

**Y**
- `settings`: shows rows "Password" and "Profile" (plus an "Edit profile" header link) but the actions list only reaches digest, export and delete. Two visible rows with no destination and no screens behind them: dead ends an engineer must invent.
- `digest`: "Not your time zone?" links to Profile, which does not exist in the spec.
- `export`: the "Request export" action is marked `by: system` and jumps straight to `export-ready`. Requesting is a user action; as written the transition costs nothing and the few-minute build has no explicit user-triggered start. The error state names "Try again" but no action carries it.
- `digest-saved`: toast "stays until dismissed because it carries an action", yet the transition back to settings is `by: system`. The two statements conflict.
- `deleted`: "Go to start page" loops to `deleted`; a dead end rather than a stub pointing outward.
- `settings` header duplicates the "Profile" row (avatar/name/email shown twice).
- Final message claims 9 screens; the file has 7.

## Winner

**P1: X. Overall: X.**

Both sides land the same core move (digest first on a flat settings home, pick-to-save with Undo, no re-entered email, no Save dialog, typed-email delete separated from everything else), and both get the digest to two user taps from settings. X wins on completeness and buildability: every row on its settings page has a defined screen, export is modeled as a user request followed by a system "Ready" transition with a leave-and-notify state, and every error has a named way out. Y's spec has the right shape but leaves Password, Profile and the time-zone link unresolved, mis-models the export request as a system step, and its message misreports the screen count, so a team could not build it without guessing.

```json
{"X": {"P1": {"success": 5, "flow": 5, "states": 5, "ia": 5, "asks": 5, "fit": 4, "handoff": 5, "scope": 4}, "clarity": 5}, "Y": {"P1": {"success": 4, "flow": 3, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 3, "scope": 4}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
