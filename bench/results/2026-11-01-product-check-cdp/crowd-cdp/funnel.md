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

Decisions (mixed): d1 213 (80%), haiku 54 (20%), sonnet 0 (0%); d1 asked for Sonnet 0 times.

Cost: $0.1117 (Claude $0.0997 over 40 sessions with recorded usage, d1 $0.01197), $0.00279 per persona.

## Drop-off reasons

- A p01 (hurried, hard), stopped after `confirm_account`: Checkout kept asking me to re-confirm my account details, and I ran out of patience before getting to payment.
- A p04 (hurried, hard), stopped after `confirm_account`: Нужно было заново вводить логин и пароль, а терпение кончилось, так и не добрался до доставки
- A p05 (hurried, hard), stopped after `confirm_account`: Checkout sent me to a re-login step, I entered my details but ran out of patience before the order went through
- A p06 (hurried, hard), stopped after `confirm_account`: Checkout kept asking me to re-enter my login before paying, and I ran out of patience before getting past it.
- A p07 (hurried, hard), stopped after `confirm_account`: Out of patience; checkout kept asking me to re-confirm my account before I could get to the bread and milk, too many steps for a hurry
- A p10 (hurried, hard), stopped after `confirm_account`: Out of patience on a re-login detour before reaching checkout; still hadn't got to the card and delivery step.
- A p11 (hurried, hard), stopped after `confirm_account`: После входа в корзину Pantry неожиданно попросил ввести почту и пароль заново, я ввела их, но на шестом действии терпение закончилось, до оформления заказа не дошла.
- A p17 (hurried, hard), stopped after `confirm_account`: Got stopped at a re-authenticate page on checkout; I filled in my email and password, but I ran out of patience before I could hit Continue.
- A p18 (hurried, hard), stopped after `confirm_account`: Сайт попросил повторно ввести логин и пароль перед checkout, и за шесть действий я так и не дошёл до доставки; терпение кончилось
