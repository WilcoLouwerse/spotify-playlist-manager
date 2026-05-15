# Architecture

How the code is organised and why certain decisions exist.

## File layout

```
spotify-playlist-manager/
├── .tracks_log.json          # local duplicate-guard log (gitignored, auto-managed)
├── .env                    # secrets (gitignored)
├── .env.example            # template
├── .gitignore              # excludes .env, .venv, token cache, adds log, playlists.json
├── .spotify_token_cache    # OAuth token cache (gitignored, auto-managed by Spotipy)
├── .venv/                  # local virtualenv (gitignored)
├── README.md               # short overview, points into docs/
├── docs/
│   ├── setup.md            # credentials, env vars, playlist config
│   ├── commands.md         # CLI reference
│   └── architecture.md     # this file
├── exportify-exports/      # drop Exportify CSVs here for `log-import` (contents gitignored)
├── playlist_manager.py     # the CLI
├── playlists.json          # local playlist config (gitignored, see playlists.example.json)
├── playlists.example.json  # worked example of the playlist config schema
├── requirements.txt        # pinned dependencies
└── tests/
    ├── test_playlist_manager.py  # pytest unit tests (pure functions)
    └── test_spotify.py           # OAuth smoke test (run as a script)
```

## Components

### `playlist_manager.py`

A single-file CLI built on `argparse`:

- `list-playlists` — prints the playlists in `playlists.json`, or with `--all` lists every writable playlist on the Spotify account.
- `add` — direct, single-target add with duplicate guard.
- `remove` — direct, single-target removal; mirrors `add` — dry-run by default, `--execute` to write. Updates `.tracks_log.json` on success.
- `smart-add` — OpenAI classifier + confirmation prompt + duplicate guard.
- `analyze-only` — same classification pipeline as `smart-add`, no prompts, no writes.
- `list-tracks` — prints every track in a playlist as tab-separated `URI<TAB>Artist - Title`. Read-only; used by skills (`/playlist-audit`, `/playlist-triage`, `/playlist-scan`) to get a track list without a full classification round-trip.
- `review-playlist` — walk a source playlist track-by-track with per-track y/N/s/q.
- `bulk-playlist` — classify every track in a source playlist, show a per-target tally, then apply everything after a single y/N. Uses the local tracks log directly for duplicate detection to keep request volume bounded.
- `scan-for` — pick one target playlist and scan a source playlist for tracks the classifier would route to that target. Same single-y/N UX as `bulk-playlist`, but the output is one candidate list instead of a per-target tally.
- `audit-playlist` — OpenAI-backed batch audit: classifies every track in a playlist and reports a confidence score for each against the playlist's own genre/theme. See `/playlist-audit` skill for the Claude AI + web-search version.
- `log-import` — seeds the local `.tracks_log.json` from a file of track URIs/URLs/IDs (e.g. an Exportify CSV), to cover playlist contents the dev-tier API refuses to expose.

Key data sources:

