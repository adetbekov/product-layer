# Module: generative UI in chat

For AI chat products where the agent can render blocks (cards, choices,
forms, sliders, tables) instead of plain text, and some content lives on
pages outside the chat. Use with the core files; rule format as in core.

## The block router

Decide per reply by the **shape of the content**, top to bottom, first match:

| Content shape | Render as |
|---|---|
| Short fact, explanation, opinion, reassurance (under ~3 sentences, no options) | text only |
| One recommended item with a verdict or action | single card |
| 2-8 alternatives to choose from | card stack or carousel, each with its action |
| Same attributes across 2+ items | comparison table |
| Ordered process of 4+ steps (routine, recipe, instructions) | steps block |
| Need a bounded answer from the user (2-7 options) | choice chips |
| Need a value on a range (budget, intensity) | slider or stepper with bounds |
| Need several related facts at once (address, dates) | inline form, max ~5 fields |
| Something saved, followed over time, or revisited | page / tab, plus a summary card linking to it |
| Progress of long work | status line, then the result block |

More than 8 options: show the top 3-5 and a "show more" or filter, never a
wall of cards.

## GC-1 · Route by content shape, not by habit · CRITICAL

**Rule.** Use the router above. A block appears only when its shape matches;
text stays text. The agent never renders a block just to look rich.
**Why.** Blocks for plain answers slow reading; text for choices forces
typing.
- Bad: three product options described in a paragraph, "reply with the name".
- Good: three cards, each with its own "Add" action.

## GC-2 · Closed component catalogue · CRITICAL

**Rule.** The agent picks only from a fixed list of components. Each entry
states when to use it, its required fields and its actions; the product code
renders it. Unknown shapes fall back to text. Spec new components as product
work, not as agent improvisation.
**Why.** Free-form generated layouts are inconsistent and untestable.
- Bad: the agent invents a "timeline widget" the app cannot render.
- Good: the agent picks `steps` from the catalogue; unknown shape falls back to text.

## GC-3 · Answer first, assume the typical case · HIGH

**Rule.** When a request is ambiguous but a typical reading exists, answer
for it at once, state the assumption in one line, and offer chips to switch
("For oily skin · change").
**Why.** A clarifying question costs a full turn; a stated assumption costs
one tap only when wrong.
- Bad: "Which skin type do you have?" before any answer.
- Good: a routine for the typical case plus "For combination skin · change".

## GC-4 · Buttons, not suggestions · HIGH

**Rule.** Next actions are tappable (chips, card actions), never prose like
"you could ask me to...". At most 3-4 next-action chips per reply.
**Why.** Users act on buttons; they rarely retype suggestions.
- Bad: "You can also ask me to compare these."
- Good: chips "Compare" and "Cheaper options" under the cards.

## GC-5 · No blank chat · HIGH

**Rule.** A new or empty conversation shows 2-4 starter actions tied to the
product's main jobs, and the user's own context if known (ON-4).
**Why.** An empty input box makes users guess what the product can do.
- Bad: an empty chat with only an input box.
- Good: three chips: "Check my product", "Build a routine", "Scan my skin".

## GC-6 · One main block per turn, text does not repeat it · HIGH

**Rule.** Each agent turn has at most one primary block (plus small chips).
Accompanying text adds what the block cannot (why, caveat), in 1-2
sentences, and never restates the block's contents. Superseded blocks of the
same kind collapse to the latest.
**Why.** Several competing blocks and echoed text bury the answer.
- Bad: a plan card, a product carousel and a table in one reply, text repeating the plan.
- Good: one plan card plus one sentence on why step 2 matters.

## GC-7 · Controls are local until committed · HIGH

**Rule.** Sliders, filters, toggles and steppers update the block on the
client immediately. Only an explicit action (Apply, Add, Send) sends a
message to the agent and starts a turn.
**Why.** Sending each slider move to the agent floods the chat and waits on
the model for what arithmetic can do.
- Bad: every slider move sends "budget 12 000" to the agent.
- Good: the slider filters cards locally; "Show these" sends one message.

## GC-8 · Questionnaires: one question per card, all before the result · HIGH

**Rule.** In chat, ask one question per card with chips, show progress
("2 of 4"), allow skip and back, keep answers on interruption (FL-6). Use a
photo when the answer is visual. Every question the result needs is in the
questionnaire; none is added as text after the result (ON-2). Answers are
saved to the profile and shown on its page.
**Why.** A text question after the result means the result was guessed.
- Bad: skin-type question appears in the first reply, after "Build my plan".
- Good: skin type is chip question 2; the plan arrives with nothing to ask.

## GC-9 · Card in chat or page outside · CRITICAL

**Rule.** One-off answers stay in chat. Anything the user will follow, update
or return to (plan, profile, shelf, order, saved comparison) has a page, and
the chat shows a compact card linking to it. Changes made on the page are
visible to the agent; changes made by the agent update the page.
**Why.** Important things scroll away in chat; pages give them a home (IA-3).
- Bad: the user's routine lives only in an old chat message.
- Good: the routine is a Plan page; chat shows a card "Open plan".

## GC-10 · Editable previews over upfront forms · MEDIUM

**Rule.** When the agent can draft (a routine, an order, a message), show the
draft as an editable block with Confirm, not a form to fill first (SR-8).
**Why.** Correcting a draft takes fewer steps than specifying everything.
- Bad: a form "morning steps, evening steps, products" before any suggestion.
- Good: a drafted routine with editable steps and Confirm.

## GC-11 · Free text always works · MEDIUM

**Rule.** Every block can be answered by typing as well; the agent maps the
text to the same action.
**Why.** Users mix tapping and typing; a block must not trap them.
- Bad: typing "the second one" under cards gets "Please tap a button".
- Good: typing "the second one" adds the second card's product.

## GC-12 · Agent progress in user words · MEDIUM

**Rule.** While working, show a status line naming the current step in user
terms ("Checking ingredients"), streaming partial blocks when useful. Tool
failures are explained in one line with a retry, never silent.
**Why.** A silent agent looks stuck; tool names look like errors.
- Bad: "Calling tool compute_verdict…"
- Good: "Checking ingredients…", then the verdict card.

## Output additions

For each agent turn type in the spec: trigger → block (router row) →
required fields → actions → what goes to the agent → page it links to.
