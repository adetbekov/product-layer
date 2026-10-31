# Blind review: betke-skin-quiz-r1 (X vs Y)

## Scores (P1)

| criterion | X | Y |
|---|---|---|
| success | 5 | 4 |
| flow | 5 | 4 |
| states | 5 | 4 |
| ia | 4 | 4 |
| asks | 5 | 5 |
| fit | 4 | 4 |
| handoff | 4 | 4 |
| scope | 4 | 5 |
| clarity (per side) | 4 | 4 |

Both sides made the same core calls, and they are the right ones: `greet` text with a `by: system` hop into `skin-type`, chips for the two questions, cards for `picks`, steps for `routine`, text for `followup`. Both ask only skin type and concerns, never phone or language. Both reach picks in 3 user actions. The differences are at the edges.

## Defects: X

- `picks`: each card carries an "Add / View action". There is no cart or product page in the brief or the spec, so "Add" is unrequested scope and "View" has no destination; an engineer would have to guess.
- `concerns`: `shows` lists a secondary "back to the skin-type question", but `actions` has no such transition. Spec is internally inconsistent.
- `greet`: the loading state says "if slower than ~1 s the skin-type message follows without waiting for a tap", yet the system action already does that unconditionally. The sentence confuses more than it specifies.
- `followup` is `render: text` but ships "Next-action chips". Harmless, but blurs the text/block rule the spec itself states.
- Rule codes (GC-6, SR-1, ON-2) appear in the spec and reply with no legend; noise for a reader outside the authoring skill.

## Defects: Y

- `concerns`: "Show my picks" is disabled until a chip is selected and there is no Skip. A user with none of the five concerns has no in-block way forward; free text to `followup` is claimed in the reply but not listed as an action here, and it would not deliver picks.
- `skin-type` and `concerns` have no loading state: nothing says what the user sees between a tap and the next message.
- `picks` empty state covers "fewer than 3" but not zero matches.
- `routine` offers no chip back to picks or to ask; `followup` lists "Back to the picks" as an action while `shows` has no control for it.
- No `nav` section, which the success criterion names.
- `notes.md` says the selfie is "offered later in follow-up", but `followup` never mentions it.

## Winner

**P1: X. Overall: X.** The two specs are close, but X closes the gaps Y leaves open: a Skip on concerns so nobody is stuck, a stated assumption with a change chip when the user says "not sure", progress labels, loading and partial states on every screen, and the optional selfie placed where it costs nothing. X loses a point on scope and handoff for the undefined "Add / View" card actions and the stray rule codes; Y is tighter in scope but its missing Skip, missing loading states and unlisted controls would send the engineer back with questions.

```json
{"X": {"P1": {"success": 5, "flow": 5, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 4, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 5}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
