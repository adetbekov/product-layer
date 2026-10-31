#!/usr/bin/env python3
"""Thin wrapper over a browser CLI for product-check: Playwright CLI or agent-browser, one interface. Stdlib only.

Every action is logged, followed by a wait for chat streams and a snapshot; the command prints what changed and
marks actions that changed nothing on the page.

    pc.py open URL [--session S] [--mobile] [--slow]
    pc.py do [--session S] [--note TEXT] [--tier T] -- click e12   # engine command after --; refs as e12 or @e12
    pc.py look [--session S] [--ask]                          # screenshot <= 512 px; --ask: d1 vision questions
    pc.py shot NAME [--session S] [--ref e5]                  # shots/NAME.png in the current folder
    pc.py inventory [--session S] [--all]                     # components inside chat messages
    pc.py metrics [--session S]                               # stream timings of the last action
    pc.py end --outcome done|quit|blocked [--reason TEXT]     # crowd personas close their run with this
    pc.py close [--session S]

Engine: --engine or $PC_ENGINE, `playwright` (default), `agent-browser` or `cdp` (direct DevTools session through
cdp.py: one daemon per session holds Chrome, a step is a few socket round trips instead of CLI processes). Commands
after `do --` use Playwright CLI names (click, fill, select, check, press, go-back, ...); pc.py translates them for
the other engines. Session:
$PC_SESSION, else one per working folder. Run folder: $PC_RUN or ./pc-run/<session> (log.jsonl, snapshots, looks,
end.json). $PC_BUDGET caps the number of actions (a persona's patience): past it, `do` refuses and asks the persona
to end. $PC_LOOK=1 takes a look after every open / do and prints its path. $PC_TIER labels who decided each action
(d1, haiku, sonnet; crowd.py sets it). Binaries: $PC_PLAYWRIGHT_CLI, else `playwright-cli` on PATH, else
`npx -y @playwright/cli@0.1.23`; $PC_AGENT_BROWSER, else `agent-browser` on PATH, else
`npx -y agent-browser@0.27.0`; cdp: $PC_CHROME, else an installed Chrome / Chromium (see cdp.py). Every log entry
carries `ms`, the engine time of that command.
"""

import argparse
import base64
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
PINNED_AB = "agent-browser@0.27.0"
LOOK_PX = 512
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


CDP_LOOK = """const [ws_url, page_url, px] = process.argv.slice(1);
const ws = new WebSocket(ws_url); let id = 0; const wait = {};
const send = (method, params = {}, sessionId) => new Promise(ok => {
  wait[++id] = ok; ws.send(JSON.stringify({ id, method, params, sessionId })); });
ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && wait[m.id]) wait[m.id](m.result || {}); };
ws.onopen = async () => {
  const pages = (await send('Target.getTargets')).targetInfos.filter(t => t.type === 'page');
  const t = pages.find(t => t.url === page_url) || pages[0];
  const { sessionId } = await send('Target.attachToTarget', { targetId: t.targetId, flatten: true });
  const r = await send('Runtime.evaluate', { expression: '[innerWidth, innerHeight]', returnByValue: true }, sessionId);
  const [w, h] = r.result.value, s = Math.min(1, px / Math.max(w, h));
  const shot = await send('Page.captureScreenshot',
    { format: 'jpeg', quality: 70, clip: { x: 0, y: 0, width: w, height: h, scale: s } }, sessionId);
  process.stdout.write(shot.data); process.exit(0);
};
setTimeout(() => process.exit(2), 20000);"""
PW_LOOK = """async page => {
  const cdp = await page.context().newCDPSession(page);
  const [w, h] = await page.evaluate(() => [innerWidth, innerHeight]);
  const s = Math.min(1, %d / Math.max(w, h));
  const r = await cdp.send('Page.captureScreenshot',
    { format: 'jpeg', quality: 70, clip: { x: 0, y: 0, width: w, height: h, scale: s } });
  return r.data;
}""" % LOOK_PX
REF = re.compile(r"@?(e\d+)")
AB_NAMES = {"go-back": "back", "go-forward": "forward"}


def bare(ref):
    """e12 from e12 or @e12."""
    return REF.sub(r"\1", ref)


def run_dir(session):
    path = Path(os.environ.get("PC_RUN") or Path("pc-run") / session).resolve()
    path.mkdir(parents=True, exist_ok=True)
    return path


def result(text):
    """The value printed under '### Result' by eval / run-code."""
    m = re.search(r"### Result\n(.*?)(\n### |\Z)", text, re.S)
    return m.group(1).strip() if m else ""


