# Onboarding

The path from first contact to first value. Count it with FL-4; most products
lose most new users here.

## ON-1 · First value in the first session · CRITICAL

**Rule.** Define the first value moment (first split, first plan, first
preview clip, first booked lesson) and get a new user there in one session,
in the fewest steps. Write its steps-to-value number in the spec.
**Why.** Users who never reach value never come back to finish setup.
- Bad: sign-up, profile, tour, settings, then an empty dashboard.
- Good: send a photo → see the split, then optional setup.

## ON-2 · At most two questions before value · HIGH

**Rule.** Before the first result ask at most 1-2 questions, and only ones
that change that result. Everything else is collected later (ON-3) or
inferred (SR-1). Every needed question is asked before the result, not as a
follow-up right after it.
**Why.** A long intake feels like work before any reward; a question right
after "here is your result" means the result was premature.
- Bad: 4 screens of preferences, then the first reply asks skin type in text.
- Good: photo + skin type chips + main concern → first plan; budget asked
  when products are suggested.

## ON-3 · Build the profile progressively · HIGH

**Rule.** Ask further profile questions at the moment they improve a result
("To pick products, what's your budget?"), one at a time, skippable. Show
what the product remembers and let users edit or delete it.
**Why.** Questions with an obvious payoff get answered; visible memory builds
trust.

## ON-4 · Never start empty · HIGH

**Rule.** The first screen offers a concrete start: example content, a demo,
templates, or 2-4 starter actions. Sample data is labelled and removable.
**Why.** A blank canvas forces users to invent a task before they understand
the product.
- Bad: empty chat with a blinking cursor.
- Good: three starter chips based on what the product does best.

## ON-5 · Invited users skip generic onboarding · CRITICAL

**Rule.** A user arriving by invite, deep link or shared object lands in that
object with the one action expected of them. Generic onboarding is skipped or
shown after that action.
**Why.** They came to do one thing for someone else; extra steps make them
drop out and block the inviter (FL-7).
- Bad: participant from a join link must pick a language and read a welcome.
- Good: participant sees the bill and "Select your items".

## ON-6 · New and returning users have different doors · MEDIUM

**Rule.** "Sign in" and "Start" are separate entries; returning users land
where they left off (FL-6), new users go to the first-value path.
**Why.** Sending both through one door makes one of them take wrong steps.

## ON-7 · Teach in context, not with tours · MEDIUM

**Rule.** No multi-screen product tours. Explain a feature where and when it
is first needed: empty states, a one-line hint next to the control, an
example in the first reply.
**Why.** Tours are skipped and forgotten; contextual hints are read when
relevant.

## ON-8 · Permissions and accounts at the moment of need · HIGH

**Rule.** Ask for a permission (camera, notifications, contacts) or an
account only when the user triggers the feature that needs it, with a
one-line reason. If refused, offer the fallback path (type instead of photo).
**Why.** Upfront requests without context get denied and are hard to undo.

## ON-9 · Role and setup choices are inferred or deferred · HIGH

**Rule.** Infer the role from the entry (invite as student, link from a
teacher signup page). Ask once only if unknown, and allow changing it later.
Workspace setup (name, team, settings) is defaulted and editable later.
**Why.** A wrong irreversible role choice at sign-up locks users out of
their main task.

## Output

```
First value: <moment>   Steps now: N   Proposed: M
Before value: <questions asked, each with the result it changes>
After value: <questions deferred, with the moment they are asked>
Entries: new | returning | invited → <landing screen each>
```
