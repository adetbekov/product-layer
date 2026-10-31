# product-check

Checks a built interface by using it like its user: a QA walk by one agent, or a crowd of personas on two variants.
Companion of `skills/product-layer` (which decides what to show before visual work); product-check runs after the UI
is built and reports where it fails the user, with rule ids from both skills.

## Install

```bash
cp -r skills/product-check ~/.claude/skills/
npm install -g @playwright/cli@0.1.23           # pinned engine version, Apache-2.0
playwright-cli install-browser chromium         # or use an installed Chrome
```

`scripts/pc.py` finds the engine as `$PC_PLAYWRIGHT_CLI`, then `playwright-cli` on `PATH`, then
`npx -y @playwright/cli@0.1.23`. Without Chrome, set `PLAYWRIGHT_MCP_BROWSER=chromium`. The engine refuses `file:`
URLs: serve local pages over HTTP (`python3 -m http.server`).

Python 3.11+, stdlib only. Crowd runs over the API also need `pip install anthropic` and `ANTHROPIC_API_KEY`.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | modes, principles, router |
| `references/walk.md` | QA walk: persona lock, clicks vs optimum, round trip, silent controls, states |
| `references/genui-walk.md` | chat with generative UI: stream markers, component inventory, old messages, regenerate |
| `references/personas.md` | persona schema, hard-persona share, crowd run steps and limits |
| `references/report.md` | finding format, verdict, RED / YELLOW / WHITE / GREEN filter, dedup |
| `scripts/pc.py` | engine wrapper: logged actions, diff after each action, `changed: false`, stream wait, metrics |
| `scripts/personas.py` | stratified persona sampler and validator |
| `scripts/crowd.py` | crowd plan, parallel run on Claude Haiku, funnel and drop-off aggregation, cost |

## Quick start

```bash
python3 scripts/pc.py open http://localhost:3000            # prints the page as an accessibility tree
python3 scripts/pc.py do --note "add to cart" -- click e12  # prints what changed, or "changed: false"
python3 scripts/pc.py shot issue-1-after                    # shots/issue-1-after.png
python3 scripts/pc.py inventory                             # components in the last chat message

python3 scripts/personas.py sample --n 20 --goal "Buy oat milk" --optimal 5 > personas.json
python3 scripts/crowd.py plan --personas personas.json --flow flow.json \
  --variant A=http://localhost:3000/?v=a --variant B=http://localhost:3000/?v=b --out crowd
python3 scripts/crowd.py run --out crowd --workers 10       # or one Haiku session per crowd/runs/*/prompt.md
python3 scripts/crowd.py aggregate --out crowd              # crowd/funnel.md
```

## Not in v0.1

Jev / TypeSafe decision models, Browser Use Cloud and runs of 1000 personas (next iteration, after the API key
decision); protocol mode for generative UI without a browser; video evidence.
