#!/usr/bin/env python3
"""Direct Chrome DevTools Protocol session for pc.py --engine cdp. Stdlib only.

pc.py runs once per step, so the browser has to outlive it: `pc.py open` starts one small daemon per session that
launches headless Chrome, keeps a single CDP connection to its page and listens on a unix socket. Every later pc.py
call sends raw CDP commands through that socket, so emulation (mobile, slow network) and the console error log stay
with the session. The page state for a decision (controls, text, refs) comes from one Runtime.evaluate, the idea
behind the browser layer of browser-use/jev-ultrafast (MIT); the code here is our own.

    python3 cdp.py serve SESSION     # the daemon; pc.py starts it, you never need to
    python3 cdp.py stop SESSION      # same as pc.py close --engine cdp

Env: $PC_CHROME (Chrome or Chromium binary), else google-chrome / chromium on PATH, else a Playwright or
agent-browser download. $PC_CDP_HOME (default ~/.cache/pc-cdp, else the temp folder) holds one folder per session: socket, profile,
daemon.log. $PC_CDP_IDLE (seconds, default 1800): the daemon closes its browser after that long without a call.
"""

import base64
import glob
import hashlib
import json
import os
import selectors
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from pathlib import Path

IDLE = int(os.environ.get("PC_CDP_IDLE", "1800"))
DESKTOP = {"width": 1280, "height": 720, "deviceScaleFactor": 1, "mobile": False}
MOBILE = {"width": 390, "height": 844, "deviceScaleFactor": 3, "mobile": True}
MOBILE_UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
             "Version/18.0 Mobile/15E148 Safari/604.1")
GONE = ("Execution context was destroyed", "Cannot find context", "Inspected target navigated or closed",
        "Cannot find default execution context")

