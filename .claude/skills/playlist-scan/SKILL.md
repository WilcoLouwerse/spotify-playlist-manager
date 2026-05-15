---
name: playlist-scan
description: Scans a source playlist for tracks that fit a chosen target playlist via the project's scan-for CLI command — fires on 'welke tracks in X passen in House', 'mine candidates for Y', 'scan-for', or 'find house tracks in random sht'.
metadata:
  category: Workflow
  tags: [spotify, scan-for, playlist-mining, candidate-tracks, dutch]
---

# Playlist Scan

Wraps the project's source-to-one-target workflow: classify every track in a source playlist, keep only those whose classification includes a specific target playlist, then add the candidates after one `y/N`. The **default classifier is Claude AI + live web search** (same methodology as [`/playlist-match`](../playlist-match/SKILL.md)) for small source playlists; the OpenAI-backed `scan-for` CLI is the faster fallback for larger ones.

Different shape from [playlist-triage](../playlist-triage/SKILL.md):

| | playlist-triage | **playlist-scan** |
|--|--|--|
| Targets | All matches the classifier returns | One playlist you choose |
| Output | Sorted into many target playlists | A single list of candidates for the target |
| Use case | "Sort this triage playlist into all my buckets" | "Which of these would fit my House playlist?" |

User-facing prose is **Dutch**. Keep SKILL.md, references, templates, and examples in English.

**Input**: A target playlist name + a source (Spotify playlist URL/URI/ID, CSV path under `exportify-exports/`, or bare name resolving against that folder). Also fires on phrases like "welke tracks passen in House", "scan op X", "find house-fits in my triage".

