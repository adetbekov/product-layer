# Crowd run: Buy oat milk and rye bread and get them delivered as soon as possible, paying with your saved card.

Optimal path: 5 actions.

| Stage | A | B |
|---|---|---|
| catalog | 20 / 20 | 20 / 20 |
| cart | 20 / 20 | 20 / 20 |
| confirm_account | 20 / 20 | - |
| checkout | 11 / 20 | 20 / 20 |
| done | 11 / 20 | 19 / 20 |

| | A | B |
|---|---|---|
| completed | 11 / 20 | 19 / 20 |
| completed, hard personas | 3 / 12 | 11 / 12 |
| median actions (completers) | 8 | 5 |
| top drop-off (last stage reached) | confirm_account: 9 | checkout: 1 |
| clicks that changed nothing | - | - |
| said done, page disagrees | 0 | 0 |

Direction: **B** completes more often (90% bootstrap interval of the completion difference B - A: [0.2, 0.6]). direction only; simulated completion is not a conversion forecast.

Cost: $0.1122 over 40 sessions with recorded usage.

## Drop-off reasons

- A p01 (hurried, hard), stopped after `confirm_account`: Out of patience at the sign-in re-check step before payment; I still have not reached delivery or the saved card.
- A p04 (hurried, hard), stopped after `confirm_account`: Положил молоко и хлеб в корзину, но на Checkout попросили заново ввести email и пароль, хотя я уже вошел как Aigerim. Терпение кончилось, доставку не оформил.
- A p05 (hurried, hard), stopped after `confirm_account`: Потерпение вышло: после корзины магазин попросил повторно ввести почту и пароль 'для безопасности', а кнопка Continue не дала ни подтверждения, ни заказа.
- A p06 (hurried, hard), stopped after `confirm_account`: Cart was easy, but checkout asked me to re-enter email and password, and I ran out of patience before reaching delivery.
- A p07 (hurried, hard), stopped after `confirm_account`: Ran out of patience on the forced re-login step before checkout finished; I was in a hurry and it's not clear the order went through.
- A p10 (hurried, hard), stopped after `confirm_account`: Ушёл из-за лимита терпения: до оплаты не дошёл, на шаге подтверждения аккаунта ещё нужно нажать Continue, а процесс затянулся.
- A p11 (hurried, hard), stopped after `confirm_account`: Положила молоко и хлеб, дошла до оформления, но сайт попросил заново ввести почту и пароль, хотя я уже вошла. Терпение закончилось, заказ не оформлен.
- A p17 (hurried, hard), stopped after `confirm_account`: Out of patience: after adding oat milk and rye bread and starting checkout, I was asked to re-enter my email and password and the Continue step was not reached within my patience budget.
- A p18 (hurried, hard), stopped after `confirm_account`: После корзины просят повторно ввести email и пароль для подтверждения аккаунта, и на этом я застрял без доставки и оплаты картой; терпение кончилось.
- B p02 (patient, hard), stopped after `checkout`: В итоге 1 940 ₸, но по условиям доставки до 5 000 ₸ стоит 490 ₸, и этой суммы в итоге нет. Не понимаю, сколько спишется с карты, поэтому не оформляю заказ.
