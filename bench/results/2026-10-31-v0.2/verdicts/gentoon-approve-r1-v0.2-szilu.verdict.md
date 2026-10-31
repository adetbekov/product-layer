## Scores

| P1 | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|
| X | 4 | 4 | 4 | 4 | 5 | 4 | 4 | 5 | 4 |
| Y | 5 | 4 | 5 | 5 | 5 | 5 | 4 | 4 | 4 |

## Defects, X

- `ready`: the scene list promises "a Retry for it" on a missing scene, but no action leaves `ready` toward `storyboard` for that retry. Only `Change the plan` and `Make another clip` exist, so the retry is a dead element.
- `plan`: "regenerate the whole plan, or one scene" appears under shows but has no action, no loading state and no cost note. The engineer must guess whether it is free and what happens to edits.
- `storyboard`: `Cancel generation` jumps straight to `plan` with no confirmation on a paid, minutes-long job. The spec also never says what the system does when a scene is still failed and the user does nothing: does `Clip assembled` fire, or does it wait?
- `plan`: the shows list carries "what happens on cancel after start" and the restated brief alongside concept, scenes, lyrics and price. That is the right single approval point, but the screen is overloaded; the cancel note belongs on the storyboard, where it already is.
- `brief` has no loading state; the handoff to `plan` covers it only by implication.

## Defects, Y

- `cancel-confirm`: purpose says "finished shots would be lost", shows says "Shots already made are kept for 7 days". One of them is wrong, and the modal copy depends on which.
- `storyboard`: the error state offers "Continue without the shot", but the only transition to `ready` is the system one "All shots done, assembling". The user path out of a stuck failure is described, not wired.
- `ready` -> `Re-make a scene` lands on `storyboard` with no price or confirmation, while the brief says generation is paid and slow. Either it is covered by the clip price (say so) or it needs the same gate as approve.
- `download-started` is a toast modelled as a screen with its own "Open" action that is not defined. Over-modelled; a line in `ready` would do.
- `brief` says changing defaults "happens on the plan screen", but they live in the `plan-edit` sheet; small inconsistency for the builder.

## Winner

P1 and overall: **Y**. Both put the single approval before generation, show a readable plan with the price, and isolate a failed shot to its tile with per-shot retry, which is the core of the request. Y is more complete where it matters for this product: it pauses before assembly when shots remain failed, guards cancel on a paid job with a confirmation that states charges, streams the plan in, handles connection loss, and separates reading the plan (page) from editing it (sheet), so the fast creator never sees controls. X is leaner and its in-place editing and "Change the plan shows the redo cost before approval" are genuinely good, but its ready-screen retry has no transition and its regenerate actions are unspecified, which a builder cannot resolve alone.

```json
{"X": {"P1": {"success": 4, "flow": 4, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 5, "asks": 5, "fit": 5, "handoff": 4, "scope": 4}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
