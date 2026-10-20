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

Before you start, check two account rules that apply to every app in Spotify's Development Mode since February 2026 (see the [Feb 2026 migration guide](https://developer.spotify.com/documentation/web-api/tutorials/february-2026-migration-guide)):

- **The app owner needs an active Spotify Premium subscription.** Create the app with the same Spotify account whose playlists you manage. If the owner's Premium lapses, every API call fails until it is renewed.
- **At most 5 users per app.** The owner can always log in. Anyone else has to be added under the app's **User Management** tab (name + the e-mail address of their Spotify account) before they can grant consent.

1. Open https://developer.spotify.com/dashboard and log in with your Spotify account.
2. Click **Create app**.
3. Fill in:
   - **App name**: anything (e.g. `Wilco Playlist Manager`).
   - **App description**: anything (e.g. `Personal CLI to manage my playlists`).
   - **Redirect URI**: exactly `http://127.0.0.1:8888/callback` — case- and path-sensitive. Click **Add**. Spotify refuses `localhost` as a redirect URI; it has to be the loopback IP ([Spotify: Redirect URIs](https://developer.spotify.com/documentation/web-api/concepts/redirect_uri)).
   - **Which API/SDKs are you planning to use?**: tick **Web API**.
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
- `user-library-modify` (used by `like` to add tracks to Liked Songs)
- `user-read-private`

You only consent once. The token is cached in `.spotify_token_cache` (also gitignored) and refreshes automatically.

When a new version adds a scope to this list, the cached token does not pick it up and commands that need it fail with `403`. Delete `.spotify_token_cache` and run any command to consent again.

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

> Developing this repo from VS Code + Claude Code on Windows? Run through [vscode-claude-setup.md](vscode-claude-setup.md) first (WSL, the Claude Code extension, auth), then come back here for the Python venv.

Once `.env` is filled in, set up the runtime once:

```bash
cd ~/spotify-playlist-manager
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Ubuntu/WSL you may need `sudo apt install python3.12-venv` before `python3 -m venv .venv` will work.

Run every command from the repo root with the venv activated (`source .venv/bin/activate`), or call `.venv/bin/python` directly.


## Connect to Spotify

Log in once and check the connection before you configure playlists. The smoke test only reads, so it is safe to run at any time:

```bash
python tests/test_spotify.py
```

1. The script opens the Spotify consent page in your browser. On WSL it opens in the Windows browser; if no browser appears, copy the URL the terminal prints into one.
2. Log in with the app owner's account (or a user added under **User Management**) and click **Agree**.
3. Spotify redirects to `http://127.0.0.1:8888/callback`. The script catches that callback itself, stores the token in `.spotify_token_cache` and prints `Connected as: <your name>` followed by your playlists.

From then on every command reuses the cached token and refreshes it silently. Background on the flow: [architecture.md → Authentication](architecture.md#authentication).

### When the connection fails

| Symptom | Cause | Fix |
|---------|-------|-----|
| Browser shows `INVALID_CLIENT: Invalid redirect URI` | `SPOTIPY_REDIRECT_URI` in `.env` differs from the dashboard entry | Make both exactly `http://127.0.0.1:8888/callback` |
| Browser shows `INVALID_CLIENT: Invalid client` | Wrong `SPOTIPY_CLIENT_ID` | Copy it again from the app's **Settings** page |
| Token exchange fails with `invalid_client` after login | Wrong or rotated `SPOTIPY_CLIENT_SECRET` | Copy the current secret into `.env` |
| `403` on every call, also right after login | The account is not the app owner and not listed under **User Management**, or the owner's Premium has lapsed | Add the user, or renew Premium |
| `403` only on one command (e.g. `like`) | The cached token predates a scope that command needs | Delete `.spotify_token_cache` and run the smoke test again |
| Commands hang until a timeout | WSL's broken IPv6 route | The script forces IPv4 on WSL automatically; set `SPOTIFY_FORCE_IPV4=1` if auto-detection misses your setup ([architecture.md → Network quirks](architecture.md#network-quirks)) |

## Configure your playlists

The script needs to know **which playlists** to write to and **how to talk about them**. That config lives in `playlists.json` at the repo root, next to `.env`. It is **gitignored** — never commit it. A complete worked example lives at [playlists.example.json](../playlists.example.json).

The fastest path to a working config:

1. **Seed from the example**:
   ```bash
   cp playlists.example.json playlists.json
   ```
2. **Discover your Spotify playlists** (after [Connect to Spotify](#connect-to-spotify) printed `Connected as: …`):
   ```bash
   python playlist_manager.py list-playlists --all
   ```
   This prints every writable playlist on your account in paste-ready JSON, split into "already tracked" and "untracked". Copy the lines you want into `playlists.json` under `"playlists"`, replacing the example entries with your own.
3. **Verify**:
   ```bash
   python playlist_manager.py list-playlists
   ```
   Should print the names you just added.

### Schema

```jsonc
{
  // Required. name -> Spotify playlist ID. The 22-char path segment after /playlist/.
  "playlists": {
    "House": "0BEX4bI5xtkEVA4BfYTKg2",
    "Techno": "7lRL294p8uvOOXTxNPIBhn"
  },

  // Optional. Shorthand -> canonical playlist name. Used by `add` and `smart-add`
  // to resolve aliases like `dnb` to `Drum & Bass`. Case-insensitive lookup.
  "aliases": {
    "edm": "Electronic Music",
    "dnb": "Drum & Bass"
  },

  // Optional, but recommended for `smart-add`. Groups playlists into buckets shown
  // to the OpenAI classifier. Common buckets: "genre", "mood", "theme".
  // Without this, the classifier sees one flat list.
  "categories": {
    "genre": ["House", "Techno"],
    "mood":  ["Party", "Happy tunes"],
    "theme": ["Funny meme"]
  },

  // Optional. Per-playlist rules the OpenAI classifier should respect.
  // Use this for narrow/odd buckets that should only catch specific tracks,
  // or for inclusive "umbrella" playlists that should be suggested alongside subgenres.
  "special_rules": {
    "Funny meme": "Only for meme songs, internet classics, absurd/funny lyrics.",
    "Electronic Music": "Suggest 'Electronic Music' for ALL electronic tracks alongside their subgenre."
  },

  // Optional. Programmatic fallback. After classification, if no other playlist
  // scored >= threshold, the script appends this playlist to the suggestions
  // with confidence 100. The catch-all playlist is NEVER shown to the classifier
  // itself — it's a script-side safety net.
  "catch_all": {
    "playlist": "Random sht",
    "threshold": 85,                          // default 85 if omitted
    "rule": "Free-text description — informational only, not sent to the model."
  }
}
```

### What gets validated on load

- `playlists` is present, non-empty, and every value is a 22-character Spotify ID.
- Every `aliases` target exists in `playlists`.
- Every name listed under `categories` exists in `playlists`.
- Every key in `special_rules` exists in `playlists`.
- `catch_all.playlist` exists in `playlists`; `catch_all.threshold` (if present) is an int 0-100 (default 85); `catch_all.rule` (if present) is a string.

The script exits cleanly with a pointer to this section if validation fails.

### Where do playlist IDs come from?

Two paths:

- **From the script** (recommended): `python playlist_manager.py list-playlists --all`. Lists every writable playlist on your account in paste-ready format.
- **From the Spotify UI**: open a playlist, click "…" → Share → Copy link to playlist. The ID is the 22-char path segment after `/playlist/`. Example: `https://open.spotify.com/playlist/0BEX4bI5xtkEVA4BfYTKg2` → `0BEX4bI5xtkEVA4BfYTKg2`.

## Useful Spotify links

- [Spotify Web API documentation](https://developer.spotify.com/documentation/web-api) — endpoint reference, scopes, authorization flows.
- [Feb 2026 Dev Mode migration guide](https://developer.spotify.com/documentation/web-api/tutorials/february-2026-migration-guide) — endpoint renames, removed fields, new Premium requirement for app owners. Relevant to the script — see [architecture.md → February 2026 Spotify API migration](architecture.md#february-2026-spotify-api-migration).
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) — where you manage your app, secrets, and allow-listed users.
- [Exportify](https://exportify.net) — third-party browser tool to export playlists to CSV. Needed only for playlists this app can't read directly (playlists owned by someone else); the CSV works as a source for `review-playlist`, `bulk-playlist`, `scan-for`, `list-tracks` and `audit-playlist --csv`, and feeds `log-import`. See [commands.md → log-import](commands.md#log-import).