# Page state in one evaluate: a flat list of nodes {d, role, name, ref, attrs, tail, url, placeholder} or {d, text}.
# Refs live in the page (window.__pcSnap) so they survive between pc.py calls; an element keeps its ref while it is
# in the DOM, a re-rendered element gets a new one, as in Playwright CLI.
SNAPSHOT = r"""() => {
  const S = window.__pcSnap || (window.__pcSnap = { refs: new WeakMap(), els: new Map(), n: 0 });
  const refOf = el => {
    let r = S.refs.get(el);
    if (!r) { r = 'e' + (++S.n); S.refs.set(el, r); S.els.set(r, new WeakRef(el)); }
    return r;
  };
  const norm = s => (s || '').replace(/\s+/g, ' ').trim();
  const cut = s => s.length > 300 ? s.slice(0, 300) + '...' : s;
  const SKIP = new Set(['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE', 'HEAD', 'META', 'LINK', 'TITLE', 'IFRAME']);
  const LANDMARK = 'article,aside,main,nav,section';
  const INPUTS = { button: 'button', submit: 'button', reset: 'button', image: 'button', checkbox: 'checkbox',
    radio: 'radio', range: 'slider', number: 'spinbutton', search: 'searchbox', hidden: null };
  const TAGS = { BUTTON: 'button', NAV: 'navigation', MAIN: 'main', ASIDE: 'complementary', FORM: 'form',
    H1: 'heading', H2: 'heading', H3: 'heading', H4: 'heading', H5: 'heading', H6: 'heading', P: 'paragraph',
    UL: 'list', OL: 'list', MENU: 'list', LI: 'listitem', TEXTAREA: 'textbox', OPTION: 'option', TABLE: 'table',
    TR: 'row', TD: 'cell', TH: 'columnheader', DIALOG: 'dialog', ARTICLE: 'article', STRONG: 'strong',
    B: 'strong', EM: 'emphasis', I: 'emphasis', CODE: 'code', BLOCKQUOTE: 'blockquote', HR: 'separator',
    FIELDSET: 'group', DETAILS: 'group', SUMMARY: 'button', PROGRESS: 'progressbar', METER: 'meter',
    DL: 'list', DT: 'term', DD: 'definition', FIGURE: 'figure', SVG: null };
  const FROM_CONTENT = new Set(['button', 'link', 'heading', 'option', 'tab', 'menuitem', 'menuitemcheckbox',
    'menuitemradio', 'cell', 'columnheader', 'rowheader', 'checkbox', 'radio', 'switch', 'treeitem', 'tooltip']);
  const LEAF = new Set(['textbox', 'searchbox', 'spinbutton', 'slider', 'combobox', 'listbox', 'img', 'progressbar',
    'meter', 'separator']);
  const byIds = ids => norm(ids.split(/\s+/).map(id => document.getElementById(id)).filter(Boolean)
    .map(e => e.textContent).join(' '));
  const role = el => {
    const r = (el.getAttribute('role') || '').split(/\s+/)[0];
    if (r) return r === 'none' ? 'presentation' : r;
    const t = el.tagName;
    if (t === 'A') return el.hasAttribute('href') ? 'link' : 'generic';
    if (t === 'INPUT') { const k = (el.type || 'text').toLowerCase(); return k in INPUTS ? INPUTS[k] : 'textbox'; }
    if (t === 'SELECT') return el.multiple || el.size > 1 ? 'listbox' : 'combobox';
    if (t === 'IMG') return el.getAttribute('alt') === '' ? 'presentation' : 'img';
    if (t === 'HEADER') return el.closest(LANDMARK) ? 'generic' : 'banner';
    if (t === 'FOOTER') return el.closest(LANDMARK) ? 'generic' : 'contentinfo';
    if (t === 'SECTION') return el.hasAttribute('aria-label') || el.hasAttribute('aria-labelledby') ? 'region' : 'generic';
    if (t in TAGS) return TAGS[t];
    return el.namespaceURI === 'http://www.w3.org/2000/svg' ? null : 'generic';
  };
  const name = (el, r) => {
    const lb = el.getAttribute('aria-labelledby');
    if (lb) { const t = byIds(lb); if (t) return t; }
    const al = norm(el.getAttribute('aria-label'));
    if (al) return al;
    const t = el.tagName;
    if (t === 'INPUT' || t === 'TEXTAREA' || t === 'SELECT') {
      const l = el.labels && norm([...el.labels].map(x => x.textContent).join(' '));
      if (l) return l;
      if (t === 'INPUT' && r === 'button') return el.type === 'image' ? norm(el.alt) : el.value || (el.type === 'submit' ? 'Submit' : '');
      return norm(el.title || el.placeholder);
    }
    if (t === 'IMG') return norm(el.alt || el.title);
    if (t === 'FIELDSET') { const lg = el.querySelector(':scope > legend'); if (lg) return norm(lg.textContent); }
    if (FROM_CONTENT.has(r)) return cut(norm(el.textContent)) || norm(el.title);
    return '';
  };
  const attrs = (el, r) => {
    const a = [];
    if (r === 'heading') a.push('level=' + (el.getAttribute('aria-level') || el.tagName.slice(1) || 2));
    const checked = el.getAttribute('aria-checked') ?? (el.type === 'checkbox' || el.type === 'radio' ? String(el.checked) : null);
    if (checked === 'true') a.push('checked'); else if (checked === 'mixed') a.push('checked=mixed');
    if (el.disabled || el.getAttribute('aria-disabled') === 'true') a.push('disabled');
    if (el.getAttribute('aria-expanded') === 'true' || (el.tagName === 'DETAILS' && el.open)) a.push('expanded');
    if (el.getAttribute('aria-pressed') === 'true') a.push('pressed');
    if (el.getAttribute('aria-selected') === 'true') a.push('selected');
    if (el === document.activeElement) a.push('active');
    return a;
  };
  const visible = el => el.checkVisibility ? el.checkVisibility({ visibilityProperty: true }) : !!el.getClientRects().length;
  const out = [];
  const kids = n => n.shadowRoot ? [...n.shadowRoot.childNodes, ...n.childNodes] : n.childNodes;
  const walk = (n, d) => {
    for (const c of kids(n)) {
      if (c.nodeType === 3) { const t = norm(c.data); if (t) out.push({ d, text: cut(t) }); }
      else if (c.nodeType === 1) visit(c, d);
    }
  };
  const visit = (el, d) => {
    if (SKIP.has(el.tagName) || el.hidden || el.getAttribute('aria-hidden') === 'true') return;
    if (!visible(el)) { if (getComputedStyle(el).display === 'contents') walk(el, d); return; }
    const r = role(el);
    if (r === null) return;
    if (r === 'presentation') { walk(el, d); return; }
    const node = { d, role: r, name: name(el, r), ref: refOf(el), attrs: attrs(el, r) };
    if (r === 'link') node.url = el.getAttribute('href');
    out.push(node);
    if (el.tagName === 'SELECT') {
      for (const o of el.options) out.push({ d: d + 1, role: 'option', name: norm(o.label || o.text), attrs: o.selected ? ['selected'] : [] });
      return;
    }
    if (LEAF.has(r) || el.tagName === 'INPUT') {
      if ('value' in el && el.type !== 'checkbox' && el.type !== 'radio' && r !== 'button' && el.value) node.tail = el.type === 'password' ? '•'.repeat(el.value.length) : cut(el.value);
      if (el.placeholder && el.placeholder !== node.name) node.placeholder = el.placeholder;
      return;
    }
    const at = out.length;
    walk(el, d + 1);
    const sub = out.slice(at);
    if (sub.every(x => 'text' in x)) {  // only text below: fold it into the line
      out.length = at;
      const t = cut(norm(sub.map(x => x.text).join(' ')));
      if (t && t !== node.name) node.tail = t;
      if (r === 'generic' && !node.name && !node.attrs.length) {
        const cs = getComputedStyle(el);  // inline text wrappers read as text, as in Playwright CLI
        if (!node.tail) { if (cs.cursor === 'pointer') node.attrs.push('cursor=pointer'); else out.pop(); }
        else if (cs.display.startsWith('inline') && cs.cursor !== 'pointer') out[out.length - 1] = { d, text: node.tail };
      }
    } else if (FROM_CONTENT.has(r) && node.name && !el.querySelector('a[href],button,input,select,textarea,[role]')) {
      out.length = at;  // a control named by its own content: the children repeat the name
    }
  };
  visit(document.body, 0);
  return { url: location.href, nodes: out };
}"""

