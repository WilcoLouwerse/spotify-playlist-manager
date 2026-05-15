# CLI Reference — `list-tracks` and `audit-playlist`

Quick reference for the two CLI commands the audit skill uses. For the authoritative reference, see [`docs/commands.md`](../../../../docs/commands.md).

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

**Empty output:** Spotify dev-tier may return no tracks (stripped playlist contents). In that case use an exportify CSV path as the input instead.

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
- `--csv <path>` — Use an exportify CSV instead of the Spotify API for the track list (required in dev-tier)
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

Same command as [`/playlist-remove`](../../playlist-remove/references/remove-command.md). Used in the audit skill's step 10 to remove confirmed low-confidence tracks. Loop once per track per playlist.

Always double-quote both arguments. Always pass `--execute` (the AskUserQuestion confirmation in step 9 is the safety gate).
