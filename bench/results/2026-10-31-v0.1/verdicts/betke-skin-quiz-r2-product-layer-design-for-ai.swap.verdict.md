# Blind review: betke skin quiz, P1

| Step | Side | success | flow | states | ia | asks | fit | handoff | scope |
|---|---|---|---|---|---|---|---|---|---|
| P1 | X | 5 | 4 | 4 | 4 | 5 | 5 | 4 | 5 |
| P1 | Y | 4 | 4 | 5 | 4 | 5 | 4 | 3 | 3 |

Clarity: X 4, Y 4.

## Defects

**X**
- `picks`: the optional selfie chip is listed under `shows` but has no action and no target. Offering a selfie *after* the picks also adds little; it would only help if it could refine the skin type before ranking.
- `concerns`: the skin-type echo "so it can be corrected" has no action behind it. There is no path from `concerns` or `picks` back to `skin-type`, so a mistaken tap can only be fixed by typing.
- `concerns`: no Skip. The disabled "Show my picks" means a user with no listed concern must pick a chip or type; acceptable but a tiny forced step.
- `followup` only loops to itself; fine for a chat, but no chip back to `routine`.

**Y**
- No `nav` section, which the fixed format calls for.
- `picks`: "Cheaper options" chip has no action and is an unrequested budget feature; `skin-type`: "Skip" duplicates "not sure".
- `skin-type`: "Analyse a selfie" transitions straight to `concerns` while the loading state says the chips "stay tappable meanwhile". What happens when the analysis result lands after the user has moved on is not specified; an engineer must guess.
- `greet` allows free text to `followup`, whose answers are "grounded in the chosen products" that do not exist yet.
- `picks` "Change my answers" restarts at `skin-type` rather than the answer in question; "Back" chips sit oddly in a chat, where the grain is a new message, not undo.
- Spec cites codes (ON-4, GC-5, SR-10, GC-12) from a rulebook the reader does not have; noise for a handoff.

## Winner

**P1: X. Overall: X.** Both specs land on the same correct skeleton: text greet handed over by system, two chip blocks, cards, steps, text follow-up, three taps to the first picks, and only the two questions the user alone can answer. Y has the richer state coverage (selfie loading with Cancel, "Change my answers" on an empty catalog) and the better selfie placement, but it leaks a dangling "Cheaper options" feature, an ambiguous selfie transition, undecodable rule codes and no nav, so a builder would have to guess more often. X is tighter and fully buildable apart from one dead selfie chip and a missing correction path.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 5, "handoff": 4, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 4, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 3, "scope": 3}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
