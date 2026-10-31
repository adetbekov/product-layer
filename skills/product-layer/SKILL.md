---
name: product-layer
description: Decides what the user sees and where before any visual work - information architecture, user flows, step reduction, screen states, onboarding - and hands a spec to visual / motion skills. Modules for generative UI in chat, Telegram bots, AI pipelines with approvals, and multi-role SaaS. Use when the user designs or reviews a product, screen, flow, bot, onboarding, navigation or chat UI; asks "where should this go", "card or page", "too many steps", "what screens do we need", "map the flow", "UX audit"; or before calling a design / taste / animation skill on new UI.
---

# product-layer - what to show and where

This skill owns the product layer: structure, flows, steps, states. It does not
own looks. Its output is a **product spec** (`references/handoff.md`) that
visual, taste and motion skills take as input. Run it first; call them after.

## Fixed principles

1. **Value in the fewest steps.** Count steps to the first result for every flow
   you touch, before and after. A change that adds a step needs a reason.
2. **Ask only what only the user knows.** Everything the platform, the input or
   history can tell you is inferred, defaulted or deferred.
3. **No dead ends.** Every screen, message and state has a next action or exit,
   except a screen that ends the journey on purpose and says so.
4. **Every state is designed.** Empty, loading, partial, error and success are
   part of the spec, not an afterthought.
5. **Meaning, not style.** Name components by role (primary action, choice,
   progress), emphasis by rank (1-3). Never colours, fonts, sizes, spacing or
   motion timing - that belongs to visual skills.
6. **Facts from the product.** Read the code, routes, prompts or bot handlers
   before proposing. Mark guesses as assumptions.
7. **Rule ids stay internal.** Ids like `SR-2` or `TG-1` belong in audit
   findings and working notes only. A spec or a reply to the user says the
   decision in plain words ("budget is asked when products appear"), never
   the id: the engineer and the visual skill cannot decode it.
8. **Design what was asked, nothing more.** No features, policies, numbers or
   screens the brief does not need (retention windows, budgets, extra nav,
   placeholder screens). An assumption you had to make goes to the notes in
   one line, not into the product.

## Router

Load only what the task needs. Core files by task:

| Task | Read |
|---|---|
| Sections, navigation, "where does X live", card vs page | `references/core/ia.md` |
| Map or design a flow, multi-actor process | `references/core/flows.md` |
| "Too many steps", forms, questions, simplify | `references/core/step-reduction.md` |
| Screen spec, empty / loading / error | `references/core/states.md` |
| First run, sign-up, invite landing | `references/core/onboarding.md` |
| Audit an existing product or a spec | `references/core/review.md` |
| Writing the output for visual skills | `references/handoff.md` (always, at the end) |

Plus one module by product type (two if the product mixes them):

| Product looks like | Module |
|---|---|
| AI chat that renders cards, forms, sliders | `references/modules/genui-chat.md` |
| Telegram bot or Mini App | `references/modules/telegram-bot.md` |
| AI generation with stages and approvals | `references/modules/ai-pipeline.md` |
| Web app with roles, workspaces, marketplace | `references/modules/saas-roles.md` |
| None of these | core only; note the gap in the spec |

## Workflow

1. **Frame.** One-sentence goal: who, what result, how we know it worked.
   Pick the product type and module. Find the code or spec and read it.
2. **Inventory.** List top tasks, objects and roles (`ia.md`). For an existing
   product, record current flows with step counts (`flows.md` FL-4).
3. **Structure.** Decide sections and where each object lives (IA-1..IA-9).
4. **Flows.** Write each top-task flow with branches, then cut steps
   (`step-reduction.md`, in order: remove, default, defer, combine).
5. **Module rules.** Apply the module: what renders as text vs block, message
   edit vs new, gate vs auto, which role sees what.
6. **States.** Fill the state matrix for every screen or message (`states.md`).
7. **Spec.** Write the product spec in the `handoff.md` format, or in the
   format the project or the user gives (that format wins; add nothing it
   does not ask for). End with steps to value (before / after) and open
   questions.
8. **Check before handing off** (`review.md`, self-review). Every action
   leads somewhere real and different; no loops back to the same screen, no
   stub or "coming soon" targets; every final screen has a next step, or is
   marked as the intended end of the journey ("account deleted"). Delete
   anything the brief did not ask for. A YAML or JSON spec must parse: a
   value that holds quoted copy plus more text is quoted as a whole
   (`error: 'Not saved - retry'`, not `error: "Not saved" - retry`); if you
   can run code, load the file once to prove it.
9. **Hand off.** Fill the visual brief context, pick the visual skill by
   product type (`handoff.md` table) and pass the spec with a concrete
   request, not a bare skill call. Telegram bots without a Mini App need no
   visual step. Do not pick colours or layout grids yourself.

For an audit, run steps 1-2 and 6, then `review.md`; output findings, not a
redesign, unless asked.

## Output size

- Small ask (one screen, one question): answer plus the relevant spec block.
- Flow or feature: full spec for the flows touched.
- Whole product: IA map + top 3-5 flows; leave the rest as a list.

Keep specs short: tables and numbered steps, no essays. A spec that is longer
than the brief needs is worse, not safer. If the user's request contradicts a
rule, the request wins; say in one line what it costs.

## Never

- Choose colours, typography, spacing, icons, animation curves or durations.
- Add a confirmation, tour or sign-up wall without the rule that justifies it.
- Invent components outside the product's catalogue (genui) or Telegram's API.
- Copy private product code or data into public files.
- Put rule ids, invented features or placeholder screens into a spec.
- Leave an action without a real target, or a target that loops back.
