# Blind review: betke-skin-quiz-r1 (X vs Y)

## Scores

| P1 | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|
| X | 5 | 3 | 4 | 3 | 4 | 4 | 4 | 5 | 4 |
| Y | 5 | 5 | 5 | 4 | 5 | 4 | 4 | 3 | 4 |

Both sides make the same text-or-block calls, and they are the right ones: `greet` and `followup` as text, `skin-type` and `concerns` as choice chips, `picks` as cards, `routine` as steps. Both hand the first question over `by: system`, so the first picks cost 1 skin-type tap + concern chips + one confirm. Both ask only skin type and concerns, which only the user knows.

## Defects: X

- `picks`: action "Open card (details, ingredients)" transitions to `picks` itself. Where details open (sheet? expanded card?) is unspecified, so the engineer guesses.
- `picks`: no way to change an answer. A mis-tapped skin type is locked in; the only forward move is "How do I use them?".
- `concerns`: Done requires at least one chip and there is no Skip. A user with none of the five concerns can only escape via the error-state fallback (typing), which is not a designed path.
- `followup` is reachable only from `routine`. The brief says free text comes later from anywhere; `greet`, `skin-type` and `picks` have no free-text exit.
- `skin-type` "Not sure": "picks rely on concerns only" is a vague rule for the catalog filter; no stated assumption shown to the user.
- Reply claims "2 steps" to picks; it is 3 taps minimum (skin chip, concern chip, Done).

## Defects: Y

- `picks`: cards carry an "Add / View action". "Add" to what? No cart or saved list exists in the brief; this is unrequested and undefined.
- `skin-type`: the selfie sub-flow (camera permission, analysis, retake) is pulled into the first session. The brief marks the selfie optional; it is reasonable as a secondary link but adds surface area nobody asked for.
- State labels are misused: `skin-type.empty` describes selfie decline, `skin-type.loading` and `concerns.loading` describe non-loading behaviour. `greet.loading` ("if slower than ~1 s the skin-type message follows without waiting for a tap") is hard to parse.
- `concerns` mentions "back to the skin-type question" in `shows` but has no matching action.
- Notes and reply cite rubric codes (GC-6, ON-2, SR-1) the reader cannot resolve, and the notes name a visual skill, which the spec should stay out of.
- `nav` and the "routine page" open question are outside the six moments asked for.

## Winner

**P1: Y. Overall: Y.** The two specs agree on every render decision and on the minimum tap count, so the difference is in the paths around the happy path. Y has no dead ends: Skip on concerns, a stated assumption with a "change" chip after "Not sure", free text from every message, and picks/routine/followup linked both ways; its empty/partial states (fewer than 3 matches, off-topic question) are the ones that actually happen. X is tighter in scope and cleaner to read, but it locks the user's answers, leaves the card-detail destination undefined, and offers no exit for someone with no listed concern. Y's scope creep (Add action, selfie sub-flow, rubric codes) is real and costs it points, but not enough to outweigh a flow the user can recover from.

```json
{"X": {"P1": {"success": 5, "flow": 3, "states": 4, "ia": 3, "asks": 4, "fit": 4, "handoff": 4, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 5, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 3}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
