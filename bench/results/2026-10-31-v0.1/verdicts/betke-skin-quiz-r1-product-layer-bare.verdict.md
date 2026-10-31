# Blind review: betke skin quiz, round 1 (X vs Y)

## Scores

| Step | Criterion | X | Y |
|---|---|---|---|
| P1 | success | 5 | 4 |
| P1 | flow | 5 | 3 |
| P1 | states | 5 | 3 |
| P1 | ia | 5 | 3 |
| P1 | asks | 5 | 4 |
| P1 | fit | 4 | 3 |
| P1 | handoff | 4 | 3 |
| P1 | scope | 4 | 5 |
| side | clarity | 4 | 3 |

## Defects

**X**
- `followup`: declared `render: text` but shows "Next-action chips" (Show my routine, My picks). That is a block by the spec's own rule; either make it `block: choice` or drop the chips. Same tension is milder on `picks`, where cards and a chip row share one message.
- `picks`: each card carries an "Add / View action". Nothing in the brief has a cart or a detail surface; "Add" is unrequested and "View" has no destination screen.
- `skin-type`: the selfie path jumps straight to `concerns` with "user may correct it", but no state or message shows the analysed type for confirmation, so the correction moment is unspecified.
- Spec and notes cite codes (GC-6, ON-2, SR-1) with no key, and the notes name an "Apple-style skill" for visuals, a nudge toward visual territory the product layer should leave alone.

**Y**
- `concerns`: Done is enabled only after at least one chip; there is no Skip. A user with none of the five concerns (or who just wants a routine) has no honest way to the picks. The reply's "2 steps to picks" also undercounts: chip tap plus Done is two taps on this screen alone.
- `picks`: "Open card" transitions `to: picks`, a self-loop with no detail surface defined (sheet? new message?). After picks there is no way to change skin type or concerns; the only exits are the routine chip or starting over.
- No `nav` section, although the request names nav. `followup` is reachable only from `routine` by the listed actions, and lists the user's own question as an `asks` field, which muddles what "asks" means.
- `skin-type` and `concerns` have no empty state (nothing chosen, Not sure chosen with no concerns), and `routine` has no partial state for a product used only once a day.

## Winner

**P1: X. Overall: X.**

X answers every part of the request (flow, six tagged moments, render per screen, nav) and designs the exits Y leaves out: Skip on concerns, a stated assumption with a change chip on picks, Back to picks from the routine, and selfie failure falling back to chips. Y is tighter in scope and its text/block calls are internally consistent, but it has a hard stop for users with no listed concern, an undefined card-detail destination, and no way to revise answers. X's flaws (chips on a text message, an unrequested Add action, opaque codes) are fixable in a pass; Y's are structural gaps in the flow.

```json
{"X": {"P1": {"success": 5, "flow": 5, "states": 5, "ia": 5, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 4, "flow": 3, "states": 3, "ia": 3, "asks": 4, "fit": 3, "handoff": 3, "scope": 5}, "clarity": 3}, "winner": {"P1": "X", "overall": "X"}}
```
