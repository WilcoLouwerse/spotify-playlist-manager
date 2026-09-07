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

## Freshness check via .tracks_log.json

CSVs in `exportify-exports/` are point-in-time exports — `.tracks_log.json` is updated live by every successful `add`, `bulk-playlist`, `review-playlist`, and `scan-for --execute` run. When the resolved source is a CSV, the skill should compare the two before scanning.

**When to run the check**:
- The source resolved to a CSV path (explicit or bare-name match under `exportify-exports/`).
- AND the source playlist's name is present in `playlists.json -> playlists` (so we can look up its Spotify ID).

If either condition fails, skip the check.

**How**:
1. Look up the source's Spotify ID via `playlists.json -> playlists[<source-name>]`.
2. Read `.tracks_log.json` and grab the array at `[<source-id>]` (empty array if the key is missing).
3. Parse the CSV — collect the URI set from the `Track URI` column (Exportify's first column). Normalize URLs to `spotify:track:<id>` form so the sets are comparable.
4. Compute `log_only = log_uris - csv_uris` (tracks the log has that the CSV doesn't).

**Surfacing a stale CSV** — if `len(log_only) > 0`, the CSV is likely stale. Use **AskUserQuestion**:

> "De CSV `<file>` mist {N} tracks die wel in `.tracks_log.json` voor {source} staan — de CSV is mogelijk verouderd. Hoe wil je verder?"
> - **Gebruik Spotify URL/URI** *(meest actueel)* — vraag om de URL/URI van de source en gebruik die in plaats van de CSV.
> - **Ga door met deze CSV** — accepteer dat recente toevoegingen worden gemist.
> - **Exporteer eerst opnieuw via Exportify** — stop de scan; user re-exports and re-runs.

If `log_only` is empty, proceed silently — the CSV is in sync (or newer, which is fine).

**Cases where the log is *less* complete than the CSV** (`len(csv_uris - log_uris) > 0`): do not warn. The log only records adds made via the CLI; tracks added through Spotify's UI are in the CSV but not the log. That's expected, not stale.

---

## Stripped-data CSV fallback

If a Spotify URL is given but the API returns no readable tracks (Developer Mode strips `track` URIs from `playlist_items`), `scan-for` prints:

```
Source playlist returned no readable tracks.
Found a matching CSV: exportify-exports/<file>.csv
Use it as the source instead? [y/N]:
```

Let the CLI handle that prompt — don't pre-empt it.
