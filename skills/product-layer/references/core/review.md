# Review and audit

Checks an existing product or a spec against the rules. Output is findings,
not a redesign. Use it after writing a spec too (self-review).

## Procedure

1. **Goal and type.** One-sentence product goal, product type, module.
2. **Read the product.** Routes / screens, bot handlers, agent prompts and
   tool contracts, onboarding code. Note file paths for evidence.
3. **Top tasks.** List them (`ia.md` inventory) and their entry points.
4. **Steps to value.** Walk each top-task flow as a new user and as a
   returning user; count with FL-4. Note every wait over ~3 s.
5. **Dead ends.** For every screen or message: is there a forward action or
   exit? Check error, empty and cancel branches (FL-2, FL-9).
6. **States.** Fill the state matrix (`states.md`) for the top screens; mark
   missing rows.
7. **Module checks.** Run the module's rules for the product type.
8. **Heuristic pass** (below).
9. **Write findings**, highest impact first, max ~10; group trivia in one line.

## Heuristic pass (product layer only)

Answer yes / no with evidence; every "no" is a candidate finding.

- Does every action give feedback within ~1 s (pending, result or error)?
- Do labels use the user's words, one term per concept (IA-4)?
- Can users undo or go back from every non-destructive action (FL-8, FL-9)?
- Does the product prevent likely errors (defaults, bounded inputs, checks
  before costly steps) rather than only reporting them?
- Are choices shown instead of recalled (chips, recent items, suggestions)?
- Is there a fast path for frequent users (shortcuts, remembered choices,
  repeat last)?
- Is each screen focused on one primary action (IA-5)?
- Do errors explain, keep input and offer a fix (ST-4)?
- Is help in context rather than in a separate tour or docs (ON-7)?
- Can users see what the system remembers about them and change it (ON-3)?

## Finding format

```
[IMPACT] <rule id> <one-line problem>
Evidence: <file:line or screen / message name>
Effect: <what the user loses: steps, drop-off, wrong result>
Fix: <product-level change, no visual detail>
Confidence: high | medium | low      Not verified: <what you could not check>
```

Impact: CRITICAL (blocks the result or loses data), HIGH (extra steps or
confusion on a top task), MEDIUM (friction on secondary tasks), LOW (polish).
Confidence is low when you read code but could not run the product.

## Scorecard

End the review with:

| Check | Result |
|---|---|
| Steps to first value (new user) | N (target M) |
| Top tasks within 3 actions (IA-1) | k of n |
| Dead ends found (FL-2) | count |
| Screens with full state matrix (ST-1) | k of n |
| Questions before value (ON-2) | count |
| Internals visible to users (ST-7) | count |

## Self-review of a spec

Before handing a spec to visual skills, check:

- Every flow has a result, branches and a steps-to-value number.
- No step lacks a verdict from the step test.
- Every screen has one primary action and a filled state matrix.
- No colour, font, size, spacing or animation timing appears in the spec.
- Assumptions and open questions are listed, not hidden in prose.
