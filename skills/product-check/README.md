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

The second engine is [agent-browser](https://github.com/vercel-labs/agent-browser) (`--engine agent-browser` or
`PC_ENGINE=agent-browser`; `npm install -g agent-browser@0.27.0`). Same commands, refs as `e12` or `@e12`. Its
screenshots for `look` go through Chrome DevTools and need Node 22+; `--slow` works on Playwright and cdp only.

The third engine, `--engine cdp`, needs no npm package: `scripts/cdp.py` starts headless Chrome with one small
daemon per session, keeps a single DevTools connection open and reads the page state in one `Runtime.evaluate`.
A step takes about 0.5 s against about 5 s through Playwright CLI (JEB-2059), so use it for crowd runs. Chrome comes
from `$PC_CHROME`, else `google-chrome` / `chromium` on `PATH`, else a Playwright or agent-browser download. The
snapshot reads like Playwright CLI's (`- button "Name" [ref=e5]: text`), refs are `e12`, commands are the Playwright
CLI names (click, dblclick, hover, fill, type, select, check, uncheck, press, go-back, go-forward, reload, goto,
console). Not covered: iframes, new tabs, file upload, drag. `pc.py close` stops the browser; an idle daemon stops
itself after `$PC_CDP_IDLE` seconds (default 1800).

Python 3.11+, stdlib only. The light decision tier and `look --ask` need `LIQUID_AI_API_KEY` (Liquid d1-ultra,
`https://api.liquid.ai/v1/systemone`, about $0.00005 per step). Crowd runs over the API also need
`pip install anthropic` and `ANTHROPIC_API_KEY`.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | modes, principles, router |
| `references/walk.md` | QA walk: persona lock, clicks vs optimum, round trip, silent controls, states |
| `references/genui-walk.md` | chat with generative UI: stream markers, component inventory, old messages, regenerate |
| `references/personas.md` | persona schema, hard-persona share, crowd run steps and limits |
| `references/report.md` | finding format, verdict, RED / YELLOW / WHITE / GREEN filter, dedup |
| `scripts/pc.py` | engine wrapper (Playwright CLI, agent-browser or cdp): logged actions, diff after each action, `changed: false`, stream wait, screenshots <= 512 px, metrics |
| `scripts/cdp.py` | the cdp engine: session daemon, minimal websocket client, page snapshot in one evaluate |
| `scripts/d1.py` | light tier: d1-ultra questions about the page and the screen, routing to Haiku / Sonnet |
| `scripts/personas.py` | stratified persona sampler and validator |
| `scripts/crowd.py` | crowd plan, runs routed d1 -> Haiku -> Sonnet, funnel and drop-off aggregation, steps per tier, cost |

## Quick start

```bash
python3 scripts/pc.py open http://localhost:3000            # prints the page as an accessibility tree
python3 scripts/pc.py do --note "add to cart" -- click e12  # prints what changed, or "changed: false"
python3 scripts/pc.py look --ask                            # screenshot <= 512 px; d1: screen vs tree
python3 scripts/pc.py shot issue-1-after                    # shots/issue-1-after.png
python3 scripts/pc.py inventory                             # components in the last chat message

python3 scripts/personas.py sample --n 20 --goal "Buy oat milk" --optimal 5 > personas.json
python3 scripts/crowd.py plan --personas personas.json --flow flow.json \
  --variant A=http://localhost:3000/?v=a --variant B=http://localhost:3000/?v=b --out crowd --engine cdp
python3 scripts/crowd.py run --out crowd --workers 10       # or one Haiku session per crowd/runs/*/prompt.md
python3 scripts/crowd.py aggregate --out crowd              # crowd/funnel.md
```

## Not yet

Browser Use Cloud; protocol mode for generative UI without a browser; video evidence; per-step engine switching
inside one run (a run keeps one browser, so the engine is chosen per run and the tier per step).
