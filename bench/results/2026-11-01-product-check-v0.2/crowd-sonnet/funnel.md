# Crowd run: Buy oat milk and rye bread and get them delivered as soon as possible, paying with your saved card.

Optimal path: 5 actions.

| Stage | A | B |
|---|---|---|
| catalog | 20 / 20 | 20 / 20 |
| cart | 20 / 20 | 20 / 20 |
| confirm_account | 20 / 20 | - |
| checkout | 10 / 20 | 20 / 20 |
| done | 10 / 20 | 20 / 20 |

| | A | B |
|---|---|---|
| completed | 10 / 20 | 20 / 20 |
| completed, hard personas | 2 / 12 | 12 / 12 |
| median actions (completers) | 8.0 | 5.0 |
| top drop-off (last stage reached) | confirm_account: 10 | - |
| clicks that changed nothing | - | - |
| said done, page disagrees | 0 | 0 |

Direction: **B** completes more often (90% bootstrap interval of the completion difference B - A: [0.3, 0.7]). direction only; simulated completion is not a conversion forecast.

Decisions (sonnet): d1 0 (0%), haiku 0 (0%), sonnet 241 (100%); d1 asked for Sonnet 0 times.

Cost: $2.2772 (Claude $2.2772 over 40 sessions with recorded usage, d1 $0.0), $0.05693 per persona.

## Drop-off reasons

- A p01 (hurried, hard), stopped after `confirm_account`: Out of time: checkout asked me to re-enter email and password even though I was signed in, and I never reached delivery or card payment.
- A p03 (patient, hard), stopped after `confirm_account`: Already signed in, but checkout asks me to re-enter email and password again - that's paperwork, I'm leaving.
- A p04 (hurried, hard), stopped after `confirm_account`: Out of time: checkout asked me to re-enter email and password, and I ran out of steps before ordering.
- A p05 (hurried, hard), stopped after `confirm_account`: Дошла до подтверждения аккаунта, где снова просят почту и пароль, хотя я уже вошла; терпение кончилось до оплаты и доставки, заказ не оформлен.
- A p06 (hurried, hard), stopped after `confirm_account`: Ran out of patience: the extra re-enter-your-password step after checkout felt like paperwork, and I never got to pay.
- A p07 (hurried, hard), stopped after `confirm_account`: Ran out of time; extra re-login step at checkout ate my actions and I never got to delivery or payment.
- A p10 (hurried, hard), stopped after `confirm_account`: Out of patience: still re-entering email and password after checkout, never reached delivery or card payment
- A p11 (hurried, hard), stopped after `confirm_account`: Терпение кончилось: после корзины сайт попросил заново ввести почту и пароль, до оплаты картой и доставки не дошла
- A p17 (hurried, hard), stopped after `confirm_account`: Ran out of patience: extra re-login step at checkout ate my actions before I could pay.
- A p18 (hurried, hard), stopped after `confirm_account`: Ran out of patience: extra re-login step after checkout, never got to delivery or card payment
