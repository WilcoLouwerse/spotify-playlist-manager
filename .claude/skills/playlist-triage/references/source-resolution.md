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
| CSV path | `exportify-exports/Random_sht.csv` | Use when Spotify's Developer Mode strips playlist contents, or when the user has a recent Exportify dump. |
| Bare name | `"Random sht"` or `random-sht` | Resolves against `exportify-exports/` filenames. Matching is case-insensitive and treats spaces / underscores / `/` separators as equivalent. |

---

## When the user gives a bare name

The CLI's own resolver handles the bare-name → CSV-file mapping, so the skill can pass the name verbatim. But to give the user a sane preview, the skill should:

1. List `exportify-exports/*.csv` once.
2. Surface the matching files via **AskUserQuestion** if there are multiple plausible matches.
3. If there are zero matches, ask the user via **AskUserQuestion** whether they want to:
   - Provide a Spotify URL/URI/ID instead.
   - Export the playlist from [Exportify](https://exportify.net) first (point them at [`docs/commands.md` → log-import](../../../../docs/commands.md#log-import)).
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

## Stripped-data CSV fallback

If a Spotify URL is given but the API returns no readable tracks (Developer Mode strips `track` URIs from `playlist_items`), `review-playlist` / `bulk-playlist` print:

```
Source playlist returned no readable tracks.
Found a matching CSV: exportify-exports/<file>.csv
Use it as the source instead? [y/N]:
```

The skill should NOT pre-empt this. Let the CLI offer the fallback — the user answers `y` on stdin to use the CSV, or `N` to bail out. If running in dry-run from chat, the skill can surface the prompt's existence in its summary and let the user re-run from the terminal.
