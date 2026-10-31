# product-check: Pantry - 2026-10-31

Verdict: fail
Persona: Aigerim, returning signed-in customer; wants oat milk + rye bread delivered ASAP, paid with saved card; sometimes reads delivery terms and uses promo FRESH10; leaves if asked for things the app already knows or if totals look wrong.
Mode: walk    Engine: Playwright CLI (pc.py)    URL: http://127.0.0.1:8711/check-shop/

## Tasks
| Task | Optimum | Actions | Result |
|---|---|---|---|
| Buy oat milk + rye bread, ASAP, saved card | 5 (add, add, cart, checkout, place) | 8 (+ email, password, Continue on an extra "Confirm your account" screen) | Order placed; no promo, price did not match the terms |
| Apply promo FRESH10 | 3 from cart | 2 attempts, no effect | Fail |
| Read delivery terms | 1-2 | 1 click from checkout, but no way back in the page | Dead end |

## Findings

### ISSUE-1: Promo code "Apply" does nothing
Severity: high    Confidence: confirmed (2/2 repros)    Rule: WK-2, ST-4
Steps:
1. Open /check-shop/, add Oat milk and Rye bread, open Cart.
2. Type FRESH10 (also tried lowercase) in "Promo code", click Apply (also tried Enter).
3. Continue to Checkout.
Expected: total drops by 10%, or a message says the code is invalid.
Actual: nothing changes on the page, no message; total stays 1 940 ₸ in cart and on checkout.
Evidence: shots/issue-promo-before.png, shots/issue-promo-after.png, shots/issue-promo2.png

### ISSUE-2: Checkout asks the signed-in user to re-enter email and password
Severity: high    Confidence: confirmed (2/2 repros)    Rule: WK-5, SR-1, SR-4
Steps:
1. Add any item, open Cart, click Checkout.
2. See "Confirm your account - please re-enter your account details".
3. Leave fields empty and click Continue, then enter the email with a wrong password and click Continue.
Expected: a signed-in user goes straight to Checkout; at most one confirmation for risky actions.
Actual: extra screen with 3 actions (email, password, Continue). Empty submit says "Email does not match your account." (it does not say the email is required). A wrong password with the right email is accepted, so the step adds friction with no security value.
Evidence: shots/issue-confirm.png, shots/issue-confirm-wrong.png

### ISSUE-3: "Delivery terms" page is a dead end (no header, no links)
Severity: medium    Confidence: confirmed (2/2 repros)    Rule: WK-4, FL-2
Steps:
1. Add an item, go to Checkout (via the confirm screen), click "Delivery terms".
2. Look for a way back to checkout or cart.
Expected: header with Pantry link / Cart, or a "Back to checkout" link.
Actual: only the text; no header, no links. Only browser Back works. Terms are also reachable only from Checkout, not from home or cart.
Evidence: shots/issue-terms.png, shots/issue-terms2.png

### ISSUE-4: Cart counter in the header is stale after changing quantity in the cart
Severity: high    Confidence: confirmed (2/2 repros)    Rule: WK-3
Steps:
1. Add Eggs twice from home so header shows "Cart (2)", open Cart.
2. Press "+" once: quantity 3, total 2 970 ₸, header still "Cart (2)".
3. Press "-" until the cart is empty: page says "Your cart is empty." but header still shows "Cart (2)".
4. Reload: header shows "Cart (0)".
Expected: header follows the cart immediately.
Actual: header shows old count until reload.
Evidence: shots/issue-header-stale.png, shots/issue-empty-stale.png

### ISSUE-5: Total ignores the 490 ₸ delivery fee from the terms
Severity: high    Confidence: confirmed (2/2 repros)    Rule: ST-4 (price honesty)
Steps:
1. Add Oat milk + Rye bread (1 940 ₸), checkout, open Delivery terms: "orders over 5 000 ₸ are delivered free; smaller orders cost 490 ₸".
2. Go back to Checkout and look at the total.
Expected: the total (or a line) shows the 490 ₸ delivery fee, or a "free over 5 000 ₸" hint.
Actual: Checkout shows "Total: 1 940 ₸" with no delivery line, contradicting the terms the user has to leave the page to read. The fee is not shown anywhere before "Place order".
Evidence: shots/issue-checkout.png, shots/issue-terms.png

### ISSUE-6: "Added ✓" button keeps adding items on every click
Severity: low    Confidence: confirmed (2/2 repros)    Rule: WK-7
Steps:
1. On home click "Add to cart" on Eggs; it turns into "Added ✓".
2. Click "Added ✓" again: header goes from Cart (1) to Cart (2).
Expected: the label means "already added" and does not silently add again, or shows the quantity.
Actual: each click adds another unit; the label never changes, so a double click orders two.
Evidence: shots/issue-home-added.png

## Not tested
- Mobile layout, slow/offline states, console errors (not run within the action budget).
- Double submit on "Place order" and Back from the confirmation screen.
- Other promo codes / invalid-code handling (Apply gave no feedback at all).
