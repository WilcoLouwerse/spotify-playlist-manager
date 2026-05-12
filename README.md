# spotify-playlist-manager

Local CLI to manage my Spotify playlists. Built on the [Spotify Web API](https://developer.spotify.com/documentation/web-api) via [Spotipy](https://spotipy.readthedocs.io/), with optional OpenAI-powered playlist classification for `smart-add`.

```bash
# After setup
python playlist_manager.py list-playlists
python playlist_manager.py add "https://open.spotify.com/track/<id>" "House" --execute
python playlist_manager.py smart-add "https://open.spotify.com/track/<id>" --execute --per-playlist
```

## Documentation

- **[docs/setup.md](docs/setup.md)** — credentials, `.env` values, where to get them (Spotify Developer Dashboard + OpenAI platform), Python venv setup.
- **[docs/commands.md](docs/commands.md)** — CLI reference for every subcommand, including aliases, dry-run behavior, and the duplicate guard.
- **[docs/architecture.md](docs/architecture.md)** — how the code is structured, the OAuth flow, the OpenAI classifier, and the IPv4-only network workaround for WSL.

## Safety defaults

Three layers protect against unintended writes:

1. **Dry-run is the default.** Add `--execute` to actually write.
2. **`smart-add` requires interactive confirmation** (single y/N for all, or `--per-playlist` for individual y/N).
3. **Duplicate guard is always on.** A track already in the target playlist is skipped — no override flag.

## Security notes

- `.env` and `.spotify_token_cache` are gitignored. Never commit them.
- If you leak your Spotify Client Secret, rotate it in the Dashboard immediately.
- If you leak your OpenAI API key, revoke it on the OpenAI platform and create a new one.
