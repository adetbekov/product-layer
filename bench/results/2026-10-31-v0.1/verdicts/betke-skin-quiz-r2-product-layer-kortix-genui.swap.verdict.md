# Blind review: betke skin quiz, P1

## Scores

| Step | Side | success | flow | states | ia | asks | fit | handoff | scope |
|---|---|---|---|---|---|---|---|---|---|
| P1 | X | 5 | 5 | 4 | 4 | 5 | 5 | 4 | 4 |
| P1 | Y | 5 | 4 | 4 | 4 | 4 | 4 | 5 | 5 |

Clarity: X 4, Y 4.

## Defects

**X**
- `picks`: the chip "Cheaper options" is shown but has no action target; an engineer has to guess what it does. Unrequested as well.
- `skin-type`: "Analyse a selfie" transitions straight to `concerns`, so the user never sees or confirms the detected skin type; "Skip" duplicates "Not sure" and adds a chip without adding a choice.
- Across screens: purposes cite opaque codes (ON-4, GC-5, SR-10, `notice.error`) that are not in the brief; a reader without that rulebook gains nothing from them.
- `skin-type` error covers only the selfie path; a plain send failure on a chip tap is not designed (Y has it).

**Y**
- `concerns`: "Show my picks" is enabled only after at least one chip and there is no Skip or "none of these", so a user with no listed concern must pick a false one to reach the picks. That is the one real gate before the goal.
- `picks`: no way to change answers after the picks (no Back, no "Change my answers"); the only route is free text, which is not listed as an action from `greet`, `skin-type` or `concerns` either.
- `followup`: the only chip loops back to `followup`; no chip returns to routine or picks (recoverable by scrolling, but unstated).
- The brief lists a photo request button and an optional selfie; Y drops it entirely with a note. Defensible for scope, but it leaves the photo block undefined for the engineer.
- Reply point 5 talks about which skill rules were or were not followed, which is process talk, not a decision the reader needs.

## Winners

**P1: X.** Both reach the picks in the same minimal path (greet costs nothing by system, one tap for skin type, chips plus confirm for concerns, three cards). Text-or-block calls are identical and correct on both sides: text for greet and followup, choice for the two questions, cards for picks, steps for routine. X wins on the quiz's exits: Skip on both questions, Back, "Change my answers" from an empty or wrong result, free text accepted from the greeting onward, and the optional selfie placed where the brief put it with permission asked only on tap. Y is the cleaner document to build from (no foreign codes, concrete copy, "Not sure stored as unknown", spinner on the confirm button) but forces a concern and offers no revision path once the picks land.

**Overall: X**, narrowly. Its noise (guideline codes, a dangling chip) is easier to strip than it is to add Y's missing escape hatches, and the brief's core ask, reaching three picks while asking only what the user alone knows, is met more gracefully by X.

```json
{"X": {"P1": {"success": 5, "flow": 5, "states": 4, "ia": 4, "asks": 5, "fit": 5, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 4, "fit": 4, "handoff": 5, "scope": 5}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
