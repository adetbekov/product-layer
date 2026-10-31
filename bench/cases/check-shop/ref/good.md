# product-check: Pantry

## Findings

### ISSUE-1: Signed-in user must re-enter email and password before checkout
Severity: high    Rule: WK-1, SR-4
Steps:
1. Open /, add Oat milk, open Cart (0 -> 1).
2. Press Checkout.
Expected: checkout with the saved address and card.
Actual: "Confirm your account" asks for email and password again although the header says "Hi, Aigerim".
Evidence: shots/issue-1.png

### ISSUE-2: Delivery terms is a dead end
Severity: high    Rule: WK-4, FL-2
Steps:
1. Go to Checkout.
2. Open "Delivery terms".
Actual: the header disappears and the page has no link or button back; only browser back works.
Evidence: shots/issue-2.png

### ISSUE-3: Promo code Apply does nothing
Severity: high    Rule: WK-2
Steps:
1. Open Cart.
2. Type FRESH10 and press Apply.
Actual: nothing changes, no message.
Evidence: shots/issue-3.png

### ISSUE-4: Header cart counter is stale after changing quantities
Severity: medium    Rule: WK-3
Steps:
1. Add two products; header shows Cart (2).
2. In Cart press + on one product, then Continue shopping.
Actual: header still says Cart (2) until a reload.
Evidence: shots/issue-4.png

## Not tested
- Payment failure.
