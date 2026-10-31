# Full run of product-layer v0.1, 2026-10-31

Skill under test: `skills/product-layer` at `397d73b` (v0.1, JEB-2030). Bench as merged in JEB-2031, plus one check fix
(below). Results: [report.md](report.md), [runs.tsv](runs.tsv), per-pair reports, and `verdicts/`.

## What ran

- Driver: agent-driven (`prepare / next / record / pack / report`), because `claude -p` is not authenticated on the
  runner. Each agent session ran in a fresh Sonnet 5.5 subagent with its own `HOME`; each blind verdict ran in a fresh
  Fable 5.1 subagent. Seed 1877.
- Arms: `bare`, `product-layer`, `szilu`, `design-for-ai` (`ai-native` + `journey`), `kortix-genui` (betke case only),
  `product-layer+visual` (product-layer plus `apple-design`, `design-taste-frontend`, `improve-animations`; the visual
  skills were given by path and are not in this repo). Third-party arms at the SHAs pinned in `arms/fetch.sh`.
- 6 cases x 2 repeats: 62 sessions. Blind pairs: product-layer against every other arm.
- Tokens (subagent totals): sessions 2.44M, verdicts 3.12M; total 5.56M for the bench. The cap agreed for JEB-2033 was
  6M including the product audits (0.37M, not in this repo), so 5.93M was spent.

## Deviations from the plan

- Two repeats, not three: the issue asked for 2, and 3 would not fit the 6M cap.
- `product-layer+visual` vs `product-layer` got 8 verdicts instead of 24, to stay under the cap: four cases where a
  visual layer applies (betke, gentoon, warmplace, checkout; a Telegram bot has none, settings is close to checkout),
  one order per repeat (r1 as packed, r2 swapped), so position bias is balanced across repeats but not within one.
- Check fix, applied with `recheck` (no session rerun): `asks` treated "approve the plan and price" as asking the user
  for the price, which failed two gentoon specs that do exactly what the brief wants (show the computed price, ask for
  approval). Asks that start with approve / confirm / consent / agree / accept are now decisions, not requests for the
  value; `test_approving_a_shown_value_is_not_asking_for_it` pins it.
- Not changed, worth a look before v0.2: `dead_ends` counts a terminal "account deleted" or "bill settled" screen with
  no action as a dead end. That is the rule as written (every screen has a way out) and it hit every arm equally, but a
  case may want to allow an explicit terminal screen.

## Reading the numbers

- Hidden checks: product-layer 8/12, same as szilu and product-layer+visual; bare 2/12, design-for-ai 3/12,
  kortix-genui 0/2. Invalid YAML alone sinks bare 4/12, design-for-ai 4/12 and kortix 2/2; product-layer is the only
  arm with valid YAML in all 12 runs.
- product-layer gives the shortest flows (2.8 user steps vs 3.6 bare) and the fewest asks on the happy path
  (1.8 vs 3.1 bare, 2.2 szilu).
- Blind review: product-layer beats bare 16:8, szilu 15:9, design-for-ai 20:4, kortix-genui 3:1. It scores higher on
  flow, states, IA, asks, fit and handoff, and lower on scope and clarity against every arm.
- product-layer+visual loses to product-layer 2:6 with the same hidden-check score: loading the visual skills at the
  spec stage adds nothing and costs scope. Keep the order "product-layer first, visual skills after the spec".
- Cost: product-layer sessions are the most expensive (47k tokens per step vs 30k bare, 38k szilu). Per solved step it
  is 71k, against 57k for szilu and 178k for bare.

## Why product-layer loses when it loses (from the verdicts)

1. Rule ids leak into the spec and the reply (`GC-4`, `SR-2`, `TG-6`): judges call them "undecodable codes" and mark
   handoff and clarity down. Principle 7 ("cite rule ids") is meant for audits, not for specs.
2. Dangling or self-looping actions: a chip with no target ("Cheaper options"), an empty-cart exit that points back at
   the empty cart, a stub `landing` screen. Checkout and settings losses are mostly this.
3. Scope: invented features (14-day restore window, budget chip, extra nav) and specs 30% longer than the others.
4. Telegram: TG-6 sends friends into a private chat by deep link, which the stb brief names as the pain; the winning
   pattern is in-group buttons plus callback popups. One spec also put buttons inside callback alerts, which Telegram
   does not support.
5. WarmPlace: product-layer fails the hidden checks in both runs, on `nav` (the tutor gets 6-7 top-level sections,
   limit 5) and `asks` (no slot is asked). It still wins all 12 blind verdicts on this case; the saas-roles module has
   no cap on sections per role.
