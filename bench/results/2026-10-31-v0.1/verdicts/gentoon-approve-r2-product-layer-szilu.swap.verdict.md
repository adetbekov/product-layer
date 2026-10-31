# Blind review: gentoon approve r2 (X vs Y)

## Scores (P1)

| criterion | X | Y |
|---|---|---|
| success | 5 | 4 |
| flow | 4 | 3 |
| states | 5 | 4 |
| ia | 4 | 4 |
| asks | 5 | 5 |
| fit | 5 | 4 |
| handoff | 4 | 3 |
| scope | 3 | 4 |
| clarity (once) | 4 | 5 |

Both sides get the core right: one-field brief, defaults for length/aspect/style, model and seed removed, the plan as the single approval gate with the price on the approve action, per-scene status on the storyboard, per-shot retry that does not fail the clip, leave-and-notify, and a cancel confirm that states what is kept. The differences are in completeness and in a few flow edges.

## Defects: X

- `plan`: carries a version badge with compare/restore of earlier plan versions, plus a "what happens on cancel midway" statement. Neither was asked for; versioning is real engineering cost for a P1 flow spec.
- `storyboard`: "Lyrics stay editable but changes after render say which scene redoes and its cost" puts a second editing surface on a progress screen, mid-render. It blurs the gate (edits now trigger paid redo from the storyboard) and an engineer has to guess the interaction.
- `brief`: optional voice input is unrequested.
- `ready`: "New clip from this brief" and "New clip" both go to `brief`; the distinction is not specified.
- Reply cites internal codes (SR-1, AP-4) a reader cannot resolve.

## Defects: Y

- `confirm-cancel`: "Stop generation" goes to `brief`, so a user who approved and paid for a plan and then stopped lands on an empty field with the plan out of view. X returns to `plan`, which is the right place to revise and restart.
- `storyboard`: the all-failed error offers "Cancel and refund" but no action with that label or destination exists; "Regenerate this shot" is the only recovery, with no "assemble without the failed scene" option, so a stubbornly failing shot has only retry or cancel.
- No `nav` block; "link to past clips" on `brief` is the only hint where finished clips live, and the notification path promised on `storyboard` has no surface or return route.
- `ready`: "Regenerate one shot" shows no cost, although every finished clip is priced; "Share" is unrequested.
- Shows are flat lists without ordering; handoff relies on the engineer to decide hierarchy.

## Winner

P1: X. Overall: X.

X answers every part of the request including nav, designs partial and stale states where paid work can be half-done (failed shots, recompute of price, assembly without failed scenes, cost shown before redo), and routes cancel back to the plan so the revise-then-approve loop stays intact. Y is cleaner and its reply reads better, but it loses the plan on cancel, leaves a named action undefined, and gives the engineer less to build from. X's scope creep (plan versions, voice input, lyric edits on the storyboard) is its main weakness and is why the margin is moderate rather than wide.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 4, "asks": 5, "fit": 5, "handoff": 4, "scope": 3}, "clarity": 4}, "Y": {"P1": {"success": 4, "flow": 3, "states": 4, "ia": 4, "asks": 5, "fit": 4, "handoff": 3, "scope": 4}, "clarity": 5}, "winner": {"P1": "X", "overall": "X"}}
```
