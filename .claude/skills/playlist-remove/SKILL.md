---
name: playlist-remove
description: Removes a track from one or more playlists via the project's remove CLI command — fires on 'verwijder X uit House', 'remove this track from playlist', 'verwijder uit mijn playlists', or a Spotify URL with remove intent.
metadata:
  category: Workflow
  tags: [spotify, remove, playlist-remove, dutch]
---

# Playlist Remove

Removes a specific track from one or more of your configured playlists using the project's
`remove` CLI command ([playlist_manager.py](../../../playlist_manager.py)).

User-facing prose is **Dutch**. Keep SKILL.md, references, templates, and examples in English.

**Input**: One or more Spotify track URLs/URIs/IDs (optionally with "Artist - Title"), a natural-language remove request ("verwijder X uit House", "haal dit nummer uit Techno"), or a follow-up after a `/playlist-match` or `/playlist-audit` analysis ("verwijder dit uit House").

**Source of truth**: [`playlists.json`](../../../playlists.json) for valid playlist names. [`docs/commands.md → remove`](../../../docs/commands.md#remove) and [`docs/commands.md → batch-remove`](../../../docs/commands.md#batch-remove) for CLI behaviour.

**Command picker** (covers every shape this skill handles):

| Tracks | Playlists | Command per playlist | Why |
|--------|-----------|----------------------|-----|
| 1 | 1 | `remove --execute` once | Trivial single call. |
| 1 | N | `remove --execute` looped over the N playlists | Spotify API is per-playlist; one API call per playlist, no batching is possible. |
| N (≥ 2) | 1 | `batch-remove --execute` once with a `.scratch/` URI file | One pagination + ⌈N/100⌉ API calls instead of ~3-5 per track. |
| N (≥ 2) | M (≥ 2) | `batch-remove --execute` per playlist (M invocations, each batched) | Per-playlist batching is the best the Spotify API allows. |

---

## Steps

1. **Detect input and scope**

   Parse the message for:
   - **Track**: Spotify URL/URI/ID, or "Artist - Title"
   - **Playlist(s)**: One or more playlist names or aliases from `playlists.json`

   If both are unambiguous, go to step 2. If either is missing or ambiguous, resolve via **AskUserQuestion** before proceeding.

   If the message is out of scope (no remove intent, or no track+playlist combination can be resolved), hand off to the surrounding agent. Before handing off, check whether a sibling skill is the right fit and mention it in Dutch:
   - **Adding** a track to a playlist → `/playlist-match`
   - **Auditing whether playlist tracks match the genre** → `/playlist-audit`
   - **Sorting a whole source playlist into target playlists** → `/playlist-triage`
   - **Finding tracks in a source that fit one target** → `/playlist-scan`

2. **Resolve the track to a Spotify URL/URI/ID**

   The `remove` CLI requires a Spotify URL, URI, or bare 22-char ID — it cannot search by name.

   - If the user gave a Spotify URL/URI/ID: use it verbatim.
   - If only "Artist - Title" was given: ask via **AskUserQuestion**:

     > "Om het nummer te verwijderen heb ik een Spotify-link, URI of track-ID nodig. Plak die via 'Other', of kies 'Annuleren'."

     Do not invent or guess a track ID. If the user cancels, end the flow gracefully.

3. **Resolve the target playlist(s)**

   Read [`playlists.json`](../../../playlists.json). Accept name or alias (case-insensitive).

   - If the user named one or more playlists: validate each exists in the config.
   - If no playlist was named: use **AskUserQuestion** with `multiSelect: true` listing all playlists from the config. Exclude `Random sht` from the list by default — it is the script-side catch-all; if the user really wants to remove from it, they can type it via "Other".

4. **Optional: quick web genre check**

   When the user is uncertain whether the track truly doesn't fit, or when they ask "past dit echt niet?" / "check the genre first", use **WebSearch** + **WebFetch** to pull a quick genre classification (same sources as `/playlist-match`: AllMusic, Wikipedia, RYM, Discogs, Last.fm). Present the result in Dutch so the user can reconsider before removing.

   This step is **optional** and only triggered by user uncertainty or an explicit request. Skip it for direct, confident remove requests.

5. **Show the planned command(s)**

   Use the **Command picker** table at the top of this SKILL.md to choose between `remove` and `batch-remove`. Always with `--execute` (the **AskUserQuestion** in step 6 is the safety gate):

   - **1 track × 1 playlist**:
     ```bash
     .venv/bin/python playlist_manager.py remove "<track>" "<Playlist Name>" --execute
     ```

   - **1 track × N playlists** (loop, no batching possible per Spotify API):
     ```bash
     .venv/bin/python playlist_manager.py remove "<track>" "<Playlist A>" --execute
     .venv/bin/python playlist_manager.py remove "<track>" "<Playlist B>" --execute
     ```

   - **N tracks × 1 playlist** (batch):
     ```bash
     # Write the N URIs to .scratch/remove-<playlist>.txt (one per line), then:
     .venv/bin/python playlist_manager.py batch-remove "<Playlist Name>" .scratch/remove-<playlist>.txt --execute
     ```

   - **N tracks × M playlists** (batch per playlist):
     ```bash
     .venv/bin/python playlist_manager.py batch-remove "<Playlist A>" .scratch/remove-A.txt --execute
     .venv/bin/python playlist_manager.py batch-remove "<Playlist B>" .scratch/remove-B.txt --execute
     ```

   `.scratch/` is gitignored — see [`.gitignore`](../../../.gitignore). Quote playlist names verbatim from `playlists.json`. See `references/remove-command.md` for quoting rules.

6. **Mandatory confirmation via AskUserQuestion**

   Show the user exactly what will run, then ask:

   ```
   question: "Klaar om {dit nummer | deze {N} nummers} te verwijderen?"
   options:
     - Ja, verwijder
     - Nee, annuleren
   ```

   Only proceed on explicit **Ja**. On **Nee**, end the flow gracefully without running anything.

7. **Run and surface output verbatim**

   - **`remove --execute`**: run each command via **Bash** sequentially. Print output as-is.
     - `DONE: track removed (snapshot …)` — success
     - `SKIP: track not found in playlist. No changes made.` — track wasn't in the playlist (may have been added outside this tool; see guardrails below)
     - `FAILED: Spotify returned …` — API error; surface verbatim
   - **`batch-remove --execute`**: write the URI file under `.scratch/`, run the command via **Bash**, print output as-is. The per-batch snapshot lines and final `DONE: removed {R}, failed {F}, skipped {S} (not in playlist)` are what the user needs to see.

   Do not paraphrase these messages.

8. **Summarise (one Dutch line)**

   > "Klaar! {N} verwijderd, {M} overgeslagen (niet in playlist)."

   Then ask via **AskUserQuestion** if the user wants to do anything else (e.g. add the track to a different playlist via `/playlist-match`):
   - "Voeg toe aan andere playlist" → hand off to `/playlist-match` with this track pre-loaded
   - "Klaar" → end

9. **Capture Learnings**

   If anything was non-obvious (track not found because it was added outside this tool, a playlist-name edge case, an unexpected SKIP), append a dated entry to `learning-candidates.md`. Promote to `learnings.md` after 3+ recurrences. Skip if nothing new.

---

## Guardrails

- **Never** run `remove --execute` or `batch-remove --execute` without explicit **AskUserQuestion** confirmation in the same turn. The confirmation in step 6 is the only safety gate.
- **Never** loop `remove --execute` per track when ≥ 2 tracks are removed from the **same** playlist. Use `batch-remove` with a `.scratch/remove-<playlist>.txt` file — see [`docs/commands.md → batch-remove`](../../../docs/commands.md#batch-remove). The per-track loop costs ~3-5 API calls per track and bootstraps Python every time; `batch-remove` is 1 pagination + 1 API call per 100 URIs.
- **Never** ask the user "batch or per-track?" when the answer is obviously batch (≥ 2 tracks, single playlist). Default to `batch-remove`. Only ask if the user has a specific structural reason (e.g. wants to confirm each track separately).
- **Do** loop `remove --execute` when removing **one track from N playlists** — there is no batch equivalent in the Spotify API (one API call per playlist is the floor). For **N tracks × M playlists**, batch per playlist (M `batch-remove` invocations).
- **Never** invent or guess a Spotify track ID. If only "Artist - Title" was given, ask for a URL via **AskUserQuestion** before proceeding.
- **Never** remove from `Random sht` without extra confirmation — it is the script-side catch-all and tracks there may be intentional; the user should say so explicitly.
- **If** the script prints `SKIP: track not found in playlist` (or `SKIP {N} URIs not in playlist` for batch) — explain in Dutch that the track may have been added through the Spotify UI (not via this tool), so the local `.tracks_log.json` log doesn't know about it. In Development Mode the Spotify API also cannot confirm presence. Suggest using `log-import` to seed the log from an Exportify CSV if the track should be tracked.
- **Never** remove from a playlist that is not in `playlists.json`. Validate names before showing the plan.
- Always invoke the venv python (`.venv/bin/python`) from the repo root — IPv4 routing and venv state both depend on it.
- Always double-quote both the track argument and the playlist name to survive spaces, `/`, `'`, and `&`.
- Read `playlists.json` each run — user edits are authoritative.
- User-facing prose is **Dutch**. CLI commands and playlist names stay verbatim.
