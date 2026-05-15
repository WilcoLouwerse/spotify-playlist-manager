---
name: playlist-audit
description: Audits a playlist by classifying each track against the playlist's genre/theme with confidence scores and offers to remove low-confidence tracks — fires on 'controleer mijn House playlist', 'welke nummers in House passen er niet in', 'audit House', or 'check my playlist'.
metadata:
  category: Workflow
  tags: [spotify, audit, genre-classification, playlist-remove, web-search, dutch]
---

# Playlist Audit

Audits one of your playlists by classifying every track against the playlist's own genre or theme, reports a confidence score for each track, and offers to remove tracks below a threshold the user chooses. Two audit modes are available:

- **Web-first (recommended for ≤ 20 tracks)** — Claude AI + live web search (AllMusic, RYM, Wikipedia, Discogs, Last.fm) per track. Same multi-source methodology as [`/playlist-match`](../playlist-match/SKILL.md). Higher accuracy; slower.
- **Quick (OpenAI CLI, default for > 20 tracks)** — Runs `audit-playlist` CLI which classifies all tracks in one batch via OpenAI. Faster; relies on training-data recall rather than live web sources.

The user can always override the default mode choice.

User-facing prose is **Dutch**. Keep SKILL.md, references, templates, and examples in English.

**Input**: A playlist name (from `playlists.json`), a Spotify playlist URL, or a phrase like "controleer mijn House playlist", "audit mijn Techno", "welke nummers passen er niet in House?", "check House op mismatches".

**Source of truth**: [`playlists.json`](../../../playlists.json) for valid playlist names and their declared genre/category. [`docs/commands.md`](../../../docs/commands.md) for CLI behaviour.

**Conversation memory**: Remember the playlist name and the audit results within the session so follow-up removal requests don't require re-running the audit.

---

## Steps

1. **Detect intent and playlist**

   Parse the message for a playlist name or URL. Common shapes:
   - "audit mijn House" / "controleer House"
   - "welke nummers in House passen er niet in?"
   - "check mijn Techno playlist op mismatches"

   If no playlist is specified, ask via **AskUserQuestion**.

   If the message is out of scope (no audit/check intent), hand off to the surrounding agent. Before handing off, mention the right sibling skill in Dutch:
   - **Adding a single track** → `/playlist-match`
   - **Removing one specific track** → `/playlist-remove`
   - **Sorting a source playlist into multiple targets** → `/playlist-triage`
   - **Finding tracks in a source that fit one target** → `/playlist-scan`

2. **Resolve the playlist**

   Read [`playlists.json`](../../../playlists.json). Accept name, alias, or Spotify URL (extract the ID from the URL).

   - If the name matches a key under `"playlists"` or `"aliases"`: proceed.
   - If the name isn't in the config: suggest `/playlist-config` to add it, then stop.
   - Note the playlist's declared category from `"categories"` (genre / mood / theme) and any `"special_rules"`. These define what "fits" the playlist.
   - **Never** audit `Random sht` — it is the catch-all by design; every track belongs there if it fits nothing better. If the user asks, explain this in Dutch.

3. **Get the track list**

   Run `list-tracks` from the repo root via **Bash**:

   ```bash
   .venv/bin/python playlist_manager.py list-tracks "<playlist>"
   ```

   Parse the output: skip the first line (`Playlist: … (N tracks)`), then for each remaining line split on the first tab → `(uri, label)`.

   **If the output is empty (Spotify dev-tier returns no tracks):**
   - Ask the user via **AskUserQuestion** if they have an exportify CSV export:
     - **Ja, ik heb een CSV** — ask for the path and re-run `list-tracks "<csv-path>"`
     - **Nee** — suggest exporting via https://exportify.net and stop.

4. **Choose audit mode**

   Based on track count (the skill may recommend a mode, but the user always decides):

   | Track count | Default recommendation |
   |-------------|----------------------|
   | ≤ 20 tracks | **Web-first** (Claude + WebSearch, per track, slower but most accurate) |
   | 21–50 tracks | **Quick** (OpenAI via `audit-playlist` CLI) — warn that web-first will take ~5–10 min |
   | > 50 tracks | **Quick** (OpenAI via `audit-playlist` CLI) — web-first impractical at this scale |

   Use **AskUserQuestion**:
   ```
   question: "Welke auditmodus wil je gebruiken?"
   options:
     - Web-first (Claude + web, nauwkeuriger)        ← recommended for ≤20 tracks
     - Quick (OpenAI CLI, sneller)                    ← recommended for >20 tracks
   ```

   For playlists > 50 tracks, skip the choice and use quick mode unless the user explicitly asked for web-first.

5a. **Web-first audit** (Claude + WebSearch per track)

   For each track in the list, in order:

   i. **Announce the track** — print `[N/total] Artist - Title` so the user can follow along.

   ii. **Web genre lookup** — follow [`references/genre-sources.md`](references/genre-sources.md). Use **WebSearch** + **WebFetch** on 2–3 sources (AllMusic, Wikipedia or RYM, and one more if signals conflict). Scope the search to the specific track first; fall back to album then artist if no track-level data exists.

   iii. **Score against the playlist** — compare the sourced genres/moods/theme to what this playlist expects:
   - Cross-reference the playlist's declared category from `playlists.json` (genre / mood / theme)
   - Apply `special_rules` if present (e.g., "Funny meme: only meme songs")
   - Use the same confidence bands as `/playlist-match` references: 90-100% = multiple strong sources agree; 75-89% = mostly agree; 60-74% = mixed signals; <60% = weak match or likely mismatch

   iv. **Record**: `{uri, label, confidence, reason, sources}` — keep in memory for the report (step 6).

   Skip a track and mark as "not found" if web sources return nothing after 2 tries — don't fabricate a score.

