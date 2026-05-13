---
name: playlist-config
description: Bootstraps or extends playlists.json from your Spotify account via the project's list-playlists CLI command — fires on 'add my new playlist to the config', 'welke playlists ken ik', 'list-playlists', or 'sync playlists.json'.
metadata:
  category: Workflow
  tags: [spotify, list-playlists, playlists-json, config, bootstrap, dutch]
---

# Playlist Config

Wraps the project's config-maintenance workflow: discover writable playlists on the user's Spotify account, diff them against the current [`playlists.json`](../../../playlists.json), and add the picked entries under `"playlists"` (and optionally `"aliases"` / `"categories"` / `"special_rules"`). The CLI itself only reads; **the skill is what mutates `playlists.json`**.

Different shape from the other `playlist-*` skills:

| | playlist-triage / playlist-scan / playlist-match | playlist-log-import | **playlist-config** |
|--|--|--|--|
| Effect | Writes to Spotify | Writes to local `.adds_log.json` | Writes to `playlists.json` |
| Spotify API | Yes (reads + writes) | No | Yes (reads only, via `list-playlists --all`) |
| Dry-run | `--execute` flag | N/A (local only) | The CLI is read-only — the edit step is what to confirm |
| y/N prompt | Yes | None | **AskUserQuestion** before editing `playlists.json` |
| Use case | Sort / match tracks | Seed the duplicate guard | Bootstrap or extend the target-playlist registry |

User-facing prose is **Dutch**. Keep SKILL.md, references, templates, and examples in English.

**Input**: A request to inspect, bootstrap, or extend `playlists.json`. Also fires on phrases like "list-playlists", "welke playlists staan in mijn config", "ik heb een nieuwe playlist gemaakt — voeg toe", "sync mijn playlists.json met Spotify", "show me all my writable playlists".

