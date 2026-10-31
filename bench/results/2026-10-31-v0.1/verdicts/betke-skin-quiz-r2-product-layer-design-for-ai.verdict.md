# Blind review: betke-skin-quiz-r2 (P1)

| Step | Criterion | X | Y |
|---|---|---|---|
| P1 | success | 5 | 5 |
| P1 | flow | 5 | 3 |
| P1 | states | 5 | 4 |
| P1 | ia | 4 | 4 |
| P1 | asks | 5 | 5 |
| P1 | fit | 5 | 4 |
| P1 | handoff | 4 | 3 |
| P1 | scope | 4 | 5 |
| - | clarity | 4 | 4 |

## Defects

**X**
- `skin-type`: both "Skip" and "not sure" exist and both go to `concerns`; the difference is never stated, so copy and engineering must guess which one the picks treat as unknown. One of them should go.
- `skin-type`: the "Analyse a selfie" action jumps straight to `concerns`; the detected skin type is never shown or confirmed, so the user cannot correct a wrong read before answering question 2.
- `greet` -> `followup` by free text before any picks exist, while `followup` is specified as "grounded in the chosen products". The stated-assumption line covers it loosely, but the screen does not say what it answers with when there are no picks yet.
- `picks`: "Cheaper options" chip introduces a budget path nobody asked for and no screen defines it (listed in shows, missing from actions).
- Rule codes (ON-4, GC-5...) in `purpose` are noise for a visual designer or engineer who does not have that document.

**Y**
- `picks`: the selfie chip appears in `shows` but has no action, no target, no states; an engineer cannot build it, and it sits after the picks where a photo can no longer change them without a path back.
- `concerns`: "echo of the skin type so it can be corrected", yet there is no Back action and no edit action; correction is only implied through free text. Same for `picks`: no "change my answers" exit, so a wrong skin type is a mild dead end once the cards are out.
- `concerns`: at least one chip is required (button disabled when empty, no Skip). A user with no listed concern must type free text; the brief's "several allowed" did not mean "at least one required".
- `routine` and `followup` have no action back to picks or routine; recoverable only by scrolling, which the spec should say.
- `skin-type` error covers only an unmappable typed answer, not a failed send.

## Winner

**P1: X. Overall: X.** Both land on the same correct shape: greet as text handed over by the system, two chip blocks, cards, steps, text follow-up, three taps to picks, only the two facts the user alone knows. X wins on completeness of the paths around that spine: Back, Skip, "Change my answers", a selfie that is specified with permission, loading, cancel and failure states, and a Retry that keeps answers at every screen. Y is tighter in scope and its typed-answer-to-chip mapping is a nice use of the chat grain, but it leaves the selfie chip undefined and gives the user no way to correct an answer once past it. X's extra "Cheaper options" chip and the Skip/not-sure duplication are the main things to trim.

```json
{"X": {"P1": {"success": 5, "flow": 5, "states": 5, "ia": 4, "asks": 5, "fit": 5, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 3, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 3, "scope": 5}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
