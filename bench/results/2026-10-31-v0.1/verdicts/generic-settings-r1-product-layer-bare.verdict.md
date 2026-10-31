# Blind review: generic-settings r1 (X vs Y)

## Scores

| Step | Side | success | flow | states | ia | asks | fit | handoff | scope |
|---|---|---|---|---|---|---|---|---|---|
| P1 | X | 5 | 4 | 4 | 4 | 5 | 4 | 3 | 3 |
| P1 | Y | 5 | 4 | 5 | 4 | 5 | 4 | 4 | 4 |

Clarity: X 4, Y 4.

Both answer every explicit part of the request: flow `digest` with entry `settings` and done `digest-saved`, all four moments tagged, nav declared. Both cut the digest path from 8 steps to 3 (Settings, digest row, pick), drop the email re-entry, save on pick with toast plus Undo, move export to one tap with background build, and isolate deletion at the bottom with typed-email confirmation. The differences are in rigor.

## Defects: X

- `settings`: action "Back to notes (nav)" points to `settings` itself. Either a self-loop or a wrong target; an engineer cannot tell.
- `export`: the "Export my notes" action goes straight to `export-ready` `by: user`. The minutes-long build exists only as a loading-state string; there is no `by: system` transition for "built" or "failed", so the async path is not actually in the flow graph.
- `digest`: loading is "Not shown", but a save happens on pick. The in-flight state is missing even though the error state ("Save failed ... Retry") depends on it.
- `digest-saved`: Undo returns to the `digest` sheet instead of reverting in place; that is an extra step after an undo.
- `delete-done`: a 14-day grace period and "Restore account" (to `settings`, for a deleted account) is an unrequested product policy that changes backend semantics; flagged as an assumption but still shipped as the flow.
- Minor visual leakage: "link-style action", "primary-looking", "not styled as the main action".

## Defects: Y

- `profile`: email is read-only with "Change email", but no screen or action for it exists anywhere. Dangling reference.
- `export`: adds a format choice (Markdown zip default). Pre-selected so it costs nothing, but nobody asked for it.
- `export-building`: error offers "contact support" with no target.
- `account-deleted`: `actions: []`; the sign-up link lives only in `shows`. Acceptable as a terminal screen, but inconsistent with the format.
- `digest-saved`: no states, and Undo also reopens the sheet rather than reverting in place.
- Minor visual leakage: "plain text, no primary styling".

## Winner

**P1: Y. Overall: Y.**

On the three judging questions the two are close: both remove steps without hiding profile or password, both keep deletion deliberate and away from Save, both default time zone and stop re-asking the email. Y wins on loading and errors: it models the digest save in flight (spinner, options disabled, revert plus "Try again"), gives profile and password loading states, and expresses the export build as real `by: system` transitions (built -> ready, failed -> export), where X collapses the build into a single user action and leaves a self-referencing nav action. X's spec is more legible (ranks, purposes) but its 14-day restore window is scope it invented, and its two graph bugs would make an engineer guess. Y's one dangling "Change email" is the smaller hole.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 3, "scope": 3}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
