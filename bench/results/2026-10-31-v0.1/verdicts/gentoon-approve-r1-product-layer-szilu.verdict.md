## Scores

| P1 | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|
| X | 5 | 4 | 5 | 4 | 5 | 4 | 5 | 3 | 4 |
| Y | 5 | 4 | 4 | 4 | 5 | 3 | 4 | 5 | 4 |

## Defects

**X**
- `plan` / `scene-edit`: "Change length, aspect or style" reuses the per-scene edit sheet. One sheet now carries a scene description, a lyric line and three global defaults; the layout has to be guessed and the purpose line contradicts itself.
- `plan`, `storyboard`: lyrics stay editable after approval and "while frames render". Edits after the only approval gate, during paid generation, were not asked for and blur what the user actually approved.
- `plan`, `ready`: plan versions with compare/restore, clip v1/v2, "Make a variation", share link — none requested. Scope creep that also lengthens the plan screen.
- `ready`: no error for assembly itself failing (only download failing); the storyboard's "whole run impossible" state does not clearly cover the assembly step.

**Y**
- `storyboard`: "Cancel generation" goes straight to `plan` with no confirmation and no word on what happens to the clip that was charged once at approval. On a prepaid, minutes-long job this is the one place a cost statement matters and it is missing.
- `storyboard` / `clip-ready-notice`: "Leave and notify me" is a user action whose target is a notification. In a web app leaving is closing the tab; the notification should be a `by: system` transition, as `shows` already implies.
- `brief`: "My clips" action targets `brief` itself — a self-loop with no destination.
- `options`, `scene-edit`: no loading state although `options` computes a price and `scene-edit` saves; `options` has two "Done" actions whose routing depends on unstated context.
- Reply: "(in PROJECT)" is an unsubstituted placeholder.

## Winner

**P1: X. Overall: X.** Both put the single approval on the plan, before anything is generated, price beside the button, and both make long jobs and per-shot failures visible with retry and skip per scene — the core of the brief is met equally. X is more complete where money is at stake: it says before approval what a mid-run cancel keeps and refunds, confirms the cancel with that same statement, and handles insufficient credit without losing the plan, whereas Y leaves a cancel after payment unexplained. Y is tighter in scope and its separate options sheet and streaming plan draft are cleaner, but X's fuller states and ranked, copy-level handoff outweigh its unrequested versioning.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 5, "scope": 3}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 3, "handoff": 4, "scope": 5}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
