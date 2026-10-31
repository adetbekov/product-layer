# Handoff contract with visual skills

product-layer decides **what** and **where**. Visual, taste and motion skills
decide **how it looks and moves**. This file is the contract between them.

Status: draft, written from general principles. To be checked against the
actual visual skills it feeds (Apple-style design, taste, animation).

## Who owns what

| Decision | product-layer | visual / motion skills |
|---|---|---|
| Sections, pages, navigation model | owns | style the chosen model |
| Flow steps, their order and count | owns | must not add or remove steps |
| Which blocks a screen or reply has, and their rank | owns | lay them out to express the rank |
| Primary / secondary / destructive action | owns | make the ranks visibly distinct |
| States and what each must say | owns | style each state |
| Copy intent (what a message must convey) | owns | may tighten wording, keep the meaning |
| Colour, type, spacing, grid, icons, imagery | never | owns |
| Animation, transitions, durations, easing | names the state change only | owns |
| Platform components (sheet vs dialog look) | names placement: inline / overlay / page | picks the platform-native form |

If a visual skill needs a structural change (for example, a layout cannot hold
three rank-2 actions), it reports it back instead of changing the spec
silently.

## Spec format

One markdown document. Sections in this order; omit ones that do not apply.

```
# Product spec: <product / feature>
Goal: <who, what result, how we know it worked>
Type: <web app | chat genui | telegram bot | ai pipeline | saas roles>
Modules used: <...>

## Top tasks
| Task | Role | Frequency | Entry | Steps now → proposed |

## IA (page map, placement decisions, glossary)        - ia.md output

## Flows                                               - flows.md output
<one flow block per top task, with branches and steps to value>

## Screens / messages
<one screen spec per screen, card type or bot message>  - states.md template

## Transitions
| From state | To state | Meaning | Trigger |
e.g. processing → result | same object, new state | parse finished

## Steps to value
| Flow | Actor | Now | Proposed | Rules applied |

## Assumptions and open questions
```

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
- Icon choices, illustration style, brand tone of visuals.

Allowed instead: rank, placement, component by meaning, state change name.

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
Transitions: processing → receipt card (edit in place)
```
