# Credits

product-layer is written from scratch. The ideas below come from other skills,
guides and books; they are re-expressed in our own words. No text is copied.
Sources under non-permissive licenses (Elastic 2.0, CC-BY-NC-SA, Commons
Clause) were used only as inspiration for ideas, never as text.

Research behind these choices: `docs/research/2026-10-ux-skills-landscape.md`.

| Source | License | Ideas used | Where |
|---|---|---|---|
| [szilu/ux-designer-skill](https://github.com/szilu/ux-designer-skill) | MIT | modal / panel / page decision; suggest → act-with-undo autonomy scale; design every state; Tesler's law; 1-2 onboarding questions, progressive profile | `ia.md` IA-6, `ai-pipeline.md` AP-2, `states.md` ST-1, `step-reduction.md` SR-1, `onboarding.md` ON-2/3 |
| [ryanthedev/design-for-ai](https://github.com/ryanthedev/design-for-ai) (`ai-native`, `journey`) | MIT | goal contract before generation; flow states; page spec structure | `ai-pipeline.md` AP-3, `states.md` template |
| [julianoczkowski/designer-skills](https://github.com/julianoczkowski/designer-skills) (information-architecture) | Apache-2.0 | short IA interview; page content priorities; naming glossary | `ia.md` inventory, IA-4, IA-5 |
| [rampstackco/claude-skills](https://github.com/rampstackco/claude-skills) (information-architecture) | MIT | top tasks within a few clicks; categories vs tags | `ia.md` IA-1, IA-7 |
| [ThomasPraun/ux-flow-designer](https://github.com/ThomasPraun/ux-flow-designer) | MIT | use cases with pre/post-conditions and alternative branches; diagram size limit | `flows.md` FL-1, FL-5 |
| [bitjaru/styleseed](https://github.com/bitjaru/styleseed) `ss-flow` (copied as lingxling/ux-flow) | MIT | no dead ends; entry and exit for every flow | `flows.md` FL-2, FL-3 |
| [wondelai/skills](https://github.com/wondelai/skills) | MIT | steps-to-value; remove → default → defer → combine; Krug / Nielsen heuristics | `step-reduction.md`, `review.md` |
| cuellarfr design-critique / interaction-design | MIT | keep / cut / automate / hide test per step; frequent full-page forms become inline; chips and bounded sliders over number fields | `step-reduction.md` step test, SR-6, `ia.md` IA-6 |
| civitai ux-design | Apache-2.0 | state template; screen spec with entry / exit points | `states.md` |
| [Owl-Listener/designer-skills](https://github.com/Owl-Listener/designer-skills) | MIT | when conversation beats a form; Tesler's law | `genui-chat.md`, `step-reduction.md` SR-1 |
| [imsaif/aiux-skills](https://github.com/imsaif/aiux-skills) | MIT | buttons instead of suggestions; no empty chat; editable previews | `genui-chat.md` GC-4, GC-5, GC-10 |
| [CopilotKit OpenIntelligentUI](https://github.com/CopilotKit) | MIT | one presentation per turn; controls compute locally, only explicit actions reach the agent | `genui-chat.md` GC-6, GC-7 |
| kortix-genui (kortix-ai/suna) | Elastic-2.0 (ideas only) | routing by content shape (choices → cards, process → steps, short facts → text); answer first, assume the typical case | `genui-chat.md` router, GC-1, GC-3 |
| Google A2UI, Vercel AI SDK generative UI docs | Apache-2.0 / docs | closed catalogue of components described as tools | `genui-chat.md` GC-2 |
| Tambo, BuilderIO generative UI articles | docs | component in chat vs page the AI updates; one-off result stays in chat, saved result gets a page | `genui-chat.md` GC-9 |
| Shape of AI (shapeof.ai) | CC-BY-NC-SA-4.0 (ideas only) | AI pattern vocabulary used as a checklist when writing the pipeline module | `ai-pipeline.md` |
| Microsoft HAX guidelines, Google PAIR Guidebook | public guidance | make clear what the system can do; efficient correction; explain AI behaviour | `ai-pipeline.md`, `genui-chat.md` |
| Vercel agent-skills (react-best-practices) | MIT | rule format: one rule, why, bad / good, impact | all reference files |
| Vercel web-design-guidelines | MIT | form and navigation checks | `review.md` heuristic pass |
| [Anthropic frontend-design skill](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | Apache-2.0 | copy of empty and error states | `states.md` ST-2, ST-4 |
| [AccessLint claude-marketplace](https://github.com/accesslint/claude-marketplace) | MIT | finding format with severity, confidence, what was not verified | `review.md` |
| borghei/Claude-Skills product-designer | MIT + Commons Clause | reviewed, nothing taken | - |
| Steve Krug, *Don't Make Me Think*; Jakob Nielsen, 10 usability heuristics; Larry Tesler, law of conservation of complexity | books / articles | heuristic pass; ask only what only the user knows | `review.md`, `step-reduction.md` |
| [Telegram Bot API](https://core.telegram.org/bots/api) | docs | platform facts: bots cannot message users first, edited messages do not notify, 64-byte callback data, deep-link start parameter | `telegram-bot.md` |

## product-check

`skills/product-check` is also written from scratch. Research behind it: JEB-2036,
`docs/research/2026-10-qa-user-simulation.md`. Text from borghei (Commons Clause), SimAB (CC BY-NC-ND) and Skyvern
(AGPL) is not copied; where their ideas overlap ours they are re-expressed below.

| Source | License | Ideas used | Where |
|---|---|---|---|
| [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) `dogfood` | Apache-2.0 | reproduce before recording; evidence matched to the bug type; record each issue when found; never read the app's source; 5-10 well-evidenced findings; do not wait for network idle on streams | `walk.md`, `genui-walk.md`, `SKILL.md`; bench arm |
| [jezweb/claude-skills](https://github.com/jezweb/claude-skills) `ux-audit` | MIT | persona lock and drift check; clicks against the optimum; round trip A to B to A; "a click that changed nothing is a bug"; five questions per step; fresh-subagent dedup with KEEP / GENERIC / DUPLICATE; no pass without an artifact | `walk.md`, `report.md`, `personas.md` |
| [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) `adversarial-ux-test` | MIT | RED / YELLOW / WHITE / GREEN filter for persona complaints; "would a busy competent adult complain too" | `report.md` RP-2 |
| [garrytan/gstack](https://github.com/garrytan/gstack) `/qa-only` | MIT | exact repro before a bug counts | `walk.md` |
| [ncklrs/claude-chrome-user-testing](https://github.com/ncklrs/claude-chrome-user-testing) | MIT | persona as a JSON card with patience and frustration triggers | `personas.md` |
| [neuhai/UXAgent](https://github.com/neuhai/UXAgent) | MIT | batch personas from stratified axes | `personas.py` |
| vizron (CHI'26 workshop), AgentA/B (arXiv 2504.09723), SimAB (arXiv 2603.01024, ideas only), Park et al. (arXiv 2411.10109) | papers | persona decides, executor clicks; agents are hyper-rational, so explicit patience budgets and hard personas; simulations give direction, not effect size | `personas.md`, `crowd.py` |
| [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli) | Apache-2.0 | browser engine (pinned 0.1.23), snapshots to files | `scripts/pc.py` |
| [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | Apache-2.0 | second browser engine (0.27.0): `@e` refs, `wait --fn` | `scripts/pc.py` |
| [browser-use/jev-ultrafast](https://github.com/browser-use/jev-ultrafast) | MIT | indexed element table; one decision-model request with an operation question plus speculative target questions; text written by an LLM only when the operation needs it | `scripts/d1.py` |
| [browser-use/jev-ultrafast](https://github.com/browser-use/jev-ultrafast) Browser Harness | MIT | a long-lived direct CDP session instead of a browser CLI per action; the page state read in one `evaluate`; real input events through `Input.*` (code written from scratch) | `scripts/cdp.py`, `scripts/pc.py --engine cdp` |
| [Liquid AI d1 / systemone API](https://docs.liquid.ai) | docs | choice / noul / score questions, thresholds with an unsure band, images as `data:` URLs | `scripts/d1.py` |
| borghei/Claude-Skills `qa-browser-automation` | MIT + Commons Clause | reviewed, nothing taken | - |
| Skyvern | AGPL-3.0 | reviewed, nothing taken | - |
