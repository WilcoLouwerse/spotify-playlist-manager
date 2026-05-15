# Learnings — playlist-log-import

Dated, atomic observations promoted from `learning-candidates.md` after they've been confirmed across 3+ runs or have fixed a measured eval failure.

---

## Patterns That Work

- 2026-05-13: Explicitly stating "Geen vlaggen — log-import accepteert alleen <playlist> en <file>" in the response heads off the predictable user follow-up "kan ik een dry-run doen?". Eval-1 with_skill demonstrated this; the baseline omitted it.
- 2026-05-13: Mapping bare playlist name "House" to `exportify-exports/House.csv` (capital-H) via the no-space mangling rule produces the right path on the first try. Eval-1 with_skill picked the right case; the baseline guessed lowercase from the docs example.

## Mistakes to Avoid

- 2026-05-13: Don't render the command with bare `python` — the baseline did this and it fails the venv-routing assertion. Always `.venv/bin/python` from the repo root.
- 2026-05-13: Don't leave the file argument unquoted. The baseline rendered `... "House" exportify-exports/house.csv` (file unquoted) — fine for the literal example but breaks on `Drum_&_Bass.csv` (the `&` is a shell control char) and on any path with spaces. Always double-quote both positionals.

## Domain Knowledge

- 2026-05-13: `log-import` is the **only** mutating subcommand without a `--execute` flag — because it never calls Spotify, the dry-run/execute split doesn't apply. The skill's safety gate is the AskUserQuestion confirmation *before* running, not after. Promoted to SKILL.md guardrail.
- 2026-05-13: A non-zero `Unparseable lines` count is **normal** for Exportify CSVs — the header row ("Track URI,Track Name,Album Name,...") always parses as unparseable. Only flag this number if it's a large fraction of total lines (>5% suggests the file isn't a proper export).
- 2026-05-13: The CLI does **not** resolve bare playlist names to filenames the way `scan-for` / `review-playlist` / `bulk-playlist` do for their source argument. The skill must do that lookup itself against `exportify-exports/`.
- 2026-05-13: `log-import` only mutates `.tracks_log.json`. Recovery from a wrong-playlist seeding requires hand-editing that JSON file (the script has no "un-import" command). That's why the AskUserQuestion confirmation is non-negotiable.

## Open Questions

- Should the skill offer to run `wc -l` and a quick URI-pattern scan on the file before confirmation, so the user can see "this file has ~X URIs" up front? Trade-off: useful preview vs. extra Bash call before the real one.
- Should the skill detect when a file path looks like it might be a Spotify URL (e.g. user typo'd a URL into the file argument) and bail out early?

## Consolidated Principles

*(empty — populate after 3+ confirmations of a candidate)*
