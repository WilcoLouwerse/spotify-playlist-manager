# Commands

CLI reference for [playlist_manager.py](../playlist_manager.py). Run every command from the repo root with the venv active.

## Global behavior

- **Dry-run by default.** Commands that write to Spotify (`add`, `smart-add`) print what they *would* do and exit. Add `--execute` to actually write.
- **Duplicate guard is always on.** Before writing, the script consults a local log (`.adds_log.json`) of everything it has previously added, plus Spotify's playlist contents. If the URI is found in either, it exits with `SKIP`. There is no override flag. See [architecture.md → Extended Quota Mode](architecture.md#extended-quota-mode-development-tier-restrictions) for why the local log exists.
- **IPv4 only.** The script forces IPv4 resolution because WSL's IPv6 route to `api.spotify.com` is broken. See [architecture.md](architecture.md) for the why.

## `list-playlists`

Print the configured target playlists.

```bash
python playlist_manager.py list-playlists
```

Output is the names defined in the `PLAYLISTS` dictionary in [playlist_manager.py](../playlist_manager.py). These are the only playlists the `add` and `smart-add` commands can write to.

To add a new playlist target, edit `PLAYLISTS` in the script and paste the playlist's Spotify ID (the path segment in the URL: `https://open.spotify.com/playlist/<ID>`).

## `add`

Add a single track to one specific playlist.

```bash
# Dry-run — shows what would happen, writes nothing
python playlist_manager.py add "https://open.spotify.com/track/<id>" "House"

# Actually add the track
python playlist_manager.py add "https://open.spotify.com/track/<id>" "House" --execute
```

### Arguments

| Argument | Description |
|----------|-------------|
| `track` | Spotify track URL (`https://open.spotify.com/track/...`), URI (`spotify:track:...`), or bare ID |
| `playlist` | Target playlist name — must match `PLAYLISTS` or an alias in `ALIASES` (case-insensitive) |
| `--execute` | Without this flag, nothing is written |

### Playlist aliases

The `ALIASES` map in the script accepts common shorthands. Examples:

| Alias | Resolves to |
|-------|-------------|
| `dnb`, `drum and bass` | `Drum & Bass` |
| `chill`, `calm` | `Rustig / 'anders'` |
| `pop` | `Pop / Mainstream` |
| `metal`, `rock` | `Metal & Rock` |
| `edm`, `electronic music` | `Electronic Music` |

See the full list in [playlist_manager.py](../playlist_manager.py).

### Exit behavior

- Track already in playlist → prints `SKIP: track already in playlist` and exits.
- Playlist name not recognised → raises `ValueError: Unknown playlist: ...`.
- Spotify catalog endpoint times out → still adds, but prints `(track lookup failed: ReadTimeout; continuing with URI only)` and uses the URI instead of "Artist - Title" in output.

## `smart-add`

Classify a track with OpenAI, confirm interactively, then add it to the suggested playlists.

```bash
# Dry-run — classify and prompt for confirmation, write nothing
python playlist_manager.py smart-add "https://open.spotify.com/track/<id>"

# Real run — same flow, writes to Spotify after y/N
python playlist_manager.py smart-add "https://open.spotify.com/track/<id>" --execute

# Confirm per playlist instead of one y/N for all
python playlist_manager.py smart-add "https://open.spotify.com/track/<id>" --execute --per-playlist
```

### Flow

1. Look up rich track metadata on Spotify (artists, album, release date, popularity, explicit flag, URL).
2. Ask OpenAI to pick 1–5 of the configured playlists that fit the track. The prompt includes special rules for `Funny meme`, `Ket420`, and `Hooyah`, and an `Electronic Music` catch-all rule. The response also includes inferred genres and a short summary.
3. Print the recommendation (track header, summary, genres, suggested playlists).
4. Compute **Pending actions** — for each suggestion, the script checks the duplicate guard and labels it `ADD` or `SKIP` before any confirmation.
5. Prompt for confirmation:
   - **Default**: single `y/N` that accepts all `ADD` actions at once.
   - **`--per-playlist`**: ask `y/N` separately for each `ADD` action. Rejecting one keeps the rest of the run going.
6. For each accepted playlist: either dry-run print or POST the add (under `--execute`).

`y`, `yes`, `j`, and `ja` are all accepted as confirmation.

### Example output

```
============================================================
Track: Bakermat, Nic Hanson - Walk That Walk
Album: Walk That Walk
Spotify: https://open.spotify.com/track/1W5mUuAOQSSKUbLOt7cDhq
============================================================

Summary:
Bright, uplifting deep-house track with festival energy.

Genres:
- deep house — 88% — driving bassline with vocal hook
- tropical house — 64% — bright melodies, summery vibe

Suggested playlists:
- House — 92% — uplifting deep-house with vocals
- Party — 84% — high-energy festival vibe
- Happy tunes — 78% — bright, major key

Pending actions:
- ADD: House (92%)
- SKIP: already in Party
- ADD: Happy tunes (78%)

Add this track to the listed playlists? [y/N]: ja

- House: ADDED
- Happy tunes: ADDED
```

### Arguments

| Argument | Description |
|----------|-------------|
| `track` | Spotify track URL, URI, or ID |
| `--execute` | Without this flag, accepted suggestions print `DRY RUN (would add)` instead of writing |
| `--per-playlist` | Ask y/N for each suggestion separately instead of one prompt for all |

### Requirements

- `OPENAI_API_KEY` set in `.env` — see [setup.md](setup.md).
- Spotify's `/v1/tracks/{id}` endpoint must respond. If it times out, classification cannot proceed and the script aborts cleanly. Fall back to plain `add` in that case.

### Cost

`gpt-4.1-mini` (the default) costs roughly $0.0001–$0.0003 per `smart-add` call, depending on the size of the JSON prompt. Override the model via `OPENAI_MODEL` in `.env` if you want better classifications and don't mind the cost.

## `test_spotify.py`

Not a subcommand — a standalone smoke test that authenticates with Spotify and lists all your playlists. Useful for confirming OAuth works.

```bash
python test_spotify.py
```

The first run opens a browser tab for consent; subsequent runs reuse the cached token.
