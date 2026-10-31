## Scores

| P1 | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|
| X | 5 | 5 | 5 | 4 | 5 | 5 | 5 | 5 | 5 |
| Y | 4 | 4 | 3 | 4 | 4 | 4 | 3 | 5 | 4 |

Both sides made the same core calls, and they are the right ones: `greet` is text and hands off by system, `skin-type` and `concerns` are choice blocks, `picks` is cards, `routine` is steps, `followup` is text. Both reach picks in three user actions with only two questions, both of which only the user can answer. The difference is in how completely each one is specified.

## Defects: X

- `picks` -> "Change my answers" lands on `skin-type`, so a user who only wants to swap a concern re-answers both questions. A direct route to `concerns` would save a step.
- `greet` loading prescribes a "typing indicator for at most ~1s" on a fixed template. That is a fabricated delay and a timing choice that edges toward motion design.
- `followup` error says "the question stays in the composer", but in a chat the sent message is already in the thread; the retry mechanic needs one more sentence.
- Free text typed before the questions finish is handled only in notes.md, not as a spec state or action.

## Defects: Y

- `skin-type` and `concerns` have no loading state. After a tap the user needs to see the chip lock and a typing indicator for the next message; this is the most frequent transition in the session and it is unspecified.
- `concerns` forces at least one concern and offers no "nothing specific" / "general care" option. A user with no particular problem has to pick a false concern to get picks.
- `followup` is `terminal: true` with no actions, so on paper there is no "ask another question" loop, while notes.md says the chat stays open. The spec and the notes disagree; an engineer has to guess.
- Actions omit `by:` throughout, so the only system transition (`greet`) is marked but user actions are left implicit. `greet` copy is "one or two sentences" with no wording; `picks` cards do not say which fields carry the personalisation. Thinner handoff than X.
- `picks` loading is a bare status line with no skeleton or slow-path fallback; X's "still picking after 10s, Cancel" is the kind of detail that prevents a hang with no exit.

## Winner

P1: **X**. Overall: **X**. Same shape of flow, same tap count, same text-or-block decisions, but X specifies every state on every screen with concrete copy and a way out, adds the "Nothing specific" escape so no user is forced into a false answer, and keeps followup as an explicit loop. Y's spec is sound but leaves the two most-used transitions without loading states, contradicts itself on whether followup ends the session, and would need a round of questions before a build.

```json
{"X": {"P1": {"success": 5, "flow": 5, "states": 5, "ia": 4, "asks": 5, "fit": 5, "handoff": 5, "scope": 5}, "clarity": 5}, "Y": {"P1": {"success": 4, "flow": 4, "states": 3, "ia": 4, "asks": 4, "fit": 4, "handoff": 3, "scope": 5}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
