# Blind review: gentoon-approve P1 (X vs Y)

| Step | Side | success | flow | states | ia | asks | fit | handoff | scope |
|---|---|---|---|---|---|---|---|---|---|
| P1 | X | 5 | 5 | 5 | 4 | 5 | 5 | 5 | 3 |
| P1 | Y | 4 | 3 | 3 | 3 | 4 | 4 | 3 | 4 |

Clarity: X 4, Y 4.

## Defects

**X**
- `plan` -> "Change length, aspect or style" routes to `scene-edit`, a sheet named and purposed for one scene; defaults need their own small sheet or the label is misleading for an engineer.
- `plan` / `ready`: plan versions with compare/restore, "Make a variation", Share link were not requested; they widen the build without being asked for.
- `brief` shows includes "no length, aspect, style... fields" as a show item; it is a note, not content, and the reply leans on rule codes (SR-1, AP-4) that mean nothing to a reader.
- `cancel-confirm` returns to `plan`, which is right, but the plan screen has no state describing "7 kept scenes as draft", so the engineer must infer how kept scenes appear there.

**Y**
- `storyboard` has no cancel: once a paid run starts there is no way to stop it. The only exits are regenerate a shot or leave.
- `storyboard` error: a shot that keeps failing has only Regenerate; there is no "continue without this scene", so assembly can never start and the clip is in practice failed despite the claim.
- `ready-notification` opens `ready` even for "1 shot needs a retry"; that case belongs on `storyboard`. Also "Leave and get notified" is modelled as a user navigation to a notification, which is not a screen.
- `brief` puts a "Change" link to `options` before the plan exists, reintroducing up-front parameter choice; after the plan is shown there is no way to change length/aspect/style except Edit brief -> Change -> Create plan again (a loop with a regenerate cost in time).
- `plan` has no `asks` entry for the approval itself; `options` and `scene-edit` have no loading state; `ready` has no download failure; no insufficient-funds or price-unavailable path anywhere though the whole gate is about price.
- `shows` are bare lists with no ordering or user-facing copy, so a visual designer must guess hierarchy.

## Winner

**P1: X. Overall: X.** Both put a single approval on the plan, show the price before it, and make shot failures per-scene, which is the core of the request. X goes further where it matters for a paid, minutes-long pipeline: a cancel with a statement of what is kept and refunded, "continue without scene N" so a stubborn failure cannot block assembly, a price-unavailable and no-credit path, and a notification that lands on the storyboard when a decision is needed. Y is tighter in scope but leaves a running paid job unstoppable and a repeatedly failing shot with no way to finish; X's main weakness is unrequested versioning and variation features, which cost scope points but do not break the flow.

```json
{"X": {"P1": {"success": 5, "flow": 5, "states": 5, "ia": 4, "asks": 5, "fit": 5, "handoff": 5, "scope": 3}, "clarity": 4}, "Y": {"P1": {"success": 4, "flow": 3, "states": 3, "ia": 3, "asks": 4, "fit": 4, "handoff": 3, "scope": 4}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
