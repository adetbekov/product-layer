# product-check v0.2: decisions by step difficulty, vision (JEB-2058)

Date: 2026-10-31 to 2026-11-01. A crowd run of the same 20 personas on both `check-shop` variants with three
decision setups, a walk on three cases, and a d1 vision probe.

## What changed

- `pc.py` drives Playwright CLI or agent-browser through one interface (`--engine`, `PC_ENGINE`). `look` saves a
  screenshot of at most 512 px; `look --ask` asks d1-ultra what the screen shows that the tree does not. `PC_LOOK=1`
  takes a look after every action.
- `d1.py`: the light tier. One `/v1/systemone` request per step with the persona, the goal, recent actions, the
  page's controls and the screenshot. It asks what the person does next, which control, would they quit, is the goal
  reached, how unclear the page is, why they would leave, and two vision questions. The choice is drawn from its
  probabilities, ignoring options under 0.1.
- `crowd.py` routes each step: d1 when it is sure; Haiku when d1 is unsure, text is needed, a control is on screen but
  not in the tree, or the screen shows an error; Sonnet when the last action changed nothing or the page is not
  recognised. `crowd.py run` does this over the API; `./act auto` does it inside an agent-driven session.
- New live case `check-visual` (cinema tickets): a seat map drawn on canvas, a pale "Pay" button next to a bold
  secondary one, and "Download ticket" placed off screen.

## Setup

- **Crowd.** Personas: the 20 from JEB-2037 (`2026-10-31-product-check-v0.1/crowd/personas.json`), 12 hard. Variants:
  A `/check-shop/` (with the "Confirm your account" step) and B `/check-shop/?variant=b`. Three setups, 40 sessions
  each, every session a fresh subagent with its `prompt.md` and its own browser (Playwright CLI, screenshots on):
  - `mixed`: Haiku 5.5 session that calls `./act auto`; d1-ultra plays the steps it is sure about.
  - `haiku`: Haiku 5.5 decides every step.
  - `sonnet`: Sonnet 5.5 decides every step.
- **No Anthropic API key on this runtime**, so Haiku and Sonnet ran as subagents, as in JEB-2037. d1-ultra ran over the
  hosted API with `LIQUID_AI_API_KEY`; its cost is the `usage.cost` the API returned.
- **Walk.** `live.py` with the v0.2 skill on `check-shop`, `check-genui` and `check-visual`, 2 repeats each, Sonnet 5.5,
  isolated `HOME`. On `check-visual` also the v0.1 skill from `main`, 2 repeats.
- **Discarded.** A first `mixed` run (30 sessions) used plain sampling over all options. 8 of 130 d1 clicks came from the
  tail of the distribution at p of 0.01 to 0.1, for example the logo while Checkout had 0.99. These detours cost
  hurried personas their budget. Sampling now ignores options under 0.1 (`d1.FLOOR`). All 40 `mixed` sessions were
  re-run on the fixed code, and only the re-run is reported. One session of the first run (A-p03) also ignored
  `./act auto`, because the prompt still said to start with `./act open`. That was fixed in the same change.

## Crowd results

| | mixed | all Haiku | all Sonnet | JEB-2037 (Haiku, no vision) |
|---|---|---|---|---|
| Completed A / B | 11/20 / 20/20 | 11/20 / 20/20 | 10/20 / 20/20 | 11/20 / 19/20 |
| Hard personas completed A / B | 3/12 / 12/12 | 3/12 / 12/12 | 2/12 / 12/12 | 3/12 / 11/12 |
| Top drop-off (A) | confirm_account: 9 | confirm_account: 9 | confirm_account: 10 | confirm_account: 9 |
| Direction, 90% interval of B - A | B, [0.25, 0.65] | B, [0.25, 0.65] | B, [0.3, 0.7] | B, [0.2, 0.6] |
| Median actions, completers A / B | 8 / 5 | 8 / 5 | 8 / 5 | 8 / 5 |
| Steps decided: d1 / Haiku / Sonnet | 210 / 60 / 0 (78% / 22% / 0%) | 0 / 252 / 0 | 0 / 0 / 241 | - |
| Tool calls per session (mean) | 4.8 | 9.5 | 8.3 | 9-13 |

All three setups give the same direction (B) and the same drop-off point (`confirm_account`, every drop-off reason
names the re-asked email and password). The mixed run matches all-Haiku on every funnel number.