def unjson(raw):
    try:
        value = json.loads(raw)
    except ValueError:
        return raw
    return value if isinstance(value, str) else raw


class Playwright:
    """Playwright CLI. Refs are e12; page code runs through run-code."""

    name = "playwright"

    def __init__(self, session):
        self.session = session

    def binary(self):
        if env := os.environ.get("PC_PLAYWRIGHT_CLI"):
            return shlex.split(env)
        if path := shutil.which("playwright-cli"):
            return [path]
        return ["npx", "-y", PINNED]

    def cli(self, *args, timeout=120):
        out = subprocess.run([*self.binary(), f"-s={self.session}", *args], cwd=run_dir(self.session),
                             capture_output=True, text=True, check=False, timeout=timeout)
        text = (out.stdout + out.stderr).strip()
        return out.returncode == 0 and "### Error" not in text, text

    def open(self, url, mobile=False):
        ok, text = self.cli("open", url, *(["--mobile"] if mobile else []))
        return ok, text

    def act(self, cmd):
        """(ok, error or None, raw output) of one action."""
        ok, text = self.cli(*[REF.sub(r"\1", c) if REF.fullmatch(c) else c for c in cmd])
        error = re.search(r"### Error\n(.+)", text)
        return ok, error.group(1) if error else None, text

    def js(self, fn, timeout=120):
        """Value of a page function `() => ...`, as printed by the engine."""
        return result(self.cli("eval", fn, timeout=timeout)[1])

    def snapshot(self):
        ok, text = self.cli("snapshot")
        url = re.search(r"Page URL: (\S+)", text)
        body = re.search(r"```yaml\n(.*?)```", text, re.S)
        errors = re.search(r"Console: (\d+) errors", text)
        return (url.group(1) if url else ""), (body.group(1) if body else text), (int(errors.group(1)) if errors else 0)

    def settle(self, timeout_ms):
        ok, text = self.cli("run-code", STREAM_WAIT % (timeout_ms, OBSERVER), timeout=timeout_ms / 1000 + 30)
        try:
            return int(result(text))
        except ValueError:
            return None

    def screenshot(self, dest, ref=None):
        return self.cli("screenshot", *([REF.sub(r"\1", ref)] if ref else []), f"--filename={dest}")

    def look(self):
        raw = unjson(result(self.cli("run-code", PW_LOOK)[1]))
        return base64.b64decode(raw) if raw else b""

    def slow(self):
        self.cli("run-code", SLOW)

    def close(self):
        return self.cli("close")[1]


