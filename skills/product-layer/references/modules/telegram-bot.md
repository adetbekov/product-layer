# Module: Telegram bot

For bots in private and group chats, with inline keyboards and optional Mini
Apps. Use with the core files; rule format as in core.

## Message map

Before rules, list every message the bot sends, as a table:

| Message | Chat (DM / group) | Sent new or edited | Buttons | Next message |
|---|---|---|---|---|

Treat a message as a screen: it needs a purpose, a primary action and states
(`states.md`).

## TG-1 · Edit for progress, send new for news · CRITICAL

**Rule.** One live message per process: status changes of the same object
(processing → result → dashboard) edit that message in place. Send a new
message when someone must notice (edits do not notify), when the content is
a new object, or when the old message has scrolled far up.
**Why.** New messages for every state spam the chat; edits for news go
unseen.
- Bad: "Processing", "Parsed", "Dashboard" as three separate messages.
- Good: one message moves through the three states; the final bill goes to
  each participant as a new DM.

## TG-2 · Buttons over commands · HIGH

**Rule.** Every action a user takes in a normal flow is an inline button.
Commands exist for power users and as entry points (`/start`, `/help`),
never as the only way. Typed input only for facts that are not choices.
**Why.** Users do not remember commands; a button is one tap.
- Bad: "Send /split to start, /done when finished".
- Good: buttons "Split this receipt" and "Done" under the message.

## TG-3 · Small keyboards, primary first · HIGH

**Rule.** At most ~6-8 buttons per message, at most 3 per row (1-2 when labels
are long). The primary action is first and alone on its row; rare actions go
behind "More", which edits the same message.
**Why.** Large keyboards bury the main action on small screens.
- Bad: 12 buttons in four rows of three.
- Good: "Select my items" alone on row 1, two secondary on row 2, "More" on row 3.

## TG-4 · Every tap is answered at once · HIGH

**Rule.** Each callback is acknowledged within ~1 s (a toast or an edit). Slow
work shows a processing state in the message, with Cancel when it takes more
than a few seconds.
**Why.** An unanswered tap leaves a spinner and users tap again.
- Bad: a tap leaves the button spinning for 10 s.
- Good: instant toast "Added" and the message updates.

## TG-5 · Group = shared status, DM = personal action · CRITICAL

**Rule.** In a group, post one short shared message per object (a panel) and
keep editing it; personal choices, payments and private data happen in DM or
a Mini App, reached by a deep-link button from the panel. Do not post a new
group message per participant action.
**Why.** Groups tolerate little bot noise; personal steps in public are
awkward and spammy.
- Bad: each participant's choice is a new message in the group.
- Good: one group panel edited to "3 of 5 chose items"; choices made in DM.

## TG-6 · Deep links carry the context · HIGH

**Rule.** Links to the bot use a start parameter that opens the exact object
and action. A first-time user from such a link lands in that task; language
and welcome are inferred or shown after (ON-5).
**Why.** Every extra screen between a link and the task loses invitees.
- Bad: an invite link opens `/start` with the generic welcome.
- Good: `/start join_<id>` opens that bill with "Select your items".

## TG-7 · Handle the user the bot cannot reach · CRITICAL

**Rule.** A bot cannot message a user who has never started it. When such a
user acts in a group, reply in the group with a deep-link button that starts
the bot and resumes the action. Never ignore the action silently.
**Why.** Silent ignores are dead ends for exactly the new users you need.
- Bad: a photo from a user who never started the bot is ignored.
- Good: group reply "Tap to continue in private" with a deep link to that receipt.

## TG-8 · Infer language and locale · MEDIUM

**Rule.** Use the client's reported language for the first reply; offer a
change in settings, not as a first-run question (SR-1).
**Why.** Asking costs every new user a tap the platform already answered.
- Bad: "Choose language: RU / KZ / EN" as the first message.
- Good: first reply in the client's language; language switch in settings.

## TG-9 · Mini App only when chat is the wrong shape · MEDIUM

**Rule.** Use a Mini App for: picking from long lists (over ~10 items with
quantities), rich forms, maps, comparisons, drag. Keep it inline otherwise.
Note that Mini App buttons in groups have limits; route group users through
a DM link.
**Why.** A Mini App costs a context switch; inline buttons cost none.
- Bad: a Mini App opened to pick one of three options.
- Good: inline buttons for 3 options; a Mini App for a 25-item receipt.

## TG-10 · Long lists paginate inside the message · MEDIUM

**Rule.** Lists longer than a keyboard paginate with prev / next that edit the
message, keep the selection, and show "page 2 of 4". State lives on the
server; callback data only holds a short key (Telegram limits it to 64 bytes).
**Why.** Huge keyboards and lost selections break item picking.
- Bad: 40 items as one giant keyboard.
- Good: 8 items per page, "‹ 2/5 ›", selection kept across pages.

## TG-11 · Old buttons stay safe · HIGH

**Rule.** Buttons on old messages act on current state or answer "This bill is
already closed" and point to the current message. Closed objects edit their
messages to remove obsolete buttons.
**Why.** Chats keep history; users tap old buttons.
- Bad: an old "Finalize" button finalizes a bill again.
- Good: "This bill is already closed" with a link to the current panel.

## TG-12 · Text and voice as fallback · MEDIUM

**Rule.** Where users may need to correct or explain (parse errors, special
cases), accept free text or voice and map it to the action.
**Why.** Buttons cover the expected path; free input covers the rest.
- Bad: "Use the buttons" in reply to "the water was 500, not 700".
- Good: the bot fixes the item from text or voice and shows the new card.

## TG-13 · Show each participant their running state · HIGH

**Rule.** In shared processes every participant sees their current share or
status as it changes, not only at the end; the organiser sees who is pending
and has ways around them (FL-7).
**Why.** Waiting blind is the main reason participants drop out.
- Bad: participants see their total only after the payer finalizes.
- Good: "Your share so far: 4 200 ₸" updates as they pick.
