# product-layer

**An agent skill for the product layer of an app: information architecture, user flows, fewer steps, screen states, onboarding — plus modules per product type (generative UI in chat, Telegram bots, AI pipelines with approvals, multi-role SaaS).**

It decides *what* the user sees and *where* (page, card, form, bot message, approval step) before visual skills decide *how it looks*.
It runs before visual / animation skills (Apple-style design, taste, motion) and hands them a spec, not a design.

Status: **v0.1 — first draft.** Usable, not yet benchmarked. Changes reach `main` only after winning the A/B bench (`bench/`, in progress).

## Install

Copy `skills/product-layer/` into your agent's skills folder, for example `~/.claude/skills/product-layer/`.
The agent loads it when you design or review a product, flow, screen, bot or chat UI, or before a visual skill works on new UI.

## How it works

1. **Frame** the goal and product type; read the product's code or spec.
2. **Structure**: top tasks, sections, where each object lives (inline / overlay / page).
3. **Flows** with branches and a step count to first value; cut steps in order remove → default → defer → combine.
4. **Module** rules for the product type.
5. **States** for every screen or message: empty, loading, partial, error, success.
6. **Spec** in the handoff format, with a before / after steps-to-value table, passed to visual skills.

Every rule has an id (`SR-1`, `TG-5`), a reason, a bad / good example and an impact level, so findings are checkable.

## Layout and sizes

Tokens are estimated as words × 1.3 (`python tests/test_skill.py` prints them).
Budgets: `SKILL.md` ≤ 1.5k, all core references together ≤ 12k, each module ≤ 2k.

| File | Purpose | ~Tokens |
|---|---|---|
| `skills/product-layer/SKILL.md` | principles, router, workflow | 1.0k |
| `references/core/ia.md` | top tasks, navigation, placement (inline / overlay / page) | 1.3k |
| `references/core/flows.md` | use cases, dead ends, step counting, multi-actor flows | 1.1k |
| `references/core/step-reduction.md` | step test, ask only what only the user knows | 1.1k |
| `references/core/states.md` | state matrix, screen spec template | 1.1k |
| `references/core/onboarding.md` | first value, invited users, progressive profile | 0.9k |
| `references/core/review.md` | audit procedure, finding format, scorecard | 0.7k |
| **core total** | | **6.3k** |
| `references/modules/genui-chat.md` | block router: text / card / choice / slider / page | 1.3k |
| `references/modules/telegram-bot.md` | edit vs new message, groups vs DM, deep links | 1.1k |
| `references/modules/ai-pipeline.md` | gates vs auto, price before commit, long generation | 1.1k |
| `references/modules/saas-roles.md` | role matrix, invite loop, marketplace paths | 1.0k |
| `references/handoff.md` | contract and spec format for visual skills | 1.0k |

A typical run loads `SKILL.md` + 2-3 core files + one module + `handoff.md`: about 5-6k tokens.

## Tests

```
python tests/test_skill.py      # or: python -m pytest tests/
```

Checks budgets, unique rule ids, that every referenced rule and file exists, that every rule has a reason, and that no visual values (px, ms, hex colours, easing) slip into the skill.

## Bench

`bench/` (in progress) runs the same product tasks in fresh sessions with no skill, with this skill, and with popular existing UX skills, with hidden checks and a blind X/Y review.

## License

MIT. Ideas from other skills and guides are re-expressed and credited in [`CREDITS.md`](CREDITS.md); no text is copied from non-permissive sources.
