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

**Rule.** At most ~6-8 buttons per message, at most 3 per row. The primary
action is first and alone on its row; rare actions go behind "More", which
edits the same message.
**Why.** Large keyboards bury the main action on small screens.
- Bad: 12 buttons in four rows of three.
- Good: "Select my items" alone on row 1, two secondary on row 2, "More" on row 3.

## TG-4 · Every tap is answered at once · HIGH

**Rule.** Each callback is acknowledged within ~1 s (a toast, a popup or an
edit). Popups and toasts hold short text only (about 200 characters) and
never buttons; any action goes on the message keyboard. Slow work shows a
processing state in the message, with Cancel when it takes more than a few
seconds.
**Why.** An unanswered tap leaves a spinner and users tap again.
- Bad: a tap leaves the button spinning for 10 s.
- Good: instant toast "Added" and the message updates.

## TG-5 · Groups work inside the group · CRITICAL

**Rule.** In a group, each process is one shared card (panel) that the bot
keeps editing. Anyone in the group can tap its inline buttons; the bot knows
who tapped, so personal choices (my items, I paid) happen right there, and
the personal answer (your share, what you picked) comes back as the popup
answer to that tap. Send someone to a DM only when the step cannot be done
in the group: a private fact (a card number), a Mini App with a long list,
or a user the bot must reach later. Do not post a new group message per
participant action.
**Why.** Every hop to a DM loses people; a stream of messages floods the
group. One card plus popups keeps the group quiet and the steps short.
- Bad: "Pick your items in private" deep link for every friend.
- Good: friend taps item buttons on the group card, popup "Your share: 4 200 ₸",
  card edits to "3 of 5 picked".

## TG-6 · Deep links carry the context · HIGH

**Rule.** When a DM or Mini App is needed (TG-5), the link uses a start
parameter that opens the exact object and action. A first-time user from
such a link lands in that task; language and welcome are inferred or shown
after (ON-5).
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

## TG-14 · One live card per process per chat · HIGH

**Rule.** A process has one current card in each chat where it appears
(the group panel, a DM copy). A state change edits every copy, so no chat
shows a stale state with live buttons.
**Why.** Two cards with different states make users act on the wrong one.
- Bad: the group shows "Paid" while the payer's DM still says "Waiting".
- Good: marking paid edits the group panel and the payer's DM card together.

## TG-15 · Never close what others still owe · CRITICAL

**Rule.** A timer, a new process or "Cancel" must not close or delete an
object that holds other people's unsettled shares. Warn the owner with the
choices on the message ("Remind", "Mark settled", "Keep open"), and keep the
data until someone decides.
**Why.** Silently lost debts cost real money and trust.
- Bad: an unpaid bill closes itself after 24 h; "Start new bill" cancels the old one.
- Good: "2 people still owe on the last bill · Remind · Keep both open".

## TG-16 · Limits keep the input · HIGH

**Rule.** When a quota, rate limit or plan limit blocks an action, keep what
the user sent (photo, text) and offer another path: wait with a reminder,
enter items by hand, upgrade. Never "try tomorrow" and drop the input.
**Why.** Re-sending is the step users skip; the input is the hard part.
- Bad: "Scan limit reached, try tomorrow." and the photo is gone.
- Good: "Scan limit reached · Type the items · Remind me tomorrow", photo kept.
