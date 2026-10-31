## Scores

| Step | Criterion | X | Y |
|---|---|---|---|
| P1 | success | 5 | 5 |
| P1 | flow | 4 | 4 |
| P1 | states | 4 | 5 |
| P1 | ia | 4 | 4 |
| P1 | asks | 4 | 5 |
| P1 | fit | 4 | 5 |
| P1 | handoff | 4 | 4 |
| P1 | scope | 5 | 4 |
| — | clarity | 4 | 4 |

Both specs are close: one `onboarding` flow, `greet` → `picks`, six chat-message screens tagged by moment, greet as text handing off `by: system`, two questions then three cards, routine as steps, followup as text, selfie and budget not asked, three taps to the first picks. The differences are in the edges.

## Defects, X

- `concerns`: the chip set has no "nothing specific" / "just a routine" option, and the only action is "Show my picks" gated on at least one chip. A user with none of the five listed concerns is pushed to pick a false one; the reply says free text works under every block, but the screen does not list a typing action and has no empty state explaining the disabled button.
- `followup`: no self-loop. The brief says the user keeps asking free-text questions; the only actions are "Show my routine" and "Show my picks", which puts option chips under a plain-text answer, exactly where a block adds nothing.
- `picks`: "one short sentence that adds a caveat" is left for the engineer to invent; "typical case" for "not sure" is not defined (Y at least says gentle products).
- `greet` has an error state but no loading; small, but the format asks for it where it can happen.
- Strengths worth keeping: "Question 1 of 2 / 2 of 2" progress, the basis line "For oily skin, acne - change", typing a question straight from `picks` to `followup`, and the empty state that says which answer was relaxed.

## Defects, Y

- `picks`: no path from the cards to `followup`; a user who types "is the serum ok with retinol?" right after the picks has no specified destination (X handles this). The ">10s Still picking, Cancel" state names a Cancel with no `to`.
- `picks` summary line is specified for a known skin type ("For combination skin with dark spots…") but not for "not sure", even though the hint on `skin-type` promises "I'll play it safe".
- `skin-type`/`concerns`: no progress indicator, so the "two quick questions" promise in `greet` is the only cue the user is almost done.
- Scope creep, mild: AI labels on greet and picks, dermatologist hedge, composer hints. Defensible but not requested. "Card skeletons so the layout does not jump" edges toward a visual call.
- Strengths: "Nothing specific" chip removes the forced-choice dead end; the disabled button states its reason; streaming with a Stop button on followup; plain-text fallback if the steps block fails to render; the self-loop on `followup`.

## Winner

P1: Y. Overall: Y.

Both answer every explicit part of the request and reach the picks in the same three taps, so the decision rests on the edges of the flow. Y's "Nothing specific" option, stated disabled-button reason and followup self-loop close the two real gaps in X (a forced concern pick and a text answer with chips under it), and Y's states are more buildable. X's progress labels and its picks→followup path are better and cost it nothing; Y should borrow them, and should give its Cancel a destination.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 4, "fit": 4, "handoff": 4, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 5, "handoff": 4, "scope": 4}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
