# product-check: Kino

## Findings

### ISSUE-1: Seat map is a canvas: seats cannot be chosen by keyboard or screen reader
Severity: high    Rule: WK-2, GC-7
Steps:
1. Open /, pick 19:40.
2. On "Choose your seat" try to reach a seat with Tab or find it in the accessibility tree.
Expected: every free seat is a focusable control with a name.
Actual: the map is a canvas with no role or label; only a mouse click by position selects a seat, "Continue" stays
disabled otherwise.
Evidence: shots/issue-1.png

### ISSUE-2: "Pay" button has almost no contrast and looks disabled
Severity: high    Rule: WK-5
Steps:
1. Choose a seat, Continue.
Actual: "Pay 3 200 ₸" is pale grey text on light grey, while "Change seat" is the dark bold button.
Evidence: shots/issue-2.png

### ISSUE-3: "Download ticket" is off-screen on the confirmation page
Severity: medium    Rule: FL-3
Steps:
1. Pay.
2. Look for a way to keep the ticket.
Actual: the button exists in the page tree but is positioned outside the viewport on the right; it cannot be seen
or scrolled to.
Evidence: shots/issue-3.png

## Not tested
- Payment failure.
