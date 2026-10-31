# Credits

product-layer is written from scratch. The ideas below come from other skills,
guides and books; they are re-expressed in our own words. No text is copied.
Sources under non-permissive licenses (Elastic 2.0, CC-BY-NC-SA, Commons
Clause) were used only as inspiration for ideas, never as text.

Research behind these choices: `docs/research/2026-10-ux-skills-landscape.md`.

| Source | License | Ideas used | Where |
|---|---|---|---|
| [szilu/ux-designer-skill](https://github.com/szilu/ux-designer-skill) | MIT | modal / panel / page decision; suggest → act-with-undo autonomy scale; design every state; Tesler's law; 1-2 onboarding questions, progressive profile | `ia.md` IA-6, `ai-pipeline.md` AP-2, `states.md` ST-1, `step-reduction.md` SR-1, `onboarding.md` ON-2/3 |
| [ryanthedev/design-for-ai](https://github.com/ryanthedev/design-for-ai) (`ai-native`, `journey`) | see repo | goal contract before generation; flow states; page spec structure | `ai-pipeline.md` AP-3, `states.md` template |
| [julianoczkowski/designer-skills](https://github.com/julianoczkowski/designer-skills) (information-architecture) | Apache-2.0 | short IA interview; page content priorities; naming glossary | `ia.md` inventory, IA-4, IA-5 |
| [rampstackco/claude-skills](https://github.com/rampstackco/claude-skills) (information-architecture) | MIT | top tasks within a few clicks; categories vs tags | `ia.md` IA-1, IA-7 |
| [ThomasPraun/ux-flow-designer](https://github.com/ThomasPraun/ux-flow-designer) | MIT | use cases with pre/post-conditions and alternative branches; diagram size limit | `flows.md` FL-1, FL-5 |
| styleseed `ss-flow` (via lingxling/ux-flow) | see repo | no dead ends; entry and exit for every flow | `flows.md` FL-2, FL-3 |
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
| Anthropic frontend-design skill | see repo | copy of empty and error states | `states.md` ST-2, ST-4 |
| AccessLint | see repo | finding format with severity, confidence, what was not verified | `review.md` |
| borghei/Claude-Skills product-designer | MIT + Commons Clause | reviewed, nothing taken | - |
| Steve Krug, *Don't Make Me Think*; Jakob Nielsen, 10 usability heuristics; Larry Tesler, law of conservation of complexity | books / articles | heuristic pass; ask only what only the user knows | `review.md`, `step-reduction.md` |
| [Telegram Bot API](https://core.telegram.org/bots/api) | docs | platform facts: bots cannot message users first, edited messages do not notify, 64-byte callback data, deep-link start parameter | `telegram-bot.md` |
