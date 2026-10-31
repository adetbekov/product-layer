# Information architecture

Decides which sections exist, what lives where, and how the user gets there.
Rule format: rule, why, bad / good, impact. Impact: **CRITICAL** - users cannot
reach the result; **HIGH** - extra steps or confusion on a top task;
**MEDIUM** - friction on secondary tasks.

## Inventory first (5 questions)

Answer from the code or docs; ask the user only for what is missing.

1. Who uses it, and in which roles? (one line per role)
2. What are the 5-10 top tasks, ranked by frequency x importance?
3. Which objects does the user create, find or change? (bill, project, lesson)
4. How often is each task done: many times a day, weekly, once?
5. Where do users arrive from: home screen, link, notification, chat, search?

Write the answers as a table: task, role, frequency, object, entry point.
Every later decision cites this table.

## IA-1 · Top tasks within three actions · HIGH

**Rule.** Each top task is reachable in at most 3 actions from the place users
usually arrive. Tasks done several times a day are 1 action away (on the home
screen, in the chat, or as a persistent button).
**Why.** Depth hides frequent work; users stop doing what they cannot find.
- Bad: "Book a lesson" is Schedule → Calendar tab → find free slot → open.
- Good: the student home shows the next free slots with a book action.

## IA-2 · Navigation model follows section count · HIGH

**Rule.** Up to 5 top-level sections: flat tabs or bottom bar. 6-9: grouped
sidebar. More: a hub page plus search. Max depth 3 levels below a section;
deeper trees need search or breadcrumbs.
**Why.** Users scan 5 items at a glance; long flat menus turn into reading.
- Bad: 11 equal items in a bottom bar overflow menu.
- Good: 4 tabs (Chat, Plan, Shelf, Profile), settings inside Profile.

## IA-3 · One canonical home per object · HIGH

**Rule.** Every object type has exactly one page or place where it is fully
shown and edited. Other places show a summary that links there.
**Why.** Two full editors drift apart and users do not know which is true.
- Bad: a bill is editable both in the group panel and in the DM dashboard.
- Good: the DM dashboard is the bill's home; the group panel is a status
  summary with a "Join" link.

## IA-4 · Users' words, one term per concept · MEDIUM

**Rule.** Name sections and objects with words users say, and keep a glossary:
one term per concept, used the same in navigation, buttons and messages.
Never surface internal names (enum values, model terms, table names).
**Why.** Mismatched words make users doubt they are in the right place.
- Bad: "Segments", "Shots", "Assets" for what the user calls scenes.
- Good: glossary row "scene - one shot of the clip; never 'segment' in UI".

## IA-5 · One primary action per screen · HIGH

**Rule.** Each screen or message has one primary action (emphasis 1), at most
two secondary ones, everything else behind "More". Content is ranked: one
primary block, then supporting blocks in order of the task.
**Why.** Equal-weight options slow every decision and hide the next step.
- Bad: a dashboard with six buttons of the same rank.
- Good: "Select my items" rank 1; Share, Details rank 2; Remind, Refresh under
  More.

## IA-6 · Place by lifetime and frequency (inline / overlay / page) · CRITICAL

**Rule.** Decide where content lives with this order:
1. Edits one value in the current context, or answers in under ~10 seconds →
   **inline** (in the list, card or chat message).
2. Short task that must return to the current context (confirm, pick, quick
   form under ~5 fields) → **overlay** (sheet, dialog, popover).
3. Has its own lifetime: saved, revisited, shared, linked, has several tasks,
   or long form → **page** with its own address.
4. Used many times a day → move it one level closer than the rule above says
   (a frequent full-page form becomes inline or an overlay).
**Why.** Wrong placement either buries saved things in transient views or
breaks context for a quick edit.
- Bad: a care routine the user follows daily exists only as a chat message.
- Good: routine is a Plan page; chat shows a card linking to it.

## IA-7 · Browse tree plus filters, search at scale · MEDIUM

**Rule.** One category tree for browsing (each item in one place). Shared
attributes are filters or tags, not more categories. Add search once a
collection passes ~50 items or users usually know the name they want.
**Why.** Items in several branches get lost; deep trees replace search badly.
- Bad: products filed under both "Acne" and "Serums" categories.
- Good: category = product type; concern = filter.

## IA-8 · Every page answers three questions · MEDIUM

**Rule.** A page spec states: where am I (title / location), what can I do
here (primary action), where can I go next (exits). If one is missing, the
page is unfinished.
**Why.** These are the first things users look for on arrival.
- Bad: a confirmation screen with only "OK" that returns to home.
- Good: "Booking confirmed" with "Add to calendar" and "Open lesson room".

## IA-9 · Return to the next likely task, not home · HIGH

**Rule.** After finishing a task, land the user where the next likely task
starts (the created object, the next step, the list it belongs to).
**Why.** Dropping users on home makes them navigate back to continue.
- Bad: after publishing a clip, redirect to the projects list.
- Good: stay on the clip page with share actions.

## Output: page map

```
Section (role: all | teacher | ...)       primary action    depth
├─ Page / object home                       ...               1
│  └─ Sub-page                              ...               2
Placement decisions: <object> → inline | overlay | page (IA-6 reason)
Glossary: term - meaning - never call it
```