class AgentBrowser:
    """agent-browser (vercel-labs, Apache-2.0). Refs are @e12; waits use `wait --fn`; looks go through CDP."""

    name = "agent-browser"

    def __init__(self, session):
        self.session = session

    def binary(self):
        if env := os.environ.get("PC_AGENT_BROWSER"):
            return shlex.split(env)
        if path := shutil.which("agent-browser"):
            return [path]
        return ["npx", "-y", PINNED_AB]

    def cli(self, *args, timeout=120):
        out = subprocess.run([*self.binary(), "--session", self.session, "--json", *args], cwd=run_dir(self.session),
                             capture_output=True, text=True, check=False, timeout=timeout)
        try:
            data = json.loads(out.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            data = {"success": False, "error": (out.stdout + out.stderr).strip()[-500:] or "no output"}
        return bool(data.get("success")), data

    def open(self, url, mobile=False):
        ok, data = self.cli("open", url)
        if ok and mobile:
            self.cli("set", "viewport", "390", "844")
        return ok, json.dumps(data)

    def act(self, cmd):
        name, *rest = cmd
        args = [AB_NAMES.get(name, name)] + [REF.sub(r"@\1", c) if REF.fullmatch(c) else c for c in rest]
        ok, data = self.cli(*args)
        return ok, None if ok else str(data.get("error")), json.dumps(data, ensure_ascii=False)

    def js(self, fn, timeout=120):
        ok, data = self.cli("eval", f"({fn})()", timeout=timeout)
        value = (data.get("data") or {}).get("result")
        return value if isinstance(value, str) else json.dumps(value)

    def snapshot(self):
        ok, data = self.cli("snapshot")
        d = data.get("data") or {}
        url = d.get("origin") or (self.cli("get", "url")[1].get("data") or {}).get("url", "")
        errors = (self.cli("errors")[1].get("data") or {}).get("errors") or []
        return url, d.get("snapshot", ""), len(errors)

    def settle(self, timeout_ms):
        self.cli("eval", f"({OBSERVER})()")
        self.cli("wait", "300")
        t = time.time()
        ok, _ = self.cli("wait", "--fn", "!document.querySelector('[aria-busy=\"true\"],[data-streaming=\"true\"]')",
                         timeout=timeout_ms / 1000 + 30)
        self.cli("eval", f"({OBSERVER})()")
        return round((time.time() - t) * 1000) if ok else -1

    def screenshot(self, dest, ref=None):
        ok, data = self.cli("screenshot", *([REF.sub(r"@\1", ref)] if ref else []), str(dest))
        return ok, json.dumps(data)

    def look(self):
        cdp = (self.cli("get", "cdp-url")[1].get("data") or {}).get("cdpUrl") or ""
        url = (self.cli("get", "url")[1].get("data") or {}).get("url") or ""
        node = shutil.which("node")
        if cdp.startswith("ws") and node:
            out = subprocess.run([node, "-e", CDP_LOOK, cdp, url, str(LOOK_PX)], capture_output=True, text=True,
                                 check=False, timeout=40)
            if out.returncode == 0 and out.stdout:
                return base64.b64decode(out.stdout)
        # no node 22: full-size viewport JPEG, more d1 tokens but the same answers
        dest = run_dir(self.session) / "look-full.jpg"
        self.cli("screenshot", str(dest), "--screenshot-format", "jpeg", "--screenshot-quality", "60")
        return dest.read_bytes() if dest.exists() else b""

    def slow(self):
        print("warning: --slow (network throttling) needs --engine playwright", file=sys.stderr)

    def close(self):
        return json.dumps(self.cli("close")[1])


class CDP:
    """Direct DevTools session (cdp.py): one daemon per session holds Chrome, each call is a unix-socket round trip
    instead of a browser CLI process. Refs are e12 as in Playwright CLI; commands use Playwright CLI names."""

    name = "cdp"

    def __init__(self, session):
        import cdp

        self.cdp, self.session = cdp, session
        self.client = cdp.Client(session)

    def call(self, method, params=None, timeout=60):
        return self.client.call(method, params, timeout)

    def eval(self, expr, timeout=60):
        """Value of a page expression; raises CDPError on a page exception."""
        r = self.call("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True},
                      timeout)
        if "exceptionDetails" in r:
            d = r["exceptionDetails"]
            raise self.cdp.CDPError((d.get("exception") or {}).get("description") or d.get("text", "page error"))
        return r.get("result", {}).get("value")

    def open(self, url, mobile=False):
        self.client.start()
        if mobile:
            self.call("Emulation.setDeviceMetricsOverride", self.cdp.MOBILE)
            self.call("Emulation.setTouchEmulationEnabled", {"enabled": True, "maxTouchPoints": 5})
            self.call("Emulation.setUserAgentOverride", {"userAgent": self.cdp.MOBILE_UA})
        r = self.call("Page.navigate", {"url": url})
        if r.get("errorText"):
            return False, f"navigation to {url} failed: {r['errorText']}"
        return True, json.dumps(r)

    def target(self, ref):
        info = self.eval(f"{self.cdp.TARGET}({json.dumps(bare(ref))})")
        if info.get("error"):
            raise self.cdp.CDPError(info["error"])
        if info.get("covered"):
            raise self.cdp.CDPError(info["covered"])
        return info

    def mouse(self, x, y, clicks=1):
        self.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})
        for n in range(1, clicks + 1):
            for kind in ("mousePressed", "mouseReleased"):
                self.call("Input.dispatchMouseEvent", {"type": kind, "x": x, "y": y, "button": "left",
                                                       "clickCount": n})

    def act(self, cmd):
        """(ok, error or None, raw output) of one Playwright-CLI-style command."""
        name, *args = cmd
        try:
            out = self.run(name, args)
        except self.cdp.CDPError as e:
            return False, str(e), str(e)
        except (IndexError, ValueError) as e:
            return False, f"bad arguments for {name}: {e}", ""
        return True, None, json.dumps(out, ensure_ascii=False)

    def run(self, name, args):
        if name in ("click", "dblclick"):
            t = self.target(args[0])
            if t["disabled"]:
                raise self.cdp.CDPError("element is disabled")
            self.mouse(t["x"], t["y"], 2 if name == "dblclick" else 1)
            return {"clicked": args[0]}
        if name == "hover":
            t = self.target(args[0])
            self.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": t["x"], "y": t["y"]})
            return {"hovered": args[0]}
        if name in ("check", "uncheck"):
            t = self.target(args[0])
            if bool(t["checked"]) != (name == "check"):
                self.mouse(t["x"], t["y"])
            return {name: args[0]}
        if name == "fill":
            ref, text = args[0], " ".join(args[1:])
            t = self.target(ref)
            if not t["editable"]:
                raise self.cdp.CDPError("Element is not an <input>, <textarea> or [contenteditable] element")
            self.eval(f"{self.cdp.FOCUS}({json.dumps(bare(ref))})")
            if text:
                self.call("Input.insertText", {"text": text})
            else:
                self.eval("document.execCommand('delete')")
            return {"filled": ref}
        if name == "select":
            self.target(args[0])
            r = self.eval(f"{self.cdp.SELECT}({json.dumps(bare(args[0]))}, {json.dumps(args[1:])})")
            if r.get("error"):
                raise self.cdp.CDPError(r["error"])
            return r
        if name == "type":
            self.call("Input.insertText", {"text": " ".join(args)})
            return {"typed": len(" ".join(args))}
        if name == "press":
            for event in self.cdp.key_events(args[0]):
                self.call("Input.dispatchKeyEvent", event)
            return {"pressed": args[0]}
        if name in ("go-back", "go-forward"):
            h = self.call("Page.getNavigationHistory")
            i = h["currentIndex"] + (-1 if name == "go-back" else 1)
            if 0 <= i < len(h["entries"]):
                self.call("Page.navigateToHistoryEntry", {"entryId": h["entries"][i]["id"]})
            return {"history": i}
        if name == "reload":
            return self.call("Page.reload")
        if name == "goto":
            return self.call("Page.navigate", {"url": args[0]})
        if name == "console":
            return self.client.op("errors")
        raise self.cdp.CDPError(f"unknown command '{name}' for --engine cdp; use: click, dblclick, hover, fill, type, "
                                "select, check, uncheck, press, go-back, go-forward, reload, goto, console")

    def js(self, fn, timeout=120):
        try:
            value = self.eval(f"({fn})()", timeout)
        except self.cdp.CDPError as e:
            return f"error: {e}"
        return value if isinstance(value, str) else json.dumps(value)

    def retry(self, fn, tries=40):
        """Run a page call again while a navigation replaces the document under it."""
        for _ in range(tries):
            try:
                return fn()
            except self.cdp.CDPError as e:
                if not any(g in str(e) for g in self.cdp.GONE):
                    raise
            time.sleep(0.1)
        return fn()

    def snapshot(self):
        data = self.retry(lambda: self.eval(f"({self.cdp.SNAPSHOT})()"))
        return data["url"], self.cdp.yaml(data["nodes"]), self.client.op("state")["errors"]

    def settle(self, timeout_ms):
        t = time.time()
        try:
            wait = self.retry(lambda: self.eval(self.cdp.SETTLE % (timeout_ms, OBSERVER), timeout_ms / 1000 + 30))
            while self.client.op("state")["loading"] and time.time() - t < timeout_ms / 1000:
                time.sleep(0.05)
            if self.eval("document.readyState") != "complete":  # a navigation started after the first wait
                wait = self.retry(lambda: self.eval(self.cdp.SETTLE % (timeout_ms, OBSERVER), timeout_ms / 1000 + 30))
        except self.cdp.CDPError:
            return None
        return wait

    def capture(self, fmt, scale_px=None, ref=None, quality=None):
        if ref:
            t = self.target(ref)
            clip = {"x": t["left"], "y": t["top"], "width": t["w"], "height": t["h"], "scale": 1}
        else:
            w, h, dpr = self.eval("[innerWidth, innerHeight, devicePixelRatio]")
            s = min(1, scale_px / max(w, h)) / dpr if scale_px else 1
            clip = {"x": 0, "y": 0, "width": w, "height": h, "scale": s}
        params = {"format": fmt, "clip": clip, **({"quality": quality} if quality else {})}
        return base64.b64decode(self.call("Page.captureScreenshot", params)["data"])

    def screenshot(self, dest, ref=None):
        try:
            Path(dest).write_bytes(self.capture("png", ref=ref))
        except self.cdp.CDPError as e:
            return False, str(e)
        return True, str(dest)

    def look(self):
        try:
            return self.capture("jpeg", LOOK_PX, quality=70)
        except self.cdp.CDPError:
            return b""

    def slow(self):
        self.call("Network.enable")
        self.call("Network.emulateNetworkConditions",
                  {"offline": False, "latency": 400, "downloadThroughput": 50000, "uploadThroughput": 25000})

    def close(self):
        return self.cdp.stop(self.session)


