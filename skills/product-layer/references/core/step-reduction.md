# Step reduction

How to cut steps from a flow without losing what the result needs. Run it on
every flow from `flows.md` after counting steps (FL-4).

## The step test

For each step ask, in this order, and stop at the first yes:

1. **Remove** - is the result fine without it? Cut it.
2. **Default** - is one answer right for most users? Preselect it, keep it
   editable, show what was assumed.
3. **Automate / infer** - can the platform, the input, history or a model
   produce the answer? Do it, show the result, allow a fix.
4. **Defer** - is it needed only later (or only by some)? Ask at that moment.
5. **Combine** - can it share a screen or message with a neighbour step?
6. **Keep** - it needs a fact only the user has, now. Make it as cheap as
   possible (SR-6).

Record the verdict per step: `keep | cut | default | infer | defer | combine`.

## SR-1 · Ask only what only the user knows · CRITICAL

**Rule.** Before asking, list where else the answer could come from: platform
data (locale, timezone, Telegram `language_code`, device), the input itself
(receipt currency, photo), earlier answers, the account. Ask only if none
works or the guess would be wrong often enough to hurt.
**Why.** Every question costs attention and some users leave at each one.
- Bad: "Choose your language" when the client already reports it.
- Good: reply in the reported language; a language switch lives in settings.

## SR-2 · Default visibly, never silently · HIGH

**Rule.** A default is shown as a chosen value the user can change in one tap
("Currency: KZT · change"). Defaults that change money, privacy or who gets
notified are never hidden.
**Why.** Silent defaults save a step but cost trust when they are wrong.
- Bad: currency silently set to USD for a receipt in tenge.
- Good: "Currency: KZT · change" shown on the receipt card.

## SR-3 · Defer to the moment of need, then remember · HIGH

**Rule.** Ask for a fact when the flow first needs it, not upfront. Store the
answer and reuse it; offer a change instead of asking again.
**Why.** Upfront questions delay value; repeated questions feel careless.
- Bad: payment details asked on every bill, even after they were given.
- Good: asked on first finalize, then shown as "Pay to: Kaspi ···1234 · edit".

## SR-4 · Never ask twice, never ask overlapping questions · HIGH

**Rule.** No question whose answer is already known or implied by another
answer. Merge questions that users perceive as the same ("concerns" and
"goals" → one "what do you want to fix").
**Why.** Overlap makes users wonder what the difference is, and slows them.
- Bad: asking city after the address was already entered.
- Good: city filled from the address; one "what do you want to fix" instead of concerns + goals.

## SR-5 · Combine related steps, split only when answers branch · MEDIUM

**Rule.** Put related short inputs on one screen or message. Split into
separate steps only when a later question depends on an earlier answer, or
on small screens / chat where one question per message reads better.
**Why.** Fewer screens means fewer transitions and fewer waits.
- Bad: share link is a separate step after confirming the receipt.
- Good: the confirmed receipt card already carries the share action.

## SR-6 · Choices over typing · HIGH

**Rule.** Up to ~7 known options → chips or buttons. A bounded range → slider
or stepper with sensible bounds. A known set with many options → search with
suggestions. Free text is the fallback, always available, never the only way
for a common answer. Photo or voice when describing is harder than showing.
**Why.** Picking is faster and less error-prone than typing.
- Bad: "Type your monthly budget in tenge".
- Good: chips "up to 10k / 10-30k / 30k+ / other".

## SR-7 · Show value before asking for commitment · HIGH

**Rule.** Sign-up, payment details, permissions and profile questions come
after the user has seen a first result, unless the result is impossible
without them.
**Why.** Users commit when they know what they get.
- Bad: register with email and password before seeing a demo clip.
- Good: generate a short preview first; ask to sign in to save or export.

## SR-8 · Generate a draft, then let users edit · HIGH

**Rule.** When the system can produce a reasonable first version, produce it
and make it editable instead of collecting every parameter upfront.
**Why.** Reacting to a draft is faster than specifying from scratch.
- Bad: a 9-field form before any plan exists.
- Good: one-line brief → plan draft with editable scenes.

## SR-9 · Optimistic actions with undo · MEDIUM

**Rule.** Routine actions apply immediately and show an undo (FL-8). The
system reconciles in the background and reports only failures.
**Why.** Waiting for a round trip on each tap multiplies wait steps.
- Bad: each "+" on an item waits for the server before the count changes.
- Good: the count changes at once; a failed sync shows "Not saved · retry".

## SR-10 · Fewer screens, not denser screens · MEDIUM

**Rule.** Do not "save" steps by cramming unrelated decisions into one screen.
Each screen still has one primary action (IA-5). If a combined screen needs
explanation, split it back.
**Why.** A screen users must study costs more than a tap.
- Bad: profile, budget, delivery and payment on one long screen to "save steps".
- Good: two short screens, each with one primary action.

## Output

| # | Step now | Verdict | Rule | New behaviour |
|---|---|---|---|---|
| 2 | Pick language | infer | SR-1 | use client locale; switch in settings |

Then the before / after steps-to-value row from FL-4.
