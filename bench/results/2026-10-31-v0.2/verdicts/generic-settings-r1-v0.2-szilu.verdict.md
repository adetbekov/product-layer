# Blind review: Synthetic settings page (P1)

## Scores

| Criterion | X | Y |
|---|---|---|
| success | 5 | 4 |
| flow | 4 | 3 |
| states | 5 | 4 |
| ia | 5 | 3 |
| asks | 5 | 5 |
| fit | 4 | 4 |
| handoff | 4 | 3 |
| scope | 4 | 5 |
| clarity (per side) | 4 | 4 |

## Defects

**X**
- `digest-saved`: the Undo action goes `to: digest`, i.e. reopens the sheet. Undo should revert the value in place and return to `settings`; as written it adds a step to the one recovery path the toast exists for.
- `delete`: declares a `loading` state ("delete button shows progress while the request runs") but its only forward action goes to the `delete-confirm` modal, not to a request. Either the password is verified on this page (then say so) or the loading state belongs only on `delete-confirm`. An engineer has to guess.
- `export`: "Download earlier export" is modelled as a transition `to: settings`. A download is an affordance, not a navigation; the user should stay on the page.
- Slight visual leakage ("danger-styled", "equal-size", "plain text style") and invented content ("Sent at 8:00"). Tolerable as emphasis cues, but the 8:00 is a product fact nobody supplied.
- Scope: promotes Settings to a top-level nav item and trims the avatar menu; not asked, though harmless.

**Y**
- `delete`: "Delete my account" goes straight `to: account-deleted` with no re-authentication and no second confirmation. For an irreversible, under-1% action, a single tap on a page the user may have reached by mis-tap is not safe enough; "Cancel is rank 1" is emphasis, not a safeguard.
- `export`: lists a `Delete account` action. There is no reason to route from data export into account deletion; it is a stray edge that an engineer would build and a user would trip over.
- Password change (5% of visits) and profile editing (name, email, time zone) are dropped with "they stay reachable the way the product decides later". The brief describes them as part of settings today; the redesign removes their home and offers none. That is hiding things people need, not reducing steps.
- `digest` error text promises a "Retry action" but the actions list has only "Back to settings"; the retry has no transition.
- No surface differentiation: every screen is a page. The digest change is a three-option pick and would sit naturally in a sheet; a full page is one more context switch than needed on mobile web.

## Winner

**P1: X. Overall: X.**

Both reach the digest in three taps, save on choice, swap the confirm dialog for Undo, and stop re-asking the email. X wins on the parts the review asked to judge beyond step count: deletion is deliberate (password plus a named final confirmation) and physically separated from any Save; export has a real building state the user can leave, plus an expired-link recovery; and password and profile keep a home instead of vanishing. Y is leaner and strictly on-scope, but the one-tap delete, the export-to-delete edge, and the deleted-without-replacement profile and password screens are the kind of "fewer steps" that costs people something they need.

```json
{"X": {"P1": {"success": 5, "flow": 4, "states": 5, "ia": 5, "asks": 5, "fit": 4, "handoff": 4, "scope": 4}, "clarity": 4}, "Y": {"P1": {"success": 4, "flow": 3, "states": 4, "ia": 3, "asks": 5, "fit": 4, "handoff": 3, "scope": 5}, "clarity": 4}, "winner": {"P1": "X", "overall": "X"}}
```
