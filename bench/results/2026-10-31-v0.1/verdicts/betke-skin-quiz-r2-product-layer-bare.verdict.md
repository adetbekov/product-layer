# Blind review: betke skin quiz r2 (X vs Y)

## Scores

| Step | Side | success | flow | states | ia | asks | fit | handoff | scope |
|---|---|---|---|---|---|---|---|---|---|
| P1 | X | 5 | 4 | 5 | 4 | 5 | 4 | 4 | 5 |
| P1 | Y | 4 | 4 | 3 | 4 | 5 | 5 | 3 | 3 |

Clarity: X 4, Y 4.

## Defects

**X**
- `skin-type` / `concerns`: a mistaken chip tap has no way back. `picks` has no "change my answers" action; the only recovery is the free-text prompt in the empty state, which is not the same case.
- `picks` / `routine`: actions "Show me how to use them" and "Ask a question in the input" do not say whether they are chips under the block, a button on the cards, or just something the user is expected to type. An engineer has to guess.
- `concerns`: the disabled-until-one-chip Done rule lives in `shows`, not in an `empty` state; small, but states is where it belongs.
- Reply and notes claim "2 user steps to picks"; the real minimum is 3 taps (skin chip, at least one concern chip, Done). Harmless but inaccurate.

**Y**
- `picks`: "Cheaper options" chip is shown but has no action and no target screen. It is a dead affordance and implies an unrequested budget feature.
- `skin-type`: the selfie action transitions straight to `concerns`, while the loading state says the chips "stay tappable meanwhile" on `skin-type`. The two statements contradict each other, and the spec does not say what the user sees if the analysis fails after they have already moved on.
- `skin-type`: loading and error cover only the selfie path; nothing covers the question block itself failing to arrive. `concerns` has no loading state at all.
- `skin-type`: three ways to not answer (Not sure, Skip, selfie). Skip duplicates Not sure and, unlike the concerns Skip, does not say what the picks assume.
- `greet`, `skin-type`, `concerns`, `picks`, `followup`: purpose and shows fields cite codes (ON-4, GC-5, SR-10, GC-12) and a component "notice.error" that are defined nowhere in the deliverable. For a visual designer or engineer this is noise they must ask about.
- `followup` is `render: text` yet carries a chip-style action "Show my routine"; either the render is wrong or the action is.
- No `nav` section, which the request's success criterion names explicitly.

## Winners

**P1: X.** Both sides made the same text/block calls and both reach the picks in two questions with no dead ends, so the call comes down to buildability. X's spec is complete and internally consistent: every screen has loading and error with a way out, the asks are exactly skin type and concerns, and nothing unrequested slipped in. Y shows better chat grain (named next-step chips, status lines for costly waits, answers kept on retry, a back path) but undermines it with a dead "Cheaper options" chip, a contradictory selfie path, missing loading states, and undefined reference codes scattered through the spec.

**Overall: X.** Only one step, so the same verdict holds. If Y had dropped the budget chip and the reference codes and reconciled the selfie transition, its richer recovery paths would have made it the better spec.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 4, "flow": 4, "states": 3, "ia": 4, "asks": 5, "fit": 5, "handoff": 3, "scope": 3}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
