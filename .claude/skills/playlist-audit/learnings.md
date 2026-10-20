# Learnings — playlist-audit

Dated, atomic observations promoted from `learning-candidates.md` after they've been confirmed across 3+ runs or have fixed a measured eval failure.

---

## Patterns That Work

- 2026-05-15: For mood playlists (Happy tunes, Sad tunes), lyrical sentiment from web sources is a far stronger signal than genre match alone. A pop track can score 90% on a mood playlist even if its genre doesn't match any other playlist.
- 2026-05-15: Always show the URI in the audit report alongside the track name — the `remove` command needs it and fetching it again mid-flow breaks the conversation rhythm.

## Mistakes to Avoid

- 2026-05-15: Do not skip the mandatory AskUserQuestion confirmation before running `remove --execute`, even when the user said "verwijder alles onder 60%" in an earlier turn. The confirmation in step 9 is always required.
- 2026-05-15: Do not fabricate a confidence score when web sources return nothing. Mark the track as "geen data" and exclude it from candidates — a 0% score would incorrectly flag it for removal.

## Domain Knowledge

- 2026-05-15: `list-tracks` returns an empty result in Spotify Developer Mode. This is the most common failure point — always check the output for emptiness and offer the exportify CSV fallback before proceeding.
- ⚠️ contradicted 2026-10-20: the empty result came from Spotify's Feb 2026 `track`→`item` rename, now handled by the CLI. `list-tracks` reads every playlist in `playlists.json` live; the CSV fallback is only for playlists Spotify can't read (owned by someone else).
- 2026-05-15: `audit-playlist` (OpenAI quick mode) classifies against ALL playlists and then shows the score for the target. When the target doesn't appear in the top-10 results, the score is 0%. This is a real signal — but set `max_playlists=10` to give the target the best chance.
- 2026-05-15: The `Electronic Music` playlist is an umbrella — tracks should score high there if they score high on any electronic subgenre. Don't penalise a House track for also matching Electronic Music.
- 2026-05-15: Theme playlists (Funny meme, Ket420, Hooyah) have `special_rules` in `playlists.json`. These rules override generic genre matching — a track doesn't need to match a genre, it needs to match the theme context. Always read `special_rules` before scoring theme playlists.

## Open Questions

- For web-first mode on large playlists (>20 tracks), should the skill offer a "batch" option that classifies in groups of 5 rather than individually? Would save some web round-trips.
- Should the audit show ⚠️ tracks (60-79%) in the removal candidates list by default, or keep the default threshold at 60%?

## Consolidated Principles

*(empty — populate after 3+ confirmations of a candidate)*
