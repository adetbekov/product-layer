# product-check: Kino cinema tickets - 2026-10-31

Verdict: fail
Persona: Daniyar, signed in, saved Visa 4417. Job: buy one ticket for tonight's "The Long Steppe" and keep it to show at the entrance. Leaves if he cannot tell he has a ticket.
Mode: walk    Engine: Playwright CLI    URL: http://127.0.0.1:8711/check-visual/

## Tasks
| Task | Optimum | Actions | Result |
|---|---|---|---|
| Buy a ticket (time, seat, Continue, Pay) | 4 | 4 | Booked, but the ticket cannot be reached (ISSUE-1) |
| Keep the ticket for the entrance | 1 | not possible | ISSUE-1, ISSUE-2 |

## Findings

### ISSUE-1: "Download ticket" button is off-screen on the confirmation page; the ticket cannot be kept
Severity: critical    Confidence: confirmed (2/2 repros)    Rule: WK-9, WK-4, ST-4
1. Open http://127.0.0.1:8711/check-visual/, pick 19:40.
2. Click a green seat (Row 2, seat 5), Continue, Pay 3 200 ₸.
3. On "Your ticket is booked" look for a way to save or show the ticket.
Expected: a visible ticket (code or card) or a visible Download button.
Actual: only the text and "Book another" are visible. "Download ticket" exists in the page structure but sits outside the viewport to the right (no visible button, no scrollbar cue). Reaching it by ref and clicking it only shows a small "Ticket saved ✓" badge at the far screen edge, and the page shifts sideways, cutting the heading and card. No ticket or code is shown.
Evidence: shots/s6-paid.png (visible page, no button), shots/s7-reload.png (same after reload), shots/s8-after-download.png (page shifted, badge at the edge)

### ISSUE-2: No way back to a booked ticket after leaving the confirmation page
Severity: high    Confidence: confirmed (2/2 repros)    Rule: WK-4, FL-2
1. Complete a purchase as in ISSUE-1.
2. Click "Book another" (or the "Kino" logo).
3. Look for the ticket (tickets, "my bookings").
Expected: the purchased ticket is listed or linked from the home page or header.
Actual: the home page is the same time picker, the header only has "Hi, Daniyar". The ticket exists only on the one confirmation page, which shows nothing to show at the entrance beyond a sentence. Reload keeps the confirmation, but there is no link to it.
Evidence: shots/s11-home-after.png

### ISSUE-3: Browser Back after paying returns to Payment with a live Pay button; paying twice is accepted
Severity: high    Confidence: confirmed (2/2 repros)    Rule: WK-7, FL-8
1. Buy a ticket (19:40, Row 2 seat 5) and reach "Your ticket is booked".
2. Press browser Back: the Payment page appears again with Pay 3 200 ₸.
3. Press Pay.
Expected: a warning that the seat is already booked, or no second charge.
Actual: "Your ticket is booked" again for the same seat, with no warning. Daniyar's card was charged twice as far as the UI tells him.
Evidence: shots/s9-back-after-pay.png

### ISSUE-4: A booked seat stays free, and all showtimes share one seat map
Severity: high    Confidence: confirmed (2/2 repros)    Rule: SR-4
1. Buy 19:40 Row 2, seat 5.
2. Click "Book another", pick 19:40 again (or 14:30).
Expected: Row 2 seat 5 shows as taken at 19:40; the map differs by showtime.
Actual: the same layout with the same grey seats appears for 14:30 and 19:40, and Row 2 seat 5 is selectable again.
Evidence: shots/s12-1430.png, shots/s13-1940-again.png

### ISSUE-5: On Payment, "Pay" looks disabled while "Change seat" is the boldest button
Severity: medium    Confidence: confirmed (2/2 repros)    Rule: WK-9, GC-7
1. Pick time and seat, press Continue.
2. Look at the two buttons on Payment.
Expected: Pay is the primary, dark button.
Actual: "Change seat" is solid black; "Pay 3 200 ₸" is pale grey text on a light fill and looks disabled. It is clickable (it works). A hurried user may tap Change seat or think payment is unavailable.
Evidence: shots/s4-next.png

### ISSUE-6: Seat map cannot be used with the keyboard and has no labels or legend
Severity: medium    Confidence: confirmed (2/2 repros)    Rule: WK-9, GC-7
1. Pick any time, land on "Choose your seat".
2. Press Tab: focus goes to Back, not to a seat; Enter then returns to the home page.
3. Look at the map: no row or seat numbers, no legend for green, grey and selected.
Expected: seats are focusable and named; grey means "taken" and is explained.
Actual: seats are unnamed blocks, reachable only by mouse. The chosen seat name appears only after the click ("Your seat: Row 2, seat 5").
Evidence: shots/s1-seats.png

### ISSUE-7: Clicking a taken (grey) seat gives no response
Severity: low    Confidence: confirmed (2/2 repros)    Rule: WK-2, ST-4
1. Pick a time.
2. Click a grey seat, for example Row 3, seat 7.
Expected: a message such as "Seat taken".
Actual: nothing changes; "Your seat" stays "none"; no message.
Evidence: shots/s2-click.png (click on a grey seat, page unchanged)

## Not tested
- Mobile layout, offline and slow-network states - action budget spent on the main flow.
- Console errors: none were reported by the tool during the run (0 errors).
- Real payment failure paths - none exposed by the UI.
