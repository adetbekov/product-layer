# Blind review: betke skin quiz, P1

| Step | Side | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|---|
| P1 | X | 5 | 4 | 5 | 4 | 4 | 5 | 4 | 4 | 4 |
| P1 | Y | 5 | 3 | 4 | 4 | 5 | 4 | 4 | 5 | 5 |

Both specs name the `onboarding` flow (greet to picks), tag all six moments, and make the same text/block calls: greet and followup as text, skin-type and concerns as choice blocks, picks as cards, routine as steps. Greet hands over by system in both, so no tap is wasted. The difference is in recovery paths and in the loose ends.

## Defects: X

- `picks`: the chip "Cheaper options" is listed in `shows` but has no action and no target; an engineer has to guess where it goes and what it asks. It also smuggles a budget dimension into a step where nothing was requested about price tiers.
- `skin-type`: "Not sure" and "Skip" both lead to `concerns` with no skin type; two routes for one outcome, and the spec never says what picks a skipped skin type yields (concerns skip is defined, this one is not).
- `skin-type`: the "Analyse a selfie" action jumps straight to `concerns`; where the analysis result is shown and confirmed is not specified, even though the loading state implies the user can keep tapping chips meanwhile.
- `followup`: "Show my routine" is offered even when the user reached followup from `greet` with no picks yet; that chip has nothing to show.
- Throughout: opaque codes (ON-4, GC-5, SR-10) in `purpose` lines are noise for a reader who does not have the key.

## Defects: Y

- `picks` and after: there is no way to change an answer. Once the cards land, the only exits are routine or free text; a user who mistapped "Oily" has no chip to go back, and typed corrections are not an action anywhere.
- `concerns`: at least one concern is mandatory (Done disabled otherwise). A user with none of the five listed is forced to lie or stall; no Skip, no "none of these".
- `followup`: the optional selfie offer is placed inside the text answer to a question like "can I use this with retinol?", which is the wrong moment; the brief puts the selfie near skin-type, where it can actually change the picks.
- `greet`: no action for typing a question straight away, though the brief says the user asks in free text later; `followup` is reachable only after picks.
- `skin-type` error "type the skin type in the input" has no matching action or parsing note.

## Winner

P1: X. Y is leaner (2 taps, clean nav, a crisp "Not sure means sensitive-safe picks" default) and its reply is the clearer of the two, but it leaves the user with no way back after picks and forces a concern. X spends a little more (Back, Skip, "Change my answers", a defined empty state on picks) and keeps the selfie where it belongs, at skin-type, as an optional secondary action with just-in-time permission. X's loose "Cheaper options" chip and the unexplained codes cost it handoff points, but its flow has fewer traps.

Overall: X, by a narrow margin, for the same reasons.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 4, "fit": 5, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 3, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 5}, "clarity": 5}, "winner": {"P1": "X", "overall": "X"}}
```
