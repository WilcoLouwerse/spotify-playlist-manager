# spotify-playlist-manager

Local CLI to manage my Spotify playlists. Built on the [Spotify Web API](https://developer.spotify.com/documentation/web-api) via [Spotipy](https://spotipy.readthedocs.io/), with optional OpenAI-powered playlist classification for `smart-add`, `analyze-only`, `review-playlist`, `bulk-playlist`, `scan-for` and `audit-playlist`.

```bash
# After setup
python playlist_manager.py list-playlists
python playlist_manager.py add "https://open.spotify.com/track/<id>" "House" --execute
python playlist_manager.py remove "https://open.spotify.com/track/<id>" "House" --execute
python playlist_manager.py like "https://open.spotify.com/track/<id>" --execute
python playlist_manager.py smart-add "https://open.spotify.com/track/<id>" --execute --accept-all
python playlist_manager.py review-playlist "https://open.spotify.com/playlist/<id>" --execute
python playlist_manager.py bulk-playlist "https://open.spotify.com/playlist/<id>" --execute
python playlist_manager.py scan-for "House" "https://open.spotify.com/playlist/<id>" --execute
```

## Documentation

- **[docs/setup.md](docs/setup.md)** — credentials and `.env` values (Spotify Developer Dashboard + OpenAI platform), Python venv setup, connecting to Spotify (smoke test + troubleshooting), and `playlists.json` config (see [playlists.example.json](playlists.example.json) for the schema).
- **[docs/commands.md](docs/commands.md)** — CLI reference for every subcommand, including `list-playlists --all` (Spotify discovery), aliases, dry-run behavior, and the duplicate guard.
- **[docs/architecture.md](docs/architecture.md)** — how the code is structured, the OAuth flow, the OpenAI classifier, and the IPv4-only network workaround for WSL.

## Claude Code skills

If you're working in this repo with [Claude Code](https://claude.com/claude-code), the repo ships eight slash commands:

- `/playlist-match` — paste a Spotify URL or *"Artist - Title"* and Claude classifies the genres, recommends matching playlists from your `playlists.json`, and can invoke `add` for you — every track it adds to a playlist also goes into your Liked Songs via `like`.
- `/playlist-triage` — sort a whole source playlist into many target playlists in one go, via `review-playlist` (per-track y/N) or `bulk-playlist` (single y/N).
- `/playlist-scan` — mine a source playlist for tracks that fit *one* chosen target, via `scan-for`.
- `/playlist-remove` — remove a track from one or more playlists via `remove`.
- `/playlist-audit` — audit a playlist's genre/theme fit: confidence scores per track and one-click removal of low-confidence tracks.
- `/playlist-log-import` — seed the local fallback duplicate log (`.tracks_log.json`) for a playlist from an Exportify CSV, via `log-import`. Only needed when Spotify hides a playlist's contents.
- `/playlist-config` — bootstrap or extend `playlists.json` from your Spotify account, via `list-playlists --all`.
- `/event-radar` — get personalised concert and festival recommendations from the artists in your playlists, filtered on your free dates, genres and venue size; writes the lists to `docs/events/`.

Full skill reference: [.claude/docs/commands.md](.claude/docs/commands.md). New to Claude Code in VS Code? See [docs/vscode-claude-setup.md](docs/vscode-claude-setup.md) for the WSL + extension + auth walkthrough. Contributor docs (skill authoring, doc conventions, the command index) live in [.claude/docs/README.md](.claude/docs/README.md).

## Safety defaults

Three layers protect against unintended writes:

1. **Dry-run is the default.** Add `--execute` to actually write.
2. **`smart-add` requires interactive confirmation** (per-playlist y/N by default, or `--accept-all` for a single bulk y/N).
3. **Duplicate guard is always on.** Before every add the script reads the playlist's current contents from Spotify, so tracks you added in the Spotify app are caught too. If Spotify ever hides a playlist's contents, it falls back to the local `.tracks_log.json` (seeded via [`log-import`](docs/commands.md#log-import)). Background: [docs/architecture.md → Duplicate detection](docs/architecture.md#duplicate-detection).

## Security notes

- `.env`, `.spotify_token_cache`, `playlists.json`, `event-radar.config.json`, `.tracks_log.json` and the contents of `exportify-exports/` are gitignored. Never commit them.
- If you leak your Spotify Client Secret, rotate it in the Dashboard immediately.
- If you leak your OpenAI API key, revoke it on the OpenAI platform and create a new one.