ENGINES = {"playwright": Playwright, "agent-browser": AgentBrowser, "cdp": CDP}


def engine(a):
    return ENGINES[a.engine](a.session)


def snapshot(eng):
    """Current URL, snapshot text (also saved under snaps/), its relative path and console error count."""
    url, body, errors = eng.snapshot()
    snaps = run_dir(eng.session) / "snaps"
    snaps.mkdir(exist_ok=True)
    file = snaps / f"{len(list(snaps.glob('*.yml'))):03d}.yml"
    file.write_text(body)
    return url, body, str(file.relative_to(run_dir(eng.session))), errors


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


def take_look(eng, ask=False, snap=None):
    """Save a <= 512 px screenshot under looks/; with ask, d1 compares the screen with the tree's controls."""
    raw = eng.look()
    if not raw:
        return None, None
    looks = run_dir(eng.session) / "looks"
    looks.mkdir(exist_ok=True)
    file = looks / f"{len(list(looks.glob('*.jpg'))):03d}.jpg"
    file.write_bytes(raw)
    seen = None
    if ask:
        import d1

        cs = d1.controls(snap if snap is not None else recall(eng.session)["snap"])
        answers, usage = d1.ask(None, d1.vision(cs[:d1.MAX_TARGETS], each=ask == "each"), images=[raw])
        seen = {"look": str(file.relative_to(run_dir(eng.session))), "controls_in_tree": len(cs),
                "names": {c["ref"]: f"{c['role']} '{c['name']}'" for c in cs}, "answers": answers,
                "cost_usd": usage.get("cost")}
        with open(run_dir(eng.session) / "looks.jsonl", "a") as f:
            f.write(json.dumps(seen, ensure_ascii=False) + "\n")
    return file, seen