**Source of truth**: [`docs/commands.md → scan-for`](../../../docs/commands.md#scan-for) for CLI behaviour. [`playlists.json`](../../../playlists.json) for valid target names. [`exportify-exports/`](../../../exportify-exports/) for local CSV sources.

---

## Steps

1. **Detect intent**

   The message references a target playlist + a source. Common shapes:
   - "welke tracks in [SOURCE] passen in [TARGET]"
   - "[TARGET] tracks vinden in [SOURCE]"
   - "scan [SOURCE] op [TARGET]"
   - "find house-fitting tracks in my triage"

   If either the target or the source is missing, ask via **AskUserQuestion**.

2. **Resolve the target**

   Read [`playlists.json`](../../../playlists.json). The target must match a key under `"playlists"` or an entry under `"aliases"`. Case-insensitive. If the user typed a name that maps to multiple plausible playlists, ask via **AskUserQuestion**.

   **Never** pass `Random sht` as the target — the script will accept it (it's in the playlists dict) but the user's intent is almost never "scan for the catch-all playlist". If they ask for it anyway, confirm via **AskUserQuestion** that they really mean the catch-all.

3. **Resolve the source**

   Follow `references/source-resolution.md` (same rules as playlist-triage). Accept Spotify URL/URI/ID, CSV path, or bare name (resolved against `exportify-exports/`). Quote the source verbatim.

4. **Choose scan mode**

   Based on the source playlist's track count, use **AskUserQuestion** to offer the right path:

   | Source size | Default | How it works |
   |-------------|---------|--------------|
   | ≤ 20 tracks | **Claude + web** | Claude AI + live WebSearch per track (AllMusic, Wikipedia, RYM, Discogs, Last.fm). Same methodology as `/playlist-match`. Produces the candidate list in-chat; add via `add --execute`. |
   | > 20 tracks | **scan-for CLI** | OpenAI-backed `scan-for` CLI. Faster batch classification. Requires terminal for `--execute` or `yes |` pipe. |

   The user can always override the default. If the source count is unknown (Spotify URL, dev-mode), default to the CLI path and note that the count was not available.

   **Web-first path (Claude + web):**
   - Run `list-tracks "<source>"` via Bash. Parse the tab-separated output.
   - For each track: use **WebSearch** + **WebFetch** (AllMusic, Wikipedia, RYM, Discogs, Last.fm) to determine genres and playlist matches — same as `/playlist-match` steps 5–6.
   - Keep only tracks where the target playlist appears in the classification with confidence ≥ the user's chosen threshold (default 80%).
   - Present the candidate list. Use **AskUserQuestion** (multiSelect) to let the user pick which candidates to add.
   - Run `add --execute` per accepted candidate. Confirm before running.
   - This path does NOT invoke `scan-for` CLI. `list-tracks` (read-only) and `add` (confirmed write) are the only commands used.

5. **Tune the classifier**

   - **Web-first**: adjust threshold with plain Dutch ("alleen nummers boven 85%"). No CLI flags needed.
   - **scan-for CLI** default: `--min-confidence 80`. Deviate only when asked:
     - "stricter" → `--min-confidence 90`
     - "more lenient" → `--min-confidence 60`

6. **Dry-run vs execute (CLI path only)**

   Default: **dry-run**. Use **AskUserQuestion**:
   - **Dry-run** *(recommended)* — list the candidates that would be added, write nothing.
   - **Execute** — actually add the candidates to the target after one `y/N`.

   For the **web-first path**, there is no dry-run — the skill confirms per candidate via **AskUserQuestion** before running `add --execute`.

7. **Render the planned command (CLI path only)**

   Use `templates/plan.md`. One command, from the repo root:

   ```bash
   .venv/bin/python playlist_manager.py scan-for "<TARGET>" "<SOURCE>"            # dry-run
   .venv/bin/python playlist_manager.py scan-for "<TARGET>" "<SOURCE>" --execute  # execute, single y/N
   ```

   Quote both `<TARGET>` (canonical name from `playlists.json`) and `<SOURCE>` (verbatim user input).

8. **Confirm (execute only, CLI path)**

   `scan-for --execute` prompts on stdin with a single `y/N` after listing candidates. Use **AskUserQuestion**:

   - **Vanuit mijn terminal** — copy-paste the command and answer y/N interactively.
   - **Hier draaien met automatische 'y'** — `yes | ...` auto-accepts the single y/N.
   - **Annuleren** — end the flow.

   For dry-run, no confirmation needed — run directly via Bash.

9. **Run and surface output verbatim**

   - **Dry-run (CLI)**: run via Bash, print the script's output (the candidate list) verbatim.
   - **Execute (terminal path)**: do NOT run — show the user the command and an interactive hint.
   - **Execute (`yes |` path)**: run as `yes | .venv/bin/python playlist_manager.py scan-for "<TARGET>" "<SOURCE>" --execute`, print output verbatim.
   - **Web-first path**: run `add --execute` per confirmed candidate, print each output verbatim.

   Don't paraphrase the candidate list, the `ADDED ...` / `SKIP ...` lines, or the final `Scan complete (EXECUTED): N added, M failed`.

10. **Summarise (one Dutch line)**

    - Dry-run (CLI): "Dry-run klaar — {N} kandidaten voor {TARGET}. Niets geschreven."
    - Execute via skill (CLI or web-first): "Klaar! {A} toegevoegd aan {TARGET}, {S} overgeslagen (al in playlist)."
    - Execute via user's terminal: "Commando staat klaar. Draai 'm in je terminal en typ y wanneer de prompt verschijnt."

11. **Capture Learnings**

    If anything was non-obvious (an alias resolution surprise, a target that was the catch-all, a `--min-confidence` value that yielded too few/too many candidates, a web-first classification that contradicted the CLI result), append a dated entry to `learning-candidates.md`. Promote to `learnings.md` after 3+ recurrences.

---

## Guardrails

- **Never** run `--execute` without explicit user confirmation in the same turn.
- **Never** scan with `Random sht` as the target unless the user explicitly confirms — it's the script's catch-all, not a normal playlist match.
- **Never** invent a Spotify playlist URL or CSV filename. If the source doesn't match anything, ask via **AskUserQuestion**.
- **Never** auto-pipe `yes` into `--execute` without offering the terminal alternative — the user may want to see the candidate list before saying y.
- Always invoke the venv python (`.venv/bin/python`) from the repo root — IPv4 routing and venv state both depend on it.
- Always quote both the target and the source arguments (playlist names contain spaces, `/`, and `'`).
- Read `playlists.json` each run so user edits (new aliases, renamed playlists) are honored.
- If the user wants tracks from many playlists into many targets in one go, route them to [playlist-triage](../playlist-triage/SKILL.md). `scan-for` is one-target-at-a-time by design.
- User-facing prose is **Dutch**. CLI commands and playlist names stay verbatim.
