# product-check: Glow

## Findings

### ISSUE-1: Skin type chips in the first message look active but do nothing
Severity: high    Rule: GW-1, GC-7
Steps:
1. Pick Oily; the budget message arrives.
2. Scroll up and tap Dry in the first message.
Actual: nothing happens, no feedback; the chip still looks clickable.
Evidence: shots/issue-1.png

### ISSUE-2: Budget slider has no role="slider" and no keyboard support
Severity: high    Rule: GW-2
Steps:
1. Pick a skin type.
2. Inspect the budget card: the slider is missing from the accessibility tree; arrow keys do nothing.
Evidence: shots/issue-2.png

### ISSUE-3: After Regenerate the budget slider does not move
Severity: high    Rule: GW-3
Steps:
1. Pick a skin type, press Regenerate on the budget message.
2. Drag the new slider.
Actual: the value stays at 15 000; the slider is dead.
Evidence: shots/issue-3.png

### ISSUE-4: Send routine can be submitted twice
Severity: medium    Rule: GW-4
Steps:
1. Reach the picks, type an email, press Send routine.
2. Press Send routine again.
Actual: a duplicate "sent" message appears each time.
Evidence: shots/issue-4.png
