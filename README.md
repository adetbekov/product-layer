# product-layer

**An agent skill for the product layer of an app: information architecture, user flows, fewer steps, screen states — and, as a module, generative UI in chat.**

It decides *what* the user sees and *where* (page, card, form, bot message, approval step) before visual skills decide *how it looks*.
It is built to run before visual / animation skills (Apple-style design, taste, motion) and hand them a clear spec, not to replace them.

Status: **v0 — under construction.** Not ready to install yet.

## Plan

- `skills/product-layer/` — the skill in [Agent Skills](https://agentskills.io) format: a short core plus modules loaded per product type
  (generative UI in chat, Telegram bot, AI pipeline with approval steps, multi-role SaaS).
- `bench/` — repeatable A/B: the same product tasks in fresh sessions with no skill, with this skill, and with popular existing UX skills;
  hidden checks plus a blind X/Y review.

## License

MIT. Ideas from other skills are re-expressed and credited in `CREDITS.md`; no text is copied from non-permissive sources.
