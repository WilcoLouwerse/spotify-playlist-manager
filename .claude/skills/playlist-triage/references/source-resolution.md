# Source resolution

How to turn the user's source input into a single positional argument for `review-playlist` / `bulk-playlist`. The CLI accepts three forms; the skill should pass whichever the user gave, verbatim.

See [`docs/commands.md`](../../../../docs/commands.md#source-input) for the authoritative list.

---

## Accepted forms (in order of preference)

| Form | Example | Notes |
|------|---------|-------|
| Spotify URL | `https://open.spotify.com/playlist/3aBcDeFgHiJkLmNoPqRsTu` | Most direct; works in any environment that has Spotify API access. |
| Spotify URI | `spotify:playlist:3aBcDeFgHiJkLmNoPqRsTu` | Same as URL, alternate format. |
| Bare 22-char ID | `3aBcDeFgHiJkLmNoPqRsTu` | Quote it so a leading hyphen never gets parsed as a flag. |
| CSV path | `exportify-exports/Random_sht.csv` | Use for a playlist owned by someone else (Spotify won't expose its contents), or to deliberately process a snapshot. |
| Bare name | `"Random sht"` or `random-sht` | Resolves against `exportify-exports/` filenames. Matching is case-insensitive and treats spaces / underscores / `/` separators as equivalent. |

---

## When the user gives a bare name

The CLI's own resolver handles the bare-name → CSV-file mapping, so the skill can pass the name verbatim. But to give the user a sane preview, the skill should:

1. List `exportify-exports/*.csv` once.
2. Surface the matching files via **AskUserQuestion** if there are multiple plausible matches.
3. If there are zero matches, ask the user via **AskUserQuestion** whether they want to:
   - Provide a Spotify URL/URI/ID instead.
   - Export the playlist from [Exportify](https://exportify.net) first (point them at [`docs/commands.md` → Source input](../../../../docs/commands.md#source-input)).
   - Cancel.

Don't surprise the user — the skill should always show which CSV it picked before invoking the command.

---

## Filename mangling

Spotify display names contain characters that don't survive filesystems. Exportify uses these mappings:

| Display | Filename |
|---------|----------|
| `House` | `House.csv` |
| `Drum & Bass` | `Drum_&_Bass.csv` |
| `Jazz / Funk / Soul` | `Jazz_/_Funk_/_Soul.csv` *(slashes preserved)* |
| `Rustig / 'anders'` | `Rustig_/_'anders'.csv` |
| `Random sht` | `Random_sht.csv` |

The CLI's bare-name matcher handles this. The skill shouldn't try to invert the mangling — just list the files and let the user pick.

---

## Prefer the live playlist over a CSV

Spotify returns the live contents of every playlist you own or collaborate on; a CSV in `exportify-exports/` is a point-in-time snapshot. So when the source resolves to a CSV, check whether the live playlist is available.

**When to run the check**: the source resolved to a CSV path (explicit or bare-name match) AND the CSV's playlist name is present in `playlists.json -> playlists`. Every playlist in that file is readable via the API. If the name isn't there, skip the check — the CSV is likely the only way to read that playlist (e.g. one owned by someone else).

**How**: use **AskUserQuestion** in Dutch:

> "Voor {source} staat een CSV-export klaar, maar Spotify kan deze playlist ook live uitlezen. Welke bron wil je gebruiken?"
> - **Live via Spotify (Recommended)** — meest actueel; geef de Spotify-ID uit `playlists.json -> playlists[<source-name>]` door in plaats van de CSV.
> - **Deze CSV** — bijvoorbeeld om bewust een momentopname te verwerken.

---

## CSV fallback for unreadable playlists

Spotify only exposes the contents of playlists you own or collaborate on; for anyone else's playlist the items endpoint answers `403`. If a Spotify URL is given but no readable tracks come back, `review-playlist` / `bulk-playlist` print:

```
Spotify returned no readable tracks for '<name>' (<id>). Spotify only exposes the contents of playlists you own or collaborate on, so a playlist owned by someone else can't be read directly.
Found local export at exportify-exports/<file>.csv — use that instead? [y/N]:
```

The skill should NOT pre-empt this. Let the CLI offer the fallback — the user answers `y` on stdin to use the CSV, or `N` to bail out. If running in dry-run from chat, the skill can surface the prompt's existence in its summary and let the user re-run from the terminal.