| Name | Source | Purpose |
|------|--------|---------|
| `playlists.json` | gitignored file at repo root | Playlist names, IDs, aliases, smart-add categorization, special rules, and catch-all configuration (playlist + threshold). Validated at load. See [setup.md → Configure your playlists](setup.md#configure-your-playlists). |
| `playlists.example.json` | committed | Worked example of the schema, also used as the source for `cp playlists.example.json playlists.json`. |
| `SCOPE` | `playlist_manager.py` constant | Space-separated OAuth scopes requested at login. |

### Playlist config loader

`load_config()` reads `playlists.json` once per process and caches the result. `load_config(required=False)` returns `None` instead of exiting when the file is missing — used by `list-playlists --all` so it can still help bootstrap an empty config. `_validate_config()` enforces:

- `playlists` is a non-empty object with 22-char Spotify IDs as values.
- Every `aliases` target resolves to a `playlists` key.
- Every name under `categories.*` resolves to a `playlists` key.
- Every key in `special_rules` resolves to a `playlists` key.
- If `catch_all` is present: `catch_all.playlist` must resolve to a `playlists` key; `catch_all.threshold` (if set) is an int 0–100 (default 85); `catch_all.rule` (if set) is a string.

Validation failures exit cleanly with a pointer to the offending field — no stack trace.

### `tests/`

- `tests/test_playlist_manager.py` — pytest unit tests covering the pure helpers (URI/ID parsing, config validation, catch-all logic, adds-log I/O, classification validation). Run with `pytest` from the repo root.
- `tests/test_spotify.py` — standalone smoke test, run as a script. Uses the same OAuth machinery as `playlist_manager.py` but only reads — useful for verifying `.env` is correct before trying to write anything.

## Authentication

Spotify's Authorization Code Flow, via [Spotipy](https://spotipy.readthedocs.io/):

1. First run prints a URL and opens the browser.
2. User logs in to Spotify and approves the scopes.
3. Spotify redirects to `http://127.0.0.1:8888/callback` with a code.
4. Spotipy's local HTTP server catches the callback, exchanges the code for an access + refresh token, and writes both to `.spotify_token_cache`.
5. Future runs read the cache; if the access token has expired, Spotipy uses the refresh token to renew it silently.

The redirect URI must match exactly what's configured in the Spotify Developer Dashboard. `127.0.0.1` and `localhost` are *not* interchangeable — Spotify rejects mismatches.

## Network quirks

### IPv4-only resolution

WSL2's IPv6 route to `api.spotify.com` is broken — the TCP connect silently hangs until the read timeout fires. Python's `getaddrinfo` returns IPv6 addresses first by default, so requests intermittently failed.

The fix lives at the top of `playlist_manager.py` and `tests/test_spotify.py`:

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

## OpenAI classifier (smart-add)

`classify_track_with_openai(track, max_playlists, min_playlists)` does the heavy lifting:

1. Reads `OPENAI_API_KEY` (and optional `OPENAI_MODEL`, default `gpt-4.1-mini`) from env.
2. Builds a JSON-mode chat completion with:
   - **System**: "You are a strict music classification assistant. Return only valid JSON…"
   - **User**: a structured prompt object containing the full track metadata (artists, album, popularity, etc.), the available playlists **grouped by the buckets in `playlists.json -> "categories"`** (typically `genre` / `mood` / `theme`; falls back to a single `all` bucket if `categories` is empty), and a `rules` section that includes:
     - `classification_signals` — explicit checklist (genre, BPM, energy, mood, lyrics, production, cultural context, meme context, listening scenario).
     - `anti_shortcuts` — forbids classifying on artist name alone, requires weighing multiple independent signals, and tells the model to lower confidence on conflict rather than pick a source.
     - `category_balance` — discourages returning multiple overlapping subgenres, but allows umbrella playlists (declared via `special_rules`) alongside the matching subgenre.
     - `special_playlists` — only included if `playlists.json -> "special_rules"` is non-empty; passes those rules straight through to the model. Used for both narrow buckets ("only meme songs") and inclusive umbrellas ("suggest alongside any electronic subgenre").
     - `max_playlists` / `min_playlists` — driven by the `--max-playlists` and `--min-playlists` CLI flags. Defaults vary per subcommand; for `smart-add` they're 5 / 3.
   - The catch-all playlist (`playlists.json -> "catch_all".playlist`) is **omitted** from `available_playlists` so the model cannot select it. It's appended programmatically post-classification (see [Catch-all and confidence filtering](#catch-all-and-confidence-filtering)).
3. Parses the response JSON. Expected schema:
   ```json
   {
     "genres": [{"genre": "...", "confidence": 0, "reason": "..."}],
     "playlist_matches": [{"playlist": "...", "confidence": 0, "reason": "..."}],
     "short_summary": "..."
   }
   ```
4. Hands the parsed object to `validate_classification`, which enforces: non-empty `playlist_matches`, every `playlist` must exist in `playlists.json -> "playlists"`, every `confidence` must be an integer 0–100. A validation failure aborts the run cleanly.

The model is locked into JSON mode (`response_format={"type": "json_object"}`), and `temperature=0.2` keeps results stable across runs.

### Catch-all and confidence filtering

After classification returns, `smart_add` post-processes the matches:

1. Sort by confidence descending and truncate to `--max-playlists` (default 5 for `smart-add`; other subcommands use 3).
2. If `playlists.json -> "catch_all"` is configured and no remaining match has confidence >= `catch_all.threshold` (default 85), append `{"playlist": catch_all.playlist, "confidence": 100, "reason": "..."}`. This step can push the total to `max-playlists + 1` — the catch-all is intentional overflow. If the catch-all playlist is already in the matches (shouldn't happen since it's hidden from the model, but defensive), nothing is appended.
3. Drop any match with confidence < `--min-confidence` (default 0). The catch-all entry is always confidence 100 so it survives any filter < 100.

The duplicate guard and confirmation prompts run after this pipeline, so the user sees the final filtered set.

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
2. **Interactive confirmation in `smart-add`.** Even with `--execute`, you must answer `y` for each suggested playlist. With `--accept-all`, a single bulk `y/N` covers the whole set.
3. **Duplicate guard.** Before every add, the script checks the local adds log (`.tracks_log.json`, gitignored) — every URI the script has successfully added or has been seeded with via `log-import`, keyed by playlist ID. If present → `SKIP`, no write. No override flag. See [Duplicate detection](#duplicate-detection) below for why this log is authoritative.

## Duplicate detection

`.tracks_log.json` is the primary (and authoritative) source for the duplicate guard. The flow:

- Every successful `add` / `smart-add` write that returns a `snapshot_id` from Spotify is appended to the log.
- The `log-import` subcommand seeds the log from a CSV/text file containing track URIs/URLs/IDs — typically an [Exportify](https://exportify.net) export of an existing playlist, dropped into [`exportify-exports/`](../exportify-exports/) at the repo root. See [commands.md → log-import](commands.md#log-import) for the full workflow.
- `playlist_contains_uri()` checks this log first, then makes a best-effort Spotify API call as a secondary signal. If the API does return URIs, they're consulted too.

Why the log is needed:

The Spotify Web API in this app's tier returns playlist items with the embedded `track` object empty (`uri`, `id`, and `name` are all `null`; only `added_at` survives). That means server-side duplicate detection over the API alone cannot work — every track looks "not present". The log fills that gap. See [Spotify Web API documentation](https://developer.spotify.com/documentation/web-api) for the underlying endpoint behaviour.

Tracks that you added through the Spotify UI (not via this script) and were never seeded via `log-import` are invisible to the guard. Either re-run `log-import` after large UI edits, or edit `.tracks_log.json` by hand.

## February 2026 Spotify API migration

Spotify's [Feb 2026 Dev Mode migration guide](https://developer.spotify.com/documentation/web-api/tutorials/february-2026-migration-guide) lists changes the script will need to track:

- `GET/POST/DELETE/PUT /playlists/{id}/tracks` is renamed to `/playlists/{id}/items`. Spotipy's `playlist_items` and `playlist_add_items` will follow when the library is updated; if not, we'll need to call the new path directly.
- The response shape changes: `tracks.items[].track` becomes `items.items[].item`.
- Tracks lose `available_markets`, `external_ids`, `linked_from`, and `popularity` fields. We currently send `popularity` into the OpenAI prompt; after Feb 2026 it will simply be `None`, which the classifier still handles.
- Batch endpoints (`GET /tracks`, `/albums`, `/artists`) are removed — fetch individually.
- Owner-only constraint: playlist `items` are only returned for playlists the user owns or collaborates on. `list-playlists --all` already filters to that set, so anything you can add to `playlists.json` is also a valid write target post-migration.

App owners must also have an active Spotify Premium subscription from Feb 2026 onwards.

## Adding a new playlist target

1. Run `python playlist_manager.py list-playlists --all` to print every writable playlist on your account in paste-ready JSON, or copy the 22-char ID from the playlist's Spotify URL (`https://open.spotify.com/playlist/<ID>`).
2. Add the entry to `playlists.json`:
   ```json
   "playlists": {
     "My New Playlist": "<id from step 1>"
   }
   ```
3. (Optional) Add an alias under `"aliases"`, and add the name under one of the buckets in `"categories"` so `smart-add` knows whether it's a genre, mood, or theme.
4. Verify with `python playlist_manager.py list-playlists`.

No restart needed — `playlists.json` is read each run. See [setup.md → Configure your playlists](setup.md#configure-your-playlists) for the full schema.

## Adding a new subcommand

`main()` uses `argparse` subparsers. To add a new command, e.g. `my-command`:

1. Define a `my_command(sp, ...)` function alongside the existing command functions.
2. In `main()` register it:
   ```python
   my_parser = subparsers.add_parser("my-command", help="What it does")
   my_parser.add_argument("track", help="...")
   my_parser.add_argument("playlist", help="...")
   my_parser.add_argument("--execute", action="store_true")
   ```
3. Dispatch in the `if/elif` chain:
   ```python
   elif args.command == "my-command":
       my_command(sp, args.track, args.playlist, args.execute)
   ```

Keep the dry-run default and duplicate/safety guards consistent with existing commands (`add`, `remove`, `smart-add`, etc.).
