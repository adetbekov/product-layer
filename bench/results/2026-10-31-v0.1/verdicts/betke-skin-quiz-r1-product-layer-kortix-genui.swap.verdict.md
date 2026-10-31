## Scores (P1)

| | success | flow | states | ia | asks | fit | handoff | scope | clarity |
|---|---|---|---|---|---|---|---|---|---|
| X | 4 | 4 | 3 | 4 | 4 | 4 | 4 | 5 | 4 |
| Y | 5 | 5 | 5 | 4 | 5 | 4 | 3 | 4 | 4 |

Both sides made the same core calls, and made them right: greet and followup as text, skin-type and concerns as choice blocks, picks as cards, routine as steps; greet hands off to the first question `by: system`, so the user reaches picks in 3 taps; only skin type and concerns are asked. The difference is in states, in the escape hatches, and in how clean the handoff is.

## Defects, X

- `routine`: no loading state, although building a routine is a generated answer like picks; only picks and followup get a typing indicator.
- `concerns`: at least one chip is required and there is no skip. A user with no particular concern must invent one to reach the picks; no empty state is written for "nothing selected".
- `skin-type`: "Not sure" is accepted, but what the picks do with it is only a hint ("gentle options"); the picks message does not state the assumption or offer a way to correct just the skin type. "Change my answers" restarts from skin-type and re-asks concerns too.
- `nav: {}` with no comment; defensible for a chat-only product, but the request named nav and it is left unexplained.
- Reply says the selfie is "offered after the picks", but no screen shows that offer; reply and spec disagree.
- Reply ends with a note about a skill found in HOME, which is tool noise for the reader.

## Defects, Y

- `followup` is `render: text` yet shows "Next-action chips", so the text-or-block decision is muddied on exactly the screen the request asked to decide.
- `picks`: cards carry an "Add / View action". Nothing in the brief has a cart or product page; this is unrequested and undefined for the engineer.
- `concerns`: shows mention "back to the skin-type question" but no such action exists; the actions list and the shows list disagree.
- `greet` loading: "if slower than ~1 s the skin-type message follows without waiting for a tap" contradicts the action, which says it always follows automatically.
- Rule codes (GC-3, GC-6, ON-2, SR-1) appear in spec, notes and reply without a key; the meaning is usually stated inline, but a builder still has to guess what they bind to. Notes also name a specific visual skill, which edges toward the visual pass.
- Cards omit the product photo, which the catalog has and X includes.

## Winner

P1: Y. Y designs the states X leaves blank (loading on every generated message, partial and empty on picks and routine, selfie refusal and photo failure with a way back to chips, off-topic followup), gives the concerns step a Skip so the path to value can be 2 taps, and makes the "not sure" assumption visible on the picks with a change chip instead of an unstated hint. X is tighter in scope and cleaner in handoff, with no stray cart action, no rule codes and a consistent render decision for followup, but it is the thinner spec where the brief's product actually lives: states and recovery. Overall: Y, by a modest margin; the fixes it needs (remove Add, make followup chips a declared block or drop them, reconcile the concerns back action, drop the codes) are edits, while X's gaps are design work.

```json
{"X": {"P1": {"success": 4, "flow": 4, "states": 3, "ia": 4, "asks": 4, "fit": 4, "handoff": 4, "scope": 5}, "clarity": 4}, "Y": {"P1": {"success": 5, "flow": 5, "states": 5, "ia": 4, "asks": 5, "fit": 4, "handoff": 3, "scope": 4}, "clarity": 4}, "winner": {"P1": "Y", "overall": "Y"}}
```
