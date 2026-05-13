Yes — "House" is a valid target. Here's the command:

```bash
python playlist_manager.py log-import "House" exportify-exports/house.csv
```

A few quick notes:

- This is local-only (no Spotify API call). It seeds `.adds_log.json` so the duplicate guard knows about everything currently in House.
- I'm assuming the export file is at `exportify-exports/house.csv`. If yours is named differently (e.g. `House.csv` or `House_export.csv`), swap the path — the convention is that exportify CSVs live in `exportify-exports/` at the repo root.
- Make sure you run it from the repo root with the venv active.

Expected output will look something like:

```
Playlist: House (0BEX4bI5xtkEVA4BfYTKg2)
  Imported new URIs: 142
  Already in log:    1
  Duplicate in file: 0
  Unparseable lines: 1   ← typically the CSV header row
  Total URIs logged: 143
```

After this, future `add` / `smart-add` / `bulk-playlist` / `scan-for` runs will recognise everything currently in House as a duplicate and skip it.

Wil je dat ik 'm meteen draai? Geef me dan even de exacte bestandsnaam in `exportify-exports/` (of bevestig dat het `house.csv` is) — dan voer ik 'm uit.
