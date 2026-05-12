# spotify-playlist-manager

Local toolkit to manage my Spotify playlists via the [Spotify Web API](https://developer.spotify.com/documentation/web-api) using [Spotipy](https://spotipy.readthedocs.io/) and OAuth.

The workflow: I run scripts locally, Spotify grants access via OAuth, and the script (or assistant-generated commands) reads/writes my playlists.

## Setup

### 1. Create a Spotify app

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
2. Click **Create app**.
3. Set the redirect URI to exactly: `http://127.0.0.1:8888/callback`
4. Copy the **Client ID** and **Client Secret**.

### 2. Local environment

```bash
cd ~/spotify-playlist-manager
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure secrets

```bash
cp .env.example .env
# edit .env and paste your Client ID / Client Secret
```

`.env` and `.spotify_token_cache` are gitignored — never commit them.

### 4. Smoke test

```bash
python test_spotify.py
```

A browser tab opens for Spotify login + consent. After approving, the script prints your user info and lists all your playlists.

## playlist_manager.py

CLI for managing the configured target playlists. **Default is dry-run** — nothing is written without `--execute`.

```bash
# List the configured target playlists
python playlist_manager.py list-playlists

# Dry-run: show what would happen
python playlist_manager.py add "https://open.spotify.com/track/<id>" "House"

# Actually add the track
python playlist_manager.py add "https://open.spotify.com/track/<id>" "House" --execute

# Add even if the track is already in the playlist
python playlist_manager.py add "<track>" "House" --execute --allow-duplicate
```

Playlist names accept aliases (e.g. `dnb` → `Drum & Bass`, `chill` → `Rustig / 'anders'`). See `ALIASES` in [playlist_manager.py](playlist_manager.py).

Duplicate protection is on by default: if the track URI is already in the target playlist, the script reports `SKIP` and exits without changes.

## Scopes used

- `playlist-read-private`
- `playlist-read-collaborative`
- `playlist-modify-private`
- `playlist-modify-public`
- `user-library-read`
- `user-read-private`

## Security notes

- **Never commit `.env` or `.spotify_token_cache`** — both contain credentials/tokens.
- The Client Secret stays local; do not paste it into chats or issues.
- Tokens cache locally in `.spotify_token_cache` and refresh automatically.
