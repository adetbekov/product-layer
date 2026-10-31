# Blind review: gentoon-approve-r2 (X vs Y)

## Scores (P1)

| criterion | X | Y |
|---|---|---|
| success | 4 | 5 |
| flow | 5 | 4 |
| states | 5 | 4 |
| ia | 4 | 4 |
| asks | 5 | 5 |
| fit | 5 | 4 |
| handoff | 4 | 4 |
| scope | 3 | 4 |
| clarity (once) | 3 | 4 |

## Defects

**X**
- `nav` / `brief` / `clip-notice`: "Clips" is referenced as where drafts and rendering clips live, but no `clips` screen exists. The leave-and-return path depends on an undefined screen.
- `plan`: loading state says the page is only reached after the plan exists, while `brief` loading says the user may leave during drafting and find the plan in Clips, and `plan` error covers "whole plan generation failed". Where the user actually waits for the draft is ambiguous.
- `storyboard`: "Lyrics stay editable" mid-render opens a paid re-render path during generation; unrequested and risky in the one place the user should mostly watch.
- `plan`: version badge with compare/restore, and `brief` voice input, are unrequested complexity for creators who "want a clip fast".
- `ready`: two actions ("New clip from this brief", "New clip") both go to `brief` with no stated difference; whether Redo scene is paid is left open in notes rather than decided.
- Reply leans on internal codes (SR-1, AP-4) a reader cannot decode.

**Y**
- `storyboard`: no Cancel or Stop. After approval the user cannot abort a multi-minute paid run; the brief's economics make this the one abort that matters.
- `storyboard`: assembly "waits until every shot is done" and there is no skip or assemble-without-scene path. A scene that keeps failing traps the user in a regenerate loop (Edit scene softens but does not end it).
- `ready`: "Regenerate one scene" has no cost statement; notes only make failures free, so a taste-driven redo of a finished shot is unpriced.
- `plan-edit`: a single action covers "a scene or the lyrics" without saying how the scene is selected; the engineer guesses.
- `nav`: "Account" is listed but never specified.

## Winners

**P1: X.** Both land the same minimal spine (brief, Draft, Approve-with-price, system-driven to ready) and both ask only for the brief. X is stronger exactly where the brief hurts: a cancel that states what is kept and charged, per-shot retry plus assemble-without-failed so one bad scene never blocks the clip, cost shown before any redo, and partial/stale states on price. Y is cleaner and better scoped, and price-from-brief is a nice touch, but missing cancel and the no-skip assembly rule are real holes in a paid, slow pipeline.

**Overall: X.** X's flaws are scope creep and an undefined Clips screen, which a second pass trims; Y's flaws are missing guards around the expensive step, which is the core of this product.

```json
{"X": {"P1": {"success": 4, "flow": 5, "states": 5, "ia": 4, "asks": 5, "fit": 5, "handoff": 4, "scope": 3}, "clarity": 3}, "Y": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
