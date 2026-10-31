## Блок 4. Коммерческие сервисы синтетических пользователей и AI-юзабилити-тестов

Дата среза: 2026-10-31. Источники указаны по номерам [N], список в конце. Если факт найти не удалось, так и написано («н/д» означает «нет данных в открытых источниках»). Большинство цифр точности сообщают сами вендоры, независимой проверки почти нигде нет.

### Две разные категории (важно для сравнения)

1. **Агенты в реальном интерфейсе** (кликают живой URL или прототип): Simulithic, Uxia, FuguUX, частично Synthetic Users (live-website стимулы), SimUX (заявлено), Blok/Seldon (Figma + данные продукта).
2. **Симуляция мнений и аудиторий** (опросы, фокус-группы, реакции на концепт, текст или картинку): Simile, Artificial Societies, Brox, Aaru, Vectorial (смешанный вариант, заявляет тесты AI-агентов и продуктовых путей), Evelance.

Для нашего скилла (product-layer, генеративный UI в чате) полезны обе: из первой берём механику прогона флоу, из второй берём методологию персон и валидации.

### Сводная таблица

| Сервис | URL | Что делает | Реальный браузер | Отчёт | Масштаб | Цена | Валидация (заявлено) | Деньги / команда |
|---|---|---|---|---|---|---|---|---|
| Simile | simile.com | Фундаментальная модель поведения людей. Симуляции популяций для концептов, цен, сообщений, удержания [1] | Нет. Тест UI-апдейтов упомянут только в прессе [3] | Сравнение сценариев на одной популяции, у каждого результата метка уверенности [1] | 1000 агентов в исследовании 2024 [1][4] | По запросу, частично по числу агентов [5] | 85% от точности самоповтора людей (GSS, 1052 чел.) [4]. Более 7000 сверок с людьми в неделю [1] | $100M A (Index, фев-2026) [3], $200M B при оценке $2B (Greenoaks, июль-2026) [2]. Park, Bernstein, Liang (Stanford) |
| Vectorial | vectorial.ai (сайт пуст для парсера) | Синтетические пользователи на модели SAPIENS. Тест продуктового пути, кампании или **клиентского AI-агента** в web, mobile и AI-native приложениях [6] | н/д | «Наблюдаете реакцию модельных клиентов», первые выводы за минуты [6] | Смоделировано 2,5M+ людей, 30k+ симуляций [6]. У одного клиента 10k сессий с AI-агентами за часы [7] | н/д | +30% точности к общим LLM, >85% воспроизведения прошлых user-study [6] | $3M seed (Smilegate, SenseAI, окт-2026) [6] |
| FuguUX | fuguux.com | AI User Test (агенты выполняют задачи на сайте), CX Scan (автопроверки), Site Audit [8] | Вероятно да (граф действий агента на сайте), но явно не сказано [8] | Оценка CX, проблемы по severity, roadmap. По каждому агенту: граф действий и usability-оценка [8] | До 20 персон за тест [9] | **Публичная**: 1 кредит = $8–10, 2 кредита на агента, 10 кредитов бесплатно [9] | Нет цифр [8] | н/д |
| Simulithic | simulithic.com | AI-«пользователи» сами картируют флоу (`simulithic map <url>`) и прогоняют их как E2E (`simulithic qa`) [10] | **Да**: изолированная VM на флоу, Safari, Chrome, Firefox, iOS, Android, профили сети от 3G до 5G [10] | Комментарий в PR о том, что сломалось. Алерты в Slack из продакшена, интервал до 30 мин [10][11] | н/д (персон нет, это QA) | н/д («Plans» без цен) [10] | Нет цифр [11] | YC F26, запуск 21.10.2026. Ryan Ning, Satyam Singh [11]. Dealroom: $500K [12] |
| Blok, ныне, вероятно, Seldon | joinblok.co → редирект на seldon.com | Агенты-персоны по данным продукта клиента, прогоны экспериментов. На входе Figma + гипотеза + цель пользователя [13][14]. Сейчас: Finch (UX), Wren (QA) [15] | Частично (Figma-флоу) [14] | «Где расходятся траектории» + доказательства [15] | н/д | По запросу (demo) [15] | 87% «behavioral fidelity», совпадение выборов с людьми на всём пути, методика не раскрыта [15] | $7,5M seed (MaC VC, июль-2025). Tom Charman, Olivia Higgs [13]. Футер seldon.com: «© 2026 Blok Intelligence Inc.» [15] |
| SimUX | simux.ai | Агенты симулируют сессии: онбординг, checkout, pricing, A/B вариантов [16][17] | н/д | Сравнение A/B по Clarity, Navigation, Friction, Cognitive Load, Completion Likelihood, Path Efficiency, Trust Signals [17] | «5000+ синтетических пользователей» [17] | По запросу (созвон) [17] | Нет [17] | Основана в 2026, Майами [16] |
| Synthetic Society | syntheticsociety.ai | Одна строка: «синтетические пользователи для автоматизации E2E QA и UX-тестов» [18] | н/д | н/д | н/д | н/д | н/д | PitchBook: SF, 2025, 2 сотрудника, $500K seed [19]. Не путать с Arima «Synthetic Society™» [19]. Данных почти нет |
| Brox.ai | brox.ai | 60 000 цифровых двойников реальных людей (часы интервью, до 300 стр. данных на человека). Опросы с цепочкой рассуждений [20] | Нет | Ответы + reasoning chain [20] | 60k двойников [20] | **$100k–1,5M в год**, безлимит [20] | «Validated», без цифр [20][21] | ~14 чел., CEO Hamish Brocklebank. Scribble, Wonder, Vela [20] |
| Artificial Societies | societies.ai (бывш. societies.io) | Сети связанных персон (социальный граф, влияние). Опросы, фокус-группы, conjoint, «multiverse»-эксперименты [22][23] | Нет | Рынок, сегмент, отдельная персона [23] | Общества от 12 до 3500 персон, база 3M+ персон [22][23] | По запросу [22] | 86% distribution accuracy против 91% потолка самоповтора людей, 1000 опросов. Галлюцинации <2% [23] | $5,35M (Unite.ai) [24], YC [25] |
| Synthetic Users | syntheticusers.com | AI-интервью с персонами (OCEAN-профиль). Стимулы: картинки, видео, **живой сайт**. RAG по данным клиента [26][27] | Частично (live-website стимул, механика не раскрыта) [26][27] | Executive summary, темы, цитаты, рекомендации, транскрипты, saturation score [27] | 10–12 для качественного исследования, сотни для количественного [26] | **Публичная**: от $12 500/год, $2–60 за интервью [26] | 85–92% «synthetic-organic parity», 21 рецензируемая статья [27][28] | н/д |
| Uxia | uxia.app | Немодерированные юзабилити-тесты: AI-тестеры ходят по Figma-прототипам, живым сайтам и AI-сгенерированным приложениям (в т.ч. за логином), думают вслух [29] | **Да** (navigate + think aloud) [29] | Единый отчёт AI + люди: паттерны, точки трения, аналитика [29] | Free: 1 тест × 3 тестера. Custom: без лимита [30] | Free / по запросу [30] | Калибровка по «Golden Dataset», страницы о паритете AI и людей. Цифры: «17x быстрее», «~15 мин до инсайта» [29] | ~€1M pre-seed (дек-2025), Барселона [31]. **MCP-интеграция** с ChatGPT, Codex, Claude [29] |
| Evelance | evelance.io | Предиктивные персоны: оценка дизайна, A/B, бенчмарк конкурентов, в т.ч. по live URL [32][33] | Неясно (вероятнее оценка, не клики) | «Scored feedback» за ~10 мин, synthesis-отчёты [33] | База 1M+ / 1,8M+ / 800M+ (цифры расходятся) [32][33] | **Публичная**: $2,99 за персону, $2,39 при пакете на 300 [33] | 89,78% совпадения с людьми, источник G2, методики нет [34] | н/д |
| Aaru | aaru.com (сайт не открывался) | Синтетические популяции для прогнозов: опросы, продукты, политика [35] | Нет | н/д | ~5000 агентов в кейсе праймериз NY [35] | н/д | Праймериз NY-2024: ошибка <400 голосов [35] | Series A, оценка $1B, лид Redpoint (дек-2025) [35][36] |

