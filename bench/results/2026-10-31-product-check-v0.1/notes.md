# product-check v0.1: live-UI bench and crowd run (JEB-2037)

Date: 2026-10-31. Two synthetic fixtures with planted bugs, three arms, two repeats, two iterations of the skill;
then one crowd run of 20 personas on two variants.

## Setup

- **Cases** (`bench/cases/check-*`, served by `bench/live.py serve`):
  - `check-shop` - grocery checkout on regular pages. Planted: re-asked email and password for a signed-in user
    (extra step), "Delivery terms" page with no way out (dead end), promo "Apply" that does nothing (silent control),
    header "Cart (n)" not updated after quantity changes (stale copy / round trip).
  - `check-genui` - chat with streamed answers and components. Planted: skin-type chips in the first message look
    active but ignore clicks (dead button in an old message), budget slider without `role="slider"` or keyboard
    support, slider dead after "Regenerate", "Send routine" form that repeats on every submit.
- **Arms.** `bare` (no skill), `product-check` (`skills/product-check`), `dogfood` (vercel-labs/agent-browser
  `dogfood`, Apache-2.0, pinned to v0.27.0 by `bench/arms/fetch.sh`). Every arm got the same prompt
  (`bench/live.py` TASK) and the same tools: Playwright CLI 0.1.23 and agent-browser 0.27.0 on `PATH`.
- **Sessions.** `claude -p` is not logged in on this runtime, so sessions ran agent-driven: one fresh Sonnet 5.5
  subagent per workspace, isolated `HOME` with only its arm's skills, as in the spec bench.
- **Scoring.** Hidden `check.py` regexes match each `### ISSUE-n` block against the planted bugs; recall is the
  share of planted bugs named by at least one block. The regexes are lenient, so every block was also read by hand
  (table below); the hand count is the result we stand by.
- A first attempt was discarded before scoring: the shop fixture crashed on load (`const top` collides with
  `window.top`) and Playwright CLI looked for its browser in a read-only path. Both fixed; no results kept from it.

## Results (hand-checked recall, planted bugs found out of 4 per run)

| Iteration | Case | bare | product-check | dogfood |
|---|---|---|---|---|
| 1 | check-genui | 2, 3 | 3, 4 | 1, 2 |
| 1 | check-shop | 4, 3 | 3, 3 | 4, 4 |
| 1 | **total** | **12 / 16** | **13 / 16** | **11 / 16** |
| 2 (final) | check-genui | 2, 3 | 3, 4 | 3, 2 |
| 2 (final) | check-shop | 3, 4 | 4, 4 | 3, 4 |
| 2 (final) | **total** | **12 / 16 (0.75)** | **15 / 16 (0.94)** | **12 / 16 (0.75)** |

The regex scores (`report.md`, `iter1/report.md`) differ from the hand count in a few places, in both directions:
the regex credited "Regenerate does nothing" as the dead-slider bug and "old slider" as the accessibility bug,
and missed "header cart count wrong" and "can be re-sent". Hand rules: a bug counts when the block describes its
observable symptom, even with a wrong guess at the cause ("badge counts lines, not items" with 3 units showing
"Cart (2)" counts as the stale counter).

- **product-check vs bare:** 15 vs 12 of 16 in the final iteration, 13 vs 12 in the first. It wins on recall in both
  iterations, by a small margin over two repeats per case.
- **product-check vs dogfood:** 15 vs 12 in the final iteration. In iteration 1 dogfood was better on the shop
  (8/8 vs 6/8): product-check never checked the header counter after changing quantities. That led to the only skill
  change between iterations: WK-3 (round trip) now asks to list every value shown in two places and re-read each
  copy after a change, and genui-walk tells the walker to operate controls missing from the snapshot by position
  and read values before and after. Iteration 2 used fresh workspaces and a new seed for all three arms.
- **What nobody found reliably:** the slider that dies after "Regenerate" (product-check 2 of 4 runs, bare 0 of 4,
  dogfood 0 of 4). Most arms reported "Regenerate does nothing" without testing the new slider.
- **Evidence.** Every product-check finding in both iterations has numbered steps and a screenshot that exists
  (51 of 51); bare 56 of 58, dogfood 49 of 49.
- **Precision is not correctness.** All arms also reported real, unplanted problems in the fixtures: the 490 ₸
  delivery fee from the terms missing in the total, payment choice reset after the terms page, "3 products sent"
  with none added, reload losing the chat. They count against regex precision but are genuine.
- **Cost.** Mean tokens per session, final iteration: product-check 49.5k, bare 39.9k, dogfood 39.6k
  (product-check reads its references and runs more checks). Wall time per session 1-13 minutes.

Two repeats per case is a small sample: one run more or less changes a total by 1-2 bugs. The fixtures were built by
the same agent that wrote the skill, and the hand check was not blind. Next run: a third fixture written by someone
else, a blind X/Y review of the reports, three repeats.

## Crowd run (`crowd/`)

- 20 personas from `personas.py sample --n 20 --optimal 5` (12 hard; 9 hurried, 5 normal, 6 patient; ru / kk / en;
  mobile and desktop; slow network emulated for half), the same 20 on both variants of `check-shop`:
  A (`/check-shop/`, with the "Confirm your account" step) and B (`/check-shop/?variant=b`, without it).
- Each persona ran as a fresh Claude Haiku 5.5 subagent with its `prompt.md`, acting only through its `act` wrapper
  (its own browser session, `PC_BUDGET` = patience). Funnel stages were read from the pages, not from the personas.
- **Result:** completed A 11 / 20, B 19 / 20; hard personas A 3 / 12, B 11 / 12. All 9 drop-offs in A happened at
  `confirm_account`, every one with the re-asked email and password named as the reason. Median actions for
  completers: A 8, B 5 (optimum 5). Direction: B, 90% bootstrap interval of the difference [0.2, 0.6].
- One B persona (patient doubter) quit at checkout because the delivery fee from the terms was missing from the
  total: an unplanted real problem the walk arms also found.
- **Caveat on size.** A needs 8 actions, a hurried persona's budget is 6, so every hurried persona fails A by
  construction. The direction and the drop-off point are the finding; the size of the gap is a product of the
  patience model and must not be read as a conversion forecast.
- **Cost.** 40 sessions, 1.13M context tokens counted by the runtime (27-29k per session, 9-13 tool calls). At Haiku
  5.5 list prices ($0.10 / $0.50 per MTok) that is $0.11 when each session's tokens are counted once
  (`funnel.md`); the upper bound, if every turn re-read the full context at the full input price plus about
  300 output tokens per turn, is about $0.9. Wall time: about 4.5 minutes per batch of 20 in parallel.
- `crowd.py run` (the API runner, Haiku deciding each step) was not exercised: no `ANTHROPIC_API_KEY` on this
  runtime. Its parsing, planning and aggregation are covered by `bench/test_live.py`.
