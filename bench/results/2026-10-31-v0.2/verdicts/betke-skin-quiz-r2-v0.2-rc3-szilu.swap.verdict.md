## Scores (P1)

| | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|
| X | 5 | 4 | 4 | 4 | 5 | 4 | 4 | 5 | 4 |
| Y | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 3 | 4 |

Both sides made the same text-or-block calls (text for greet and followup, choice for skin-type and concerns, cards for picks, steps for routine), and both are right. Both ask only the two things the user alone knows. The difference is discipline versus garnish.

## X defects

- `followup` is `render: text` but `shows` lists a chip ("Show my routine") and two chip actions. A chip is a block; either the render tag is wrong or the chips should be dropped (free text already does this). Small format contradiction an engineer will have to resolve.
- `picks`: card "action" is never named (open? add? compare?). Also "which type was assumed" for Not sure is left to the notes ("a typical skin type") with no actual default stated.
- `concerns` carries a "Back" chip to `skin-type`; in a chat the previous message is still on screen, so this is a slightly non-chat pattern and an extra control, though harmless.
- `greet` has no loading state; minor since it is text, but the first message is where a blank chat is most felt.

## Y defects

- Claims "two taps to picks" in reply and notes; the spec actually needs three (skin chip, concern chip, confirm). Even "Nothing in particular" still requires a confirm tap, which could have advanced by itself. X counted honestly and offers a real 2-tap path via Skip.
- `skin-type` adds an "Analyse a selfie" path (not requested in P1) with no states: camera permission denied, photo unreadable, analysis fails, and "the user confirms the pre-filled type" has no screen or transition to live in. An undesigned sub-flow in the done-critical path.
- `concerns`: "Nothing in particular" sits inside a multi-select set with no exclusivity rule stated; the engineer has to guess whether it clears other chips.
- Format: no `nav` key, and user actions carry no `by:` field (only greet's system transition does). The brief's format treats `by` as the cost signal.
- `picks` "Edit my answers" returns to `skin-type`, forcing the user to re-answer both questions even when only concerns changed.
- Scope creep: AI labels, safety line, dermatologist note, streaming Stop control, fallback greeting. Several are good product instincts, but none were asked for in P1 and together they blur what was actually decided.

## Winner

**P1: X. Overall: X.** Y shows the better chat instinct (a chip tap becomes the user's message, skeletons so the layout does not jump, permission asked in context, error states that keep the cards on screen), which is why it takes fit. But X answers exactly the request in the required format, counts its own steps honestly, and leaves no undesigned branch, while Y's extras introduce a selfie path with no failure handling and a mislabelled step count. For a first-pass flow spec meant to hand to visual and engineering, X is the one you can build from without a second round of questions.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 4, "flow": 4, "states": 4, "ia": 4, "asks": 4, "fit": 5, "handoff": 4, "scope": 3}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
