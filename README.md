# spotify-playlist-manager

Local CLI to manage my Spotify playlists. Built on the [Spotify Web API](https://developer.spotify.com/documentation/web-api) via [Spotipy](https://spotipy.readthedocs.io/), with optional OpenAI-powered playlist classification for `smart-add`.

```bash
# After setup
python playlist_manager.py list-playlists
python playlist_manager.py add "https://open.spotify.com/track/<id>" "House" --execute
python playlist_manager.py remove "https://open.spotify.com/track/<id>" "House" --execute
python playlist_manager.py smart-add "https://open.spotify.com/track/<id>" --execute --accept-all
python playlist_manager.py review-playlist "https://open.spotify.com/playlist/<id>" --execute
python playlist_manager.py bulk-playlist "https://open.spotify.com/playlist/<id>" --execute
python playlist_manager.py scan-for "House" "https://open.spotify.com/playlist/<id>" --execute
```

## Documentation

- **[docs/setup.md](docs/setup.md)** — credentials, `.env` values, where to get them (Spotify Developer Dashboard + OpenAI platform), `playlists.json` config (see [playlists.example.json](playlists.example.json) for the schema), Python venv setup.
- **[docs/commands.md](docs/commands.md)** — CLI reference for every subcommand, including `list-playlists --all` (Spotify discovery), aliases, dry-run behavior, and the duplicate guard.
- **[docs/architecture.md](docs/architecture.md)** — how the code is structured, the OAuth flow, the OpenAI classifier, and the IPv4-only network workaround for WSL.

## Claude Code skills

If you're working in this repo with [Claude Code](https://claude.com/claude-code), the repo ships seven slash commands:

- `/playlist-match` — paste a Spotify URL or *"Artist - Title"* and Claude classifies the genres, recommends matching playlists from your `playlists.json`, and can invoke `add` for you.
- `/playlist-triage` — sort a whole source playlist into many target playlists in one go, via `review-playlist` (per-track y/N) or `bulk-playlist` (single y/N).
- `/playlist-scan` — mine a source playlist for tracks that fit *one* chosen target, via `scan-for`.
- `/playlist-remove` — remove a track from one or more playlists via `remove`.
- `/playlist-audit` — audit a playlist's genre/theme fit: confidence scores per track and one-click removal of low-confidence tracks.
- `/playlist-log-import` — seed the local duplicate-guard log (`.tracks_log.json`) for a playlist from an Exportify CSV, via `log-import`.
- `/playlist-config` — bootstrap or extend `playlists.json` from your Spotify account, via `list-playlists --all`.

Full skill reference: [.claude/docs/commands.md](.claude/docs/commands.md). New to Claude Code in VS Code? See [docs/vscode-claude-setup.md](docs/vscode-claude-setup.md) for the WSL + extension + auth walkthrough. Contributor docs (skill authoring, doc conventions, the command index) live in [.claude/docs/README.md](.claude/docs/README.md).

## Safety defaults

Three layers protect against unintended writes:

1. **Dry-run is the default.** Add `--execute` to actually write.
2. **`smart-add` requires interactive confirmation** (per-playlist y/N by default, or `--accept-all` for a single bulk y/N).
3. **Duplicate guard is always on.** Reads from a local `.tracks_log.json` — every URI the script has successfully added or has been seeded with via `log-import`. Run `log-import` once per playlist after setup (see [docs/commands.md → log-import](docs/commands.md#log-import)) to cover tracks the script didn't add. Background: [docs/architecture.md → Duplicate detection](docs/architecture.md#duplicate-detection).

## Security notes

- `.env`, `.spotify_token_cache`, and `playlists.json` are gitignored. Never commit them.
- If you leak your Spotify Client Secret, rotate it in the Dashboard immediately.
- If you leak your OpenAI API key, revoke it on the OpenAI platform and create a new one.
