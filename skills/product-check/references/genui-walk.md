# genui-walk - walking a chat that renders components

For products where the assistant answers in a stream and puts cards, buttons,
choice chips, sliders and forms inside its messages. Run it on top of
`walk.md`: the same persona, tasks, optimum and finding format.

## Waiting for a message

A chat keeps a connection open, so the network never goes quiet: never wait
for network idle. Wait for the stream marker instead:

- the message element has `aria-busy="true"` or `data-streaming="true"` while
  it streams and `false` when done;
- `pc.py do` waits for both markers after every action (up to 30 s) and warns
  when a stream is still busy;
- no marker at all: that is a finding (`GW-6`), then wait for the text of the
  last message to stop changing across two snapshots.

Decide only on finished messages. A component that appears mid-stream may
still change.

## After each answer

1. `pc.py inventory` lists the components in the last message: role, name,
   disabled, value, plus "suspects" - clickable elements without a role and
   slider-like elements without `role="slider"`.
2. `pc.py metrics` gives, for the last action: time to first text, time to
   the end of the stream, time to the first interactive component.
3. Count messages to the goal. Compare with the optimum, like actions in
   `walk.md` WK-1.
4. A control missing from the snapshot (a suspect) still gets used: click or
   drag it by position with `pc.py do -- run-code "async page => { const b =
   await page.locator('.<class from inventory>').last().boundingBox();
   await page.mouse.click(b.x + b.width * 0.8, b.y + b.height / 2) }"`.

## GW-1 · Old messages stay honest · CRITICAL

**Check.** After the conversation has moved on, go back to a component in an
earlier message and use it: tap a chip, press a button, submit a form.
**Why.** Users scroll up and tap old buttons. An old control must either still
work (and say what it changed) or look and act disabled (`GC-7`, `TG-11`).
**Bug if.** An old control looks active but does nothing (`changed: false`),
or it silently changes state that later messages depend on.

## GW-2 · Controls are accessible to the agent and to people · HIGH

**Check.** Every control in the inventory has a role and a name. Sliders have
`role="slider"` with `aria-valuenow`, min and max, and move with arrow keys.
Use the suspects list: anything clickable without a role is a candidate.
**Why.** A control missing from the accessibility tree is invisible to screen
readers and to every testing agent, and usually not keyboard operable.
**Bug if.** A slider, chip or toggle has no role, no value or no keyboard
support.

## GW-3 · Regenerate keeps components alive · HIGH

**Check.** Press regenerate (or edit and resend) on a message with a
component, wait for the stream, then use the new component: move the slider,
press its buttons. Read the value before and after each move; compare with
the same move on the original component.
**Why.** Re-rendered components often lose their handlers or state.
**Bug if.** The regenerated component does not respond, shows the old value,
or the old one remains active next to it.

## GW-4 · Repeated submit is predictable · HIGH

**Check.** Submit a form inside a message twice, and send the same chat text
twice quickly.
**Why.** Double submits in chat create duplicate orders, emails or bookings.
**Bug if.** The second submit repeats the effect with no warning, or the form
stays editable after a final action without saying so.

## GW-5 · Free text and the components agree · MEDIUM

**Check.** Answer a component's question in free text instead of using the
component, then continue.
**Why.** Users type; the flow must accept it (`GC-11`).
**Bug if.** Free text is ignored, re-asks the same question, or leaves the
component in a state that contradicts the answer.

## GW-6 · Streaming is visible and interruptible · MEDIUM

**Check.** During a stream: is there a busy marker, a visible progress hint,
a stop control for long answers? After: does the input come back?
**Why.** Users need to know the assistant is working and how to stop it
(`GC-12`).
**Bug if.** No marker, no progress, input locked after the stream, or no stop
for long answers.

## GW-7 · Time to something useful · MEDIUM

**Check.** From `pc.py metrics`: time to first text and to the first
interactive component, per answer.
**Why.** A long blank wait before the first word feels broken; a component
that arrives long after the text gets missed.
**Bug if.** First text takes several seconds with no progress sign, or the
component only appears long after the text ends. Report the numbers and the
network profile.

## What not to judge here

Wording style, colours, motion and layout belong to visual skills. Report
them only when they block the task (hidden button, unreadable error).
