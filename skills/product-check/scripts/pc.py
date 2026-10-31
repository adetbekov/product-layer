#!/usr/bin/env python3
"""Thin wrapper over Playwright CLI for product-check. Stdlib only.

Every action is logged, followed by a wait for chat streams and a snapshot; the command prints what changed and
marks actions that changed nothing on the page.

    pc.py open URL [--session S] [--mobile] [--slow]
    pc.py do [--session S] [--note TEXT] -- click e12        # any playwright-cli command after --
    pc.py shot NAME [--session S] [--ref e5]                  # shots/NAME.png in the current folder
    pc.py inventory [--session S] [--all]                     # components inside chat messages
    pc.py metrics [--session S]                               # stream timings of the last action
    pc.py end --outcome done|quit|blocked [--reason TEXT]     # crowd personas close their run with this
    pc.py close [--session S]

Session: $PC_SESSION, else one per working folder. Run folder: $PC_RUN or ./pc-run/<session> (log.jsonl,
snapshots, end.json). $PC_BUDGET caps the number of actions (a persona's patience): past it, `do` refuses and asks
the persona to end. Binary: $PC_PLAYWRIGHT_CLI, else
`playwright-cli` on PATH, else `npx -y @playwright/cli@0.1.23`.
"""

import argparse
import difflib
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path

PINNED = "@playwright/cli@0.1.23"
MSG = '[aria-busy],[data-streaming]'
STREAM_WAIT = """async page => {
  await page.waitForTimeout(300);
  const t = Date.now();
  try {
    await page.waitForFunction(() => !document.querySelector('[aria-busy="true"],[data-streaming="true"]'),
      null, { timeout: %d });
  } catch (e) { return -1; }
  await page.evaluate(%s);
  return Date.now() - t;
}"""
# Timestamps, per chat message, of creation, first text, end of stream and first interactive element.
OBSERVER = """() => {
  if (window.__pc) return;
  const pc = window.__pc = { t0: Date.now(), msgs: [] };
  const seen = new Map();
  const busy = el => el.getAttribute('aria-busy') === 'true' || el.dataset.streaming === 'true';
  const live = 'button,a[href],input,select,textarea,[role=button],[role=slider],[role=radio],[role=checkbox]';
  const scan = () => {
    const now = Date.now();
    document.querySelectorAll('%s').forEach(el => {
      let m = seen.get(el);
      if (!m) { m = { t0: pc.t0, created: now, first_text: null, done: null, interactive: null }; seen.set(el, m); pc.msgs.push(m); }
      if (m.first_text === null && el.textContent.trim()) m.first_text = now;
      if (m.done === null && !busy(el)) m.done = now;
      if (m.interactive === null && el.querySelector(live)) m.interactive = now;
    });
  };
  new MutationObserver(scan).observe(document.body, { subtree: true, childList: true, attributes: true, characterData: true });
  scan();
}""" % MSG
INVENTORY = """() => {
  const msgs = [...document.querySelectorAll('%s')];
  const name = el => (el.getAttribute('aria-label') || el.textContent || el.value || '').trim().replace(/\\s+/g, ' ').slice(0, 60);
  const live = 'button,a[href],input,select,textarea,[role=button],[role=slider],[role=radio],[role=checkbox],[role=switch]';
  return msgs.slice(%s).map((m, i) => {
    const items = [...m.querySelectorAll(live)].map(el => ({
      role: el.getAttribute('role') || (el.type === 'range' ? 'slider' : el.tagName.toLowerCase()),
      name: name(el), disabled: el.disabled || el.getAttribute('aria-disabled') === 'true',
      value: el.getAttribute('aria-valuenow') ?? (el.value || undefined) }));
    const suspects = [...m.querySelectorAll('*')].filter(el => !el.closest(live)).filter(el => {
      const cls = String(el.className || '');
      const pointer = getComputedStyle(el).cursor === 'pointer';
      return pointer || /slider|range|knob|thumb|track|toggle|switch|chip/i.test(cls);
    }).map(el => ({ tag: el.tagName.toLowerCase(), class: String(el.className).slice(0, 40), role: el.getAttribute('role'),
      focusable: el.tabIndex >= 0, text: name(el) }));
    return { message: msgs.indexOf(m), busy: m.getAttribute('aria-busy') || m.dataset.streaming, items, suspects };
  });
}"""
SLOW = """async page => {
  const cdp = await page.context().newCDPSession(page);
  await cdp.send('Network.emulateNetworkConditions',
    { offline: false, latency: 400, downloadThroughput: 50000, uploadThroughput: 25000 });
  return 'slow network on';
}"""


