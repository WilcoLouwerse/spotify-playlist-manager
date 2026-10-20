# Learnings — playlist-config

Dated, atomic observations promoted from `learning-candidates.md` after they've been confirmed across 3+ runs or have fixed a measured eval failure.

---

## Patterns That Work

*(empty — populate after first runs)*

## Mistakes to Avoid

*(empty)*

## Domain Knowledge

- 2026-05-13: `list-playlists` (no flag) is a pure read of `playlists.json` — no Spotify call. `--all` is the only sub-command that hits the Spotify API.
- 2026-05-13: `list-playlists --all` filters server-side to playlists the user **owns or collaborates on**. Followed playlists never appear because they aren't writable via the Spotify API.
- 2026-10-20: Correction — the owner/collaborative filter is applied client-side in `list_all_spotify_playlists`, not by Spotify; Spotify returns followed playlists too.
- 2026-05-13: The untracked block in `--all` output uses **trailing commas** so users can paste a range straight into `"playlists"`. Skill must strip trailing commas when capturing the last entry of a paste.
- 2026-05-13: `load_config` validates that every `aliases` value, every `categories` entry, every `special_rules` key, and `catch_all.playlist` resolves to a key under `"playlists"`. Any dangling reference makes every CLI command refuse to run at startup. Promoted to SKILL.md guardrail.
- 2026-05-13: `playlists.json` is gitignored — never paste contents into chat in full, only names and counts. Promoted to SKILL.md guardrail.

## Open Questions

- Should the skill offer to rename a playlist key when the user renames it on Spotify (detected via ID match + name mismatch in `--all` output)?
- Should the skill flag playlists that disappeared from `--all` (i.e. tracked IDs no longer in the writable set — user deleted or un-shared a playlist)?

## Consolidated Principles

*(empty — populate after 3+ confirmations of a candidate)*
