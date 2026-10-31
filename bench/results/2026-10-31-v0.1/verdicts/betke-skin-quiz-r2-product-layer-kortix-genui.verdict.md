# Blind review: betke-skin-quiz-r2 (X vs Y)

| Step | Side | success | flow | states | ia | asks | fit | handoff | scope |
|---|---|---|---|---|---|---|---|---|---|
| P1 | X | 5 | 4 | 5 | 4 | 4 | 5 | 5 | 5 |
| P1 | Y | 5 | 4 | 4 | 4 | 5 | 4 | 3 | 3 |

Clarity: X 4, Y 4.

## Defects

**X**
- `concerns`: the confirm button is disabled until at least one chip is chosen and there is no Skip and no free-text action listed. A user whose concern is not among the five (or who just wants maintenance) has no listed way forward; the only exit is to pick something untrue.
- `concerns`: no explicit empty state, only the implied "enabled after at least one chip" in shows.
- `greet`: the error state is a fixed template that then needs a Retry to "re-send the opening request" — a template cannot fail to compose, so the error should be about the connection, not the greeting.
- `picks`: "photo" on each card assumes a catalog field the brief never lists (prices, ingredients, tags only).
- Reply point 5 leaks internal tooling ("kortix-genui skill", "openui syntax") into a message meant for the product team.

**Y**
- Whole spec: purposes and shows cite opaque codes (ON-4, GC-5, SR-10, GC-11, GC-12, "notice.error") that are defined nowhere in the snapshot. An engineer or visual designer cannot resolve them; they are noise in a handoff document.
- `skin-type`: "Analyse a selfie" jumps straight to `concerns`. Nothing says how the analysed type is shown, confirmed, or corrected; the loading state has Cancel but no action for what Cancel leads to. This is the biggest guess left for the builder.
- `skin-type`: Skip and "Not sure" are two buttons for one answer; the extra option adds reading without removing a step.
- `concerns` and `routine`: "Back" and "Back to picks" are page-navigation ideas in a chat, where earlier messages are still on screen. Unasked-for and against the grain.
- `picks`: "Cheaper options" introduces a budget feature no moment requested. `followup` adds "Show my routine" the same way.
- `concerns`: no loading state while picks are matched (it is only covered from the picks side).

## Winner

**P1: X.** Both reach the picks in two user turns with the same text/block calls (greet text, two chip blocks, cards, steps, text followup), and both keep the greeting free by moving on `by: system`. X is tighter: every state has a way out, the selfie is deliberately left out of the first session, and the spec is self-contained enough to build from. Y asks slightly better (Skip on concerns gives general picks instead of forcing a false answer) and accepts free text everywhere, but it pays for that with undefined reference codes, an underspecified selfie path, Back buttons in a chat, and unrequested budget and navigation chips.

**Overall: X.** One step, so the same call. X's single real gap is the forced concern pick; Y's gaps spread across handoff, scope and fit, which cost more at build time than one missing Skip.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 4, "fit": 5, "handoff": 5, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 3, "scope": 3}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
