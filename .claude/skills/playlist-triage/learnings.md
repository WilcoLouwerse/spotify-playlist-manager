# Learnings — playlist-triage

Dated, atomic observations promoted from `learning-candidates.md` after they've been confirmed across 3+ analyses or have fixed a measured eval failure.

---

## Patterns That Work

*(empty — populate after first runs)*

## Mistakes to Avoid

*(empty)*

## Domain Knowledge

- 2026-05-13: `review-playlist` per-track prompts are `[y/N/s/q]` where `y` accepts ALL suggested playlists for the track at once — there is no per-playlist control. For per-playlist control on a single track, route the user to `playlist-match` / `smart-add` instead.
- 2026-05-13: `bulk-playlist`'s single `y/N` may be auto-accepted via `yes | ...`. `review-playlist`'s per-track prompts must NOT be auto-accepted — that defeats the curation purpose. Promoted to SKILL.md guardrail.
- 2026-05-13: Both commands default to `--max-playlists 3 --min-confidence 80`. The skill should preserve defaults unless the user explicitly asks to tighten / loosen.
- 2026-05-13: Source argument accepts three forms in one slot: Spotify URL/URI/ID, CSV path, or bare name (resolved against `exportify-exports/`). No separate `--source` flag — pass it as the positional argument.

## Open Questions

- Should the skill detect "tracks already classified previously" via `.adds_log.json` and warn the user before running execute? The CLI's duplicate guard handles it, but a heads-up might be useful.
- For execute mode, should the skill open a new terminal window instead of asking the user to copy-paste the command?

## Consolidated Principles

*(empty — populate after 3+ confirmations of a candidate)*
