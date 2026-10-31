# bench: repeatable A/B for product-layer

Every change to the skill goes into `main` only after it wins here. The bench gives the same product tasks to fresh,
isolated sessions with no skill, with product-layer and with popular UX skills, then scores each answer with hidden
checks and a blind X/Y review. The protocol follows [lab-forge's bench](https://github.com/adetbekov/lab-forge/tree/main/bench),
adapted to UX: the agent writes a flow-and-screens spec instead of code.

Latest results: [`results/2026-10-31-v0.1`](results/2026-10-31-v0.1/report.md) (full run of v0.1: 6 cases, 2 repeats, 6 arms, 84 blind verdicts).

## Run it

Needs `git`, Python 3.11+ with PyYAML, and for headless runs the `claude` CLI authenticated through
`ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN`. Each session gets its own `HOME` holding only its arm's skills, so
user-level skills and rules never leak in.

```bash
bash bench/arms/fetch.sh                                        # third-party arms at pinned SHAs -> bench/arms/.cache
python bench/bench.py all --out /tmp/plb --cases generic-settings --reps 1      # smoke: bare vs product-layer
python bench/bench.py all --out /tmp/plb \
  --arm bare= --arm product-layer=skills/product-layer \
  --arm szilu=bench/arms/.cache/szilu --arm design-for-ai=bench/arms/.cache/design-for-ai \
  --arm kortix-genui=bench/arms/.cache/kortix-genui --only kortix-genui=betke-skin-quiz \
  --pair product-layer,bare --pair product-layer,szilu --pair product-layer,design-for-ai \
  --pair product-layer,kortix-genui
python bench/bench.py all --out /tmp/plb --arm pl=skills/product-layer \
  --arm pl+visual=skills/product-layer,~/.claude/skills/apple-design,~/.claude/skills/design-taste-frontend
```

`--arm NAME=PATH[,PATH]` takes skill folders (with `SKILL.md`) or folders of skills; an empty value is the bare agent.
Without `--arm` the arms are `bare` and `product-layer=skills/product-layer`, or the stub in `arms/stub/` while the
skill does not exist yet (the bench warns). `--only ARM=CASE[,CASE]` limits an arm to some cases. The result is
`/tmp/plb/report.md` and `/tmp/plb/runs.tsv`; with three or more arms, also one `report-A-B.md` per judged pair. Only
those files, the verdicts and a `notes.md` go into `results/<date>-<what>/`; workspaces and logs stay out of git.

### Without a headless CLI (agent-driven)

When `claude -p` is not available, an orchestrating agent runs each step in a fresh subagent:

1. `bench.py prepare --out DIR` creates the workspaces (`BRIEF.md`, `SPEC-FORMAT.md`, git) and their homes.
2. `bench.py next --out DIR` writes the next prompt for every workspace and prints the paths. Run each one in a new
   session (all in parallel), then `bench.py record --out DIR WS STEP --tokens N --tools N --ms N`. Repeat until
   `next` prints nothing.
3. `bench.py pack --out DIR [--pair A,B]` writes one blind review prompt per case, repeat and order. Run each in a new
   session, on another model line than the agents'; the reviewer saves `<key>.verdict.md` next to the prompt.
4. `bench.py report --out DIR [--pair A,B]`.

If a hidden check turns out to be wrong, fix it and run `bench.py recheck --out DIR`; no session needs to rerun.

## Cases

Each case is `cases/<name>/case.toml` (title, `brief` written to the workspace as `BRIEF.md`, steps, reviewer notes),
`check.py` (the hidden rules) and `ref/good.yaml`, `ref/bad.yaml` (reference answers the tests run the check on).
Product cases describe the product in neutral words; no private code or text from the product repos is copied.

| Case | What the agent designs | Hidden rules besides structure and dead ends |
|---|---|---|
| `betke-skin-quiz` | chat-first skincare advisor: skin quiz to product picks, generative UI | ≤ 4 steps; text-or-block markup matches the reference on 5 of 6 moments; picks have loading, empty, error; asks the skin type, not the phone |
| `stb-split-flow` | Telegram group bot: receipt photo, pick items, mark paid | payer ≤ 2 steps, friend ≤ 4; parse has loading and error; never asks prices, members or names |
| `gentoon-approve` | AI video pipeline: brief, plan, approve, generate | ≤ 3 steps; plan and storyboard have loading and error; plan offers approve and revise; never asks price, seed or model |
| `warmplace-onboarding` | tutoring SaaS: student and tutor onboarding, IA | student ≤ 4 steps, tutor ≤ 5; ≤ 5 nav sections per role; empty dashboard; room loading and error; no time zone or role asked |
| `generic-settings` | settings page with extra steps | digest ≤ 3 steps; settings and export have loading and error; no email, name or time zone asked; delete has confirm and cancel |
| `generic-checkout` | checkout for a returning customer | ≤ 3 steps; empty cart; payment loading and error; saved contact, address and card never re-asked |

The agent's answer is `spec/flow.yaml` in the format of [`spec-format.md`](spec-format.md): flows with entry and done
screens, and per screen what it shows, asks, its states and its actions. `ux.py` runs the deterministic checks:

- `structure`: valid YAML, known targets, every screen reachable from a flow entry;
- `dead_ends`: every screen has a way out;
- `steps`: user actions on the shortest path entry -> done are at most the reference (`by: system` costs nothing);
- `states`: the case's moments describe empty / loading / error where the reference needs them;
- `render`: text-or-block decisions match the reference markup (genui case);
- `asks`: the happy path asks nothing the product already knows, and the spec asks what only the user knows;
- `nav`, `actions`: section count per role, approve-and-revise style choices.

A case is solved when every check it uses passes. Adding a case: write `case.toml`, `check.py` with `RULES` and both
references; `pytest bench` must show the good one passing, the bad one failing on several checks, and an empty
workspace failing.

## Arms

| Arm | Source | License | How it enters the bench |
|---|---|---|---|
| `bare` | none | — | no skills in `HOME` |
| `product-layer` | `skills/product-layer` (JEB-2030), stub until then | MIT | copied into each session's `HOME` |
| `szilu` | [szilu/ux-designer-skill](https://github.com/szilu/ux-designer-skill) | MIT | `arms/fetch.sh`, pinned SHA |
| `design-for-ai` | [ryanthedev/design-for-ai](https://github.com/ryanthedev/design-for-ai), `ai-native` and `journey` only | none stated (not redistributed) | `arms/fetch.sh`, pinned SHA, each part wrapped as a skill |
| `kortix-genui` | [kortix-ai/suna](https://github.com/kortix-ai/suna) `kortix-genui` skill, genui case only | Elastic 2.0 | `arms/fetch.sh`, external path only, never vendored |
| `product-layer+visual` | product-layer plus visual skills given by path | theirs | `--arm` with comma-separated paths; the visual skills stay out of this repo |

Third-party skills are fetched into `bench/arms/.cache/` (git-ignored) and never committed.

## Blind review

`rubric.md` asks a strong model on another line than the agents' (default `claude-fable-5-1`) to score X and Y from 1
to 5 on success, flow, states, IA, asks, platform fit, handoff to visual and engineering, scope and clarity, and to
name a winner. Workspace names are hashes, the brief and format files are removed from the snapshots, and every pair
is judged in both orders against position bias.

## Cost

One session is about 30k tokens and one verdict about 33k (smoke, Sonnet sessions). The full run above (6 cases,
3 repeats, four arms plus `kortix-genui` on one case, four judged pairs) is 75 sessions and 114 verdicts: about 6M
tokens.