5b. **Quick audit** (OpenAI CLI)

   Run via **Bash**:

   ```bash
   .venv/bin/python playlist_manager.py audit-playlist "<playlist>"
   # Or with CSV:
   .venv/bin/python playlist_manager.py audit-playlist "<playlist>" --csv "<csv-path>"
   ```

   Default `--min-confidence` is 60 (skip passing it; let the CLI use the default). Surface the output verbatim. Then extract the "Tracks below X%" block to populate the removal candidates for step 7.

6. **Present the audit report**

   Use `templates/audit-report.md`. In Dutch. Show:

   - **Summary header** — "House geauditeerd: 42 nummers"
   - **Score distribution** — counts in three bands: ≥80% (✅), 60–79% (⚠️), <60% (❌)
   - **Low-confidence tracks** — listed with track name, confidence %, and a one-line reason

   Example output:
   ```
   **House — 42 nummers geauditeerd**

   ✅ 35 nummers  ≥80% match
   ⚠️  5 nummers  60–79% match
   ❌  2 nummers  <60% match

   **Lage match (kandidaten voor verwijdering):**
   — 42% — Dua Lipa - Levitating
          Reden: disco-pop met lichte house-elementen; voornamelijk mainstream pop
   — 38% — The Weeknd - Blinding Lights
          Reden: synth-pop / dark R&B; geen house-kenmerken
   ```

7. **Ask for removal threshold**

   After the report, use **AskUserQuestion**:
   ```
   question: "Welke drempel wil je gebruiken voor verwijdering?"
   options:
     - Verwijder alles onder 60% (standaard)
     - Verwijder alles onder 70%
     - Verwijder alles onder 80%
     - Niks verwijderen — alleen het overzicht bekijken
   ```

   (Adjust options to what makes sense given the actual distribution from step 6.)

8. **Confirm removal candidates via AskUserQuestion**

   Present the tracks below the chosen threshold in a **multiSelect** so the user can deselect any they want to keep:

   ```
   question: "Welke van deze nummers wil je verwijderen uit House?"
   multiSelect: true
   options:
     - Dua Lipa - Levitating (42%)
     - The Weeknd - Blinding Lights (38%)
   ```

   If the user selects none → skip to step 10.

9. **Show the planned remove commands and confirm**

   One `remove --execute` per selected track, then ask:

   ```
   question: "Klaar om deze nummers te verwijderen?"
   options:
     - Ja, verwijder
     - Nee, annuleren
   ```

   Only proceed on explicit **Ja**. This confirmation is **mandatory** — it is the final safety gate before Spotify writes.

   Show the commands in a code block:
   ```bash
   .venv/bin/python playlist_manager.py remove "<uri>" "<Playlist>" --execute
   ```

10. **Run and surface output verbatim**

    Execute each `remove --execute` via **Bash** sequentially. Print output as-is. Tally results.

11. **Summarise (Dutch)**

    > "Audit klaar! {N} verwijderd, {M} overgeslagen (niet in log), {K} bewaard door jou. {playlist} heeft nu {remaining} nummers."

12. **Capture Learnings**

    If anything was non-obvious (a surprising genre score, a source that contradicted others, a special_rule that was tricky to apply, a track that was SKIP'd on removal), append a dated entry to `learning-candidates.md`. Promote to `learnings.md` after 3+ recurrences. Skip if nothing new.

---

## Guardrails

- **Always** start genre identification for web-first mode with live **WebSearch** + **WebFetch**. Never skip to training-data recall when web tools are available. Follow the same source priority as [`references/genre-sources.md`](references/genre-sources.md) and [playlist-match's genre-sources](../playlist-match/references/genre-sources.md).
- **Never** run `remove --execute` without the explicit **AskUserQuestion** confirmation in step 9.
- **Never** audit `Random sht` — it is the catch-all; every track belongs there as a fallback. Explain this in Dutch if asked.
- **Never** recommend removing a track based on a confidence score fabricated without web sources. If sources return nothing after 2 tries, mark the track as "geen data" and exclude it from removal candidates.
- **Never** recommend removing a track solely because the artist's overall reputation doesn't fit the playlist — always check the specific track's genre signals.
- **Never** infer "fits" from energy or BPM alone for genre playlists. A high-BPM pop song does not automatically fit a Techno playlist.
- For **mood playlists** (Happy tunes, Sad tunes, etc.): check lyrical content and musical mood, not genre subgenre.
- For **theme playlists** (Funny meme, Ket420, Hooyah): apply the `special_rules` literally; these are highly subjective buckets.
- Always invoke the venv python (`.venv/bin/python`) from the repo root.
- Always quote playlist names and track URIs verbatim.
- Read `playlists.json` each run — user edits are authoritative.
- User-facing prose is **Dutch**. CLI commands, playlist names, and Spotify URIs stay verbatim.