# One action helper per call: resolve a ref, bring it into view, report where to click or why not.
TARGET = r"""(ref => {
  const S = window.__pcSnap, w = S && S.els.get(ref), el = w && w.deref();
  if (!el || !el.isConnected) return { error: `Ref ${ref} not found in the current page snapshot. Try capturing new snapshot.` };
  el.scrollIntoView({ block: 'center', inline: 'center', behavior: 'instant' });
  const r = el.getBoundingClientRect();
  const tag = el.tagName.toLowerCase(), type = (el.type || '').toLowerCase();
  const info = { tag, type, role: el.getAttribute('role'), checked: el.checked ?? el.getAttribute('aria-checked') === 'true',
    editable: (tag === 'input' && !['checkbox', 'radio', 'button', 'submit', 'reset', 'image', 'range', 'file', 'color'].includes(type))
      || tag === 'textarea' || el.isContentEditable,
    disabled: !!el.disabled || el.getAttribute('aria-disabled') === 'true', x: r.left + r.width / 2, y: r.top + r.height / 2,
    w: r.width, h: r.height, top: r.top, left: r.left };
  if (!r.width || !r.height) return { ...info, error: 'element is not visible' };
  const hit = document.elementFromPoint(info.x, info.y);
  const label = hit && hit.closest('label');
  if (hit && hit !== el && !el.contains(hit) && !(label && label.control === el)) {
    const cls = String(hit.className || '').trim().split(/\s+/)[0];
    info.covered = `<${hit.tagName.toLowerCase()}${hit.id ? ' id="' + hit.id + '"' : ''}${cls ? ' class="' + cls + '"' : ''}> intercepts pointer events`;
  }
  return info;
})"""
FOCUS = r"""(ref => {
  const el = window.__pcSnap.els.get(ref).deref();
  el.focus();
  if (el.select && (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA')) el.select();
  else { const s = getSelection(), rg = document.createRange(); rg.selectNodeContents(el); s.removeAllRanges(); s.addRange(rg); }
  return true;
})"""
SELECT = r"""((ref, values) => {
  const el = window.__pcSnap.els.get(ref).deref();
  if (el.tagName !== 'SELECT') return { error: 'Element is not a <select> element' };
  const opts = [...el.options], picked = [];
  for (const v of values) {
    const o = opts.find(o => o.value === v || o.label.trim() === v || o.text.trim() === v);
    if (!o) return { error: `option not found: ${v}; options: ${opts.map(o => o.label.trim()).join(' | ')}` };
    picked.push(o);
  }
  opts.forEach(o => { o.selected = picked.includes(o); });
  el.dispatchEvent(new Event('input', { bubbles: true }));
  el.dispatchEvent(new Event('change', { bubbles: true }));
  return { selected: picked.map(o => o.label.trim()) };
})"""
SETTLE = r"""(async () => {
  await new Promise(r => setTimeout(r, 300));
  const t = Date.now(), busy = () => document.querySelector('[aria-busy="true"],[data-streaming="true"]');
  while (busy()) {
    if (Date.now() - t > %d) return -1;
    await new Promise(r => setTimeout(r, 50));
  }
  (%s)();
  return Date.now() - t;
})()"""

