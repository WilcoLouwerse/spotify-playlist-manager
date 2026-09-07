# Removing a track via `playlist_manager.py`

When the user confirms a removal, the skill invokes the project's `remove` CLI command. Read [`docs/commands.md → remove`](../../../../docs/commands.md#remove) for the authoritative reference. This page is a fast index of what to call, with what flags, and what output to expect.

---

## Command — only `remove`

```bash
.venv/bin/python playlist_manager.py remove "<track>" "<Playlist Name>" --execute
```

Run from the repo root. Always pass `--execute` — the skill has already confirmed with the user via **AskUserQuestion**.

### Argument rules

- `<track>` — Spotify track URL (`https://open.spotify.com/track/<id>`), URI (`spotify:track:<id>`), or bare 22-char ID. Use verbatim from the user's original message. **Never invent or guess one.**
- `<Playlist Name>` — must match a key under `"playlists"` in [`playlists.json`](../../../../playlists.json) or an entry under `"aliases"`. Case-insensitive. **Always double-quote** the name.

Special characters to handle:
- `Jazz / Funk / Soul` → `"Jazz / Funk / Soul"`
- `Rustig / 'anders'` → `"Rustig / 'anders'"` (single quotes inside double quotes are fine)

---

## What the user will see

From [`docs/commands.md`](../../../../docs/commands.md):

- **Dry-run by default** — Without `--execute` the script prints what it *would* do and exits. The skill always passes `--execute` because it confirmed with the user.
- **`SKIP: track not found in playlist. No changes made.`** — The track was not found via the local `.tracks_log.json` log or the Spotify API. Most likely it was added to the playlist through the Spotify UI (not via this tool). In Development Mode, the Spotify API also returns empty track lists from `playlist_items`, so this SKIP can fire even when the track is truly in the playlist. Tip: run `log-import` to seed the log from an Exportify CSV, or switch to production Spotify access.
- **`DONE: track removed (snapshot …)`** — The track was found and removed. The snapshot confirms the change was written to Spotify.
- **`FAILED: Spotify returned …`** — API error. Surface verbatim; the user may need to re-authenticate or check their Spotify app settings.
- **IPv4 only** — Spotify's IPv6 route is broken on WSL; the script forces IPv4. No skill action needed; the first call may take a moment.

---

## Effect on `.tracks_log.json`

When a removal succeeds, the script removes the track URI from `.tracks_log.json` for that playlist. This means a future `add` call for the same track will no longer see it as a duplicate and can add it back cleanly.

If the track was added outside this tool (Spotify UI) and is not in `.tracks_log.json`, the removal still succeeds on the Spotify side but there is nothing to remove from the local log — that's expected.

---

## Looping over multiple playlists

When the user wants to remove a track from more than one playlist, loop `remove --execute` once per playlist:

```bash
.venv/bin/python playlist_manager.py remove "<track>" "<Playlist A>" --execute
.venv/bin/python playlist_manager.py remove "<track>" "<Playlist B>" --execute
```

Run sequentially and report each result verbatim before moving to the next.
