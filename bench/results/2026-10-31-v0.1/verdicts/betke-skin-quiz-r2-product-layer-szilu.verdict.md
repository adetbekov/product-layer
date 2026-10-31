# Blind review: betke-skin-quiz-r2 (X vs Y)

## Scores

| Step | Side | success | flow | states | ia | asks | fit | handoff | scope |
|---|---|---|---|---|---|---|---|---|---|
| P1 | X | 4 | 4 | 4 | 4 | 4 | 4 | 3 | 3 |
| P1 | Y | 5 | 5 | 5 | 4 | 5 | 5 | 4 | 4 |

Clarity (final message): X 4, Y 4.

## Defects

**X**
- `picks`: `shows` lists a chip "Cheaper options" that has no action and no target screen; it is a dead chip, and it smuggles a budget feature nobody asked for. Meanwhile `actions` has "Change my answers" that the `shows` block never renders. Shows and actions disagree, so an engineer has to guess.
- `routine`: same mismatch, "Back to picks" is an action but the visible chips are only "Ask a question".
- `skin-type`: both "Not sure" and "Skip" lead to `concerns` with the same meaning. The brief already gives "not sure"; the extra Skip is one more thing to read for no new outcome.
- `concerns`: no loading state, although this is the tap that triggers the catalog query; the loading on `picks` only partly covers it.
- Every `purpose` cites codes (GC-8, ON-2, SR-10) that exist nowhere in the deliverable. A visual designer or engineer cannot resolve them.
- notes.md: "3 user actions ... so 2-3" contradicts itself on the one number the brief cares about.
- Selfie action on `skin-type` goes straight `to: concerns`; the analysis result (detected type, confirm/override) has no place to land except a loading line.

**Y**
- `nav: member: [Chat, Settings]`: Settings is unrequested and never described.
- `greet`: `shows` says free text works from the first second, but there is no user action from `greet` to `followup` (X has it).
- `concerns`: "Pick up to 3" is an invented cap; the brief only says several allowed. Small, but it is a constraint without a reason.
- `picks` / `skin-type` loading states carry timing targets ("under 1s", "first progress within 1s") that lean toward engineering budgets rather than flow decisions.
- Selfie is left out entirely. Defensible for fewest steps, and the notes say where it would go later, but the photo-request block from the brief appears nowhere in the spec.

## Text-or-block calls
Both sides make the same correct calls: greet text with a system hand-off, two choice blocks, cards for picks, steps for routine, text for follow-up. Both reach picks in two taps (X optionally three with the selfie). Both ask only skin type and concerns, which only the user knows. The difference is in execution: Y's shows and actions match on every screen, every screen has all three states where they apply, and the chat grain is used more deliberately (chips lock and highlight on tap, previous answer echoed in the next question, streamed answer with a Stop button, skeleton cards, AI label on the picks). X's extras (selfie, Cheaper options) add surface without closing the loop on either.

## Winner

- P1: **Y**
- Overall: **Y**

Y answers the request with nothing dangling: every chip it shows has a transition, every screen has states with a way out, and the spec is self-contained enough to hand to a designer and engineer as is. X has the same skeleton and a sound reading of the brief, but the unexplained GC/ON codes, the shows-vs-actions mismatches, and a dead "Cheaper options" chip mean the build would stall on questions Y's spec already answers.

```json
{"X": {"P1": {"success": 4, "flow": 4, "states": 4, "ia": 4, "asks": 4, "fit": 4, "handoff": 3, "scope": 3}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 5, "states": 5, "ia": 4, "asks": 5, "fit": 5, "handoff": 4, "scope": 4}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