Escalations in the mixed run (245 d1 requests): 20 for text input (the confirm form), 2 for an unsure click, 13 for a
quit probability inside 0.2-0.8. None went to Sonnet. No click on this path changed nothing, and no page went
unrecognised, so the Sonnet tier is covered only by unit tests here.

## Cost per persona

| | mixed | all Haiku | all Sonnet |
|---|---|---|---|
| d1-ultra (API bill) | $0.00030 | - | - |
| Session tokens counted once, input price (JEB-2037 method) | $0.00289 | $0.00293 | $0.0569 |
| Upper bound: each turn re-reads the session context, no cache | $0.0158 | $0.0309 | $0.532 |
| Projected API run (`crowd.py run`): one Claude call per Claude step, measured page sizes | $0.0005 | $0.0009 | $0.017 |

- The JEB-2037 measure (each session's tokens once) is lower for mixed than for all-Haiku, by about 1%. Each session
  starts at about 22k tokens of agent context, whoever decides, so this measure barely moves.
- Mixed sessions make half the tool calls (4.8 against 9.5). With fewer turns, the realistic bill (between the two
  bounds) is about half of all-Haiku's.
- In an API run with no agent overhead, a d1 step costs about $0.00005 (about 1 200 input tokens over 6-9 questions and
  a 512 px screenshot). A Haiku step costs about $0.0001. The projection uses the page snapshots from these runs and
  80 output tokens per call; it is an estimate, not a measured bill.
- Sonnet decides like Haiku on this flow (direction and drop-off agree) at about 20 times the price.

Per-session tokens and tool calls: `crowd-sessions.tsv`. Every d1 request with its answers and route:
`crowd-mixed/d1-decisions.jsonl`.

## Walk results (hand-checked)

| Case | v0.2 (this skill) | v0.1 (`main`) | JEB-2037 v0.1 final |
|---|---|---|---|
| check-shop, 4 planted | 4, 4 | - | 4, 4 |
| check-genui, 4 planted | 4, 4 | - | 3, 4 |
| **shop + genui** | **16 / 16** | - | 15 / 16 |
| check-visual, 3 planted | 2, 3 | 2, 2 | - |

- The regex scores (`walk/report.md`) agree with the hand count. Every matched block was read. On genui both runs
  tested the slider after "Regenerate" and the slider's missing role and keyboard support. Both shop runs found the
  stale header counter.
- check-visual: both versions found the off-screen "Download ticket". v0.2 found the canvas seat map in both runs and
  the pale "Pay" in one. v0.1 found the canvas once and the pale Pay once. With two runs each, this is a lead, not a
  win.
- No walker used `PC_LOOK=ask` (d1 vision). Five of six v0.2 walks took screenshots with `PC_LOOK=1` (one of them
  only twice) and judged them by eye; one session wrote that it skipped the ask step. The visual findings came from
  Sonnet reading screenshots, which is the hard tier the skill asks for.
- Evidence: every v0.2 matched finding has numbered steps and an existing screenshot (recall with evidence = recall).
- Examples: `examples/check-visual-9583cc` (3/3) and `examples/check-shop-15a036`.

## d1 vision probe (`vision-probe.md`)

`pc.py look --ask` along the check-visual purchase, Playwright CLI, 4 screens, $0.00009 in total:

- Confirmation page: "Download ticket" is in the tree, but d1 rates it visible at p = 0.00, while "Book another" is the
  main action (0.92). The off-screen button is caught.
- Payment: "Pay 3 200 ₸" is visible at p = 0.15, and "Change seat" looks like the main action. The contrast bug is
  caught.
- Seat map: "control on screen but not in the tree" is p = 0.41, inside the unsure band, so the canvas is not caught
  by d1 alone. In crowd runs that answer escalates to Haiku only above 0.8.

## Limits

- One flow, 20 personas, three setups: the agreement on direction and drop-off is evidence for this flow, not a
  general guarantee. Calibrate thresholds (`d1.CONFIDENT`, `d1.BAND`, `d1.FLOOR`) on a real A/B before trusting them
  elsewhere.
- Costs for Haiku and Sonnet are estimates from subagent token counts, not API bills; only d1 is a real bill.
- d1-ultra questions are in English and its state is English; personas' languages only affect the Claude tiers.
- The fixtures, including check-visual, were written by the agent that wrote the skill, and the hand check was not
  blind.
