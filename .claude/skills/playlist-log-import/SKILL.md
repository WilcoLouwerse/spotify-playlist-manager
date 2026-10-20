---
name: playlist-log-import
description: Seeds the local fallback duplicate log (.tracks_log.json) with a playlist's exportify CSV via the project's log-import CLI command — fires on 'seed mijn log voor House', 'import House export', 'log-import', or 'House CSV importeren'.
metadata:
  category: Workflow
  tags: [spotify, log-import, duplicate-guard, exportify, dutch]
---

# Playlist Log-Import

Wraps the project's local-log seeding workflow: parse a Spotify export file (Exportify CSV, text, or JSON), pull every track URI/URL/ID out of it, and record those URIs against one target playlist in `.tracks_log.json`.

The duplicate guard (used by `add`, `smart-add`, `review-playlist`, `bulk-playlist`, `scan-for`) reads each playlist's live contents from Spotify. `.tracks_log.json` is only its **fallback**, consulted when Spotify hides a playlist's contents (the CLI then prints `WARN: Spotify returned playlist entries without track URIs`). So this skill is rarely needed: when the user asks for it, run it, but mention in Dutch that the guard already sees tracks added in the Spotify app and that seeding only completes the fallback. See [`docs/architecture.md → Duplicate detection`](../../../docs/architecture.md#duplicate-detection).

This is a **local-only** operation — no Spotify API call is made, no `--execute` flag exists, and the command always runs to completion the moment it's invoked. The skill's safety gate is the AskUserQuestion confirmation **before** running, not after.

Different shape from [playlist-scan](../playlist-scan/SKILL.md) and [playlist-triage](../playlist-triage/SKILL.md):

| | playlist-triage / playlist-scan | **playlist-log-import** |
|--|--|--|
| Effect | Writes to Spotify | Writes only to local `.tracks_log.json` |
| Dry-run | Yes (default) | N/A — no Spotify side-effect |
| y/N prompt | Yes (per-track or single) | None — runs to completion |
| Source | Spotify URL/URI/ID or CSV | File path only (CSV/text/JSON) |
| Use case | Sort tracks into playlists | Complete the duplicate guard's fallback log |

User-facing prose is **Dutch**. Keep SKILL.md, references, templates, and examples in English.

**Input**: A target playlist name + a file path (typically a CSV under `exportify-exports/`). Also fires on phrases like "seed mijn House log", "log-import van House CSV", "import deze export voor Techno", "registreer mijn House export".

**Source of truth**: [`docs/commands.md → log-import`](../../../docs/commands.md#log-import) for CLI behaviour. [`playlists.json`](../../../playlists.json) for valid target names. [`exportify-exports/`](../../../exportify-exports/) for export files by convention.

---

## Steps

1. **Detect intent**

   The message references a target playlist + an export file. Common shapes:
   - "seed mijn log voor [TARGET]"
   - "import [TARGET] export"
   - "log-import [TARGET] [FILE]"
   - "registreer [FILE] als [TARGET]"
   - "[TARGET] CSV importeren"

   If either the target or the file is missing, ask via **AskUserQuestion**. Don't guess the file from the target name alone — the user may have a non-standard filename.

2. **Resolve the target**

   Read [`playlists.json`](../../../playlists.json). The target must match a key under `"playlists"` or an entry under `"aliases"`. Case-insensitive. If the user typed a name that maps to multiple plausible playlists, ask via **AskUserQuestion**.

   Render the **canonical name** in the planned command (not the alias), so the user can see exactly which playlist's log will be touched.

3. **Resolve the file**

   Follow `references/file-resolution.md`. Accept absolute paths, relative paths, and bare names that should resolve against `exportify-exports/`. Verify the file exists before invoking the CLI — if it doesn't, ask via **AskUserQuestion** to correct the path. Never invent a filename.

4. **Confirm target + file**

   This is the **only** safety gate. Use **AskUserQuestion** with the resolved target + file path + (if cheap to read) the line count, so the user can sanity-check before the local log is mutated.

   - **Ja, importeer** — proceed to step 5.
   - **Nee, andere target/file** — re-resolve.
   - **Annuleren** — end the flow.

5. **Render the planned command**

   Use `templates/plan.md`. One command, from the repo root:

   ```bash
   .venv/bin/python playlist_manager.py log-import "<TARGET>" "<FILE>"
   ```

   Quote both `<TARGET>` (canonical name from `playlists.json`) and `<FILE>` (full resolved path). There are no flags — no `--execute`, no `--min-confidence`, no `--max-playlists`. If the user proposes any flag, refuse and explain that `log-import` takes only two positionals.

6. **Run and surface output verbatim**

   Run via Bash from the repo root. Print the script's output verbatim — the five counts and the playlist header:

   ```
   Playlist: <name> (<id>)
     Imported new URIs: <N>
     Already in log:    <N>
     Duplicate in file: <N>
     Unparseable lines: <N>
     Total URIs logged: <N>
   ```

   Don't paraphrase these numbers — they are the only feedback the user has that the import worked. A non-zero `Unparseable lines` is normal (the CSV header is usually one); flag it only if it's surprisingly high (>5% of total lines).

7. **Summarise (one Dutch line)**

   - Common case: "Klaar! {N} nieuwe URIs toegevoegd aan de log voor {TARGET} (totaal nu {TOTAL})."
   - Already-seeded case ({N} == 0 and `Already in log` > 0): "Niks nieuws — alles in de file zat al in de log voor {TARGET} ({ALREADY} reeds bekend)."
   - Empty-file case ({N} == 0 and `Unparseable lines` matches the line count): "Geen Spotify-URIs gevonden in {FILE} — check of dit een exportify CSV is."

8. **Capture Learnings**

   If anything was non-obvious (an unusual file format that parsed/didn't parse, a target alias surprise, a count discrepancy versus what the user expected), append a dated entry to `learning-candidates.md`. Promote to `learnings.md` after 3+ recurrences.

---

## Guardrails

- **Never** invoke `log-import` without first confirming the resolved target + file via **AskUserQuestion**. Picking the wrong target seeds the wrong playlist's log, and recovery requires hand-editing `.tracks_log.json`.
- **Never** invent a file path. If the user says "import the House export" and `exportify-exports/House.csv` doesn't exist (try common manglings — `house.csv`, `House_.csv`, `Drum_&_Bass.csv` style), ask via **AskUserQuestion** for the actual filename.
- **Never** pass flags to `log-import` — it accepts only `<playlist>` and `<file>`. There is no `--execute`, `--dry-run`, or tuning flag. If the user asks for a dry-run, explain that `log-import` is local-only and there is nothing to dry-run; offer to abort instead.
- **Never** run `log-import` against `Random sht` (the catch-all) unless the user explicitly confirms — the catch-all is a script-side fallback, not a real bucket whose contents are tracked in `.tracks_log.json`.
- **Never** chain multiple `log-import` invocations in one command. One playlist per run; if the user wants to seed several, ask via **AskUserQuestion** which to do first and loop the skill.
- Always invoke the venv python (`.venv/bin/python`) from the repo root — venv state and IPv4 routing both depend on it (the IPv4 routing isn't strictly required here since no Spotify call is made, but the venv is).
- Always quote both the target and the file arguments (playlist names contain spaces, `/`, `'`; file paths may contain spaces).
- Read `playlists.json` each run so user edits (new aliases, renamed playlists) are honored.
- If the user wants to seed many playlists in one go, offer to repeat the skill per playlist. There is no bulk mode.
- User-facing prose is **Dutch**. CLI commands, playlist names, and file paths stay verbatim.