### Оценки 1–5

«Цена 100/1000» считается по публичному прайсу. Где цены нет, стоит «?» (условно 2: enterprise-продажи). Встраиваемость: наличие API, MCP или CLI.

| Сервис | Реальный браузер | Gen-UI в чате | Качество отчёта | Масштаб | Цена 100/1000 | Простота старта | Реализм (подтверждённость) | Встраиваемость |
|---|---|---|---|---|---|---|---|---|
| Simile | 1 | 2 | 4 | 5 | ? (2) | 1 | 5 (рецензируемая статья) | 2 |
| Vectorial | ? (2) | 4 (явно тестирует AI-агентов) | 3 | 5 | ? (2) | 2 | 3 | 2 |
| FuguUX | 4 | 2 | 4 | 2 | 2 (≈$1,8k / ≈$16k) | 5 (self-serve, 10 бесплатных кредитов) | 1 | 2 |
| Simulithic | 5 | 2 | 3 (PR/Slack) | 3 | ? | 4 (CLI) | 1 (QA, не поведение) | 5 (CLI, CI, Claude Code/Codex) |
| Blok/Seldon | 3 | 2 | 3 | 3 | ? (2) | 2 | 3 (87%, без методики) | 1 |
| SimUX | ? (2) | 1 | 3 (7 метрик A/B) | 4 | ? | 2 | 1 | 1 |
| Synthetic Society | ? | ? | ? | ? | ? | ? | ? | ? |
| Brox | 1 | 1 | 3 | 4 | 1 ($100k+/год) | 1 | 3 (данные реальных людей, цифр нет) | 1 |
| Artificial Societies | 1 | 1 | 4 | 4 | ? (2) | 2 | 4 (открытая методика eval) | 2 |
| Synthetic Users | 3 | 2 | 5 | 3 | 2–3 | 3 | 3 | 4 (API) |
| Uxia | 4 | 3 (тестирует AI-built apps) | 4 | 3 | ? (2) | 4 (free trial) | 3 | 4 (MCP) |
| Evelance | 2 | 1 | 3 | 5 | 4 (≈$259 / ≈$2,4k) | 4 | 2 | 1 |
| Aaru | 1 | 1 | ? | 5 | ? | 1 | 4 (прогноз выборов) | 1 |

