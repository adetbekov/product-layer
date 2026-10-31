## Scores

| P1 | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|
| X | 5 | 5 | 5 | 4 | 5 | 5 | 4 | 5 | 4 |
| Y | 5 | 4 | 4 | 4 | 4 | 4 | 3 | 3 | 4 |

## Defects

**X**
- `storyboard`: "Try again" and "Remove scene" exist only inside the `partial` state text, not as listed actions; an engineer has to infer the transitions. Cancel on a paid, running job is a single tap straight to `plan` with no confirm; the spec does say what is kept, but a slip costs real money.
- `plan`: no explicit empty state (acceptable, a plan always has scenes) and no way to redraft the whole plan short of "Change the idea"; per-scene rewrite covers most cases but not "I dislike the concept, same brief".
- `notes.md`: refund on cancel and on removed scenes left open. Honest, but the price line on `plan` promises to say "what is kept if the user cancels later", so the open question leaks into copy.

**Y**
- `finished-notification`: title can read "One scene needs a retry" but the only action is Open -> `ready`. A clip with a failed scene is not ready; the user lands on a screen the state contradicts. Should route to `storyboard`.
- `storyboard`: repeated failure offers "Edit scene text" and "Contact support" with no target screen or action; there is no "remove scene" escape, so one shot that never renders can block assembly indefinitely. No error state for assembly itself.
- `plan`: "Not enough balance, add funds" is a `by: user` action, but insufficient balance is a fact the system knows; it should be a system transition or a disabled Approve with the sheet opening. Price "recalculated when length changes" but the brief says price depends on length, and the user can edit scenes; scene edits that change duration are not covered.
- `ready`: "Regenerate scene" after assembly goes back to `storyboard` with no statement of cost or re-assembly; "Share link", `nav`, My clips, `top-up`, Contact support were not asked for.

## Winner

**P1: X. Overall: X.**

Both designs put the one approval exactly where the money is spent, keep defaults visible rather than asked, and make failures local on the storyboard. X is tighter: five screens, every error has a named exit, a failed shot can be retried or removed so assembly always has a path, the notification distinguishes "ready" from "needs you", and price updates on scene count as well as length. Y adds reasonable things (cancel confirm with refund, top-up sheet) but also unrequested surface (nav, share, support, regenerate-from-ready), and its two routing gaps (notification to `ready` on a failed scene, stuck scene with no remove) are exactly the long-job failure cases the brief asked to fix.

```json
{"X": {"P1": {"success": 5, "flow": 5, "states": 5, "ia": 4, "asks": 5, "fit": 5, "handoff": 4, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 4, "ia": 4, "asks": 4, "fit": 4, "handoff": 3, "scope": 3}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
