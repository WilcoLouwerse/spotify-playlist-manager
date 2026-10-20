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

**Source of truth**: [`docs/commands.md`](../../../docs/commands.md) for the CLI behaviour (dry-run default, duplicate guard, CSV fallback, IPv4-only). The skill consults it rather than re-implementing the rules. The web-first path uses [`batch-add`](../../../docs/commands.md#batch-add) for bulk writes — never loop `add --execute` per track when ≥ 2 URIs go to the same target.

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

   **Prefer the live playlist.** If the source resolves to a CSV AND the source playlist is known in `playlists.json`, Spotify can read it live — offer that via **AskUserQuestion** instead of silently using the snapshot. See `references/source-resolution.md` → "Prefer the live playlist over a CSV".

3. **Pick the workflow**

   Use **AskUserQuestion** (single-select). Three options — recommend based on playlist size and user phrasing:

   | Option | When to recommend | How it works |
   |--------|------------------|--------------|
   | **Claude + web (per-track)** | ≤ 20 tracks, or user says "nauwkeurig/check/curate" | Claude AI + live WebSearch per track (AllMusic, Wikipedia, RYM, Discogs, Last.fm). Same methodology as `/playlist-match`. Slower but most accurate. No CLI round-trip — uses `list-tracks` + `batch-add` (per target playlist). |
   | **Review (CLI, per-track y/N)** | 20–50 tracks, or user says "review/controleer" | `review-playlist` CLI wraps OpenAI classification. Interactive per-track prompt (requires terminal for `--execute`). |
   | **Bulk (CLI, one y/N)** | > 50 tracks, or user says "sort/drain/leeghalen" | `bulk-playlist` CLI wraps OpenAI classification. Single y/N for the whole batch. Fastest. |

   **Web-first path (Claude + web):**
   - Run `list-tracks "<source>"` to get the track list. Parse the tab-separated output.
   - For each track: use **WebSearch** + **WebFetch** (AllMusic, Wikipedia, RYM, Discogs, Last.fm) to determine genres, then match against `playlists.json` taxonomy — same steps 5-6 of `/playlist-match`. Score 1–5 target playlists per track.
   - **Build a plan** grouped by target playlist: `{target: [uri, uri, ...]}`. Present it as a per-target tally (e.g. "House: 7 tracks, Techno: 3 tracks, Drum & Bass: 4 tracks") plus a per-track view if the user asks.
   - **Confirm once** via **AskUserQuestion**: "Pas alles toe / Selectief reviewen / Annuleren". Do NOT ask per track — the planner already has high-confidence matches. Per-track approval is only for the "Selectief reviewen" path, and even then prefer per-*target* approval ("Voeg de 7 House-tracks toe? Voeg de 3 Techno-tracks toe?") over per-track y/N.
   - **Execute via batch-add** per target. For each target playlist in the plan: write its URIs to `.scratch/triage-<target>.txt` (one per line), then run `batch-add "<target>" .scratch/triage-<target>.txt --execute`. One target playlist = one `batch-add` invocation = at most ⌈N/100⌉ Spotify API calls.
   - For targets with exactly one URI, `add --execute` is fine — both work, prefer whichever produces less noise in the output.
   - This path does NOT use `review-playlist` or `bulk-playlist` CLI. `batch-add` is the primary write command; `add` only for single-URI targets.

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

   For the **web-first path**, the plan tally from step 3 is the natural dry-run preview. Once the user confirms, run `batch-add` per target — no per-track confirmation.

6. **Render the planned command**

   Use `templates/plan.md`. Single command, in a code block, from the repo root.

   **CLI paths:**
   ```bash
   .venv/bin/python playlist_manager.py review-playlist "<source>"            # dry-run
   .venv/bin/python playlist_manager.py review-playlist "<source>" --execute  # write
   ```

   (`bulk-playlist` follows the same pattern.) Quote the source verbatim; the script accepts URL / URI / ID / CSV path / bare name.

   **Web-first path:** show one `batch-add` command per target playlist with at least one accepted URI:
   ```bash
   # Per target (the .scratch/triage-<target>.txt files were written in step 3):
   .venv/bin/python playlist_manager.py batch-add "House" .scratch/triage-house.txt --execute
   .venv/bin/python playlist_manager.py batch-add "Techno" .scratch/triage-techno.txt --execute
   ```

   `.scratch/` is gitignored — see [`.gitignore`](../../../.gitignore).

7. **Confirm (execute only)**

   **CLI paths:** Both `review-playlist` (per-track `y/N/s/q`) and `bulk-playlist` (single `y/N`) prompt on **stdin**. The skill cannot drive those prompts from chat. Before running the execute path, use **AskUserQuestion**:

   - **Run it from the terminal myself** — copy the command and run interactively (recommended for review-playlist).
   - **Run via this skill with `yes | ...` pipe** *(bulk-playlist only)* — auto-accept the single y/N. Only offer this for `bulk-playlist`, never for `review-playlist`.
   - **Cancel** — end the flow.

   For dry-run mode, no confirmation needed — run directly via Bash.

   **Web-first path:** the confirmation in step 3 ("Pas alles toe") is the safety gate. Don't ask again. If the user picked "Selectief reviewen" and approved per-target, that approval is enough to fire each `batch-add` for the approved targets.

8. **Run and surface output verbatim**

   - **Dry-run (CLI)**: run via Bash, print the script's output verbatim, then summarise in Dutch.
   - **Execute (terminal path)**: do NOT run. Show the user the exact command + a "run dit in je terminal vanuit de repo-root" hint.
   - **Execute (bulk + `yes |` path)**: run as `yes | .venv/bin/python playlist_manager.py bulk-playlist "<source>" --execute`, print output verbatim, then summarise.
   - **Web-first path**: run one `batch-add --execute` per target via Bash. Print each command's output verbatim — the per-batch `+ batch of {N}: snapshot ...` lines and the final `DONE: added {A}, failed {F}, skipped {S}` per target are what the user needs to see.

   Don't paraphrase the script's `ADDED ...`, `SKIP: already in playlist`, `DRY RUN: would add ...`, or `DONE: added ...` messages — those come from the CLI and are the user's contract.

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
- **Never** loop `add --execute` per track in the web-first path. Group accepted URIs by target playlist and use `batch-add` per target — see [`docs/commands.md → batch-add`](../../../docs/commands.md#batch-add). The per-track loop costs ~3-5 API calls per track and bootstraps Python every time; `batch-add` is 1 pagination + 1 API call per 100 URIs per target.
- **Never** ask the user "batch or per-track?" when the answer is obviously batch. Default to `batch-add` for any target with ≥ 2 accepted URIs. Only ask if there's a structural reason (e.g. the user explicitly wants to inspect each before adding).
- **Never** drive `review-playlist`'s per-track stdin from chat — recommend the terminal path instead. `bulk-playlist`'s single y/N may be piped with `yes |` only after the user opts in.
- **Never** invent a Spotify playlist URL or a CSV filename. If the source doesn't match anything, ask.
- **Never** seed `.tracks_log.json` from this skill — that is the `log-import` command's job. The duplicate guard reads Spotify directly; the log is only its fallback. If the user mentions "duplicate guard", point them at [`docs/architecture.md → Duplicate detection`](../../../docs/architecture.md#duplicate-detection).
- Always invoke the venv python (`.venv/bin/python`) from the repo root — IPv4 routing and venv state both depend on it.
- Always quote source arguments to survive playlist names with spaces, `/`, or `'`.
- If Spotify returns no readable tracks for the source (e.g. a playlist owned by someone else), the CLI itself offers a CSV fallback — let it. Don't pre-empt that path.
- User-facing prose is **Dutch**. CLI commands and playlist names stay verbatim.
