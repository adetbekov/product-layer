# walk - one agent uses the product like its user

A QA pass by one agent in a real browser. Goal: 5-10 findings, each reproduced
twice and backed by steps and a screenshot, plus steps-vs-optimum per task.
Chat UIs: also run `genui-walk.md`.

## Setup

1. **Persona lock.** Write the persona in three lines before the first click:
   who, the one job they came for, what makes them leave (`personas.md`).
   Default: a first-time user on a phone, in a hurry, who knows nothing about
   how the product is built.
2. **Tasks and optimum.** List 3-5 top tasks. Take the optimal action count
   from the product-layer spec (`Steps to value` table) when there is one;
   otherwise write your own shortest path after a first look, before walking.
3. **Session.** `pc.py open URL` (add `--mobile` for phone personas). Keep the
   printed snapshot path; `pc.py` logs every action in `pc-run/<session>/`.

## Walking

For each task, start from the real entry point (home, link, deep link), not
from a URL in the middle of the flow. After every `pc.py do`, read the diff it
prints and answer five questions at each step:

1. Where do I start? Is the first action obvious?
2. Does the screen tell me the next step?
3. Can I see progress and what is left?
4. Can I leave and come back without losing work?
5. Is the end obvious - did it work?

A "no" is a finding candidate. Note hesitation in `--note`; every hesitation
counts.

## WK-1 · Clicks against the optimum · CRITICAL

**Check.** Count actions per task (`log.jsonl` lines with `ok: true`) and
compare with the optimum. List each extra action and why it was needed.
**Why.** Extra steps are where real users drop off; the count makes it
checkable.
**Bug if.** A task takes more actions than the optimum because the product
asks for something it already knows (`SR-1`, `SR-4`), adds a confirm for a
reversible action (`FL-8`), or hides the next step.

## WK-2 · No visible change is a bug · CRITICAL

**Check.** After each action `pc.py` prints `changed: false` when the page is
the same. Look for feedback elsewhere (toast, console error, new tab). If there
is none, retry once with a clean state, then record it.
**Why.** A silent control is the most common dead interaction; users repeat
the click and then leave.
**Bug if.** A button, link or control does nothing visible and gives no
reason (`ST-4`).

## WK-3 · Round trip A to B to A · HIGH

**Check.** List every value shown in more than one place: header counters
and badges, totals, step counts, names, statuses. For each, change its source
on screen B (add, remove, change a quantity, edit a setting), then:
1. read the copy on B itself (the header is on every screen);
2. go back to A with the product's own visible link or button, not reload,
   and read it there;
3. reload and compare with what you read before.
**Why.** Stale copies make users doubt the change happened, and they hide
easily: the page you are on looks right while the header is wrong.
**Bug if.** Any copy shows old data until a reload, or the visible way back is
missing.

## WK-4 · Every screen has a way out · CRITICAL

**Check.** On every screen you reach, find a visible next action or a way
back inside the page: link, button, navigation. Browser back does not count.
**Why.** A dead end forces the browser back button or a restart (`FL-2`).
**Bug if.** A screen has no exit, or navigation disappears.

## WK-5 · Ask once, ask only what only the user knows · HIGH

**Check.** For each form field, ask: does the product already know this (it is
shown elsewhere, the user is signed in, it came from the previous step)?
**Why.** Re-entering known data is an extra step and a trust hit (`SR-1`,
`SR-4`).
**Bug if.** Known data is asked again, or a field blocks progress with no
reason given.

## WK-6 · States are designed · HIGH

**Check.** Visit empty (no items), loading (`pc.py open --slow`), error (bad
input, offline via `pc.py do -- network-state-set offline`) and success for each
task screen.
**Why.** Undesigned states are where users get stuck (`ST-1`, `ST-2`, `ST-4`).
**Bug if.** A state is blank, raw, loses input, or offers no next action.

## WK-7 · Forms behave predictably · HIGH

**Check.** Submit empty, invalid, and valid input; submit twice; go back and
forward.
**Why.** Double submits create duplicates; lost input makes people quit.
**Bug if.** Errors do not say what to fix, input is lost, or a second submit
repeats the effect without warning.

## WK-8 · Console and network stay clean · MEDIUM

**Check.** `pc.py` prints a line when the console error count grows; read
them with `pc.py do -- console error`.
**Why.** Errors often explain a silent control or a broken state.
**Bug if.** An error appears during a task step. Report it with the step.

## Recording a finding

1. **Reproduce first.** Repeat the steps from a clean start (new session or
   reload). Not reproducible twice: record it under "seen once" with lower
   confidence, never as a confirmed issue.
2. **Evidence by type.** Interactive bug: a screenshot before and after the
   action (`pc.py shot issue-3-before`, `issue-3-after`) and the numbered
   steps. Static bug (wrong text, missing exit): one screenshot.
3. **Write it now** in `report.md` in the format of `report.md`, before moving
   on. Do not batch findings at the end.
4. **Persona drift.** If you notice reasoning like "a developer would know",
   redo the step as the persona and keep only what the persona would hit.

## Coverage and stop

Stop at 5-10 confirmed findings or when every task was walked and every check
ran. Record what was not tested and why. A task with no artifact (diff,
screenshot, log line) counts as not tested.
