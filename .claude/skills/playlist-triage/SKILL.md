---
name: playlist-triage
description: Triages a source Spotify playlist into target playlists via review-playlist (per-track y/N) or bulk-playlist (single y/N) — fires on 'sort my triage', 'review this playlist', 'sorteer mijn random-sht', or a pasted playlist URL.
metadata:
  category: Workflow
  tags: [spotify, triage, review-playlist, bulk-playlist, playlist-sort, dutch]
---

# Playlist Triage

Wraps the project's two source-to-many-targets workflows:

- **`review-playlist`** — per-track `y/N/s/q` prompts. Use when the user wants veto power on each track.
- **`bulk-playlist`** — single `y/N` for the whole plan. Use when the user trusts the classifier and just wants the triage drained.

Both classify every track in a source playlist and propose target playlists from [`playlists.json`](../../../playlists.json). The **default classifier is Claude AI + live web search** (same multi-source methodology as [`/playlist-match`](../playlist-match/SKILL.md)) for smaller playlists. For larger playlists, the OpenAI-backed CLI commands are the faster fallback.

User-facing prose is **Dutch** (consistent with the rest of this project's skills). Keep SKILL.md, references, templates, and examples in English.

**Input**: A Spotify playlist URL / URI / ID, a path to an exportify CSV, or a bare name matching a CSV in [`exportify-exports/`](../../../exportify-exports/). Also fires on natural phrases like "sorteer mijn 'to triage'", "review this playlist", "haal mijn triage leeg".

**Source of truth**: [`docs/commands.md`](../../../docs/commands.md) for the CLI behaviour (dry-run default, duplicate guard, CSV fallback, IPv4-only). The skill consults it rather than re-implementing the rules.

---

## Steps

1. **Detect intent and source**

   The message must reference one of:
   - a Spotify playlist URL / URI / ID
   - a CSV path under `exportify-exports/`
   - a bare playlist name that maps to a CSV in that folder
   - a triage phrase ("sorteer", "review", "triage", "leeghalen", "sort") — in which case ask for the source via **AskUserQuestion** if not given.

   If the message is ambiguous, ask via **AskUserQuestion** rather than guessing.

2. **Resolve the source**

   Follow `references/source-resolution.md`:
   - URL/URI/ID → use as-is.
   - CSV path → use as-is (verify it exists).
   - Bare name → list `exportify-exports/*.csv` and offer matches via **AskUserQuestion**. Spotify display names map to underscored, slash-tolerant filenames; let the user pick from the actual filenames rather than guessing.

3. **Pick the workflow**

   Use **AskUserQuestion** (single-select). Three options — recommend based on playlist size and user phrasing:

   | Option | When to recommend | How it works |
   |--------|------------------|--------------|
   | **Claude + web (per-track)** | ≤ 20 tracks, or user says "nauwkeurig/check/curate" | Claude AI + live WebSearch per track (AllMusic, Wikipedia, RYM, Discogs, Last.fm). Same methodology as `/playlist-match`. Slower but most accurate. No CLI round-trip — uses `list-tracks` + `add --execute` per accepted track. |
   | **Review (CLI, per-track y/N)** | 20–50 tracks, or user says "review/controleer" | `review-playlist` CLI wraps OpenAI classification. Interactive per-track prompt (requires terminal for `--execute`). |
   | **Bulk (CLI, one y/N)** | > 50 tracks, or user says "sort/drain/leeghalen" | `bulk-playlist` CLI wraps OpenAI classification. Single y/N for the whole batch. Fastest. |

   **Web-first path (Claude + web):**
   - Run `list-tracks "<source>"` to get the track list. Parse the tab-separated output.
   - For each track: use **WebSearch** + **WebFetch** (AllMusic, Wikipedia, RYM, Discogs, Last.fm) to determine genres, then match against `playlists.json` taxonomy — same steps 5-6 of `/playlist-match`. Score 1–5 target playlists per track.
   - Ask the user per-track via **AskUserQuestion**:
     - **Voeg toe aan [playlists]** — run `add --execute` for each accepted playlist
     - **Overslaan** — skip this track
     - **Stop** — end the flow
   - After each track, confirm before running `add --execute` — or if the user pre-approved "voeg alles toe met ≥X%", run automatically within that session turn.
   - This path does NOT use `review-playlist` or `bulk-playlist` CLI. `add` is the only write command.

4. **Tune the classifier (CLI paths only)**

   Defaults per [`docs/commands.md`](../../../docs/commands.md):
   - `review-playlist`: `--max-playlists 3 --min-playlists 1 --min-confidence 80`
   - `bulk-playlist`: `--max-playlists 3 --min-playlists 1 --min-confidence 80`

   Only deviate if the user asks. Common tweaks via **AskUserQuestion**:
   - "stricter classifier" → `--min-confidence 90`
   - "more suggestions per track" → `--max-playlists 5`

   Don't surface the flags unless the user wants to tune — the defaults are sensible. For the web-first path, confidence tuning is done by describing the desired strictness in plain Dutch ("alleen nummers boven 80%"); the skill applies that when presenting per-track matches.

5. **Dry-run vs execute (CLI paths only)**

   Default: **dry-run**. Use **AskUserQuestion**:
   - **Dry-run** *(recommended)* — classify and show the plan, write nothing.
   - **Execute** — actually write the accepted adds to Spotify.

   For the **web-first path**, there is no dry-run — the skill confirms each track via **AskUserQuestion** before running `add --execute`, so confirmation is built-in per track.

6. **Render the planned command (CLI paths only)**

   Use `templates/plan.md`. Single command, in a code block, from the repo root:

   ```bash
   .venv/bin/python playlist_manager.py review-playlist "<source>"            # dry-run
   .venv/bin/python playlist_manager.py review-playlist "<source>" --execute  # write
   ```

   (`bulk-playlist` follows the same pattern.) Quote the source verbatim; the script accepts URL / URI / ID / CSV path / bare name.

   For the **web-first path**: show the `add --execute` commands for accepted tracks in a code block as they are confirmed, so the user can see what is being run.

7. **Confirm (execute only, CLI paths)**

   Both `review-playlist` (per-track `y/N/s/q`) and `bulk-playlist` (single `y/N`) prompt on **stdin**. The skill cannot drive those prompts from chat. Before running the execute path, use **AskUserQuestion**:

   - **Run it from the terminal myself** — copy the command and run interactively (recommended for review-playlist).
   - **Run via this skill with `yes | ...` pipe** *(bulk-playlist only)* — auto-accept the single y/N. Only offer this for `bulk-playlist`, never for `review-playlist`.
   - **Cancel** — end the flow.

   For dry-run mode, no confirmation needed — run directly via Bash.

8. **Run and surface output verbatim**

   - **Dry-run (CLI)**: run via Bash, print the script's output verbatim, then summarise in Dutch.
   - **Execute (terminal path)**: do NOT run. Show the user the exact command + a "run dit in je terminal vanuit de repo-root" hint.
   - **Execute (bulk + `yes |` path)**: run as `yes | .venv/bin/python playlist_manager.py bulk-playlist "<source>" --execute`, print output verbatim, then summarise.
   - **Web-first path**: run `add --execute` per accepted track after per-track confirmation. Print each command's output verbatim.

   Don't paraphrase the script's `ADDED ...`, `SKIP: already in playlist`, `DRY RUN: would add ...` messages — those come from the CLI and are the user's contract.

9. **Summarise (one Dutch line)**

   - Dry-run (CLI): "Dry-run klaar — {N} kandidaten verdeeld over {M} playlists. Niets geschreven."
   - Execute via skill: "Klaar! {A} toegevoegd, {S} overgeslagen (al in playlist)."
   - Execute via user's terminal: "Commando staat klaar. Draai 'm in je terminal en typ y/N als de prompts verschijnen."
   - Web-first path: "Triage klaar! {A} nummers toegevoegd aan {M} playlists, {S} overgeslagen, {K} overgeslagen door jou."

10. **Capture Learnings**

    If anything was non-obvious (a CSV-path edge case, an aggressive classifier output, a tracking-log gap that caused unexpected re-adds), append a dated entry to `learning-candidates.md` under the matching section. Promote to `learnings.md` after 3+ recurrences. Skip if nothing new.

---

## Guardrails

- **Never** run `--execute` without explicit user confirmation in the same turn.
- **Never** drive `review-playlist`'s per-track stdin from chat — recommend the terminal path instead. `bulk-playlist`'s single y/N may be piped with `yes |` only after the user opts in.
- **Never** invent a Spotify playlist URL or a CSV filename. If the source doesn't match anything, ask.
- **Never** seed `.tracks_log.json` from this skill — that is the `log-import` command's job. If the user mentions "duplicate guard", point them at [`docs/commands.md`](../../../docs/commands.md#log-import).
- Always invoke the venv python (`.venv/bin/python`) from the repo root — IPv4 routing and venv state both depend on it.
- Always quote source arguments to survive playlist names with spaces, `/`, or `'`.
- If `playlist_items` returns stripped data (Spotify Developer Mode), the CLI itself offers a CSV fallback — let it. Don't pre-empt that path.
- User-facing prose is **Dutch**. CLI commands and playlist names stay verbatim.
