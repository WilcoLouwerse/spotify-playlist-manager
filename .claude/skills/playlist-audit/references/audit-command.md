# CLI Reference — `list-tracks`, `audit-playlist`, `remove` and `batch-remove`

Quick reference for the CLI commands the audit skill uses. For the authoritative reference, see [`docs/commands.md`](../../../../docs/commands.md).

---

## `list-tracks` — get a raw track list

```bash
.venv/bin/python playlist_manager.py list-tracks "<playlist>"
```

Prints every track in the playlist as tab-separated `URI\tArtist - Title`. The first line is a summary header; all subsequent lines are tracks.

**Accepted inputs for `<playlist>`:**
- Playlist name from `playlists.json` (e.g. `"House"`)
- Alias from `playlists.json` (e.g. `"dnb"`)
- Spotify playlist URL (`https://open.spotify.com/playlist/<id>`)
- Spotify URI (`spotify:playlist:<id>`)
- Path to an exportify CSV (e.g. `exportify-exports/House.csv`)

**Example output:**
```
Playlist: House (42 tracks)
spotify:track:abc123	Martin Garrix - Animals
spotify:track:def456	Dua Lipa - Levitating
```

**Parsing in the skill:**
1. Skip line 1 (the `Playlist: ...` header)
2. For each remaining line: split on the first `\t` → `[uri, label]`
3. Keep `{uri, label}` pairs in memory for the audit loop

**No tracks:** instead of a `Playlist:` header the command prints `No readable tracks returned for '<name>': the playlist is empty, or Spotify hides its contents. …`. For a playlist in `playlists.json` that almost always means it is empty; pass an exportify CSV path only for a playlist Spotify can't read.

---

## Freshness check via .tracks_log.json

Only relevant when the track list came from a CSV under `exportify-exports/` (the fallback for when Spotify returns no tracks). When the Spotify API returned tracks directly, skip this check — the API is authoritative.

CSVs are point-in-time exports. The log is appended by every successful `--execute` write (`add`, `batch-add`, `smart-add`, `review-playlist`, `bulk-playlist`, `scan-for`) and pruned by `remove` / `batch-remove`, so it can hold URIs that the CSV snapshot missed.

**How**:
1. Look up the audited playlist's Spotify ID via `playlists.json -> playlists[<playlist-name>]`.
2. Read `.tracks_log.json` and grab the array at `[<playlist-id>]` (empty array if the key is missing).
3. Build the set of URIs in the parsed `list-tracks` output (the CSV-backed list).
4. Compute `log_only = log_uris - listed_uris`.

**Surfacing a stale CSV** — if `len(log_only) > 0`, use **AskUserQuestion** in Dutch:

> "De CSV `<file>` mist {N} tracks die wel in `.tracks_log.json` voor {playlist} staan — de CSV is mogelijk verouderd. Hoe wil je verder?"
> - **Audit alleen de CSV-tracks** — accepteer dat recente toevoegingen niet worden gecontroleerd.
> - **Vraag een verse CSV-export aan** *(via [exportify.net](https://exportify.net))* — stop de audit; user re-exports.
> - **Audit de extra URIs ook** — voor elke URI in `log_only` haal het label op via een dry-run `add "<uri>" "<playlist>"` (zonder `--execute`; print `Track: Artist - Title` en schrijft niets) of via WebSearch; voeg ze toe aan de auditlijst.

If `log_only` is empty, proceed silently.

**Cases where the log is *less* complete than the CSV**: do not warn. The log only records adds made via the CLI; tracks added through Spotify's UI are in the CSV but not the log. That's expected, not stale.

---

## `audit-playlist` — batch audit via OpenAI (quick mode)

```bash
.venv/bin/python playlist_manager.py audit-playlist "<playlist>" [--csv <path>] [--min-confidence <0-100>]
```

Classifies every track using OpenAI and prints:
- Per-track: `[N/total] Artist - Title` then `  <confidence>% — <reason>`
- A summary: counts in three bands (≥80%, 60-79%, <60%)
- A "Tracks below X%" block with URIs for removal candidates

**Flags:**
- `--csv <path>` — Use an exportify CSV instead of the Spotify API for the track list (only needed when Spotify returns no tracks)
- `--min-confidence <int>` — Default 60. Tracks below this threshold are listed as removal candidates with their URIs

**Parsing in the skill (quick mode):**
After running `audit-playlist`, parse stdout:
1. The summary block gives the score distribution (three numbers to show in the report)
2. The "Tracks below X%" block gives the removal candidates — extract each `<confidence>% — <label>` line and the `URI: <uri>` line below it

For web-first mode, the skill does NOT call `audit-playlist` — it uses `list-tracks` for the track list and does its own classification via WebSearch.

---

## `remove` — remove a confirmed track

```bash
.venv/bin/python playlist_manager.py remove "<track-uri>" "<Playlist Name>" --execute
```

Same command as [`/playlist-remove`](../../playlist-remove/references/remove-command.md). Used in the audit skill's step 10 only when exactly one track is selected; for two or more use `batch-remove` (below).

---

## `batch-remove` — remove several confirmed tracks

```bash
.venv/bin/python playlist_manager.py batch-remove "<Playlist Name>" .scratch/audit-<playlist>-remove.txt --execute
```

The file holds one URI per line. Output: `Target playlist:` / `Playlist ID:` / `Input URIs:` headers, an optional `SKIP N URIs not in playlist.`, `To remove: N URIs in B batch(es) of up to 100.`, one `  - batch of N: snapshot …` line per batch, and finally `DONE: removed R, failed F, skipped S (not in playlist).`

Always double-quote both arguments. Always pass `--execute` (the AskUserQuestion confirmation in step 9 is the safety gate).
