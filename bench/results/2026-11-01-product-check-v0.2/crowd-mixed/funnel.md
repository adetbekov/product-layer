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

Decisions (mixed): d1 210 (78%), haiku 60 (22%), sonnet 0 (0%); d1 asked for Sonnet 0 times.

Cost: $0.1155 (Claude $0.1033 over 40 sessions with recorded usage, d1 $0.01215), $0.00289 per persona.

## Drop-off reasons

- A p01 (hurried, hard), stopped after `confirm_account`: Checkout kept asking me to re-enter my account details on a confirm page; I was out of patience before it got me to the order.
- A p04 (hurried, hard), stopped after `confirm_account`: Checkout kept asking me to log in again and re-enter email and password; I ran out of patience before it went through, so I'm leaving.
- A p05 (hurried, hard), stopped after `confirm_account`: Ушла на подтверждение аккаунта: сайт попросил снова ввести email и пароль, и терпение закончилось до оформления заказа.
- A p06 (hurried, hard), stopped after `confirm_account`: Checkout kept asking me to re-enter my account details before I could pay; I ran out of patience and gave up before getting the oat milk and rye bread delivered.
- A p07 (hurried, hard), stopped after `confirm_account`: Checkout made me re-enter my login for a security check, and I ran out of patience before getting back to the order.
- A p10 (hurried, hard), stopped after `confirm_account`: Out of patience: stuck on a re-login confirm page before checkout, had to type email and password again
- A p11 (hurried, hard), stopped after `confirm_account`: Попросили заново ввести почту и пароль для подтверждения, потом терпение закончилось, не дошла до заказа молока и хлеба
- A p17 (hurried, hard), stopped after `confirm_account`: Pantry kept asking me to re-confirm my account on every step, and I ran out of patience before reaching the cart or checkout.
- A p18 (hurried, hard), stopped after `confirm_account`: Сайт попросил повторно ввести почту и пароль, я ввел, но терпение закончилось и заказ так и не оформился
