# Architecture

How the code is organised and why certain decisions exist.

## File layout

```
spotify-playlist-manager/
├── .env                    # secrets (gitignored)
├── .env.example            # template
├── .gitignore              # excludes .env, .venv, token cache
├── .spotify_token_cache    # OAuth token cache (gitignored, auto-managed by Spotipy)
├── .venv/                  # local virtualenv (gitignored)
├── README.md               # short overview, points into docs/
├── docs/
│   ├── setup.md            # credentials and env vars
│   ├── commands.md         # CLI reference
│   └── architecture.md     # this file
├── playlist_manager.py     # the CLI
├── requirements.txt        # pinned dependencies
└── test_spotify.py         # OAuth smoke test
```

## Components

### `playlist_manager.py`

A single-file CLI built on `argparse` with three subcommands:

- `list-playlists` — prints the `PLAYLISTS` dict.
- `add` — direct, single-target add with duplicate guard.
- `smart-add` — OpenAI classifier + confirmation prompt + duplicate guard.

Key data structures:

| Name | Type | Purpose |
|------|------|---------|
| `PLAYLISTS` | `dict[str, str]` | Playlist name → Spotify playlist ID. Hard-coded; edit this to manage which playlists the script can write to. |
| `ALIASES` | `dict[str, str]` | Lowercase alias → canonical `PLAYLISTS` key. Lets you type `dnb` instead of `Drum & Bass`. |
| `SCOPE` | `str` | Space-separated OAuth scopes requested at login. |

### `test_spotify.py`

A standalone smoke test. Uses the same OAuth machinery as `playlist_manager.py` but only reads — useful for verifying `.env` is correct before trying to write anything.

## Authentication

Spotify's Authorization Code Flow, via [Spotipy](https://spotipy.readthedocs.io/):

1. First run prints a URL and opens the browser.
2. User logs in to Spotify and approves the scopes.
3. Spotify redirects to `http://127.0.0.1:8888/callback` with a code.
4. Spotipy's local HTTP server catches the callback, exchanges the code for an access + refresh token, and writes both to `.spotify_token_cache`.
5. Future runs read the cache; if the access token has expired, Spotipy uses the refresh token to renew it silently.

The redirect URI must match exactly what's configured in the Spotify Developer Dashboard. `127.0.0.1` and `localhost` are *not* interchangeable — Spotify rejects mismatches.

## OpenAI classifier (smart-add)

`classify_track_with_openai(track)` does the heavy lifting:

1. Reads `OPENAI_API_KEY` (and optional `OPENAI_MODEL`, default `gpt-4.1-mini`) from env.
2. Builds a JSON-mode chat completion with:
   - **System**: "You are a strict music classification assistant. Return only valid JSON…"
   - **User**: a structured prompt object containing the full track metadata (artists, album, popularity, etc.), the available playlists **grouped by category** (`genre` / `mood` / `theme`), and a `rules` section that includes:
     - `classification_signals` — explicit checklist (genre, BPM, energy, mood, lyrics, production, cultural context, meme context, listening scenario).
     - `anti_shortcuts` — forbids classifying on artist name alone, requires weighing multiple independent signals, and tells the model to lower confidence on conflict rather than pick a source.
     - `category_balance` — discourages returning multiple overlapping subgenres from the genre list.
     - `special_playlists` — semantics for `Funny meme`, `Ket420`, `Hooyah`.
     - `electronic_music` — catch-all rule for electronic tracks that don't fit a specific subgenre.
3. Parses the response JSON. Expected schema:
   ```json
   {
     "genres": [{"genre": "...", "confidence": 0, "reason": "..."}],
     "playlist_matches": [{"playlist": "...", "confidence": 0, "reason": "..."}],
     "short_summary": "..."
   }
   ```
4. Hands the parsed object to `validate_classification`, which enforces: non-empty `playlist_matches`, ≤ 5 items, every `playlist` must exist in `PLAYLISTS`, every `confidence` must be an integer 0–100. A validation failure aborts the run cleanly.

The model is locked into JSON mode (`response_format={"type": "json_object"}`), and `temperature=0.2` keeps results stable across runs.

### Track metadata

`get_track(sp, track_input)` returns a dict (not a tuple) so the same lookup feeds both `add` and the OpenAI prompt:

| Key | Source | Notes |
|-----|--------|-------|
| `id`, `uri`, `name`, `artists`, `album`, `release_date`, `popularity`, `duration_ms`, `explicit`, `spotify_url` | Spotify track endpoint | |
| `label` | derived | `"<first artist> - <title>"` used for printable headers |
| `metadata_available` | derived | `False` when the catalog lookup fails — `smart-add` aborts cleanly in that case |

## Safety / guard rails

Three defences against unintended writes:

1. **Dry-run default.** No write ever happens without `--execute`.
2. **Interactive confirmation in `smart-add`.** Even with `--execute`, you must answer `y`. With `--per-playlist`, you confirm per playlist.
3. **Duplicate guard.** Before every add, the script paginates the target playlist's tracks and checks for the URI. If present → `SKIP`, no write. No override flag.

## Network quirks

### IPv4-only resolution

WSL2's IPv6 route to `api.spotify.com` is broken — the TCP connect silently hangs until the read timeout fires. Python's `getaddrinfo` returns IPv6 addresses first by default, so requests intermittently failed.

The fix lives at the top of `playlist_manager.py` and `test_spotify.py`:

```python
import socket
_orig_getaddrinfo = socket.getaddrinfo
def _ipv4_only_getaddrinfo(*args, **kwargs):
    return [info for info in _orig_getaddrinfo(*args, **kwargs) if info[0] == socket.AF_INET]
socket.getaddrinfo = _ipv4_only_getaddrinfo
```

This filters out AAAA records before any HTTPS connection is opened. No system change required.

### Request timeout and retries

The Spotipy client is constructed with `requests_timeout=30, retries=5`. The default of 5 seconds was too aggressive for the occasionally slow catalog endpoints.

### Best-effort track lookup

`get_track()` wraps `sp.track(track_id)` in a try/except. If the catalog endpoint times out (a recurring Spotify-side issue), it falls back to using the bare URI. `add` still works in that case; `smart-add` aborts because it needs the artist + title to classify.

## Adding a new playlist target

1. Open the playlist on Spotify, click "..." → Share → Copy link to playlist. Extract the ID (path segment after `/playlist/`).
2. Add an entry to `PLAYLISTS` in `playlist_manager.py`:
   ```python
   "My New Playlist": "<id from step 1>",
   ```
3. (Optional) Add an alias in `ALIASES` for shorthand.
4. Verify with `python playlist_manager.py list-playlists`.

No restart needed — `PLAYLISTS` is read each run.

## Adding a new subcommand

`main()` uses `argparse` subparsers. To add `remove`, for example:

1. Define a `remove_track(sp, ...)` function next to `add_track`.
2. In `main()` add:
   ```python
   remove_parser = subparsers.add_parser("remove", help="Remove a track from a playlist")
   remove_parser.add_argument("track", help="...")
   remove_parser.add_argument("playlist", help="...")
   remove_parser.add_argument("--execute", action="store_true")
   ```
3. Dispatch:
   ```python
   elif args.command == "remove":
       remove_track(sp, args.track, args.playlist, args.execute)
   ```

Keep the dry-run default and duplicate/safety guards consistent with existing commands.
