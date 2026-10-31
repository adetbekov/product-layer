# Blind review: betke-skin-quiz-r1 (X vs Y)

## Scores

| | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|
| X P1 | 5 | 4 | 5 | 4 | 5 | 4 | 4 | 4 | 4 |
| Y P1 | 5 | 4 | 4 | 4 | 5 | 4 | 3 | 4 | 4 |

Both answer every explicit part: flow `onboarding` (greet -> picks), one chat-message screen per moment with the moment id, and a text/block call on each. The text-or-block decisions are identical and correct on both sides: text for `greet` and `followup`, choice blocks for `skin-type` and `concerns`, cards for `picks`, steps for `routine`. Both ask only skin type and concerns, never phone or language, and both make the greet-to-first-question transition `by: system` so the first tap is already an answer.

## Defects: X

- `concerns`: "back to the skin-type question" is listed under shows but has no matching action; engineer must guess whether it exists.
- `picks`: "Change skin type or concerns" routes to `skin-type`, so changing only concerns forces re-answering skin type. Card "Add / View" is undefined (add to what, view where: sheet or message?).
- `greet` loading copy is muddled ("if slower than ~1 s the skin-type message follows without waiting") since the follow-on is unconditional anyway.
- notes.md and the reply lean on internal codes (GC-6, ON-2, SR-1) a builder does not have, and float a "routine page" and an Apple-style visual pointer, both outside the ask.
- `followup` chips "Show my routine" / "My picks" re-send content already in the thread; slightly against chat grain, though harmless.

## Defects: Y

- Every user action lacks the `by:` field the format requires; only the system transition is tagged. Inferable, but it is a format break on all five block screens.
- `skin-type` has no error state for a failed send of the chip answer; only the selfie failure is covered. `followup` has no empty/off-topic state.
- `greet` error state reads "cannot fail", which is a claim, not a design (the English fallback is the only designed part).
- `picks`: "Details" per card has no stated target surface. "Change my answers" also routes back to `skin-type` for a concerns-only change.
- Step count in reply and notes ("2 user steps") ignores the chip taps themselves; the honest number is 3, or 2 only via Skip.
- `routine` has no return to picks except typing; `followup` has no route to the routine.

## Strengths worth noting

Y's `concerns` is the better single screen: Done shows the count and turns into "Skip, show general picks" at zero, so there is no disabled button. Y's template greeting that needs no model call, and streaming with Stop, show good platform grain. X's state coverage is more complete (send failures, catalog partial/empty with best-sellers fallback, off-topic followup, selfie permission denied), its stated-assumption line with a change chip on `picks` is a clean recovery for "not sure", and its step count is honest.

## Winner

P1: X. Overall: X. The two specs make the same block/text and ask decisions, so the gap is in buildability and recovery: X designs a way out of every failure on every screen and follows the fixed format, while Y drops `by:` on all user actions, leaves a send failure and an off-topic answer undesigned, and overstates its step count. Y's concerns button and template greet are the better micro-decisions and would be worth lifting into X.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 3, "scope": 4}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
