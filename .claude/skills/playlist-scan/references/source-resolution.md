# Source resolution

How to turn the user's source input into a single positional argument for `scan-for`. Same accepted forms as `review-playlist` / `bulk-playlist` (the CLI shares a resolver). See [`docs/commands.md → scan-for`](../../../../docs/commands.md#scan-for) and the matching guide in [playlist-triage/references/source-resolution.md](../../playlist-triage/references/source-resolution.md).

---

## Accepted forms

| Form | Example | Notes |
|------|---------|-------|
| Spotify URL | `https://open.spotify.com/playlist/3aBcDeFgHiJkLmNoPqRsTu` | Direct. |
| Spotify URI | `spotify:playlist:3aBcDeFgHiJkLmNoPqRsTu` | Alternate format. |
| Bare 22-char ID | `3aBcDeFgHiJkLmNoPqRsTu` | Quote so a leading hyphen isn't parsed as a flag. |
| CSV path | `exportify-exports/Random_sht.csv` | Use when Developer-Mode strips track URIs or when the export is fresher than the Spotify state. |
| Bare name | `"Random sht"`, `Random_sht`, `random-sht` | Resolves against `exportify-exports/`. Case-insensitive, slash/underscore/space tolerant. |

---

## Target argument

In addition to the source, `scan-for` needs a **target** as the first positional. Target rules:

| | Source | Target |
|--|--|--|
| Position | Second | First |
| Accepts | URL/URI/ID/CSV/bare name | Playlist name OR alias from `playlists.json` |
| Validation | CLI's resolver | CLI checks against `playlists.json -> playlists` + `aliases` |
| Quoting | Always | Always (names contain spaces / `/` / `'`) |

```bash
.venv/bin/python playlist_manager.py scan-for "House" "Random sht"
#                                                  ^target  ^source
```

The skill should validate the target name *before* invoking the command — read `playlists.json`, accept aliases, and if the user typed something ambiguous, ask via **AskUserQuestion**.

---

## Stripped-data CSV fallback

If a Spotify URL is given but the API returns no readable tracks (Developer Mode strips `track` URIs from `playlist_items`), `scan-for` prints:

```
Source playlist returned no readable tracks.
Found a matching CSV: exportify-exports/<file>.csv
Use it as the source instead? [y/N]:
```

Let the CLI handle that prompt — don't pre-empt it.
