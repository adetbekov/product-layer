## Spec format

Write the spec to `spec/flow.yaml` (YAML, UTF-8). It describes what each screen or message shows and where the user
goes next. It does not describe the visual layer (colors, fonts, spacing, motion); a later visual pass handles that.
Prose notes may go to `spec/notes.md`. Nothing outside `spec/` is needed.

```yaml
product: Short product name
flows:                        # one entry per flow the request names, with the ids it gives
  - id: main                  # flow id from the request
    entry: home               # screen where the flow starts
    done: result              # screen where the user has what they came for
nav:                          # optional: top-level navigation per role (section labels)
  member: [Home, Settings]
screens:
  - id: home                  # unique, kebab-case
    surface: page             # page | modal | sheet | chat-message | bot-message | notification | ...
    moment: home              # optional: a moment id from the request, when the request lists them
    purpose: One line on why this screen exists
    shows: [what the user sees here]
    asks:                     # inputs the user has to give on this screen; omit when none
      - field: email          # what is asked
        why: why the product cannot know it
    render: text              # chat-message / bot-message only: text | block
    block: choice             # when render is block: card | cards | choice | form | slider | table | steps | ...
    states:                   # what this screen shows in each state; omit a key when it cannot happen
      empty: ...
      loading: ...
      error: ...              # include the way out (retry, edit, contact)
    actions:                  # every way out of this screen
      - label: Continue
        to: result            # id of the next screen
        by: user              # user (a tap, a message, a submit) | system (it happens by itself); default user
```

Rules the spec must follow:

- Every `to` names a screen in `screens`; every screen is reachable from some flow's `entry`.
- A step is one `by: user` action; `by: system` transitions (a job finishing, a timer) cost the user nothing.
- Each screen that can be waited on, fail or have nothing to show describes that state in `states`.
