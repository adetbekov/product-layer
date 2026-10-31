# product-check: Pantry - 2026-10-31

Verdict: fail
Persona: Aigerim, returning signed-in customer; job: buy oat milk and rye bread, delivered ASAP, saved card; sometimes uses FRESH10 and checks delivery terms.
Mode: walk    Engine: Playwright CLI    URL: http://127.0.0.1:8700/check-shop/

## Tasks
| Task | Optimum | Actions | Result |
|---|---|---|---|
| Buy oat milk + rye bread, ASAP, saved card | 2 add + cart + checkout + place = 5 | 9 (extra: re-enter email and password) | done, with detour |
| Apply promo FRESH10 | 2 (type, apply) | failed | broken |
| Read delivery terms | 1 from checkout | 1, then dead end | exit missing |

### ISSUE-1: Promo code "Apply" does nothing
Severity: high    Confidence: confirmed (3 tries: click twice, Enter)    Rule: WK-2
Steps:
1. Open /check-shop/, add Oat milk, open Cart.
2. Type FRESH10 in Promo code, click Apply (also try Enter).
Expected: total changes or a message says why the code is invalid.
Actual: nothing changes, no message, total stays 3 230 ₸. Checkout later also shows the full total.
Evidence: shots/issue-promo-after.png (also shots/cart-before.png)

### ISSUE-2: Checkout asks to re-enter email and password
Severity: high    Confidence: confirmed (2/2 orders)    Rule: WK-5, SR-1, SR-4
Steps:
1. Add Oat milk, open Cart, press Checkout.
Expected: go to delivery/payment page; Aigerim is already signed in.
Actual: "Confirm your account" screen demands email and password; empty submit says "Email does not match your account." The screen appears on every checkout. Extra 3 actions per order.
Evidence: shots/checkout1.png

### ISSUE-3: Header "Cart (n)" is stale after changing quantity in the cart
Severity: high    Confidence: confirmed (2/2)    Rule: WK-3
Steps:
1. Add Oat milk from the home page twice: header shows Cart (2).
2. Open Cart, press "+": quantity 3, total 3 870 ₸.
3. Header still says Cart (2); Continue shopping and back, still 2. Reload shows 3.
4. Press "−" to 0: header still Cart (3) on the "Your cart is empty" page.
Expected: header matches cart contents at once.
Actual: header updates only on add from the home page or reload.
Evidence: shots/cartcount-after.png, shots/emptycart.png

### ISSUE-4: Delivery terms page is a dead end
Severity: medium    Confidence: confirmed (2/2)    Rule: WK-4, FL-2
Steps:
1. Fill cart, Checkout, confirm account, on Checkout click "Delivery terms".
Expected: terms with header/navigation or a "Back to checkout" link.
Actual: page has only heading and text; header (Pantry, Cart) and any link are gone; only browser Back returns.
Evidence: shots/terms.png

### ISSUE-5: Delivery fee from the terms is not shown at checkout
Severity: medium    Confidence: confirmed (2/2: totals 3 230 and 650)    Rule: WK-1, honest totals
Steps:
1. Add Rye bread only (650 ₸), Cart, Checkout, confirm account.
2. Compare Total with the terms ("orders under 5 000 ₸ cost 490 ₸ delivery").
Expected: fee line shown, or total includes 490 ₸.
Actual: Total: 650 ₸, no fee line anywhere; terms promise a fee for small orders.
Evidence: shots/fee-checkout.png

## Not tested
- Wrong password message, "Today 18:00-20:00" and Cash options, mobile layout, offline/slow states: action budget.
- Double submit of Place order: not tested.
