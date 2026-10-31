# Module: SaaS with roles and marketplace

For web apps with several roles (owner, teacher, student, admin), nested
workspaces or content trees, and two-sided marketplaces. Use with the core
files; rule format as in core.

## Role matrix

Start from a table, then derive navigation from it:

| Object | Role A | Role B | Role C |
|---|---|---|---|
| Lesson | create, edit, start | view, join | - |

Actions: view / create / edit / approve / delete / share / pay.

## RL-1 · Navigation is derived from the role matrix · HIGH

**Rule.** All roles share one IA skeleton; each role sees only sections with
at least one action for them. Hidden, not disabled. Labels are the same for
everyone (IA-4).
**Why.** Disabled sections are noise; different skeletons per role break
shared links and support.

## RL-2 · Each role has its own home · HIGH

**Rule.** The landing page per role shows that role's top tasks (IA-1) and its
next item (next lesson, pending review, unpaid booking).
**Why.** A shared generic dashboard makes every role hunt for its work.

## RL-3 · Role from context, changeable later · HIGH

**Rule.** Infer the role from the entry (invite, landing page, marketplace
side); ask once only when unknown; allow switching or holding several roles
(a teacher may also be a student) without a new account (ON-9).
**Why.** An irreversible role pick at sign-up locks users out of half the
product.

## RL-4 · Create, invite, land: the core loop · CRITICAL

**Rule.** For every shared object (class, project, workspace) spec the loop:
creator creates → invites (link, email, code) → invitee lands inside the
object with one action (ON-5) → creator sees who joined. Count steps for
both sides.
**Why.** Multi-user products grow only if this loop is short; without it the
product is single-player.

## RL-5 · Empty states differ by role · HIGH

**Rule.** A new owner sees "create your first X" and a template; a new member
sees "nothing shared with you yet, ask your teacher" with an action. Seed or
demo data is labelled and removable (ON-4).
**Why.** One empty state cannot serve both creators and receivers.

## RL-6 · Permission errors say who can help · MEDIUM

**Rule.** When an action is not allowed, say why and who can grant it, with a
request button where possible. Never show a generic 403.
**Why.** Users cannot fix permissions they cannot see.

## RL-7 · Deep trees get location and search · MEDIUM

**Rule.** Nested pages (docs, courses, channels) show where the user is
(breadcrumb or parent link), open at the last visited place, and are
searchable. Beyond 3 levels, prefer search and recents over browsing (IA-2).
**Why.** Users get lost in nested trees and stop opening them.

## RL-8 · Marketplace buyer path is counted end to end · CRITICAL

**Rule.** Spec the buyer path: find (search, categories, filters) → compare
(list with the attributes that decide) → profile (offer, proof: reviews,
credentials, samples) → book / buy → pay → confirm → follow-up (reminder,
room link, receipt). Count steps; each stage has its states.
**Why.** Drop-off compounds per stage; a missing stage (no reminder, no room
link) loses the sale after payment.

## RL-9 · Marketplace seller path reaches the first listing fast · HIGH

**Rule.** A new seller publishes a usable first listing in one session with
defaults (price suggestions, slot templates), and sees what buyers will see
before publishing. Verification can follow, labelled as pending.
**Why.** An empty marketplace has no buyers; a slow seller setup keeps it
empty.

## RL-10 · Trust signals are content requirements · MEDIUM

**Rule.** Spec which facts build trust at each buyer step (reviews count,
response time, refund rule, verified badge) as content blocks with ranks.
How they look is the visual skill's job.
**Why.** Trust facts decide purchases; leaving them to visuals leaves them
out.

## RL-11 · Bookings connect to what happens next · HIGH

**Rule.** A confirmed booking carries: when, where (room link), how to prepare,
reschedule / cancel rules, and a calendar add. Both sides get a reminder
before start, and the room is one tap from the reminder.
**Why.** "Booking confirmed" with nothing after is a dead end (FL-2).

## RL-12 · Team onboarding splits the first admin from members · MEDIUM

**Rule.** The first user sets up only what blocks inviting (name, one
setting); everything else is defaulted. Members who join skip setup and land
in shared content.
**Why.** Members should not repeat or even see the admin's setup.
