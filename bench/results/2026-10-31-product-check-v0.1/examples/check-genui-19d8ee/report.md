# product-check: Glow skincare assistant - walk

Verdict: fail
Persona: woman 25, phone, wants a simple routine within budget, changes her mind halfway and scrolls up.
Mode: walk (mobile viewport)   URL: http://127.0.0.1:8700/check-genui/

## Tasks
| Task | Optimum | Result |
|---|---|---|
| skin type -> budget -> picks -> add -> email | ~7 actions | done on a clean run |
| change skin type midway | 1 tap | impossible without reload |
| change budget midway | 2 actions | impossible after first "Show picks" |

### ISSUE-1: Old skin-type chips look active but do nothing
Severity: critical    Confidence: confirmed    Rule: GW-1, GC-7
1. Open the app, tap "Oily", continue to the budget card.
2. Scroll up, tap "Dry".
Expected: skin type changes (and says so) or chips look disabled.
Actual: nothing changes, no message.
Evidence: shots/s7-dry.png

### ISSUE-2: Old budget slider moves but "Show picks" is dead; budget cannot be changed
Severity: critical    Confidence: confirmed    Rule: GW-1, WK-2
1. Choose Oily, move slider, tap "Show picks" (picks "within 7 000 ₸").
2. Scroll up, drag the slider to 48 000 - the value label changes.
3. Tap "Show picks".
Expected: new picks for the new budget, or a disabled slider.
Actual: slider looks live, label shows 48 000, but Show picks does nothing; picks stay at 7 000.
Evidence: shots/s5-oldslider.png, shots/s6-showpicks2.png

### ISSUE-3: Typing "my skin is dry" is ignored; only way to restart is page reload
Severity: critical    Confidence: confirmed    Rule: GW-5, GC-11, FL-2
1. Complete steps up to picks as Oily.
2. Type "Actually my skin is dry" and Send.
Expected: assistant switches to dry skin.
Actual: reply "Thanks! Use the card above to continue..." pointing at the dead card (ISSUE-1/2). Reload wipes the whole conversation and the added products.
Evidence: shots/s8-freetext.png, shots/s14-reload.png

### ISSUE-4: Regenerated budget card: slider cannot be moved
Severity: high    Confidence: confirmed    Rule: GW-3
1. Reload, tap "Dry".
2. Tap "↻ Regenerate" on the budget message (text changes, new card appears).
3. Click/drag the slider track at several positions.
Expected: value changes like on the original card.
Actual: stays at 15 000 ₸; no change. "Show picks" then returns picks for 15 000 only. (Regenerate on an older, non-latest message does nothing, see s9-regen.png.)
Evidence: shots/r-after.png, shots/regen-slider-dead.png, shots/s9-regen.png

### ISSUE-5: Budget slider is not accessible (no role, not focusable, no keyboard)
Severity: medium    Confidence: confirmed    Rule: GW-2, GC-7
1. Reach the budget card, run component inventory / try focusing and ArrowRight.
Expected: role=slider with value, arrow keys change it.
Actual: only unlabeled divs (track/fill/knob); not focusable; ArrowRight changes nothing.
Evidence: shots/issue-slider-norole.png

### ISSUE-6: Email "Send routine" silent on empty or invalid address
Severity: high    Confidence: confirmed    Rule: WK-7, ST-4
1. Get picks, leave the email empty, tap "Send routine".
2. Type "notanemail", tap "Send routine".
Expected: message saying what to fix.
Actual: nothing happens both times.
Evidence: shots/s10-emptysend.png, shots/s11-invalid.png

### ISSUE-7: Routine can be re-sent repeatedly with no warning; no routine summary shown
Severity: medium    Confidence: likely    Rule: GW-4
1. Get picks, add 2 products, send to a valid email: "Done! ... (2 products)".
2. Tap Send routine again - second identical "Done!" message.
3. Add a third and send again - sent again, form never locks.
Expected: the user can see the routine (list/total) before sending; repeated send warns or says "already sent".
Actual: no visible routine list or total anywhere, so "2 products" is unverifiable; duplicate sends are silent.
Evidence: shots/s12-sent.png, shots/s13-resent.png

## Not tested
- Offline/slow states, long streams, stop control: no time budget.
