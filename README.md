# product-layer

<p>
  <a href="https://github.com/adetbekov/product-layer/tags"><img src="https://img.shields.io/github/v/tag/adetbekov/product-layer?label=version" alt="version"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="license MIT"></a>
  <a href="https://agentskills.io"><img src="https://img.shields.io/badge/format-Agent%20Skills-8a2be2" alt="Agent Skills"></a>
  <img src="https://img.shields.io/badge/agents-Claude%20Code%20%7C%20Codex%20%7C%20Cursor%20%7C%20Copilot-555" alt="agents: Claude Code, Codex, Cursor, Copilot">
  <a href="https://github.com/adetbekov/product-layer/actions/workflows/tests.yml"><img src="https://github.com/adetbekov/product-layer/actions/workflows/tests.yml/badge.svg?branch=main" alt="tests"></a>
</p>

**product-layer is an agent skill for the product layer of an app: information architecture, user flows, fewer
steps, screen states, onboarding. It adds modules per product type: generative UI in chat, Telegram bots, AI
pipelines with approvals, and multi-role SaaS.**

It decides *what* the user sees and *where*: page, card, form, bot message or approval step. Visual skills then decide
*how it looks*. Run it before visual and animation skills (Apple-style design, taste, motion) and pass them its spec,
not a design.

Companion skill: **[`skills/product-check`](skills/product-check/README.md)** checks the built interface afterwards by
using it like its user - a QA walk in a real browser (pages and generative UI in chat) or a crowd of personas on two
variants - and reports dead ends, extra steps and silent controls with rule ids from this skill.

## Proof

The bench gives the same product tasks to fresh, isolated sessions (Sonnet 5.5) and scores the answers with hidden
checks and a blind X/Y review by Fable 5.1. It uses 6 cases × 2 repeats.

- [v0.2 report](bench/results/2026-10-31-v0.2/report.md) and [what ran and why](bench/results/2026-10-31-v0.2/notes.md).
- [v0.1 report](bench/results/2026-10-31-v0.1/report.md).

