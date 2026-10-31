## Scores

| P1 | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|
| X | 5 | 4 | 3 | 4 | 5 | 4 | 4 | 5 | 4 |
| Y | 5 | 4 | 5 | 5 | 4 | 5 | 4 | 4 | 4 |

Both specs answer the request fully: flow `onboarding`, entry `greet`, done `picks`, six chat-message screens tagged by moment, an explicit text/block call on each. The text-or-block calls are identical and correct on both sides (text for greet and followup, choice for the two questions, cards for picks, steps for routine), and both make greet a `by: system` hop so the first picks cost two or three taps. The differences are in states, in the chat grain, and in small scope leaks.

## X - defects

- `concerns`: no states at all. It is a model-driven message that follows a tap, yet a failed send or a slow load has no design and no way out. The only screen in either spec with nothing under `states`.
- `skin-type`: the error state covers only the selfie. A chip tap that fails to save has no retry.
- `picks` (the done screen): no way to change answers. The "Skin: oily - change" affordance sits upstream on `concerns`; once the cards appear the user who mis-tapped must type and hope.
- Typing as an alternative to any block is promised in notes.md ("every block also accepts typing") but appears in no screen action, so an engineer reading flow.yaml alone would not build it.
- Strengths to keep: `Skip` on concerns (zero-cost opt-out), `Back` that preserves the earlier answer, budget explicitly not asked, honest step count.

## Y - defects

- `picks`: cards carry "an add/open action" with no destination screen anywhere in the spec. A dangling action on the done screen; nothing in the brief asked for a cart or product page.
- `concerns`: the confirm button is disabled until a chip is picked and there is no plain skip, so opting out costs two taps (Nothing in particular + Confirm). The reply's "two taps to picks" is therefore understated; the real minimum is three.
- `picks` -> `Edit my answers` restarts at `skin-type` and replays `concerns`; there is no way to change only the concerns on the normal path (the empty state offers it, the happy path does not).
- Mild visual leakage: "skeleton so the layout does not jump", "chips appear together, never one by one" are motion decisions that belong to the visual pass.
- Strengths: every screen has loading and error with a way out; free-text answers are a first-class action on each question; streaming answer with Stop; routine carries the patch-test safety line; the done screen names the inputs it used.

## Winner

**P1: Y. Overall: Y.** X asks slightly better (Skip, Back, nothing after the picks) and leaks nothing out of scope, but it leaves the two question screens under-designed for failure and hides typing-as-input in a side note. Y is the spec an engineer could build on Monday: complete states, typed answers wired into every block, a done screen that explains itself and can be corrected, and a chat-native loading and streaming story. Its faults are a stray add/open action and an optimistic tap count, both one-line fixes; X's missing states are structural gaps.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 3, "ia": 4, "asks": 5, "fit": 4, "handoff": 4, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 5, "asks": 4, "fit": 5, "handoff": 4, "scope": 4}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