**Source of truth**: [`docs/commands.md → list-playlists`](../../../docs/commands.md#list-playlists) for CLI behaviour. [`playlists.example.json`](../../../playlists.example.json) for the full schema. [`playlists.json`](../../../playlists.json) for the live config (gitignored — never paste contents into prose, just the names).

---

## Steps

1. **Detect intent**

   Three sub-flows live under this skill — pick one before running anything:

   - **A. Inspect local** — "welke playlists ken ik", "list-playlists", "wat staat er in playlists.json". → Run `list-playlists` without flags. Read-only.
   - **B. Bootstrap** — `playlists.json` doesn't exist yet, or the user says "set up the config" / "bootstrap mijn playlists". → Run `list-playlists --all`, then walk the user through choosing which writable playlists become targets, plus optional `aliases` / `categories` / `special_rules` / `catch_all`.
   - **C. Extend / sync** — `playlists.json` exists and the user says "add my new playlist", "voeg X toe aan de config", "sync met Spotify". → Run `list-playlists --all`, surface the **untracked** list, ask which to add.

   If the user's intent is ambiguous (e.g. "check my playlists"), ask via **AskUserQuestion** which of A/B/C they mean.

2. **Run `list-playlists` (always read-only)**

   From the repo root:

   ```bash
   .venv/bin/python playlist_manager.py list-playlists          # sub-flow A
   .venv/bin/python playlist_manager.py list-playlists --all    # sub-flows B and C
   ```

   `--all` makes one Spotify API call. The script auto-filters to playlists the user **owns or collaborates on** (the only ones writable via the API). Print the output verbatim — it's the user's signal that the API call worked.

   If `--all` fails because OAuth is missing or the user's token is stale, the venv python prints a clear error — surface it and stop. Don't try to fall back to anything else; the user has to fix Spotify auth first.

3. **Parse the output (sub-flows B and C)**

   The `--all` output is two paste-ready JSON blocks separated by headers:

   ```
   Already tracked in playlists.json:
     "House": "0BEX4bI5xtkEVA4BfYTKg2"
     ...

   Untracked (paste any of these into playlists.json -> "playlists"):
     "Coffee Shop": "1def2345678901bcdefghi",
     ...
   ```

   Capture the **untracked** entries — name + 22-char ID. The "Already tracked" block is informational only. See `examples/list-all-output.txt` for the full shape.

4. **Resolve picks via AskUserQuestion**

   Show the untracked names to the user (Dutch prose, names verbatim). Use **AskUserQuestion** with `multiSelect: true` so they can pick more than one at once:

   - "Welke wil je toevoegen aan `playlists.json`?" — options are the untracked names, plus "Geen — annuleren".
   - If there are more than 4 untracked entries (the AskUserQuestion max), present them in **batches of 4** and loop until the user is done. Don't truncate silently.

   If the user wants to add one with a different display key (e.g. Spotify name is `house mix v3` but they want the key to be `House Mix`), ask via a second **AskUserQuestion** whether to use the Spotify name or a custom key. Default to the Spotify name.

5. **Decide on optional metadata per pick**

   For each picked playlist, ask via **AskUserQuestion** whether to also wire up:

   - **`aliases`** — shorthand → canonical mappings (e.g. `"dnb"` → `"Drum & Bass"`). Skip unless the user actually offers an alias.
   - **`categories`** — `genre` / `mood` / `theme`. Without this, `smart-add` sees one flat list and classifies worse. Defaults to **asking** which bucket; allow "skip" to leave uncategorised.
   - **`special_rules`** — only if the playlist is a tight semantic bucket (catch-all rules, exclusive themes). Skip for plain genres.

   For sub-flow B (bootstrap), also ask about **`catch_all`**: which playlist (if any) acts as the script-side fallback, and at what `threshold` (default 85). See [`playlists.example.json`](../../../playlists.example.json) for the schema.

6. **Render the planned edit**

   Use `templates/plan.md`. Show the user — before writing — a unified-diff-style preview of what will be added to `playlists.json`:

   ```
   In playlists.json:
     + "playlists" -> "House Mix": "1def234..."
     + "aliases"   -> "house mix": "House Mix"          (optional)
     + "categories.genre" += "House Mix"                (optional)
   ```

   If `playlists.json` doesn't exist yet (sub-flow B), the planned edit is a **full create** seeded from `playlists.example.json` minus the example IDs, plus the user's picks. Show the full proposed file (or a structural summary if >40 lines).

7. **Confirm the write via AskUserQuestion**

   This is the **only** safety gate. The CLI did no writing; the file edit is the destructive step.

   - **Ja, schrijf naar playlists.json** — proceed to step 8.
   - **Pas eerst aan** — go back to step 4 and re-pick.
   - **Annuleren** — end the flow, write nothing.

8. **Edit `playlists.json` (or create it)**

   Use **Edit** (existing file, additive change) or **Write** (sub-flow B, file did not exist). Preserve the existing file's key order and indentation — `playlists.json` is hand-curated, and re-shuffling keys produces noisy diffs that confuse the user.

   - For **sub-flow B**: seed from [`playlists.example.json`](../../../playlists.example.json). Strip the example IDs, replace the `"playlists"` block with the user's picks, and only include `aliases` / `categories` / `special_rules` / `catch_all` sections that have content. Empty sections should be omitted, not left as `{}`.
   - For **sub-flow C**: append new entries to existing sections without reordering siblings.

9. **Verify with a second `list-playlists` (local)**

   After the write, run:

   ```bash
   .venv/bin/python playlist_manager.py list-playlists
   ```

   This confirms `playlists.json` parses correctly and the new entries are visible to the CLI. If `load_config` rejects the file (invalid alias target, malformed JSON), the script prints a clear error — surface it, then offer to revert via **AskUserQuestion**.

10. **Summarise (one Dutch line)**

    - Bootstrap (B): "Klaar! `playlists.json` aangemaakt met {N} playlists{, M aliases}{, K in categories}."
    - Extend (C): "Klaar! {N} playlist(s) toegevoegd aan `playlists.json` — totaal nu {TOTAL}."
    - Inspect (A): "Je hebt {N} playlists in `playlists.json`: {comma-separated names}."
    - No changes (user cancelled): "Niks aangepast. `playlists.json` is ongewijzigd."

11. **Capture Learnings**

    If anything was non-obvious (an unusual playlist name that broke the JSON, a category bucket the user wanted that wasn't `genre`/`mood`/`theme`, a Spotify-side rename that orphaned a tracked ID), append a dated entry to `learning-candidates.md`. Promote to `learnings.md` after 3+ recurrences.

---

## Guardrails

- **Never** edit `playlists.json` without showing the planned diff via step 6 and getting explicit `Ja, schrijf naar playlists.json` via **AskUserQuestion**. The file is the source of truth for every other skill in this repo; a stealth edit breaks `add`, `smart-add`, `review-playlist`, `bulk-playlist`, and `scan-for` at once.
- **Never** add a playlist to `"aliases"` whose value isn't a key under `"playlists"` — `load_config` rejects the file at startup and every CLI command then refuses to run. Validate alias targets in step 5 before showing the diff.
- **Never** invent a Spotify playlist ID. IDs come from `list-playlists --all` only. If the user pastes one by hand, accept it but warn that it isn't being verified against the Spotify API in this flow.
- **Never** strip or reorder the existing `"playlists"` block — only append. Renaming a key or removing one orphans every entry in `aliases` / `categories` / `special_rules` / `catch_all` that referenced it.
- **Never** auto-categorise a new playlist. The user picks `genre` / `mood` / `theme` or skips. Wrong categorisation degrades the `smart-add` classifier's accuracy.
- **Never** set `catch_all.playlist` to a key that isn't in `"playlists"`. Same validation rule as aliases.
- **Never** run `list-playlists --all` more than once per turn. The output is stable across the flow; re-fetching wastes a Spotify API call (the dev-tier quota is tight).
- **Never** print the live `playlists.json` contents to chat in full unless the user asks. Names and counts are fine; pasting the whole file is noise.
- Always invoke the venv python (`.venv/bin/python`) from the repo root — venv state and IPv4 routing both depend on it (IPv4 is required for the `--all` Spotify API call).
- Always quote playlist names in commands and JSON keys verbatim — they contain spaces, `/`, `&`, `'`, and accented characters.
- Read [`playlists.json`](../../../playlists.json) and [`playlists.example.json`](../../../playlists.example.json) each run so the latest user edits are honored.
- User-facing prose is **Dutch**. CLI commands, playlist names, and JSON keys stay verbatim.