| | v0.2 | best existing skill ([szilu](https://github.com/szilu/ux-designer-skill)) | bare agent |
|---|---|---|---|
| Solved, hidden checks | **10/12** | 6/12 | 3/12 |
| Blind head to head, v0.2 wins : losses | — | 6 : 6 | **11 : 1** |
| User steps to the goal, all flows (mean) | **2.7** | 3.3 | 4.0 |
| Spec lines (mean) | 169 | 212 | 164 |
| Blind score, scope / clarity (1-5) | **4.7 / 4.1** | 3.7 / 4.0 | 4.2 / 3.6 |
| Tokens per session (mean) | 43.8k | 39.1k | 30.3k |

Against v0.1, the v0.2 specs are 28% shorter (236 → 169 lines) and carry no rule ids. They no longer lose on scope.
Cases v0.1 lost now come out level or ahead: checkout vs szilu went from 1:3 to 1:1, settings vs bare from 1:3 to 2:0,
and warmplace hidden checks from 0/2 to 2/2.

Where v0.2 is weaker:
- It ties szilu, while v0.1 led 15:9 on a different sample, so twelve verdicts do not settle it.
- Its states score is below szilu's.
- It fails the Telegram case's hidden checks.

Details: [notes](bench/results/2026-10-31-v0.2/notes.md).

## Quick start

The skill lives in `skills/product-layer/` in the [Agent Skills](https://agentskills.io) format. Install it by
copying that folder.

| Agent | Copy `skills/product-layer` to |
|---|---|
| Claude Code | `~/.claude/skills/` (all projects) or `.claude/skills/` (one repo) |
| GitHub Copilot (VS Code) | `.github/skills/` or `.claude/skills/` |
| Codex and other `AGENTS.md` agents | `.agents/skills/` |
| Cursor | `.cursor/skills/` |

```bash
git clone https://github.com/adetbekov/product-layer
cp -r product-layer/skills/product-layer ~/.claude/skills/
```

Then ask for product work in plain words, for example:

> map the onboarding flow for invited users and cut the steps

> design the group flow of our Telegram bot: what is a message, what is a button, what is edited in place

> audit our settings page: dead ends, missing states, questions we should not ask

`tests/test_install.py` copies the folder into each of the four locations and checks that the copy works on its
own. Every bench session installs the skill the same way.

## Order with visual skills

1. **product-layer** writes the spec: sections, flows with step counts, and every screen or message with its states,
   actions and ranks. It also writes the facts a visual skill needs (audience, assets, constraints) and a transitions
   table.
2. **A visual skill** takes the spec with a concrete request and styles it without adding or removing steps:
   - an Apple-style interaction skill for in-app screens, chat blocks, pipelines and Mini Apps;
   - a taste skill for landing pages and redesigns of sites.

   A Telegram bot without a Mini App needs no visual step: the spec is final.
3. **A motion audit skill** reads the built code later, using the transitions table as its frequency map.

Do not load visual skills at the spec stage. In the v0.1 bench, product-layer plus visual skills lost to product-layer
alone 2:6 with the same hidden-check score. The contract between the layers is in
[`references/handoff.md`](skills/product-layer/references/handoff.md).

## How it works

1. **Frame** the goal and the product type, and read the product's code or spec.
2. **Structure**: top tasks, sections, and where each object lives (inline, overlay or page).
3. **Flows** with branches and a step count to first value. Cut steps in this order: remove, default, defer, combine.
4. **Module** rules for the product type.
5. **States** for every screen or message: empty, loading, partial, error, success.
6. **Spec** in the handoff format, or in the format the project gives.
7. **Check before handing off**:
   - every action has a real target;
   - there are no loops or stubs;
   - final screens have a next step;
   - nothing new was invented;
   - existing features stay reachable;
   - the file parses.

Rules have ids (`SR-1`, `TG-5`), a reason, a bad and a good example, and an impact level. Audits cite the ids so a
reviewer can check each finding. Specs and replies say the decision in plain words instead.

## Layout and sizes

Tokens are estimated as words × 1.3 (`python tests/test_skill.py` prints them).
Budgets: `SKILL.md` ≤ 1.5k, all core references together ≤ 12k, each module ≤ 2k.

| File | Purpose | ~Tokens |
|---|---|---|
| `skills/product-layer/SKILL.md` | principles, router, workflow, pre-handoff check | 1.4k |
| `references/core/ia.md` | top tasks, navigation, placement (inline / overlay / page) | 1.3k |
| `references/core/flows.md` | use cases, dead ends, step counting, multi-actor flows | 1.3k |
| `references/core/step-reduction.md` | step test, ask only what only the user knows | 1.3k |
| `references/core/states.md` | state matrix, screen spec template | 1.3k |
| `references/core/onboarding.md` | first value, invited users, progressive profile | 1.1k |
| `references/core/review.md` | audit procedure, finding format, scorecard, spec self-review | 0.8k |
| **core total** | | **7.0k** |
| `references/modules/genui-chat.md` | block router: text / card / choice / slider / page; actions follow the result | 1.8k |
| `references/modules/telegram-bot.md` | edit vs new message, work inside the group, popups, debts and limits | 2.0k |
| `references/modules/ai-pipeline.md` | gates vs auto, price before commit, long generation, stale results | 1.6k |
| `references/modules/saas-roles.md` | role matrix, at most 5 sections per role, invite loop, object states in time | 1.7k |
| `references/handoff.md` | contract with visual skills: brief context, which skill per product type, transitions, spec format | 1.8k |

A typical run loads `SKILL.md`, 2-3 core files, one module and `handoff.md`: about 7k tokens.

## Tests

```
python tests/test_skill.py      # budgets, rule ids, links, examples, no visual values
python tests/test_install.py    # copy-install into every agent folder works
pytest bench                    # the bench and its hidden checks
```

CI runs all three on every pull request (`.github/workflows/tests.yml`).

## Links

- [Bench](bench/README.md): how every change is measured, and all past results. A change reaches `main` only after
  it wins there.
- [Credits](CREDITS.md): ideas from other skills and guides, re-expressed and credited. No text is copied from
  sources with a non-free license.
- Research behind the skill: [`docs/research/2026-10-ux-skills-landscape.md`](docs/research/2026-10-ux-skills-landscape.md).
- License: [MIT](LICENSE).