def print_look(file, seen):
    if not file:
        print("look: no screenshot (engine returned nothing)")
        return
    print(f"screen: {file}")
    if seen:
        a, names = seen["answers"], seen["names"]
        line = (f"screen vs tree: {seen['controls_in_tree']} controls in the tree; "
                f"control on screen but not in the tree p={a['unlisted']['noul']:.2f}; "
                f"screen shows {a['screen']['choice']} ({a['screen']['confidence']:.2f})")
        if "main" in a:
            ref = a["main"]["choice"]
            line += f"; looks like the main action: {names.get(ref, ref)} [{ref}] ({a['main']['confidence']:.2f})"
        print(line)
        unseen = [f"{names.get(k[5:], k[5:])} [{k[5:]}] p={v['noul']:.2f}" for k, v in a.items()
                  if k.startswith("seen_") and v["noul"] < 0.5]
        if unseen:
            print("in the tree but hard to see on screen: " + "; ".join(unseen) + " - open the screenshot and check")


def ms(start):
    """Engine time of this command so far, for step-time benchmarks."""
    return round((time.time() - start) * 1000)


def want_look():
    return os.environ.get("PC_LOOK") in ("1", "ask")


def cmd_open(a):
    start = time.time()
    eng = engine(a)
    ok, text = eng.open(a.url, a.mobile)
    if not ok:
        sys.exit(text[-2000:])
    if a.slow:
        eng.slow()
    wait = eng.settle(30000)
    url, snap, file, errors = snapshot(eng)
    remember(a.session, url, snap, errors)
    look, seen = take_look(eng, os.environ.get("PC_LOOK") == "ask" and "each", snap) if want_look() else (
        None, None)
    log(a.session, {"i": 0, "t": time.time(), "cmd": ["open", a.url], "url": url, "ok": True, "changed": True,
                    "snapshot": file, "wait_ms": wait, "console_errors": errors, "engine": eng.name,
                    "look": look and str(look.relative_to(run_dir(a.session))), "ms": ms(start)})
    print(f"url: {url}\nsnapshot: {run_dir(a.session) / file}\n{snap}")
    if want_look():
        print_look(look, seen)


