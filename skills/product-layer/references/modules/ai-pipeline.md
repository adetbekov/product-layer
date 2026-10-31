# Module: AI pipeline with approvals

For products where AI produces a result in stages (brief → plan → assets →
assembly → publish), some of which a human approves. Use with the core
files; rule format as in core.

## Stage map

List every stage as a table before applying rules:

| Stage | Output | Cost (money / time) | Reversible? | Mode | Who acts |
|---|---|---|---|---|---|
| Plan | scene list | low / 20 s | yes | gate | user |

Mode is one of: `auto` (runs, no stop), `review` (runs, user may edit after),
`gate` (stops until the user approves).

## AP-1 · Gates only where they pay · CRITICAL

**Rule.** A stage is a gate only if its output defines everything downstream,
or the next stage is costly or irreversible. Otherwise it is `review` or
`auto`. Count gates in steps-to-value (FL-4).
**Why.** Each gate is a stop and a wait; unnecessary ones double the time to a
result.
- Bad: approve the plan, then approve the lyrics derived from it.
- Good: plan is a gate (it defines all scenes); lyrics are `review`,
  editable while frames render.

## AP-2 · Choose autonomy per step · HIGH

**Rule.** Place each AI action on the scale: suggest → draft for approval →
act with undo → act silently. Move right only when errors are cheap and
reversible; move left when they cost money, reach others or are permanent.
**Why.** One autonomy level for all steps is either slow or risky.

## AP-3 · Restate the goal before generating · HIGH

**Rule.** Before the first costly stage, show what the system understood: goal,
audience, constraints, length, style, as an editable summary. Missing must-
know facts are asked here, with defaults (SR-2).
**Why.** A misread brief wastes the whole pipeline.

## AP-4 · Price and time before commit · CRITICAL

**Rule.** At the gate before an expensive stage, show the cost the user will
pay and the expected time, and what happens if they cancel midway.
**Why.** Users cannot approve what they cannot price; surprise cost kills
trust.
- Bad: running cost appears in the header after generation started.
- Good: "Render 12 scenes · 1 clip credit · ~6 min [Start]".

## AP-5 · Edit the artifact, not only reject it · HIGH

**Rule.** At a gate, users can change parts of the output directly (edit one
scene, reorder, delete) and regenerate only what they touched. Reject with a
note is the secondary path.
**Why.** Reject-and-regenerate for one change costs a full wait and may
break what was fine.

## AP-6 · Long work: progress, leave, notify, cancel · CRITICAL

**Rule.** Work over ~10 s shows: stage stepper, per-item status for batches
(3 of 12 ready), an estimate as a range, and results as they arrive. Users
can leave and are notified (in-app, email, push or bot message) when done or
when input is needed. Cancel is available and says what is kept.
**Why.** Users will not watch a progress bar for minutes; without a
notification they forget to come back.

## AP-7 · Failures are per item and keep successes · HIGH

**Rule.** When one item fails, mark that item with the reason in user words
and a retry for it alone; keep and show everything that succeeded (ST-5).
The whole run fails only if the result is impossible.
**Why.** Restarting a batch for one failure wastes time and money.

## AP-8 · Every gate action responds at once · HIGH

**Rule.** Approve, reject and regenerate switch to a pending state immediately
and name what is running ("Rewriting the plan"). No double submits.
**Why.** Silent buttons during model calls get pressed again.

## AP-9 · Show agent steps, collapsible · MEDIUM

**Rule.** Show what the agent is doing as short steps in user terms, collapsed
by default after completion. Expose decisions the user may want to change
(chosen variant, picked music), not internal calls.
**Why.** Visible steps build trust and explain waits; raw logs do not.

## AP-10 · Versions instead of overwrite · MEDIUM

**Rule.** Every approved or regenerated artifact is a version; users can
compare and go back. Edits after a later stage started say what will be
redone and what it costs.
**Why.** Generation is non-deterministic; losing a good version is
permanent.

## AP-11 · Auto mode is a default, gates are opt-in detail · MEDIUM

**Rule.** Offer one fast path (auto) and one careful path (with gates) as a
single choice with a sensible default, not as several settings. Returning
users get their last choice.
**Why.** Most users want a result; experts want control. One switch serves
both.

## AP-12 · No dead ends after locking · HIGH

**Rule.** When a stage locks earlier inputs, the lock message offers what can
still be done (edit downstream items, new version from this brief) (FL-2).
**Why.** "Locked" with no way forward ends the session.
