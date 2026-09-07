# Learnings — playlist-scan

Dated, atomic observations promoted from `learning-candidates.md` after they've been confirmed across 3+ runs or have fixed a measured eval failure.

---

## Patterns That Work

*(empty — populate after first runs)*

## Mistakes to Avoid

*(empty)*

## Domain Knowledge

- 2026-05-13: `scan-for` always asks the classifier for its **full top-5** matches per track (no `--max-playlists` flag) — the rationale is to give the target the best chance to appear. `--min-confidence` is the only tuning knob.
- 2026-05-13: Default `--min-confidence` is `80` (stricter than `smart-add`'s default of `0`). For a more lenient scan, suggest `60-75`; for a stricter scan, `90`.
- 2026-05-13: `scan-for`'s `target` argument accepts both canonical names (e.g. `"Drum & Bass"`) and aliases (e.g. `"dnb"`). The skill should render the canonical name in the planned command so the user can see what was resolved.
- 2026-05-13: `Random sht` is a valid playlist name in `playlists.json` (the catch-all), so the CLI accepts it as a target. But it's almost never what the user wants — confirm via AskUserQuestion first. Promoted to SKILL.md guardrail.

## Open Questions

- Does `scan-for` benefit from a "show the top-N closest near-misses" diagnostic mode for the user to see candidates that almost made the `--min-confidence` cutoff?
- Should the skill auto-suggest lowering `--min-confidence` when the candidate count is 0?

## Consolidated Principles

*(empty — populate after 3+ confirmations of a candidate)*
