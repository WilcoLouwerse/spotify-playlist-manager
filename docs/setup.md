# Setup

This document walks through every credential the project needs, where to get it, and how to put it in `.env`.

`.env` lives at the repository root next to [playlist_manager.py](../playlist_manager.py). It is **gitignored** — never commit it. A template lives at [.env.example](../.env.example).

## Required values

| Variable | Used by | Where to get it |
|----------|---------|-----------------|
| `SPOTIPY_CLIENT_ID` | All commands | Spotify Developer Dashboard (see below) |
| `SPOTIPY_CLIENT_SECRET` | All commands | Spotify Developer Dashboard |
| `SPOTIPY_REDIRECT_URI` | OAuth flow | Set to `http://127.0.0.1:8888/callback` (must match the dashboard exactly) |
| `OPENAI_API_KEY` | `smart-add` only | OpenAI platform (see below) |
| `OPENAI_MODEL` | `smart-add` only (optional) | Defaults to `gpt-4.1-mini` if unset |

## Spotify credentials

1. Open https://developer.spotify.com/dashboard and log in with your Spotify account.
2. Click **Create app**.
3. Fill in:
   - **App name**: anything (e.g. `Wilco Playlist Manager`).
   - **App description**: anything (e.g. `Personal CLI to manage my playlists`).
   - **Redirect URI**: exactly `http://127.0.0.1:8888/callback` — case- and path-sensitive. Click **Add**.
   - Tick the Spotify Developer Terms of Service.
4. Click **Save**.
5. On the app page click **Settings**. You will see:
   - **Client ID** → copy into `SPOTIPY_CLIENT_ID`.
   - **Client secret** → click **View client secret** → copy into `SPOTIPY_CLIENT_SECRET`.

If you ever expose the Client Secret (paste it in chat, push it to a public repo, screenshot it), open the same Settings page and click **Rotate client secret** to invalidate the leaked one. Then update `.env`.

### Scopes used

The OAuth flow asks for the following scopes (defined in [playlist_manager.py](../playlist_manager.py)):

- `playlist-read-private`
- `playlist-read-collaborative`
- `playlist-modify-private`
- `playlist-modify-public`
- `user-library-read`
- `user-read-private`

You only consent once. The token is cached in `.spotify_token_cache` (also gitignored) and refreshes automatically.

## OpenAI credential

Only required for `smart-add`. The plain `add` and `list-playlists` commands work without it.

1. Open https://platform.openai.com/api-keys.
2. Log in (or sign up) and add a payment method if you don't have one — the API is pay-as-you-go. `gpt-4.1-mini` (the default model) costs roughly $0.0001–$0.0003 per `smart-add` call.
3. Click **Create new secret key**.
4. Give it a recognisable name (e.g. `wilco-playlist-manager`).
5. Copy the key (it starts with `sk-...`) and paste it into `OPENAI_API_KEY` in `.env`. **You cannot see it again** after closing the dialog — if you lose it, revoke it on the same page and create a new one.

### Choosing a model

Override the default with `OPENAI_MODEL` in `.env`, e.g.:

```
OPENAI_MODEL=gpt-4.1-mini
```

`gpt-4.1-mini` is the default — strong classification quality at a low price (~$0.0001 per call). If you want to save more, try `gpt-4o-mini`. If you want better calls and don't mind paying, try `gpt-4.1` or `gpt-4o`.

## Putting it together

Your final `.env` looks like:

```
SPOTIPY_CLIENT_ID=...
SPOTIPY_CLIENT_SECRET=...
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback

OPENAI_API_KEY=sk-...
# OPENAI_MODEL=gpt-4.1-mini
```

After editing `.env`, the next time you run any command the new values are picked up automatically — no restart needed.

## Local Python environment

Once `.env` is filled in, set up the runtime once:

```bash
cd ~/spotify-playlist-manager
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Ubuntu/WSL you may need `sudo apt install python3.12-venv` before `python3 -m venv .venv` will work.

After that, run any command with the activated venv:

```bash
python playlist_manager.py list-playlists
```

See [commands.md](commands.md) for the full CLI reference.
