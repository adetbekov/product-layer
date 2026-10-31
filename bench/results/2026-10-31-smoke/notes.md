# Smoke run, 2026-10-31

Purpose: prove the pipeline end to end (prepare -> sessions -> record -> hidden check -> blind review -> report), not
to rank skills. One case (`generic-settings`), one repeat, two arms: `bare` and `product-layer` pointing at
`bench/arms/stub/product-layer` because `skills/product-layer` does not exist yet (JEB-2030). The stub's result says
nothing about the real skill.

- Driver: agent-driven (no `claude -p` auth on the runner); each session ran in a fresh Sonnet 5.5 subagent, each
  blind verdict in a fresh Fable 5.1 subagent, both orders.
- Tokens: 58.7k for the two sessions, 66.8k for the two verdicts.
- Hidden checks: stub 1/1, `bare` 0/1 (`dead_ends`: its `deleted` screen's only action loops onto itself). The
  blind review prefers `bare` in both orders anyway (more complete export and delete paths; the stub arm left two
  settings rows without screens), and both judges flagged the same self-loop.
- Two check fixes came from this run, both applied with `recheck`, no session rerun: a moment may span several
  screens (export start, building, ready), so `states` and `min_actions` look at the moment as a whole (before, `bare`
  failed on `export-ready lacks loading`); a screen whose every action leads back to itself is now a dead end.
