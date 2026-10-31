# User flows

A flow is the path from a trigger to a result the user cares about. Same rule
format and impact scale as `ia.md`.

## FL-1 · Write every flow as a use case · HIGH

**Rule.** Each flow states: actor, trigger, precondition, result (end state the
user cares about), main steps, and branches - error, cancel, back, empty,
"not now". One flow per top task.
**Why.** Happy-path-only flows hide the branches where users actually drop.
- Bad: "User uploads receipt → sees split."
- Good:
  ```
  Flow: split a receipt   Actor: payer   Trigger: photo in chat
  Pre: bot started        Result: each person sees what they owe
  1. Send photo  2. Check parsed items  3. Share link  ...
  Branches: 2a parse failed → describe fix by text/voice (max 3 tries)
            2b wrong currency → pick currency, back to 2
            *  cancel at any step → bill discarded, photo kept
  ```

## FL-2 · No dead ends · CRITICAL

**Rule.** Every screen, message and state has at least one forward action or a
clear exit. Errors offer a recovery. "Done" screens point to the next task
(IA-9). A rejected input says what to do instead. Each action must reach a
real, different place: a button that reopens the same empty screen, or leads
to a stub, is a dead end too. The one exception is an intended end ("account
deleted", "bill settled"): it says what happened and is marked as the end.
**Why.** A dead end ends the session; users rarely come back to retry.
- Bad: "Brief is locked, reject a gate first" when no gate is open; an empty
  cart whose "Back to cart" opens the same empty cart.
- Good: "Brief is locked after scenes are split. Edit a scene, or start a new
  version from this brief." with both actions.

## FL-3 · Design the entry, not only the start screen · HIGH

**Rule.** List every entry point (home, deep link, invite, notification,
shared link, search) and the screen each lands on. A user who arrives with
context (invite, link to an object) lands inside that context and skips
generic steps.
**Why.** Many users never see your start screen; they arrive mid-flow.
- Bad: invited participant gets the full new-user onboarding first.
- Good: invite link opens the shared bill with "Select your items".

## FL-4 · Count steps to value · CRITICAL

**Rule.** For each flow count steps from entry to result. A step is one of:
- a tap or click that moves the task forward (not scrolling);
- a typed input (one field = one step) or a choice;
- a wait the user must watch (over ~3 s, no way to leave);
- a context switch (another app, chat, tab, email).

Report as a table and compare before / after:

| Flow | Actor | Steps now | Steps proposed | Cut by |
|---|---|---|---|---|
| Split receipt | payer, new | 10+N | 7+N | SR-1 language, SR-5 share on card |

Repeated per-item actions count once with "+N" (select items: 1 + N).
**Why.** Without a number, "simpler" is opinion and regressions go unnoticed.
- Bad: "The new flow is simpler." with no numbers.
- Good: "Split receipt, new payer: 10+N → 7+N steps (SR-1, SR-5)."

## FL-5 · Diagrams stay readable · MEDIUM

**Rule.** A flow diagram (Mermaid) has at most ~15-20 nodes. Bigger flows are
split into sub-flows linked by name. Decisions are diamonds with labelled
exits; every branch ends at a result or rejoins.
**Why.** Large diagrams stop being read and stop being checked.
- Bad: one 45-node diagram covering sign-up, payment and refunds.
- Good: three diagrams of 12-15 nodes linked as "→ Payment flow".

## FL-6 · Long flows survive interruption · HIGH

**Rule.** Any flow over ~3 steps or ~1 minute saves progress. Returning
resumes at the same step with inputs kept. Say so when it matters ("Saved,
you can come back later").
**Why.** Users get interrupted; restarting from zero loses most of them.
- Bad: closing the questionnaire at question 4 of 5 discards all answers.
- Good: reopening the chat shows "Continue: 4 of 5" with answers kept.

## FL-7 · Multi-actor flows: nobody waits without need · HIGH

**Rule.** When several people act on one object (split, approve, book), draw
one lane per actor. Each actor sees the current shared state and their own
next action. No actor is blocked by another unless the result is wrong
without them; then show who is pending and offer a way around (remind,
take over, proceed without).
**Why.** One slow participant should not freeze everyone's result.
- Bad: payer cannot finish until every participant taps Done.
- Good: payer can finish; unclaimed items go to the payer or split evenly,
  pending people get a reminder.

## FL-8 · Confirm only the irreversible, undo the rest · HIGH

**Rule.** Ask for confirmation only when an action is destructive and cannot be
undone, costs money, or reaches other people. Everything else runs at once
with an undo (toast or edit in place) for at least ~10 seconds.
**Why.** Confirmations on routine actions train users to click through the
dangerous ones.
- Bad: "Are you sure you want to add this item?"
- Good: item added, "Undo" visible; "Delete project" asks, naming what is lost.

## FL-9 · Back and cancel are always defined · MEDIUM

**Rule.** For each step state what back and cancel do and what is kept.
Cancel never silently destroys user input that took effort to produce.
**Why.** Undefined back behaviour is where data loss bugs live.
- Bad: Back on the payment step resets the cart.
- Good: "Back: returns to cart, items kept. Cancel: closes, draft saved."

## Output: flow block

```
Flow: <name>   Actor: <role>   Trigger: <event>   Entry: <screen/link>
Pre: <condition>   Result: <end state user cares about>
Steps: 1. ... 2. ... (mark [cut] / [new] vs current)
Branches: <step>a ... → <where it goes>
Steps to value: now N → proposed M (rules applied)
```