def cmd_do(a):
    if not a.cmd:
        sys.exit("usage: pc.py do -- <command>")
    done = sum(1 for e in read_log(run_dir(a.session) / "log.jsonl") if e["i"] and e["ok"])  # failed refs are free
    if (limit := os.environ.get("PC_BUDGET")) and done >= int(limit):
        print(f"out of patience: {done} of {limit} actions used. End now: pc.py end --outcome quit --reason '...'")
        sys.exit(3)
    start = time.time()
    eng = engine(a)
    before = recall(a.session)
    eng.js("() => { if (window.__pc) window.__pc.t0 = Date.now(); }")
    ok, error, _ = eng.act(a.cmd)
    wait = eng.settle(30000)
    url, snap, file, errors = snapshot(eng)
    diff = changes(before["snap"], snap)
    changed = bool(diff) or url != before["url"]
    steps = len(read_log(run_dir(a.session) / "log.jsonl"))
    look, seen = take_look(eng, os.environ.get("PC_LOOK") == "ask" and "each", snap) if want_look() else (
        None, None)
    log(a.session, {"i": steps, "t": time.time(), "cmd": a.cmd, "url": url, "ok": ok, "changed": changed,
                    "error": error, "snapshot": file, "wait_ms": wait, "console_errors": errors, "note": a.note,
                    "engine": eng.name, "tier": a.tier,
                    "look": look and str(look.relative_to(run_dir(a.session))), "ms": ms(start)})
    remember(a.session, url, snap, errors)
    print(f"step {steps}: {' '.join(a.cmd)} -> {'ok' if ok else 'ERROR'}")
    if error:
        print(f"error: {error}")
        if "not found" in error.lower() or "unknown ref" in error.lower():
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
    if want_look():
        print_look(look, seen)


def cmd_look(a):
    eng = engine(a)
    file, seen = take_look(eng, "each" if a.ask else False)
    print_look(file, seen)


def cmd_shot(a):
    dest = Path("shots", f"{a.name}.png").resolve()
    dest.parent.mkdir(exist_ok=True)
    ok, text = engine(a).screenshot(dest, a.ref)
    if not ok or not dest.exists():
        sys.exit(str(text)[-2000:])
    print(dest.relative_to(Path.cwd().resolve()))


def cmd_inventory(a):
    print(engine(a).js(INVENTORY % (MSG, "0" if a.all else "-1")))


def cmd_metrics(a):
    raw = engine(a).js("() => JSON.stringify(window.__pc || null)")
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
    engine(a).close()
    print(f"ended: {a.outcome}")


def cmd_close(a):
    print(engine(a).close()[-500:])


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="command", required=True)
    # one browser per working folder by default, so parallel runs in other folders never share a session
    session = os.environ.get("PC_SESSION") or "pc-" + hashlib.sha1(os.getcwd().encode()).hexdigest()[:6]
    for name, fn in [("open", cmd_open), ("do", cmd_do), ("look", cmd_look), ("shot", cmd_shot),
                     ("inventory", cmd_inventory), ("metrics", cmd_metrics), ("end", cmd_end), ("close", cmd_close)]:
        s = sub.add_parser(name)
        s.add_argument("--session", default=session)
        s.add_argument("--engine", choices=sorted(ENGINES), default=os.environ.get("PC_ENGINE", "playwright"))
        s.set_defaults(fn=fn)
        if name == "open":
            s.add_argument("url")
            s.add_argument("--mobile", action="store_true")
            s.add_argument("--slow", action="store_true", help="emulate a slow mobile network (Chromium)")
        if name == "do":
            s.add_argument("--note", default=None, help="why you did it (persona think-aloud)")
            s.add_argument("--tier", default=os.environ.get("PC_TIER"), help="who decided: d1, haiku, sonnet")
            s.add_argument("cmd", nargs=argparse.REMAINDER)
        if name == "shot":
            s.add_argument("name")
            s.add_argument("--ref", default=None)
        if name == "look":
            s.add_argument("--ask", action="store_true",
                           help="ask d1 what the screen shows that the tree does not, and which controls are unseen")
        if name == "inventory":
            s.add_argument("--all", action="store_true", help="every message, not only the last")
        if name == "end":
            s.add_argument("--outcome", choices=["done", "quit", "blocked"], required=True)
            s.add_argument("--reason", default="")
    a = p.parse_args(argv)
    if getattr(a, "cmd", None) and a.cmd[0] == "--":
        a.cmd = a.cmd[1:]
    try:
        a.fn(a)
    except RuntimeError as e:  # cdp engine: no browser for this session, Chrome missing
        sys.exit(f"error: {e}")


sys.path.insert(0, str(Path(__file__).resolve().parent))  # d1.py next to this file

if __name__ == "__main__":
    main()