KEYS = {  # key -> (code, windowsVirtualKeyCode, text)
    "Enter": ("Enter", 13, "\r"), "Tab": ("Tab", 9, ""), "Escape": ("Escape", 27, ""),
    "Backspace": ("Backspace", 8, ""), "Delete": ("Delete", 46, ""), "Space": ("Space", 32, " "),
    " ": ("Space", 32, " "), "ArrowUp": ("ArrowUp", 38, ""), "ArrowDown": ("ArrowDown", 40, ""),
    "ArrowLeft": ("ArrowLeft", 37, ""), "ArrowRight": ("ArrowRight", 39, ""), "Home": ("Home", 36, ""),
    "End": ("End", 35, ""), "PageUp": ("PageUp", 33, ""), "PageDown": ("PageDown", 34, ""),
}
MODIFIERS = {"Alt": 1, "Control": 2, "Meta": 4, "Shift": 8}


def key_events(combo):
    """Input.dispatchKeyEvent params for a Playwright-style key such as Enter, a, Shift+Tab or Control+a."""
    *mods, key = combo.split("+") if combo != "+" else ["+"]
    flags = sum(MODIFIERS.get(m, 0) for m in mods)
    if key in KEYS:
        code, vk, text = KEYS[key]
        key = " " if key == "Space" else key
    elif len(key) == 1:
        code = f"Key{key.upper()}" if key.isalpha() else f"Digit{key}" if key.isdigit() else ""
        vk, text = ord(key.upper()), key
    else:
        raise ValueError(f"unknown key: {key}")
    if flags & ~MODIFIERS["Shift"]:
        text = ""  # Control+a selects, it does not type
    down = {"type": "keyDown" if text else "rawKeyDown", "key": key, "code": code, "windowsVirtualKeyCode": vk,
            "modifiers": flags}
    if text:
        down["text"] = down["unmodifiedText"] = text
    return [down, {"type": "keyUp", "key": key, "code": code, "windowsVirtualKeyCode": vk, "modifiers": flags}]


def quote(s):
    """A YAML scalar the way Playwright CLI prints it: quoted when it would not read back as plain text."""
    if s == "" or s[0] in "#&*!|>'\"%@`{[]-?,:" or ": " in s or s.endswith(":") or " #" in s or s.strip() != s \
            or s.replace(".", "", 1).replace(" ", "").lstrip("-").isdigit() or s.lower() in ("true", "false", "null"):
        return json.dumps(s, ensure_ascii=False)
    return s


def esc(name):
    return name.replace("\\", "\\\\").replace('"', '\\"')


def yaml(nodes):
    """Playwright-CLI-style accessibility snapshot from the SNAPSHOT node list, so d1.controls() and pc.norm()
    read both engines alike: `- button "Name" [attrs] [ref=e5]: text`, `- /url: ...` under links."""
    lines = []
    for i, n in enumerate(nodes):
        pad = "  " * n["d"]
        if "text" in n:
            lines.append(f"{pad}- text: {quote(n['text'])}")
            continue
        head = n["role"] + (f' "{esc(n["name"])}"' if n.get("name") else "")
        head += "".join(f" [{a}]" for a in n.get("attrs", [])) + (f" [ref={n['ref']}]" if n.get("ref") else "")
        props = [f"/url: {quote(n['url'])}"] if n.get("url") else []
        props += [f"/placeholder: {quote(n['placeholder'])}"] if n.get("placeholder") else []
        nested = i + 1 < len(nodes) and nodes[i + 1]["d"] > n["d"]
        if n.get("tail") and not props and not nested:
            lines.append(f"{pad}- {head}: {quote(n['tail'])}")
            continue
        lines.append(f"{pad}- {head}" + (":" if props or nested or n.get("tail") else ""))
        lines += [f"{pad}  - {p}" for p in props]
        if n.get("tail"):
            lines.append(f"{pad}  - text: {quote(n['tail'])}")
    return "\n".join(lines) + "\n"


# ---- transport -------------------------------------------------------------------------------------------------