def binary():
    if env := os.environ.get("PC_PLAYWRIGHT_CLI"):
        return shlex.split(env)
    if path := shutil.which("playwright-cli"):
        return [path]
    return ["npx", "-y", PINNED]


def run_dir(session):
    path = Path(os.environ.get("PC_RUN") or Path("pc-run") / session).resolve()
    path.mkdir(parents=True, exist_ok=True)
    return path


def cli(session, *args, timeout=120):
    out = subprocess.run(
        [*binary(), f"-s={session}", *args],
        cwd=run_dir(session),
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout,
    )
    text = (out.stdout + out.stderr).strip()
    ok = out.returncode == 0 and "### Error" not in text
    return ok, text


def result(text):
    """The value printed under '### Result' by eval / run-code."""
    m = re.search(r"### Result\n(.*?)(\n### |\Z)", text, re.S)
    return m.group(1).strip() if m else ""


def snapshot(session):
    """Current URL, snapshot text (also saved under snaps/) and console error count."""
    ok, text = cli(session, "snapshot")
    url = re.search(r"Page URL: (\S+)", text)
    body = re.search(r"```yaml\n(.*?)```", text, re.S)
    errors = re.search(r"Console: (\d+) errors", text)
    snaps = run_dir(session) / "snaps"
    snaps.mkdir(exist_ok=True)
    file = snaps / f"{len(list(snaps.glob('*.yml'))):03d}.yml"
    file.write_text(body.group(1) if body else text)
    return (url.group(1) if url else ""), file.read_text(), str(file.relative_to(run_dir(session))), (
        int(errors.group(1)) if errors else 0)


def norm(snap):
    """Drop refs and focus markers so only visible content counts as a change."""
    snap = re.sub(r" \[(ref=e\d+|active|cursor=pointer)\]", "", snap)
    return [line.rstrip() for line in snap.splitlines() if line.strip()]


def changes(old, new):
    """Lines that differ, compared without refs; added lines keep their new refs so the next action can use them."""
    a, raw = norm(old), [line.rstrip() for line in new.splitlines() if line.strip()]
    b = norm(new)
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag != "equal":
            out += [f"-{line}" for line in a[i1:i2]] + [f"+{line}" for line in raw[j1:j2]]
    return out


