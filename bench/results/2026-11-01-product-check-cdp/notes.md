# product-check: `pc.py --engine cdp` against Playwright CLI (JEB-2059)

Date: 2026-11-01. One crowd run of the JEB-2058 `mixed` setup on the new engine, compared with the JEB-2058 run on
Playwright CLI, and a replay of the same actions on both engines to time the steps.

## What changed

- `scripts/cdp.py`: a third engine with no npm package. `pc.py open` starts one small daemon per session. The daemon
  launches headless Chrome, keeps a single DevTools connection to the page and listens on a unix socket. Each later
  `pc.py` call is a few socket round trips. Emulation (mobile, slow network) and the console error log stay with the
  session.
- The page state comes from one `Runtime.evaluate`. It returns a node list that pc.py prints in Playwright CLI's
  snapshot format (`- button "Name" [ref=e5]: text`, `- /url:` under links), so `d1.controls()`, `pc.norm()` and the
  diff read both engines alike. Refs live in the page. An element keeps its ref while it stays in the DOM, and a
  re-rendered element gets a new one, as in Playwright CLI.
- Actions are real input events (`Input.dispatchMouseEvent`, `Input.insertText`, `Input.dispatchKeyEvent`) at the
  element's centre, after a hit test. A covered, hidden or disabled target is an error, not a silent click. The
  stream wait (`aria-busy` / `data-streaming`), `changed: false`, `look` (<= 512 px JPEG), `shot`, `metrics`,
  `inventory` and `--mobile` / `--slow` work as on the other engines.
- Every `pc.py` log entry now has `ms`, the engine time of that command, on all engines.
- `bench/engines.py` replays a finished crowd run on each engine without a decision maker. It maps each ref through
  the control it pointed at (role, name, occurrence) and writes step times.

## Setup

- **Crowd.** Same as JEB-2058 `mixed`: the 20 personas from JEB-2037 (12 hard), variants A `/check-shop/` and B
  `/check-shop/?variant=b`, 40 sessions. Each session was a fresh Haiku 5.5 subagent with its `prompt.md` that calls
  `./act auto`, with screenshots on. The only difference is `crowd.py plan --engine cdp`. The sessions ran 10 at a
  time. d1-ultra ran over the hosted API, and its cost is the `usage.cost` it returned.
- **Step time.** `engines.py` replayed the 40 sessions' 242 actions on `playwright` and on `cdp`: 4 personas in
  parallel, `PC_LOOK=1`, device flags from each persona. A second replay of 4 sessions (24 actions) ran one at a time,
  with nothing else on the machine.
- Playwright CLI 0.1.23, Chromium 156 for both engines. Same machine, same fixture server.

## Crowd results

| | cdp (this run) | playwright (JEB-2058 mixed) |
|---|---|---|
| Completed A / B | 11/20 / 20/20 | 11/20 / 20/20 |
| Hard personas completed A / B | 3/12 / 12/12 | 3/12 / 12/12 |
| Top drop-off (A) | confirm_account: 9 | confirm_account: 9 |
| Direction, 90% interval of B - A | B, [0.25, 0.65] | B, [0.25, 0.65] |
| Median actions, completers A / B | 8 / 5 | 8 / 5 |
| Steps decided: d1 / Haiku / Sonnet | 213 / 54 / 0 (80% / 20% / 0%) | 210 / 60 / 0 (78% / 22% / 0%) |
| Clicks that changed nothing | 0 | 0 |
| Session time per persona, median (A / B) | 20.4 s (23.9 / 15.5) | 144.5 s (191.7 / 114.3) |
| Tool calls per session (mean) | 4.2 | 4.8 |
| d1-ultra bill, 40 sessions | $0.01197 | $0.01215 |
| Cost per persona (JEB-2037 method) | $0.00279 | $0.00289 |

Every funnel number matches. All 9 drop-off reasons name the re-asked email and password (`crowd-cdp/funnel.md`).
The engine does not touch decisions, so the cost stays the same: a d1 step still costs about $0.00005.

## Step time (`engines/`, `engines-seq/`)

Same 242 actions on both engines:

| | playwright | cdp | ratio |
|---|---|---|---|
| Step, median, whole `pc.py do` process | 5.66 s | 0.55 s | 10.3x |
| Step, median, inside pc.py (`ms`) | 5.58 s | 0.43 s | 13.1x |
| Step, p90, inside pc.py | 6.47 s | 0.53 s | 12.2x |
| `open`, median | 6.13 s | 1.61 s | 3.8x |
| Browser time per persona, median | 37.7 s | 4.8 s | 7.9x |
| Last stage reached same as in the source run | 40 / 40 | 40 / 40 | |
| One at a time (24 actions): step median, process | 4.64 s | 0.46 s | 10.2x |

- A Playwright CLI step is four to five CLI processes: an eval, the action, the stream wait, the snapshot and the
  screenshot. Each one starts Node and connects to the browser again. A cdp step makes the same calls through one
  open connection. About 0.3 s of the 0.43 s is the fixed 300 ms pause before the stream check, which all engines
  share.
- In the crowd run itself, the median cdp step was 0.40 s (p90 0.48 s), with up to 10 personas at a time.
- With the browser out of the way, a persona's time is now mostly decision time: about 1 s per d1 request and the
  Haiku turns.

## Acceptance (JEB-2059)

- A/B direction and drop-off point same as `playwright` in JEB-2058: yes. B wins with the same interval, and the
  drop-off is `confirm_account` 9 of 20 on both engines.
- Median step time at least 3 times lower: yes, 10.3 times by process wall time and 13.1 times inside pc.py.
- Unit tests for command translation and snapshot parsing, `pytest bench` green: `test_cdp_*` in
  `bench/test_live.py`. One of them is a live test against `check-shop`, skipped when no Chrome is found. 69 tests
  pass.

## Limits

- One flow and one fixture. The snapshot is close to Playwright CLI's but not byte for byte the same. It folds
  inline text wrappers and names a link without `aria-label` by its text, so d1 sees slightly different input. On
  this flow the funnel did not move, but check a new flow on both engines before trusting cdp alone.
- Not covered: iframes, new tabs or windows (the session stays on its first page), file upload, drag. Use
  `--engine playwright` there.
- The JEB-2058 session times come from another run on another day. The engine comparison that counts is the replay,
  where both engines got the same actions on the same machine.
- Haiku costs are estimates from subagent token counts (all counted as input, as in JEB-2058). Only d1 is a real
  bill.

Files: `crowd-cdp/` (funnel and every d1 request), `crowd-sessions.tsv` (tokens, tool calls, time per session),
`engines/` and `engines-seq/` (`steps.tsv` per action, `engines.md`), and `examples/A-p02` (one full run: log,
snapshots, screenshots, d1 answers).
