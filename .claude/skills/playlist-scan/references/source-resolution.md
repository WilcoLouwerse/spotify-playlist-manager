# Source resolution

How to turn the user's source input into a single positional argument for `scan-for`. Same accepted forms as `review-playlist` / `bulk-playlist` (the CLI shares a resolver). See [`docs/commands.md → scan-for`](../../../../docs/commands.md#scan-for) and the matching guide in [playlist-triage/references/source-resolution.md](../../playlist-triage/references/source-resolution.md).

---

## Accepted forms

| Form | Example | Notes |
|------|---------|-------|
| Spotify URL | `https://open.spotify.com/playlist/3aBcDeFgHiJkLmNoPqRsTu` | Live; works for playlists you own or collaborate on (`403` + CSV offer for anyone else's). |
| Spotify URI | `spotify:playlist:3aBcDeFgHiJkLmNoPqRsTu` | Alternate format. |
| Bare 22-char ID | `3aBcDeFgHiJkLmNoPqRsTu` | Quote so a leading hyphen isn't parsed as a flag. |
| CSV path | `exportify-exports/Random_sht.csv` | Use for a playlist owned by someone else (Spotify won't expose its contents), or to deliberately process a snapshot. |
| Bare name | `"Random sht"`, `Random_sht` | Resolves against `exportify-exports/`. Case-insensitive; spaces and underscores equivalent. Names containing `/` are treated as a path and `-` is not normalised — pass the CSV path or the Spotify ID instead. A name that is in `playlists.json` but has no CSV does not resolve at all; pass its Spotify ID. |

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

## Prefer the live playlist over a CSV

Spotify returns the live contents of every playlist you own or collaborate on; a CSV in `exportify-exports/` is a point-in-time snapshot. So when the source resolves to a CSV, check whether the live playlist is available.

**When to run the check**: the source resolved to a CSV path (explicit or bare-name match) AND the CSV's playlist name is present in `playlists.json -> playlists`. Every playlist in that file is readable via the API. Match the CSV stem to `playlists.json` keys the way the CLI does: case-insensitive, `_` equals a space, `/` dropped (`Random_sht` ↔ `Random sht`, `Jazz_Funk_Soul` ↔ `Jazz / Funk / Soul`). If the name isn't there, skip the check — the CSV is likely the only way to read that playlist (e.g. one owned by someone else).

**How**: use **AskUserQuestion** in Dutch:

> "Voor {source} staat een CSV-export klaar, maar Spotify kan deze playlist ook live uitlezen. Welke bron wil je gebruiken?"
> - **Live via Spotify (Recommended)** — meest actueel; geef de Spotify-ID uit `playlists.json -> playlists[<source-name>]` door in plaats van de CSV.
> - **Deze CSV** — bijvoorbeeld om bewust een momentopname te verwerken.

---

## CSV fallback for unreadable playlists

Spotify only exposes the contents of playlists you own or collaborate on; for anyone else's playlist the items endpoint answers `403`. If a Spotify URL is given but no readable tracks come back, `scan-for` prints:

```
Spotify returned no readable tracks for '<name>' (<id>). Spotify only exposes the contents of playlists you own or collaborate on, so a playlist owned by someone else can't be read directly.
Found local export at exportify-exports/<file>.csv — use that instead? [y/N]:
```

Let the CLI handle that prompt — don't pre-empt it.
