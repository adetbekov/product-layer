# Verdict: betke-skin-quiz-r2 (X vs Y)

## Scores

| Step | Side | success | flow | states | ia | asks | fit | handoff | scope |
|---|---|---|---|---|---|---|---|---|---|
| P1 | X | 5 | 5 | 5 | 4 | 5 | 5 | 4 | 4 |
| P1 | Y | 5 | 4 | 3 | 4 | 5 | 4 | 3 | 4 |

Clarity: X 4, Y 4.

Both answer the request fully: flow `onboarding` from `greet` to `picks`, one chat-message screen per moment with the moment id, and a text/block call on each. Both make `greet` plain text handed over by `system`, so the user reaches picks in two taps (type chip, then "Show my picks"), and both accept free text in place of chips. The text-or-block calls are identical and right on both sides: chips for the two questions, cards for picks, steps for routine, text for greet and followup. Both ask only skin type and concerns, which only the user knows.

## Defects

**X**
- `nav: member: [Chat, Settings]` is unrequested, and Settings has no screen behind it.
- `concerns` adds a "Pick up to 3" cap the brief does not impose ("several allowed"); it is a small unexplained constraint.
- `picks` → "Change my answers" lands on `skin-type`, so fixing only concerns costs re-answering both (the `concerns` screen does offer "Change skin type", so the reverse path is cheap).
- Minor: free-text answers on `skin-type` go straight to `concerns` with no echo of how the text was interpreted; the echo only appears in `concerns` ("Got it, sensitive"), which partly covers it.

**Y**
- `picks` shows a "Cheaper options" chip that has no action and no target screen: a dead end in the spec and an unrequested feature.
- `picks` and `routine` list chips in `shows` that do not match `actions` ("Change my answers" and "Back to picks" are actions but not chips, "Cheaper options" is a chip but not an action). An engineer has to guess.
- `concerns` has no loading state; `routine` has no empty state; `followup` has no state for "the catalog cannot answer" (X designs all three).
- `skin-type` "Analyse a selfie" jumps straight to `concerns`: the detected type is never shown or confirmable, and the states on that screen only cover the selfie path, not a failed chip save. "Skip" next to "Not sure" is two chips for the same choice.
- Codes like `GC-8`, `ON-4`, `SR-10` pepering purposes and notes point to a rulebook the visual designer and engineer do not have; they are noise in a handoff document. notes.md's tap count ("3 user actions ... so 2-3") contradicts itself.

## Winners

**P1: X.** Both reach the first picks in two taps with the same, correct text-vs-block calls, so the difference is finish. X designs empty, loading and error on every screen with a way out of each, keeps shows and actions consistent, and writes copy an engineer can paste. Y leaves a dangling "Cheaper options" chip, mismatched chips vs actions, three missing states and opaque rule codes. X's stray `nav` block and "up to 3" cap are smaller faults than Y's gaps.

**Overall: X**, for the same reasons; a single step was reviewed.

```json
{"X": {"P1": {"success": 5, "flow": 5, "states": 5, "ia": 4, "asks": 5, "fit": 5, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 3, "ia": 4, "asks": 5, "fit": 4, "handoff": 3, "scope": 4}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
