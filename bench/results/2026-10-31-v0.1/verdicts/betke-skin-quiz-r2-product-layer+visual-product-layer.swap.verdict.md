# Blind review: betke skin quiz, X vs Y

## Scores (P1)

| criterion | X | Y |
|---|---|---|
| success | 5 | 5 |
| flow | 4 | 4 |
| states | 5 | 4 |
| ia | 4 | 4 |
| asks | 5 | 5 |
| fit | 4 | 5 |
| handoff | 4 | 3 |
| scope | 3 | 5 |
| **sum** | **34** | **35** |
| clarity (per side) | 4 | 4 |

Both sides made the same core calls, and made them right: `greet` is text and hands over to `skin-type` by system, two choice blocks before value, cards for picks, steps for routine, text for followup, selfie optional and camera asked only on tap, budget deferred to a "Cheaper options" chip. Three taps to the first picks on both. Both ask only skin type and concerns. The gap between them is in the edges.

## Defects: X

- `nav: member: [Chat, Plan, Profile]` and a "Plan page" in notes. The brief says the main screen is a chat and P1 asked for one flow with six messages; a three-tab shell is invented scope.
- `routine` action "Save to my plan" points to `routine` itself and notes call it a placeholder. A visible chip that does nothing in this spec is a dead action.
- `picks` cards carry a per-card "Add to routine" action that appears in no actions list and has no defined effect; "Cheaper options" loops to `picks` without saying what changes (price ceiling? replace all three?). An engineer has to guess both.
- `skin-type` loading covers the chip tap but not the selfie analysis wait, the one moment on that screen that actually takes time (partial and error are there, the wait itself is not).
- `concerns` carries its own loading status line for the picks request, duplicating `picks.loading`; harmless but muddles which screen owns the wait.

## Defects: Y

- `picks` shows a "Cheaper options" chip with no matching action, and lists a "Change my answers" action that only appears in the empty state. Shows and actions disagree, so the builder guesses.
- `skin-type` offers both "Not sure" and "Skip", two chips meaning the same thing; one extra option to read on a six-chip block with no gain.
- `followup` has no empty state for the question typed before any quiz answer (X handles it by stating the assumption and re-offering the chips); the only chip out is "Show my routine", which is wrong if the user has not reached picks yet.
- Methodology codes (GC-8, ON-2, SR-10) are embedded in `purpose` fields; noise for anyone building from the file, and almost no priority ranks on what is shown.
- `concerns` has no loading state and no visible restatement of the previous answer (only a "Back" chip), so a wrong skin type is less discoverable than X's inline "Skin type - Combination, change".

## Winner

P1 and overall: **Y**, narrowly. The two specs are near twins in the decisions that matter (turns to value, what is asked, text-vs-block), so the tie breaks on discipline. X is the more thoroughly stated spec (partial states, ranks, a handled pre-quiz followup) but spends that thoroughness partly on things nobody asked for: a tab bar, a Plan page, a placeholder chip and an undefined per-card action, all of which would need to be removed or argued about before a visual pass. Y stays inside the chat, keeps one block per turn with the next step always a chip, and its defects are fixable with a handful of lines (add the missing action, drop the duplicate Skip, add one empty state). If X's scope additions were stripped it would win on handoff; as delivered, Y is the cleaner input to the visual skills that run after it.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 3}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 5, "handoff": 3, "scope": 5}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
