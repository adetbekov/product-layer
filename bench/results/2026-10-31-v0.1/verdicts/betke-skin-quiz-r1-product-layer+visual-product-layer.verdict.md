# Blind review: betke-skin-quiz-r1 (X vs Y)

## Scores

| Step | Side | success | flow | states | ia | asks | fit | handoff | scope |
|------|------|---------|------|--------|----|------|-----|---------|-------|
| P1 | X | 4 | 4 | 4 | 4 | 5 | 4 | 4 | 4 |
| P1 | Y | 5 | 4 | 4 | 4 | 5 | 5 | 4 | 5 |

Clarity: X 4, Y 4.

Both specs are structurally almost identical: `onboarding` from `greet` to `picks`, six chat-message screens tagged by moment, `text` for greet and followup, `block` (choice / choice / cards / steps) for the middle four, greet handed to skin-type `by: system`, and 3 user taps to the first picks (2 with skip). The text-or-block calls are right on both sides. The differences are at the edges.

## Defects: X

- `picks`: the "Cheaper options" chip is shown but has no action and no destination; same for the "Widen search" chip in the partial state. An engineer has to invent where they go. The budget question itself is unrequested scope.
- `routine`: "Save routine" is shown as a chip and its action leads to `followup`, which is a misroute; notes admit it is a placeholder. "Back to picks" is an action but not listed in shows.
- `skin-type`: a separate "Skip" link next to a "Not sure" chip is redundant; one escape hatch is enough.
- `picks`: "one primary action per card" is undefined.
- No `nav` section (minor; the request did not spell it out).
- Strengths: rank annotations on every shown element, selfie loading with Cancel while chips stay tappable, a sensitive-skin caution in `routine`.

## Defects: Y

- `concerns`: "back to the skin-type question" appears in shows but has no matching action.
- `skin-type`: no loading state for selfie analysis (the one place in the flow that genuinely waits); the selfie-denied case is filed under `empty` rather than `error`.
- `greet` loading: "if slower than ~1 s the skin-type message follows without waiting for a tap" is ambiguous since the next message always follows by system anyway.
- `skin-type` partial: "Not sure" silently assumes combination skin; stated with a change chip, but X's "avoid strong actives" is the safer default.
- `picks`: "Add / View" on cards presumes a cart the brief never mentions.
- Strengths: every chip on every screen maps to an action; free-text answer accepted on `skin-type`; chips toggle locally and only the confirm sends; `nav: [Chat]` present; nothing unrequested.

## Winner

P1: Y. Overall: Y.

The two designs make the same core decisions, so the verdict rests on consistency and restraint. Y's action table is closed (every visible chip has a destination) and it adds nothing beyond the six moments, while X leaves three chips dangling or misrouted and smuggles in budget and save-routine features it then declares out of scope. X is better documented for a visual designer (rank ordering, richer selfie states), which keeps it close, but Y is the one an engineer could build without a follow-up question.

```json
{"X": {"P1": {"success": 4, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 5, "handoff": 4, "scope": 5}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
