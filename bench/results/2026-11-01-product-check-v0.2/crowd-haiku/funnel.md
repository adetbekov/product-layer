# Crowd run: Buy oat milk and rye bread and get them delivered as soon as possible, paying with your saved card.

Optimal path: 5 actions.

| Stage | A | B |
|---|---|---|
| catalog | 20 / 20 | 20 / 20 |
| cart | 20 / 20 | 20 / 20 |
| confirm_account | 20 / 20 | - |
| checkout | 11 / 20 | 20 / 20 |
| done | 11 / 20 | 20 / 20 |

| | A | B |
|---|---|---|
| completed | 11 / 20 | 20 / 20 |
| completed, hard personas | 3 / 12 | 12 / 12 |
| median actions (completers) | 8 | 5.0 |
| top drop-off (last stage reached) | confirm_account: 9 | - |
| clicks that changed nothing | - | - |
| said done, page disagrees | 0 | 0 |

Direction: **B** completes more often (90% bootstrap interval of the completion difference B - A: [0.25, 0.65]). direction only; simulated completion is not a conversion forecast.

Decisions (haiku): d1 0 (0%), haiku 252 (100%), sonnet 0 (0%); d1 asked for Sonnet 0 times.

Cost: $0.117 (Claude $0.117 over 40 sessions with recorded usage, d1 $0.0), $0.00293 per persona.

## Drop-off reasons

- A p01 (hurried, hard), stopped after `confirm_account`: Out of patience at the account re-check step after checkout; Sam is hurried and leaves.
- A p04 (hurried, hard), stopped after `confirm_account`: Added milk and bread, but checkout asked me to re-enter login details and I ran out of patience before finishing.
- A p05 (hurried, hard), stopped after `confirm_account`: Терпение кончилось: после корзины и подтверждения входа застряла на шаге оформления, не дошла до оплаты
- A p06 (hurried, hard), stopped after `confirm_account`: Out of patience: added oat milk and rye bread and reached checkout, but a surprise 'Confirm your account' re-login with email and password felt like paperwork, and I was not going to finish it while hurried.
- A p07 (hurried, hard), stopped after `confirm_account`: Checkout forced a re-login and I ran out of patience before it went through.
- A p10 (hurried, hard), stopped after `confirm_account`: Out of patience at the re-login step: the checkout asked me to re-enter my account details, and I ran out of actions before I could confirm and pay.
- A p11 (hurried, hard), stopped after `confirm_account`: Терпение кончилось: после добавления молока и хлеба и входа в корзину сайт потребовал повторно ввести почту и пароль, и на шаге подтверждения не хватило терпения.
- A p17 (hurried, hard), stopped after `confirm_account`: Out of patience at the account re-confirmation step before payment; the order was not placed.
- A p18 (hurried, hard), stopped after `confirm_account`: Out of patience at the account re-confirmation step before checkout; I was hurried and the extra login was a detour.