def log(session, entry):
    with open(run_dir(session) / "log.jsonl", "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def read_log(path):
    if not Path(path).exists():
        return []
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def remember(session, url, snap, errors=0):
    (run_dir(session) / "last.json").write_text(json.dumps({"url": url, "snap": snap, "errors": errors}))


def recall(session):
    path = run_dir(session) / "last.json"
    return json.loads(path.read_text()) if path.exists() else {"url": "", "snap": ""}


def settle(session, timeout_ms=30000):
    ok, text = cli(session, "run-code", STREAM_WAIT % (timeout_ms, OBSERVER), timeout=timeout_ms / 1000 + 30)
    try:
        return int(result(text))
    except ValueError:
        return None


def cmd_open(a):
    args = ["open", a.url] + (["--mobile"] if a.mobile else [])
    ok, text = cli(a.session, *args)
    if not ok:
        sys.exit(text[-2000:])
    if a.slow:
        cli(a.session, "run-code", SLOW)
    wait = settle(a.session)
    url, snap, file, errors = snapshot(a.session)
    remember(a.session, url, snap, errors)
    log(a.session, {"i": 0, "t": time.time(), "cmd": args, "url": url, "ok": True, "changed": True,
                    "snapshot": file, "wait_ms": wait, "console_errors": errors})
    print(f"url: {url}\nsnapshot: {run_dir(a.session) / file}\n{snap}")


def cmd_do(a):
    if not a.cmd:
        sys.exit("usage: pc.py do -- <playwright-cli command>")
    done = sum(1 for e in read_log(run_dir(a.session) / "log.jsonl") if e["i"] and e["ok"])  # failed refs are free
    if (limit := os.environ.get("PC_BUDGET")) and done >= int(limit):
        print(f"out of patience: {done} of {limit} actions used. End now: pc.py end --outcome quit --reason '...'")
        sys.exit(3)
    before = recall(a.session)
    cli(a.session, "eval", "() => { if (window.__pc) window.__pc.t0 = Date.now(); }")
    ok, text = cli(a.session, *a.cmd)
    wait = settle(a.session)
    url, snap, file, errors = snapshot(a.session)
    diff = changes(before["snap"], snap)
    changed = bool(diff) or url != before["url"]
    error = re.search(r"### Error\n(.+)", text)
    steps = len(read_log(run_dir(a.session) / "log.jsonl"))
    log(a.session, {"i": steps, "t": time.time(), "cmd": a.cmd, "url": url, "ok": ok, "changed": changed,
                    "error": error.group(1) if error else None, "snapshot": file, "wait_ms": wait, "console_errors": errors, "note": a.note})
    remember(a.session, url, snap, errors)
    print(f"step {steps}: {' '.join(a.cmd)} -> {'ok' if ok else 'ERROR'}")
    if error:
        print(f"error: {error.group(1)}")
        if "not found" in error.group(1):
            print("refs change when the page re-renders; current page:\n" + snap)
    if wait == -1:
        print("warning: a chat stream was still busy after the timeout")
    print(f"url: {url}" + ("  (changed)" if url != before["url"] else ""))
    if not changed and ok:
        print("changed: false - the page looks exactly the same. If no feedback was expected elsewhere, this is a bug.")
    elif url != before["url"]:
        lines = snap.splitlines()
        print("new page:\n" + "\n".join(lines[:150]) + ("\n..." if len(lines) > 150 else ""))
    else:
        print(f"diff ({len(diff)} lines):")
        print("\n".join(diff[:60]) + ("\n..." if len(diff) > 60 else ""))
    if errors > before.get("errors", 0):
        print(f"console: {errors} errors (was {before.get('errors', 0)}) - read them with: pc.py do -- console error")
    print(f"snapshot: {run_dir(a.session) / file}")


def cmd_shot(a):
    dest = Path("shots", f"{a.name}.png").resolve()
    dest.parent.mkdir(exist_ok=True)
    ok, text = cli(a.session, "screenshot", *([a.ref] if a.ref else []), f"--filename={dest}")
    if not ok or not dest.exists():
        sys.exit(text[-2000:])
    print(dest.relative_to(Path.cwd().resolve()))


def cmd_inventory(a):
    ok, text = cli(a.session, "eval", INVENTORY % (MSG, "0" if a.all else "-1"))
    print(result(text) or text[-2000:])


def cmd_metrics(a):
    ok, text = cli(a.session, "eval", "() => JSON.stringify(window.__pc || null)")
    raw = result(text)
    try:
        data = json.loads(json.loads(raw)) if raw.startswith('"') else json.loads(raw)
    except ValueError:
        data = None
    if not data:
        sys.exit("no stream data: the page has no aria-busy / data-streaming messages")
    last = [m for m in data["msgs"] if m["t0"] == data["t0"] and m["created"] >= data["t0"]]

    def since(m, key):
        return None if m[key] is None else m[key] - m["t0"]

    out = [{"time_to_first_text": since(m, "first_text"), "time_to_done": since(m, "done"),
            "time_to_interactive": since(m, "interactive")} for m in last]
    print(json.dumps({"messages_total": len(data["msgs"]), "last_action": out}, indent=1))


def cmd_end(a):
    entry = {"outcome": a.outcome, "reason": a.reason, "t": time.time()}
    (run_dir(a.session) / "end.json").write_text(json.dumps(entry, ensure_ascii=False))
    cli(a.session, "close")
    print(f"ended: {a.outcome}")


def cmd_close(a):
    print(cli(a.session, "close")[1][-500:])


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="command", required=True)
    # one browser per working folder by default, so parallel runs in other folders never share a session
    session = os.environ.get("PC_SESSION") or "pc-" + hashlib.sha1(os.getcwd().encode()).hexdigest()[:6]
    for name, fn in [("open", cmd_open), ("do", cmd_do), ("shot", cmd_shot), ("inventory", cmd_inventory),
                     ("metrics", cmd_metrics), ("end", cmd_end), ("close", cmd_close)]:
        s = sub.add_parser(name)
        s.add_argument("--session", default=session)
        s.set_defaults(fn=fn)
        if name == "open":
            s.add_argument("url")
            s.add_argument("--mobile", action="store_true")
            s.add_argument("--slow", action="store_true", help="emulate a slow mobile network (Chromium)")
        if name == "do":
            s.add_argument("--note", default=None, help="why you did it (persona think-aloud)")
            s.add_argument("cmd", nargs=argparse.REMAINDER)
        if name == "shot":
            s.add_argument("name")
            s.add_argument("--ref", default=None)
        if name == "inventory":
            s.add_argument("--all", action="store_true", help="every message, not only the last")
        if name == "end":
            s.add_argument("--outcome", choices=["done", "quit", "blocked"], required=True)
            s.add_argument("--reason", default="")
    a = p.parse_args(argv)
    if getattr(a, "cmd", None) and a.cmd[0] == "--":
        a.cmd = a.cmd[1:]
    a.fn(a)


if __name__ == "__main__":
    main()
