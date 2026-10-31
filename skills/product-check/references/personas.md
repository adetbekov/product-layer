# personas - who walks the product, and how a crowd runs

A persona is a short JSON card that fixes how a simulated user decides. In
walk mode one persona is locked for the whole pass. In crowd mode many
personas run the same goal on two variants, one isolated browser each.

## Schema

```json
{
  "id": "p07",
  "name": "Айгерим",
  "goal": "Buy oat milk and rye bread with delivery",
  "tech": "low | mid | high",
  "patience": {"label": "hurried | normal | patient", "steps": 6},
  "ai_trust": "low | mid | high",
  "device": {"type": "mobile | desktop", "network": "fast | slow"},
  "lang": "ru | kk | en",
  "constraints": ["budget under 5000 tenge", "allergic to nuts"],
  "traits": ["hurried | doubter | quitter"],
  "hard": true,
  "voice": "one sentence on how this person thinks"
}
```

- `goal` is a job in the user's words, never a feature tour.
- `patience.steps` is the action budget. `scripts/personas.py` derives it from
  the optimal path: hurried = optimum + 1, normal about 1.6x + 2, patient
  about 2.5x + 3. `pc.py` refuses actions past it (`PC_BUDGET`).
- `hard` is true for hurried, doubting or quitting personas and for low tech.

## PS-1 · Lock the persona before the first click · HIGH

**Check.** The persona card is written before the walk starts and quoted in
the report.
**Why.** Without a lock the agent drifts to a developer's view and finds
developer problems.
**Bug if.** (In the report.) Findings depend on knowledge the persona does
not have.

## PS-2 · At least a third are hard · CRITICAL

**Check.** `personas.py validate` fails when fewer than 30% are hard.
**Why.** Simulated users are hyper-rational: they make fewer actions than
people and rarely quit. Hard personas and a strict action budget push back
on that bias.
**Bug if.** A crowd of patient experts reports a flow as fine.

## PS-3 · Stratify, do not randomise · HIGH

**Check.** Every axis value appears in proportion (the sampler cycles values
and shuffles them). Prefer personas built from real interviews or analytics
when they exist, and say which source was used.
**Why.** A persona in the prompt barely changes an agent's path; variety must
come from explicit axes and budgets, and real-data personas beat
demographic ones.
**Bug if.** All personas share a language, device or patience level.

## PS-4 · The page decides the outcome, not the persona · CRITICAL

**Check.** Completion is read from the page (funnel stages in `flow.json`),
not from the persona's "done". `crowd.py aggregate` counts "said done, page
disagrees" separately.
**Why.** Model users claim success they did not reach.
**Bug if.** A run is counted as completed without the final stage on screen.

## Crowd run

1. **Flow file.** `flow.json` with the goal, optimal action count, facts the
   persona knows (account email, address), and ordered funnel stages matched
   by URL or page text. Mark stages that exist only in one variant with
   `"only": ["A"]`.
2. **Personas.** `personas.py sample --n 20 --goal "..." --optimal N`, then
   `personas.py validate`. Same personas on both variants, so the difference
   comes from the variant, not the sample.
3. **Plan.** `crowd.py plan --personas p.json --flow flow.json --variant
   A=URL --variant B=URL --out DIR [--driver mixed]` writes one `prompt.md`
   and one `act` wrapper per persona and variant. Every action also saves a
   screenshot of at most 512 px (`--no-look` turns it off).
4. **Run.** Each step goes to the cheapest model that can take it
   (`--driver mixed`, the default; see the table below). With
   `ANTHROPIC_API_KEY` and `LIQUID_AI_API_KEY`: `crowd.py run --out DIR`
   (personas in parallel, each in its own browser session). Without an
   Anthropic key: run every `prompt.md` in a fresh Haiku session, all in
   parallel; in mixed runs that session calls `./act auto` and decides only
   the steps d1 hands back. Then `crowd.py record` the tokens each session
   used.
5. **Aggregate.** `crowd.py aggregate --out DIR` writes `funnel.md` and
   `funnel.json`: stage reach per variant, completion for all and for hard
   personas, the top drop-off stage, clicks that changed nothing, a bootstrap
   interval for the direction, steps per decision tier and the cost (Claude
   plus d1) per persona.

### Decision tiers

The model that decides sets the price of a run, not the browser engine.

| Tier | Decides | Takes |
|---|---|---|
| light | d1-ultra (`scripts/d1.py`): one request of choice / yes-no / score questions over the persona, the page's controls and the screenshot; the choice is drawn from its probabilities | clicks among visible controls, going back, done, quit |
| medium | Claude Haiku, tree + screenshot | d1 unsure (choice confidence < 0.5, done or quit between 0.2 and 0.8), text and form input, a control on screen missing from the tree, an error screen |
| hard | Claude Sonnet, tree + screenshot | the last action changed nothing; the page is not recognised (no controls, confusion score >= 2.5 of 3); walk mode always |

`--driver haiku` or `--driver sonnet` puts every step on one model; use them
as baselines. `--engine agent-browser` runs the same commands on
agent-browser instead of Playwright CLI; `--engine cdp` on a direct DevTools
session, about 0.5 s a step instead of about 5 s, with the same funnel.
6. **Report.** Cluster drop-off reasons and dead clicks into findings with
   `report.md`; replay the top cluster in walk mode to get steps and a
   screenshot.

## Limits to state in every crowd report

- Direction, not size: simulations pick the better variant in roughly two of
  three to four of five A/B tests and overstate effects. Never quote a
  completion rate as a forecast.
- Personas from the sampler are not calibrated to a real audience (none are
  for Kazakhstan yet). Calibrate on one real A/B before trusting direction.
- Emotions, trust, real money and accessibility still need people.