### Заметки

- **Никто не тестирует генеративный UI внутри чата как отдельный класс.** Ближе всех Vectorial (заявлен «customer-facing AI agent» и AI-native apps [6][7]) и Uxia («AI-built apps» [29]). Отчёты всех сервисов устроены вокруг статичных экранов или опросов. Ниша скилла (решать, что и где показывать в чате) свободна.
- **Реальный браузер ≠ реализм поведения.** Simulithic ходит по настоящим браузерам и сетям, но это QA без персон. Simile и Artificial Societies сильнее всех в валидации, но не трогают UI. Вывод из независимых источников тот же: агенты идут «чистыми» путями, а люди блуждают и бросают (UXAgent, CHI 2025, через Userbrain [37]). Значит, синтетика годится для раннего «pre-flight», а не для замены людей [37][38].
- **Стандарт честной валидации задаёт Artificial Societies**: метрика (distribution accuracy) + потолок (самоповтор людей 91%) + бейзлайн (LLM с биографией 67%) + доля галлюцинаций [23]. У Simile та же логика: точность нормируется на повтор самого человека через 2 недели [4].
- **Цены**: публичные только у FuguUX, Synthetic Users и Evelance. Остальные продают через demo, Brox стоит от $100k/год. Для open-source скилла на токенах LLM это главное преимущество: 100 персон стоят единицы долларов.
- **Встраивание через агентов уже норма**: Uxia даёт MCP для Claude/Codex [29], Simulithic предлагает запускать CLI из Claude Code перед PR [10]. Наш скилл должен работать так же: вызываться агентом и выдавать машиночитаемый результат.
- Неопределённости: Synthetic Society почти не документирован (сайт в одну строку, контакт на чужом домене [18]). Связь Blok и Seldon видна только по редиректу и футеру [15]. Сайт Vectorial не отдаёт текст.

### Идеи, которые стоит заимствовать (пересказ, без копирования текста)