class WebSocket:
    """Minimal RFC 6455 client: text frames, client masking, fragmentation, ping/pong. Enough for CDP."""

    def __init__(self, url, timeout=30):
        u = urllib.parse.urlparse(url)
        self.sock = socket.create_connection((u.hostname, u.port), timeout=timeout)
        key = base64.b64encode(os.urandom(16)).decode()
        self.sock.sendall((f"GET {u.path} HTTP/1.1\r\nHost: {u.hostname}:{u.port}\r\nUpgrade: websocket\r\n"
                           f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n")
                          .encode())
        self.buf = b""
        while b"\r\n\r\n" not in self.buf:
            self._fill()
        head, self.buf = self.buf.split(b"\r\n\r\n", 1)
        if b" 101 " not in head.split(b"\r\n")[0]:
            raise ConnectionError(f"websocket handshake failed: {head[:200]!r}")

    def _fill(self):
        chunk = self.sock.recv(1 << 16)
        if not chunk:
            raise ConnectionError("websocket closed")
        self.buf += chunk

    def _take(self, n):
        while len(self.buf) < n:
            self._fill()
        out, self.buf = self.buf[:n], self.buf[n:]
        return out

    def _frame(self, op, data):
        n, mask = len(data), os.urandom(4)
        head = bytes([0x80 | op]) + (bytes([0x80 | n]) if n < 126 else bytes([0x80 | 126]) + n.to_bytes(2, "big")
                                     if n < 65536 else bytes([0x80 | 127]) + n.to_bytes(8, "big"))
        key = int.from_bytes((mask * (n // 4 + 1))[:n], "big")
        body = (int.from_bytes(data, "big") ^ key).to_bytes(n, "big") if n else b""
        self.sock.sendall(head + mask + body)

    def send(self, text):
        self._frame(0x1, text.encode())

    def pump(self):
        """Read whatever bytes are waiting on the socket, without blocking."""
        self.sock.setblocking(False)
        try:
            while True:
                chunk = self.sock.recv(1 << 16)
                if not chunk:
                    raise ConnectionError("websocket closed")
                self.buf += chunk
        except (BlockingIOError, InterruptedError):
            pass
        finally:
            self.sock.setblocking(True)

    def has_frame(self):
        """True when the buffer holds at least one whole frame."""
        if len(self.buf) < 2:
            return False
        n, at = self.buf[1] & 0x7F, 2
        if n >= 126:
            size = 2 if n == 126 else 8
            if len(self.buf) < 2 + size:
                return False
            n, at = int.from_bytes(self.buf[2:2 + size], "big"), 2 + size
        return len(self.buf) >= at + (4 if self.buf[1] & 0x80 else 0) + n

    def recv(self):
        parts = []
        while True:
            b1, b2 = self._take(2)
            n = b2 & 0x7F
            if n == 126:
                n = int.from_bytes(self._take(2), "big")
            elif n == 127:
                n = int.from_bytes(self._take(8), "big")
            mask = self._take(4) if b2 & 0x80 else None
            data = self._take(n)
            if mask:
                data = bytes(b ^ mask[i % 4] for i, b in enumerate(data))
            op = b1 & 0x0F
            if op == 0x9:
                self._frame(0xA, data)
            elif op == 0x8:
                raise ConnectionError("websocket closed by the browser")
            elif op in (0x0, 0x1, 0x2):
                parts.append(data)
                if b1 & 0x80:
                    return b"".join(parts).decode()


def home(session):
    name = hashlib.sha1(session.encode()).hexdigest()[:12]  # unix socket paths must stay short
    bases = [os.environ.get("PC_CDP_HOME"), Path.home() / ".cache" / "pc-cdp",
             Path(tempfile.gettempdir()) / f"pc-cdp-{os.getuid() if hasattr(os, 'getuid') else 'user'}"]
    for base in filter(None, bases):
        try:
            (Path(base) / name).mkdir(parents=True, exist_ok=True)
            return Path(base) / name
        except OSError:
            continue
    raise RuntimeError("no writable folder for the cdp session: set PC_CDP_HOME")


def find_chrome():
    if env := os.environ.get("PC_CHROME"):
        return env
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        if path := shutil.which(name):
            return path
    roots = [os.environ.get("PLAYWRIGHT_BROWSERS_PATH"), str(Path.home() / ".cache" / "ms-playwright")]
    for root in filter(None, roots):
        found = sorted(glob.glob(f"{root}/chromium-*/chrome-linux*/chrome") + glob.glob(
            f"{root}/chromium-*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium"), reverse=True)
        if found:
            return found[0]
    found = sorted(glob.glob(str(Path.home() / ".agent-browser" / "browsers" / "chrome-*" / "chrome")), reverse=True)
    if found:
        return found[0]
    raise RuntimeError("no Chrome found: set PC_CHROME, or install one (playwright-cli install-browser chromium)")


class CDPError(RuntimeError):
    pass


class Client:
    """pc.py side: one unix-socket connection to the session daemon, raw CDP calls over it."""

    def __init__(self, session):
        self.session, self.dir, self.conn, self.rfile = session, home(session), None, None

    def alive(self):
        try:
            self._connect()
            return True
        except OSError:
            return False

    def _connect(self):
        if self.conn is None:
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            s.connect(str(self.dir / "sock"))
            s.settimeout(300)
            self.conn, self.rfile = s, s.makefile("rb")

    def start(self):
        """Connect to the session's daemon, starting one (and its Chrome) if none is running."""
        if self.alive():
            return
        (self.dir / "sock").unlink(missing_ok=True)
        log = open(self.dir / "daemon.log", "ab")
        proc = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), "serve", self.session],
                                stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        deadline = time.time() + 30
        while time.time() < deadline:
            if proc.poll() is not None:
                break
            if (self.dir / "sock").exists() and self.alive():
                return
            time.sleep(0.05)
        tail = (self.dir / "daemon.log").read_text(errors="replace")[-800:]
        raise RuntimeError(f"the cdp daemon did not start:\n{tail}")

    def request(self, msg):
        if self.conn is None:
            try:
                self._connect()
            except OSError:
                raise CDPError(f"no browser for session {self.session}: run pc.py open first") from None
        self.conn.sendall(json.dumps(msg).encode() + b"\n")
        line = self.rfile.readline()
        if not line:
            raise CDPError("the cdp daemon closed the connection")
        reply = json.loads(line)
        if "error" in reply:
            raise CDPError(reply["error"])
        return reply.get("result", {})

    def call(self, method, params=None, timeout=60):
        return self.request({"method": method, "params": params or {}, "timeout": timeout})

    def op(self, name):
        return self.request({"op": name})


# ---- daemon ----------------------------------------------------------------------------------------------------

class Daemon:
    def __init__(self, session):
        self.dir = home(session)
        self.profile = self.dir / "profile"
        self.chrome = None
        self.ws = None
        self.next_id = 0
        self.errors, self.dialogs = [], []
        self.loading = False
        self.frame = None

    def launch(self):
        shutil.rmtree(self.profile, ignore_errors=True)
        args = [find_chrome(), "--headless=new", "--remote-debugging-port=0", f"--user-data-dir={self.profile}",
                "--no-first-run", "--no-default-browser-check", "--disable-background-networking",
                "--disable-extensions", "--disable-sync", "--disable-dev-shm-usage", "--mute-audio",
                "--hide-scrollbars", "--window-size=1280,720", "--no-sandbox", "about:blank"]  # no sandbox, as Playwright
        self.chrome = subprocess.Popen(args, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                       stderr=open(self.dir / "chrome.log", "wb"))
        port_file = self.profile / "DevToolsActivePort"
        deadline = time.time() + 20
        while not port_file.exists() or not port_file.read_text().strip():
            if time.time() > deadline or self.chrome.poll() is not None:
                raise RuntimeError(f"Chrome ({args[0]}) did not open its DevTools port, see {self.dir / 'chrome.log'}")
            time.sleep(0.02)
        port = port_file.read_text().split()[0]
        for _ in range(100):
            pages = [t for t in json.loads(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list").read())
                     if t["type"] == "page"]
            if pages:
                break
            time.sleep(0.05)
        self.ws = WebSocket(pages[0]["webSocketDebuggerUrl"])
        for method in ("Page.enable", "Runtime.enable", "Log.enable"):
            self.call(method)
        self.frame = self.call("Page.getFrameTree")["frameTree"]["frame"]["id"]
        self.call("Emulation.setDeviceMetricsOverride", DESKTOP)
        (self.dir / "daemon.json").write_text(json.dumps({"pid": os.getpid(), "chrome_pid": self.chrome.pid,
                                                          "port": port}))

    def event(self, m):
        method, p = m.get("method"), m.get("params", {})
        if method == "Runtime.consoleAPICalled" and p.get("type") == "error":
            self.errors.append(" ".join(str(a.get("value", a.get("description", ""))) for a in p.get("args", [])))
        elif method == "Runtime.exceptionThrown":
            d = p.get("exceptionDetails", {})
            self.errors.append((d.get("exception") or {}).get("description") or d.get("text", "exception"))
        elif method == "Log.entryAdded" and p.get("entry", {}).get("level") == "error":
            self.errors.append(p["entry"].get("text", ""))
        elif method == "Page.javascriptDialogOpening":
            self.dialogs.append(f"{p.get('type')}: {p.get('message')}")
            self.send("Page.handleJavaScriptDialog", {"accept": True})
        elif method == "Page.frameStartedLoading" and p.get("frameId") == self.frame:
            self.loading = True
        elif method == "Page.frameStoppedLoading" and p.get("frameId") == self.frame:
            self.loading = False
        del self.errors[:-200]

    def send(self, method, params=None):
        self.next_id += 1
        self.ws.send(json.dumps({"id": self.next_id, "method": method, "params": params or {}}))
        return self.next_id

    def call(self, method, params=None, timeout=60):
        wanted = self.send(method, params)
        self.ws.sock.settimeout(timeout)
        try:
            while True:
                m = json.loads(self.ws.recv())
                if m.get("id") == wanted:
                    if "error" in m:
                        raise CDPError(m["error"].get("message", str(m["error"])))
                    return m.get("result", {})
                if "method" in m:
                    self.event(m)
        finally:
            self.ws.sock.settimeout(None)

    def handle(self, msg):
        if op := msg.get("op"):
            if op == "state":
                return {"loading": self.loading, "errors": len(self.errors), "dialogs": self.dialogs[-5:]}
            if op == "errors":
                return {"errors": self.errors[-50:], "dialogs": self.dialogs[-20:]}
            if op == "close":
                raise SystemExit(0)
            raise CDPError(f"unknown op {op}")
        return self.call(msg["method"], msg.get("params"), msg.get("timeout", 60))

    def serve_client(self, conn):
        conn.settimeout(300)
        rfile = conn.makefile("rb")
        for line in rfile:
            try:
                reply = {"result": self.handle(json.loads(line))}
            except CDPError as e:
                reply = {"error": str(e)}
            except (socket.timeout, TimeoutError):
                reply = {"error": "timed out waiting for the browser"}
            try:
                conn.sendall(json.dumps(reply).encode() + b"\n")
            except OSError:
                break
            if self.ws.buf:  # events that arrived with the reply
                self.drain()
        conn.close()

    def drain(self):
        """Handle every event already sent by the browser, without blocking."""
        self.ws.pump()
        while self.ws.has_frame():
            self.event(json.loads(self.ws.recv()))

    def run(self):
        self.launch()
        sock_path = self.dir / "sock"
        sock_path.unlink(missing_ok=True)
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(str(sock_path))
        server.listen(8)
        sel = selectors.DefaultSelector()
        sel.register(server, selectors.EVENT_READ, "client")
        sel.register(self.ws.sock, selectors.EVENT_READ, "browser")
        last = time.time()
        while True:
            ready = sel.select(timeout=30)
            if not ready and time.time() - last > IDLE:
                return
            for key, _ in ready:
                if key.data == "client":
                    conn, _ = server.accept()
                    self.serve_client(conn)
                    last = time.time()
                else:
                    self.drain()

    def shutdown(self):
        if self.chrome and self.chrome.poll() is None:
            self.chrome.terminate()
            try:
                self.chrome.wait(5)
            except subprocess.TimeoutExpired:
                self.chrome.kill()
        (self.dir / "sock").unlink(missing_ok=True)
        (self.dir / "daemon.json").unlink(missing_ok=True)
        shutil.rmtree(self.profile, ignore_errors=True)


def serve(session):
    d = Daemon(session)
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    try:
        d.run()
    except (ConnectionError, SystemExit):
        pass
    finally:
        d.shutdown()


def stop(session):
    c = Client(session)
    if not c.alive():
        return "no browser"
    try:
        c.op("close")
    except (CDPError, OSError):
        pass
    for _ in range(100):
        if not (c.dir / "sock").exists():
            break
        time.sleep(0.05)
    return "closed"


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("serve", "stop"):
        sys.exit(__doc__)
    if sys.argv[1] == "serve":
        serve(sys.argv[2])
    else:
        print(stop(sys.argv[2]))
