# Screen states and screen spec

Every screen, card or bot message exists in several states. The spec names
each one; visual skills decide how it looks.

## The state matrix

For each screen fill one row per state. "n/a" needs a reason.

| State | When | Shows | Primary action |
|---|---|---|---|
| first-use empty | nothing created yet | value + how to start | the action that fills it |
| no results | filter / search found nothing | what was searched | clear or widen |
| loading | waiting for data or work | what is happening | cancel / leave (if long) |
| partial | some parts ready or failed | ready parts + what is missing | fix or retry the missing |
| error | action or load failed | what failed, input kept | one recovery |
| success | task done | the result | next likely task (IA-9) |
| ideal | normal content | the content | the screen's primary action |
| no access | role or permission missing | why, who can grant | request / switch |
| offline / stale | connection lost, old data | data age | retry |

## ST-1 · Design every state, not only ideal · CRITICAL

**Rule.** A screen spec is incomplete until every row of the matrix is filled
or marked n/a with a reason.
**Why.** Undesigned states ship anyway, as blank screens and raw errors.
- Bad: a spec with only the ideal state of the dashboard.
- Good: dashboard spec with first-use, loading, error and no-access rows filled.

## ST-2 · Empty states start the task · HIGH

**Rule.** A first-use empty state says in one line what will appear here and
offers the one action that fills it (or sample content to explore). Separate
"nothing yet" from "nothing matches".
**Why.** Empty is the first screen new users see; a blank one reads as broken.
- Bad: "No data."
- Good: "Your plan appears here after a short chat about your skin.
  [Start]"

## ST-3 · Loading matches the wait · HIGH

**Rule.** Under ~1 s: no indicator (keep the old content). 1-10 s: an
indicator that says what is happening in user words; for content, a
placeholder of the same shape. Over ~10 s: stage progress, an estimate if
known, the user can leave, and the system notifies when done
(`modules/ai-pipeline.md` AP-6). Every button that starts work shows a
pending state at once.
**Why.** Users judge speed by feedback; silent waits look like failures.
- Bad: "Approve" does nothing visible for 20 s while the plan regenerates.
- Good: button turns pending at once; "Rewriting the plan, ~20 s".

## ST-4 · Errors explain, keep input, offer one fix · CRITICAL

**Rule.** An error message states what happened in user words, what the user
can do, and keeps everything they entered. One recovery action is primary
(retry, edit, contact). No codes, stack traces or model jargon in the UI.
**Why.** Losing input on error doubles the cost of the failure.
- Bad: "Error 500" and an emptied form.
- Good: "Could not read the receipt - it may be blurry. [Retake] [Type the
  items]".

## ST-5 · Partial results are shown, not hidden · HIGH

**Rule.** When part of a batch succeeds, show the successful parts, mark the
failed or uncertain ones, and let users fix them in place. Do not fall back
to "everything failed" or "everything fine".
**Why.** Partial value is still value; hiding uncertainty causes silent
mistakes.
- Bad: totals do not add up but the normal "Looks good?" card is shown.
- Good: "2 items unclear - check them" with those items marked.

## ST-6 · Success confirms and moves on · MEDIUM

**Rule.** Success shows what happened (object, amount, recipients) and the
next likely action. Minor successes are inline (toast, check), not screens.
**Why.** A success screen with only "OK" is a dead end (FL-2).
- Bad: full-screen "Success!" with a single OK button.
- Good: "Booked for Tue 18:00" with "Add to calendar" and "Open room".

## ST-7 · Never show internals · HIGH

**Rule.** No raw enum values, IDs, probabilities, model names, debug fields
or placeholder words ("undefined", "not set") in user-facing states. Unknown
values are omitted or asked for.
**Why.** Internals look like bugs and erode trust in the whole product.
- Bad: "Type: MOISTURIZER", "P(met)=0.14", "Skin type: not set".
- Good: "Moisturiser"; progress shown as "on track"; skin type asked.

## ST-8 · Destructive and costly states are explicit · HIGH

**Rule.** Before an action that deletes, spends money or notifies others, the
state shows what will happen and its cost. After it, offer undo when
possible (FL-8).
**Why.** Users must be able to predict irreversible outcomes.
- Bad: "Delete?" with Yes / No.
- Good: "Delete project 'Spring promo' and its 12 clips? This cannot be undone."

## ST-9 · Stale actions are handled · MEDIUM

**Rule.** Actions on outdated content (old message buttons, a page open in
another tab, an expired link) act on current state or explain why not, and
show the current state.
**Why.** Acting on stale data silently corrupts results.
- Bad: an old "Pay" button charges a bill that was already closed.
- Good: the old button answers "This bill is closed" and links to the current one.

## Screen spec template

```
Screen: <name>          Object: <what it shows>     Roles: <who sees it>
Purpose: <one sentence, the user's goal here>
Entry: <from where>     Exits: <to where>
Primary action: <one>   Secondary: <max 2>   More: <...>
Content (ranked):
  1. <block - meaning - emphasis 1>
  2. <block - meaning - emphasis 2>
States: <matrix rows that differ from defaults>
Copy intent: <what each key message must say, not final wording>
```
