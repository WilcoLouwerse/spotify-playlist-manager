## File resolution

How to turn the user's file input into a single positional argument for `log-import`.

Unlike `scan-for` / `review-playlist` / `bulk-playlist`, **`log-import` does not accept Spotify URLs or bare playlist names** as the source — it always wants a path to a local file. The CLI doesn't fall back to a CSV by name lookup. The skill must resolve the path before invoking the command.

---

## Accepted forms

| Form | Example | Notes |
|------|---------|-------|
| Absolute path | `/home/wilco/spotify-playlist-manager/exportify-exports/house.csv` | Direct. |
| Relative to repo root | `exportify-exports/house.csv` | The recommended convention. |
| Bare filename | `house.csv` | Resolve against `exportify-exports/` first, then the repo root. |
| Bare playlist name | `House`, `"Drum & Bass"`, `dnb` | **Skill responsibility** — the CLI won't do this lookup. Map to `exportify-exports/<mangled>.csv` (see [exportify filename mangling](#exportify-filename-mangling)). |

If multiple candidate files exist (e.g. `house.csv` and `House.csv`), ask via **AskUserQuestion** which one to use rather than picking by case-folding rules.

---

## Exportify filename mangling

[Exportify](https://exportify.net) writes filenames by replacing spaces with underscores and keeping other characters literally. Examples:

| Playlist name in Spotify | Exportify filename |
|--------------------------|--------------------|
| `House` | `House.csv` |
| `Drum & Bass` | `Drum_&_Bass.csv` |
| `Rustig / 'anders'` | `Rustig_/_'anders'.csv` (rare — `/` in filenames creates a directory; Exportify will usually flatten or refuse) |
| `Random sht` | `Random_sht.csv` |

When the user types a bare playlist name, try these in order:
1. `exportify-exports/<exact-name>.csv` (covers the no-space case)
2. `exportify-exports/<name with spaces -> underscores>.csv`
3. Case-insensitive scan of `exportify-exports/` for files whose stem matches the target (with spaces/underscores/hyphens treated as equivalent)

If none match, ask via **AskUserQuestion** for the actual path.

---

## File format

`log-import` accepts **any** text-shaped file. It scans each line for:

- A Spotify track URI: `spotify:track:<22-char-id>`
- A Spotify track URL: `https://open.spotify.com/track/<22-char-id>?...` (query string ignored)
- A bare 22-character track ID (alphanumeric), either as the whole line or as the first CSV/TSV field

Everything else counts as `Unparseable lines` in the output — that's where the Exportify CSV header row ("Track URI,Track Name,Album Name,...") gets reported, which is normal.

The skill does not need to validate the file format itself — the CLI's counters in the output are authoritative. The skill should only verify that the file *exists* and is readable.

---

## Edge cases

- **File doesn't exist**: ask via **AskUserQuestion** for the correct path. List the `exportify-exports/` directory contents in the question's description so the user can see what's available.
- **File is empty or 0 bytes**: still pass it to `log-import` — the four per-file counts will be zero (`Total URIs logged` still shows the existing log size), which is informative. Don't try to short-circuit.
- **File is a JSON export from another tool** (e.g. Spotify's "Download your data"): pass it through — the line-by-line URI extractor will catch any URIs that happen to be on their own line. Warn the user that JSON exports often pack many URIs on one line and may not parse well; suggest re-exporting via Exportify if the count is suspiciously low.
- **File is binary** (e.g. `.xlsx`): reject before invoking — `log-import` reads the file as UTF-8 text and will likely crash with a `UnicodeDecodeError`, after the user already spent a confirmation cycle. Ask via **AskUserQuestion** for a CSV/text version.