1. **Метрики сравнения A/B вариантов флоу** (по SimUX [17]): ясность, навигация, трение, когнитивная нагрузка, вероятность завершения, эффективность пути, сигналы доверия. Это готовая рубрика для bench/ скилла: сравнивать «до» и «после» сокращения шагов.
2. **Граф действий по каждому агенту + severity + roadmap** (FuguUX [8]). Формат отчёта: путь персоны по экранам или сообщениям чата, место, где она застряла, приоритет исправления.
3. **Нормированная валидация** (Simile [4], Artificial Societies [23]): сообщать не голый процент, а «против потолка и против наивного бейзлайна». Для нас: скрытые проверки в bench/ сравнивают со слепым X/Y-ревью людей.
4. **Метка уверенности на каждом выводе** (Simile [1]). Каждый вывод скилла помечать как высокая, средняя или низкая уверенность и указывать, на чём он основан.
5. **Saturation score** (Synthetic Users [27]): останавливать генерацию персон, когда новые не дают новых проблем. Это дёшево, и 10–12 персон обычно хватает для качественного прогона.
6. **Персоны с разнообразием, а не «средним пользователем»** (критика Brox [20], «иллюзия консенсуса» [39]). Явно задавать разброс: торопливый, сомневающийся, бросающий, с плохой сетью. Добавить профили сети и устройства, как у Simulithic [10].
7. **Цикл «map → qa»** (Simulithic [10]): сначала скилл строит карту флоу (IA), потом проверяет каждый флоу. Это ложится на нашу последовательность: IA → user flows → состояния экранов.
8. **Комбинированный AI + human отчёт и калибровка на собственных человеческих тестах** (Uxia [29]). Даёт путь от дешёвой синтетики к валидации на реальных пользователях Split the Bill и Betke.
9. **MCP или CLI-вход для кодовых агентов** (Uxia [29], Simulithic [10]). Скилл вызывается агентом до визуальных скиллов и отдаёт JSON-спецификацию.
10. **Think-aloud в отчёте** (Uxia [29]). Короткое объяснение решения от лица персоны на каждом шаге. Для генеративного UI в чате это особенно полезно: видно, почему пользователь не понял карточку или кнопку.

### Источники

1. https://www.simile.com/
2. https://dealroom.co/news/142224-simile-raises-200m-series-b-at-2b-valuation-to-survey-ai-twins-of-consum/ ; https://letsdatascience.com/news/simile-raises-200m-series-b-at-2b-valuation-for-human-behavi-4aa05968
3. https://siliconangle.com/2026/02/12/ai-digital-twin-startup-simile-raises-100M-funding/
4. Park et al., «Generative Agent Simulations of 1,000 People», https://arxiv.org/abs/2411.10109 (исследование 2024, на которое ссылается simile.com)
5. https://stockanalysis.com/private/simile/
6. https://thenextweb.com/news/vectorial-3m-seed-human-behavior-simulation
7. https://www.sovereignmagazine.com/article/synthetic-users-vectorial
8. https://fuguux.com
9. https://fuguux.com/pricing
10. https://simulithic.com
11. https://fondo.com/blog/simulithic-sends-ai-users-through-apps-to-find-broken-flows ; https://www.ycombinator.com/companies/simulithic
12. https://dealroom.co/just-founded/simulithic/
13. https://siliconangle.com/2025/07/09/blok-raises-7-5m-build-ai-agents-simulate-human-behavior-accelerate-software-testing/
14. https://www.cxodigitalpulse.com/?p=33313 ; https://creativedestructionlab.com/companies/blok/
15. https://seldon.com/ (редирект с https://www.joinblok.co)
16. https://www.cbinsights.com/company/simux
17. https://simux.ai
18. https://syntheticsociety.ai
19. https://pitchbook.com/profiles/company/904263-49 (страница закрыта для парсера, данные из поисковой выдачи) ; пост про Arima: https://ca.linkedin.com/in/sidghose
20. https://venturebeat.com/data/market-research-is-too-slow-for-the-ai-era-so-brox-built-60-000-identical-digital-twins-of-real-people-you-can-survey-instantly-repeatedly
21. https://brox.ai/ ; https://www.emarketer.com/content/brox-s-60-000-digital-humans-could-reshape-how-brands-predict-behavior
22. https://societies.ai/
23. https://societies.ai/eval
24. https://www.unite.ai/el/artificial-societies-raises-5-35m-to-make-ai-powered-social-simulations-universally-accessible
25. https://ycombinator.com/companies/artificial-societies
26. https://www.syntheticusers.com/pricing
27. https://www.syntheticusers.com/
28. https://syntheticusers.com/science-posts/21-peer-reviewed-papers-that-support-synthetic-users
29. https://www.uxia.app/
30. https://www.uxia.app/pricing
31. https://www.mrweb.com/drno/news39138.htm
32. https://www.capterra.com/p/10033017/Evelance ; https://www.saashub.com/evelance
33. https://evelance.io/pricing
34. https://www.g2.com/products/evelance/discuss
35. https://getcoai.com/newsfeed/ai-synthetic-research-startup-aaru-raised-a-series-a-at-a-1b-headline-valuation ; https://neuronfeed.com/startups/aaru
36. https://www.redpoint.com/content-hub/written/a-step-towards-predicting-the-future-our-investment-in-aaru-/
37. https://www.userbrain.com/blog/synthetic-users-experiment/
38. https://www.nngroup.com/articles/synthetic-users/
39. https://www.antoinebuteau.com/synthetic-societies-need-belief-models-not-personas.md
