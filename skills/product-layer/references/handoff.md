# Handoff contract with visual skills

product-layer decides **what** and **where**. Visual, taste and motion skills
decide **how it looks and moves**. This file is the contract between them.
It was checked against three real visual skills: an Apple-style interaction
and motion skill (for example `apple-design`), an anti-slop taste skill for
landing pages and redesigns (for example `design-taste-frontend`), and a
motion audit skill that works on existing code (for example
`improve-animations`).

## Who owns what

| Decision | product-layer | visual / motion skills |
|---|---|---|
| Sections, pages, navigation model | owns | style the chosen model |
| Flow steps, their order and count | owns | must not add or remove steps |
| Which blocks a screen or reply has, and their rank | owns | lay them out to express the rank |
| Primary / secondary / destructive action | owns | make the ranks visibly distinct |
| States and what each must say | owns | style each state |
| Copy intent (what a message must convey) | owns | may tighten wording, keep the meaning |
| Facts for the visual brief (audience, assets, constraints) | collects and passes on | infer the design direction from them |
| Colour, type, spacing, grid, icons, imagery | never | owns |
| Animation, transitions, durations, easing | names the state change, trigger, frequency | owns |
| Platform components (sheet vs dialog look) | names placement: inline / overlay / page | picks the platform-native form |

If a visual skill needs a structural change (for example, a layout cannot hold
three rank-2 actions), it reports it back instead of changing the spec
silently.

## Which visual skill gets the spec

| Product or surface | Visual skill to call | Why |
|---|---|---|
| Landing page, marketing site, portfolio, redesign of a site | taste skill | built for these; it excludes dashboards and multi-step product UI |
| In-app screens: overlays, sheets, drag, swipe, transitions, materials | Apple-style skill | gestures, interruptible motion, depth, typography |
| AI chat with blocks (genui) | Apple-style skill | card appearance, streaming, sheets from chat |
| AI pipeline web app | Apple-style skill | progress, stage transitions, gate overlays |
| SaaS with roles | Apple-style skill for the app; taste skill for the public landing | two different surfaces |
| Telegram bot without a Mini App | none | the spec is final: message text, keyboards, edit vs new |
| Telegram Mini App | Apple-style skill | web view with touch gestures |
| Existing code with animations | motion audit skill, after the build | it reads code only and plans fixes; it does not design from a spec |

## Spec format

One markdown document. Sections in this order; omit ones that do not apply.

```
# Product spec: <product / feature>
Goal: <who, what result, how we know it worked>
Type: <web app | chat genui | telegram bot | ai pipeline | saas roles>
Modules used: <...>

## Visual brief context                    - facts only, never style choices
Surface: <landing | portfolio | redesign | in-app screens | mini app>
Audience: <who looks at it and in what situation>
Stage: <new product | redesign - keep look | redesign - overhaul>
Brand assets: <links or paths: logo, existing tokens / design system,
               screenshots, live URL; "none">
References: <products or URLs the user named, vibe words the user used;
             "none given" - never invent them>
Quiet constraints: <accessibility-critical, regulated, kids, trust-first,
                    low-end devices, languages / scripts>
Platform: <web desktop / mobile web / iOS / Android / Telegram>

## Top tasks
| Task | Role | Frequency | Entry | Steps now → proposed |

## IA (page map, placement decisions, glossary)        - ia.md output

## Flows                                               - flows.md output
<one flow block per top task, with branches and steps to value>

## Screens / messages
<one screen spec per screen, card type or bot message>  - states.md template

## Transitions
| From | To | Meaning | Trigger | Interruptible | Frequency |

## Steps to value
| Flow | Actor | Now | Proposed | Rules applied |

## Assumptions and open questions
```

### Transitions table

The motion skills decide how a change animates (or whether it should) from
three facts the spec owns:

- **Trigger:** `tap`, `drag`, `swipe`, `sheet dismiss`, `scroll`, `keyboard`,
  `system` (data arrived, timer, push). Gestures matter: drags and swipes need
  1:1 tracking and velocity handoff; system events do not.
- **Interruptible:** `yes` if the user can reverse it mid-way (grab a closing
  sheet, swipe back), `no` if it is a one-way commit.
- **Frequency:** `100+/day`, `daily`, `occasional`, `rare` (first run only).
  High-frequency and keyboard actions should feel instant; rare moments may
  carry more motion.

Example row: `processing | receipt card | same object, new state | system |
no | daily`.

## Handing off

1. **Send a concrete request, not just the skill.** A visual skill called
   without a task may only greet and wait. Pass the request plus the spec:
   "Design the in-app interaction for the screens in this spec: booking
   sheet, confirmation, room entry. Keep the steps and ranks."
2. **Taste skill:** the visual brief context answers its brief-inference
   questions (surface, audience, references, assets, constraints), so it
   should not need to ask or guess. If a fact is unknown, write "unknown"
   rather than filling it in.
3. **Apple-style skill:** point it at the transitions table and the overlays
   (sheets, dialogs) in the IA placement decisions.
4. **Motion audit skill:** call it on the repository after the screens are
   built; pass the transitions table as its frequency map.
5. **Telegram bot without Mini App:** no visual handoff; the spec goes to the
   developer as is.

## Component vocabulary (by meaning)

Use these names in specs. Visual skills map them to real components.

- **action** - `primary` (one per screen), `secondary`, `destructive`, `link`.
- **choice** - `single` (chips / segmented / radio), `multi` (chips /
  checklist), `range` (slider / stepper with bounds).
- **input** - `text`, `number`, `date`, `photo`, `voice`, `file`, `search`.
- **content** - `card` (one object), `card-list` (2-8 alternatives), `table`
  (compare attributes), `steps` (ordered process), `list` (many items),
  `detail` (one object in full), `media`, `summary` (compact link to a page).
- **status** - `progress` (stages, items n of N), `pending`, `badge`
  (state of an object), `notice` with level `info | warning | error |
  success`, `toast` (minor success with optional undo).
- **navigation** - `tabs`, `sidebar`, `breadcrumb`, `back`, `more` (hidden
  secondary actions).
- **placement** - `inline`, `overlay`, `page`, `dm` / `group` (Telegram),
  `chat-block` (genui).

## Emphasis

Rank, not size: `1` is the one thing the eye should land on, `2` supports it,
`3` is reference detail. One rank-1 item per screen. Visual skills decide how
rank is expressed.

## Forbidden in a spec

- Colour names or values, font names, sizes, weights.
- Pixel, rem or grid values, spacing, radius, shadows.
- Animation durations, easing, spring parameters.
- Icon choices, illustration style, a chosen aesthetic or vibe the user did
  not state.

Allowed instead: rank, placement, component by meaning, state change with
trigger and frequency, links to existing brand assets.

## Example (fragment)

```
Screen: receipt card (bot message, DM)     Object: bill
Purpose: payer checks parsed items and shares the bill
Entry: photo sent     Exits: dashboard (edit in place), cancel
Primary action: Share with group (action.primary)
Secondary: Fix items, Change currency     More: Retake, Cancel
Content (ranked):
  1. total and currency - content.summary - rank 1
  2. item list with prices - content.list - rank 2
  3. unclear items marked - status.badge - rank 2 (only in partial state)
States: loading = progress "Reading the receipt" + Cancel;
        partial = unclear items flagged, primary becomes "Check 2 items";
        error = notice.error + Retake / Type items
Transitions: processing → receipt card | system | no | daily
Visual handoff: none (Telegram bot without Mini App)
```
