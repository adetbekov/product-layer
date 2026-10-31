---
name: product-check
description: Checks a built interface by using it as a real user would - in a real browser, regular pages and generative UI in chat (cards, buttons, sliders, forms inside messages) - and reports illogical places, extra steps, dead ends and bugs with repro steps and screenshots. Two modes - walk (one agent, QA pass against the optimal path) and crowd (many personas in parallel, funnel and drop-off per A/B variant). Use when the user asks to "test the UI as a user", "dogfood", "QA this flow", "find extra steps", "check the chat UI", "run personas", "simulate users", "compare variant A and B", or after a product-layer spec has been built.
---

# product-check - use it like a user, report what breaks

product-layer decides what to show and where, before visual work. This skill
runs after the UI is built: it walks the real interface and reports where the
product fails its user. It never edits the product and never judges looks.

Engine: Playwright CLI or agent-browser through `scripts/pc.py`, one
interface (setup in `README.md`). Decisions: Liquid d1-ultra for easy crowd
steps, Claude Haiku for the rest, Sonnet for walk and stuck steps.

## Fixed principles

1. **The browser is the only source.** Judge what a user can see and do. Do not
   read the app's source; the spec and the app's text are allowed.
2. **Reproduce, then record.** A finding is written only after a second, clean
   repro, with steps and a screenshot at once, not batched at the end.
3. **Count against the optimum.** Every top task has an optimal step count
   (from the product-layer spec or your own shortest path). Each extra action,
   hesitation or detour is a finding candidate.
4. **No visible change is a bug.** If an action changes nothing on the page
   (`pc.py` marks it `changed: false`) and no feedback appears, report it.
5. **Look, do not only read the tree.** The tree shows what exists; the
   screenshot shows what a person sees. Compare them on every screen.
6. **Stay in the persona.** Decide as the locked persona, not as a developer.
   "A developer would know..." means you drifted: redo the step.
7. **Direction, not numbers.** Crowd runs give the direction of an A/B effect
   and the problem list. Never report simulated conversion as a forecast.
8. **Cite rules.** Link each finding to a product-layer rule id when one fits
   (`FL-2` dead end, `SR-4` asked twice, `GC-7` controls, `TG-11` old buttons).

## Router

| Task | Read |
|---|---|
| QA pass over pages, forms, navigation | `references/walk.md` |
| Chat with streamed answers and components | `references/walk.md` + `references/genui-walk.md` |
| Personas, crowd run, A/B variants | `references/personas.md` |
| Writing findings, crowd report, dedup | `references/report.md` (always, at the end) |

## Inputs

- URL (required) and the top tasks. If a product-layer `handoff.md` spec
  exists, take tasks, optimal steps, screens and states from it.
- Persona: given, from the project, or the default first-time user in
  `references/personas.md`. Lock it before the first click.
- For crowd: two URLs (variants), a goal, and a funnel file (`flow.json`).

## Modes

**walk** - one agent, 5-10 well-evidenced findings.
1. Lock the persona and list 3-5 top tasks with the optimal step count.
2. `export PC_LOOK=ask`, `pc.py open URL`, then walk each task from its real
   entry point with `pc.py do`. Read the diff and open the screenshot it
   prints after every action.
3. Run the checks in `walk.md` (and `genui-walk.md` for chat), including
   WK-9 screen vs tree.
4. Record each finding when found, with `pc.py shot`, in `report.md`.
5. Dedup with a fresh subagent, then write the verdict.

**crowd** - many personas, one isolated browser each.
1. `scripts/personas.py sample` builds personas, at least a third of them hard.
2. `scripts/crowd.py plan` writes one persona prompt per persona and variant.
3. Run them: `crowd.py run` (d1-ultra first, Haiku and Sonnet on escalation,
   parallel) or one fresh Haiku subagent per prompt when no Anthropic key is
   set; it calls `./act auto` and decides only the steps d1 hands back.
4. `crowd.py aggregate` gives the funnel and drop-off points per variant.
5. Report clusters with the noise filter from `report.md`.

## Output

`report.md`: verdict, coverage, findings (`### ISSUE-<n>: <title>`), steps vs
optimum per task; for crowd also the funnel table per variant and the cost.
Screenshots live next to it in `shots/`.

## Never

- Change the product, its data beyond test entries, or its settings.
- Report a style opinion as a finding; hand that to visual skills.
- Wait for network silence in a chat: streams never go quiet. Wait for the
  stream marker (`genui-walk.md`).
- Count a step as passed without an artifact (diff, screenshot, log line).
