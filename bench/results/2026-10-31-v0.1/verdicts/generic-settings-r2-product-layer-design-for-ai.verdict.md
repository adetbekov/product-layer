# Blind review: settings redesign (P1)

| Criterion | X | Y |
|---|---|---|
| success | 5 | 5 |
| flow | 4 | 4 |
| states | 5 | 4 |
| ia | 4 | 4 |
| asks | 4 | 4 |
| fit | 4 | 4 |
| handoff | 5 | 3 |
| scope | 4 | 4 |
| clarity | 3 | 4 |

Both sides land the same core: digest is the first row of a settings page with its value visible, a sheet with three options that saves on tap, a toast with Undo, no Save, no confirm dialog, no profile form on the way (8 steps to 3). Both derive email and time zone and show them as an info line. Both move delete last, as plain text, separated, with an export-first offer. The differences are in depth and in the edges.

## Defects: X

- `digest` vs `digest-saved`: the same save failure is specified twice with different behaviour (sheet stays open with Retry; toast says "Not saved" with Retry after optimistic change). An engineer must pick one.
- `digest-saved` Undo goes `to: digest` (reopens the sheet) instead of reverting to the previous value in place; one extra tap for the most common mistake.
- `delete`: confirmation is the typed email, which is visible on the settings home and proves intent but not ownership; a password check would be safer for an irreversible action.
- `export-ready` Download goes `to: settings`, leaving the page the moment the file is offered; and `export.states.loading` duplicates `export-building`.
- `landing` is a stub outside the brief with a Sign in self-loop; `success` and `partial` state keys are outside the fixed format.
- Reply is padded with rule codes (SR-1, FL-8) that mean nothing to the reader.

## Defects: Y

- `account`: "each field edits and saves on its own" with no description of how (inline, sheet, modal), no loading state, and Change password asks only the new password, never the current one. The 5% password flow is both unbuildable without guessing and insecure.
- `delete-confirm`: "password or the word DELETE" undercuts its own rationale; the DELETE word proves intent, not ownership, so the ownership claim is only true half the time.
- `deleted`: `actions: []` while `shows` includes a sign-up link; a technical dead end.
- `delete` page has no states (acceptable as a navigation page, but the destructive button lives there and its failure is only handled one screen later).
- `digest-saved` Undo also goes `to: digest` rather than reverting in place.
- Delete is one step longer than X (page, then modal); defensible for <1% and irreversible, but the page already explains everything the modal repeats except the input.

## Winners

**P1: X.** Both reach the same 3-step digest and both keep delete out of the way and reversible-feeling where it should be. X wins on execution: every screen has loading and error with a way out, the `profile` and `password` screens are real (current password required, Save only enabled on change), and the ranked `shows` lists give a visual designer and an engineer something to build from. Y's `account` page is a hand-wave that hides a security gap, and `deleted` ends in an empty action list. Y's reply reads better, but the spec is thinner where it matters.

**Overall: X.**

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 4, "fit": 4, "handoff": 5, "scope": 4}, "clarity": 3}, "Y": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 4, "fit": 4, "handoff": 3, "scope": 4}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
