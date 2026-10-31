# Blind review: betke-skin-quiz-r1 (P1)

| Step | Side | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|---|
| P1 | X | 5 | 4 | 4 | 4 | 5 | 4 | 4 | 5 | 5 |
| P1 | Y | 5 | 5 | 5 | 5 | 5 | 4 | 4 | 3 | 4 |

Both sides make the same text-or-block calls (greet and followup text; skin-type single chips, concerns multi chips with a confirm, picks cards, routine steps), both reach picks in 3 taps with greet advanced by system, and both ask only skin type and concerns. The differences are in edge handling and discipline.

## Defects: X

- `concerns`: no Skip. A user with no listed concern is forced to pick one before "Show my picks" enables; "not sure" exists for skin type but there is no equivalent here.
- `routine`: the only way onward is to type; no chip back to picks or to ask, which breaks the chip-driven grain the rest of the flow sets.
- `followup`: action "Back to the picks" has no trigger in `shows` (no chip), so an engineer has to guess how it is reached.
- `picks` empty state covers "fewer than 3" but not zero matches ("show what matched" is nothing).
- `concerns` shows "Chip for the skin type just chosen is echoed in the message text" — chip or text? Ambiguous.
- `skin-type` has no loading state for the tap-to-next-question latency; free text "works at any point" per the reply, but `skin-type`/`concerns` list no free-text action.

## Defects: Y

- `picks`: cards carry an "Add / View" action with no target; the brief has no cart or product page. Unrequested and unbuildable as written.
- `skin-type`: "Use a selfie instead" goes straight to `concerns` with "user may correct it" but no screen or state shows where the correction happens.
- `followup` is `render: text` yet shows two chips; that is a block by this product's own vocabulary, so the render decision is contradicted.
- `greet` loading: "if slower than ~1 s the skin-type message follows without waiting for a tap" conflicts with the by-system transition that already happens regardless.
- Rule codes (GC-6, ON-2, SR-1) leak into the spec and reply with no legend; notes name an "Apple-style skill" and propose a routine page, both outside the ask. `concerns` lists a "back" link in `shows` with no matching action.

## Winners

**P1: Y.** Y's flow has a way out at every edge: Skip on concerns, zero-match fallback to best-sellers, off-topic followup handled, Back-to-picks chips on routine and followup, progress "1 of 2 / 2 of 2" so the user knows the quiz is short. X is tighter in scope and its reply reads cleaner, but X leaves a forced concern, a chip-less routine and an untriggerable action — gaps a builder must fill. Y's creep (Add/View, selfie correction, rule codes) is real but is a cut, not a redesign.

**Overall: Y**, by a narrow margin. Same turns-to-value, same ask discipline, same block calls; Y wins on completeness of states and exits, X on restraint and prose. Completeness of the flow matters more in a flow spec.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 5}, "clarity": 5}, "Y": {"P1": {"success": 5, "flow": 5, "states": 5, "ia": 5, "asks": 5, "fit": 4, "handoff": 4, "scope": 3}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
