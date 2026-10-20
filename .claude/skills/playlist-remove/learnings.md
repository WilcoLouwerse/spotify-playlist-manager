# Learnings — playlist-remove

Dated, atomic observations promoted from `learning-candidates.md` after they've been confirmed across 3+ runs or have fixed a measured eval failure.

---

## Patterns That Work

- 2026-05-15: Always ask for a Spotify URL/URI/ID before running any command — "Artist - Title" alone cannot drive the CLI `remove` command. Catching this early (step 2) avoids a failed run later.

## Mistakes to Avoid

- 2026-05-15: Do not **run** the command without explicit **AskUserQuestion** confirmation first. Even though `--execute` is always included, the confirmation prompt is the single safety gate. Skipping it means the user has no chance to cancel.

## Domain Knowledge

- 2026-05-15: `SKIP: track not found in playlist` does NOT mean the track isn't there — it means it's not in `.tracks_log.json` and the Spotify API (in dev mode) can't confirm it either. The track was probably added through the Spotify UI. This SKIP is confusing for users; explain it clearly in Dutch. ⚠️ superseded 2026-10-20 — see next line
- 2026-10-20: `SKIP: track not found in playlist` now means Spotify's live contents don't contain that URI (often a remaster or single with a different URI). Only when the run also printed `WARN: Spotify returned playlist entries without track URIs` did the check fall back to `.tracks_log.json`.
- 2026-05-15: After a successful removal, `remove_from_log` clears the URI from `.tracks_log.json`. This is important: a future `add` for the same track will no longer see it as a duplicate and can add it back cleanly.
- 2026-05-15: `Random sht` is the script-side catch-all. Users almost never intend to remove from it directly — when they say "verwijder X", they mean from the specific genre playlist where it was mis-sorted. Always confirm before removing from `Random sht`.

## Open Questions

- Should the skill offer a "also add to a different playlist?" flow immediately after a successful removal, or wait for the user to ask? Current design: offer it in the step-8 follow-up AskUserQuestion.

## Consolidated Principles

*(empty — populate after 3+ confirmations of a candidate)*
