# Commands

CLI reference for [playlist_manager.py](../playlist_manager.py). Run every command from the repo root with the venv active.

## Global behavior

- **Dry-run by default.** Commands that write to Spotify (`add`, `remove`, `smart-add`, `review-playlist`, `bulk-playlist`, `scan-for`) print what they *would* do and exit. Add `--execute` to actually write.
- **Duplicate guard is always on.** Before writing, the script consults the local log (`.tracks_log.json`) of every URI it has successfully added or that has been seeded via `log-import`. If the URI is found, it exits with `SKIP`. There is no override flag. See [architecture.md → Duplicate detection](architecture.md#duplicate-detection) for why the local log is authoritative and how to seed it.
- **IPv4 only.** The script forces IPv4 resolution because WSL's IPv6 route to `api.spotify.com` is broken. See [architecture.md](architecture.md) for the why.

## `list-playlists`

Print the configured target playlists, or fetch every writable playlist from Spotify.

```bash
# Local: print names from playlists.json
python playlist_manager.py list-playlists

# Spotify: list every writable playlist on your account (paste-ready for playlists.json)
python playlist_manager.py list-playlists --all
```

Without flags, output is the names defined under `"playlists"` in [playlists.json](../playlists.json) (gitignored — see [playlists.example.json](../playlists.example.json) for the schema). These are the only playlists the `add` and `smart-add` commands can write to.

### `--all`: discover playlists from Spotify

`--all` calls the Spotify API, filters to playlists you own or collaborate on (the only ones you can write to), and prints them in paste-ready JSON, split by whether they're already tracked. Use this to bootstrap or extend `playlists.json` without copying IDs from the Spotify UI by hand.

Example output:

```
Writable playlists on your Spotify account: 47 (3 tracked, 44 untracked)

Already tracked in playlists.json:
  "House": "0BEX4bI5xtkEVA4BfYTKg2"
  "Techno": "7lRL294p8uvOOXTxNPIBhn"
  "Drum & Bass": "0jECuEhrsvUJCkVy9fmGmN"

Untracked (paste any of these into playlists.json -> "playlists"):
  "Coffee Shop": "1def2345678901bcdefghi",
  "My Workout Mix": "7abc1234567890abcdefgh",
  ...
```

Copy the lines you want, paste them into `playlists.json` under `"playlists"`, and they'll be live next run (no restart needed).

If `playlists.json` doesn't exist yet, `--all` still works — it shows everything as "untracked" and points you at [playlists.example.json](../playlists.example.json) for the full schema. See [setup.md → Configure your playlists](setup.md#configure-your-playlists).

### Adding a new playlist target

1. Run `python playlist_manager.py list-playlists --all` (or open the playlist in Spotify and copy the 22-char ID from the URL).
2. Paste the `"Name": "<id>"` line into `playlists.json` under `"playlists"`.
3. (Optional) Add an entry under `"aliases"` for shorthand and/or under `"categories"` so `smart-add` knows whether it's a genre, mood, or theme.
4. Verify with `python playlist_manager.py list-playlists`.

## `log-import`

Import a list of Spotify track URIs/URLs/IDs from a file into the local `.tracks_log.json` for one playlist. This is the **primary way** to teach the duplicate guard about songs already in your playlists — run it once per playlist after the initial setup, then again whenever you've added a lot of tracks through the Spotify UI. See [architecture.md → Duplicate detection](architecture.md#duplicate-detection) for the why.

By convention, drop your export files in [exportify-exports/](../exportify-exports/) at the repo root. The folder is tracked but its contents are gitignored, so personal exports don't end up in the repo.

```bash
python playlist_manager.py log-import "House" exportify-exports/house.csv
```

### Arguments

| Argument | Description |
|----------|-------------|
| `playlist` | Target playlist name — must match a key under `"playlists"` in [playlists.json](../playlists.json) or an alias under `"aliases"` |
| `file` | Path to a text/CSV/JSON file. Any line containing a Spotify track URI (`spotify:track:...`), URL (`https://open.spotify.com/track/...?...`), or a bare 22-character ID (as the whole line or the first CSV/TSV field) is imported. Other lines are reported as `Unparseable`. |

### Recommended export tool: Exportify

Spotify itself doesn't ship a built-in "export playlist to CSV." [Exportify](https://exportify.net) (open source, runs in your browser, uses your own Spotify *web* auth so it bypasses the dev-tier quota that blocks our app) produces a CSV with `Track URI` as the first column. That file imports cleanly:

```bash
# 1. Open https://exportify.net, log in with Spotify, export the "House" playlist.
# 2. Save the CSV into the repo's exportify-exports/ folder (e.g. exportify-exports/house.csv).
# 3. Seed the local log:
python playlist_manager.py log-import "House" exportify-exports/house.csv
```

After that, future `add` and `smart-add` runs will recognise everything in the imported playlist as a duplicate.

### Example output

```
Playlist: House (0BEX4bI5xtkEVA4BfYTKg2)
  Imported new URIs: 142
  Already in log:    1
  Duplicate in file: 0
  Unparseable lines: 1   ← typically the CSV header row
  Total URIs logged: 143
```

### Limits and caveats

- Local-only. No Spotify API call is made.
- One playlist per run — repeat the command for each playlist.
- Doesn't *verify* that the imported tracks are actually in the playlist on Spotify — it trusts the file.
- If you remove a track from a playlist via the Spotify UI, this log won't notice. Either re-run the import or delete the URI from `.tracks_log.json` manually.

## `add`

Add a single track to one specific playlist.

```bash
# Dry-run — shows what would happen, writes nothing
python playlist_manager.py add "https://open.spotify.com/track/<id>" "House"

# Actually add the track
python playlist_manager.py add "https://open.spotify.com/track/<id>" "House" --execute
```

### Arguments

| Argument | Description |
|----------|-------------|
| `track` | Spotify track URL (`https://open.spotify.com/track/...`), URI (`spotify:track:...`), or bare ID |
| `playlist` | Target playlist name — must match a key under `"playlists"` in [playlists.json](../playlists.json) or an alias under `"aliases"` (case-insensitive) |
| `--execute` | Without this flag, nothing is written |

### Playlist aliases

The `"aliases"` block in `playlists.json` accepts shorthand → canonical name mappings. Example block (from [playlists.example.json](../playlists.example.json)):

```json
"aliases": {
  "dnb": "Drum & Bass",
  "drum and bass": "Drum & Bass",
  "chill": "Rustig / 'anders'",
  "edm": "Electronic Music"
}
```

Each value must match a key in `"playlists"` — that's enforced at config load time. See [setup.md → Configure your playlists](setup.md#configure-your-playlists) for the full schema.

### Exit behavior

- Track already in playlist → prints `SKIP: track already in playlist` and exits.
- Playlist name not recognised → raises `ValueError: Unknown playlist: ...`.
- Spotify catalog endpoint times out → still adds, but prints `(track lookup failed: ReadTimeout; continuing with URI only)` and uses the URI instead of "Artist - Title" in output.

## `remove`

Remove a single track from one specific playlist.

```bash
# Dry-run — shows what would happen, writes nothing
python playlist_manager.py remove "https://open.spotify.com/track/<id>" "House"

# Actually remove the track
python playlist_manager.py remove "https://open.spotify.com/track/<id>" "House" --execute
```

### Arguments

| Argument | Description |
|----------|-------------|
| `track` | Spotify track URL (`https://open.spotify.com/track/...`), URI (`spotify:track:...`), or bare ID |
| `playlist` | Target playlist name — must match a key under `"playlists"` in [playlists.json](../playlists.json) or an alias under `"aliases"` (case-insensitive) |
| `--execute` | Without this flag, nothing is written |

### How it checks the track is in the playlist

`remove` uses the same two-layer check as `add` — first the local `.tracks_log.json`, then a best-effort Spotify API call. In Spotify Developer Mode, `playlist_items` returns empty URIs, so the API check may show "not found" even when the track is present. If the log doesn't know about the track (e.g. it was added through the Spotify UI), the script prints `SKIP: track not found in playlist` and exits without writing.

### Effect on `.tracks_log.json`

On a successful removal, the script removes the track URI from `.tracks_log.json` for that playlist. This means a future `add` call for the same track will no longer see it as a duplicate and can add it back cleanly.

### Exit behavior

- Track not found in playlist (not in log, not confirmed by API) → prints `SKIP: track not found in playlist. No changes made.` and exits.
- Track removed successfully → prints `DONE: track removed (snapshot …)`.
- Playlist name not recognised → raises `ValueError: Unknown playlist: ...`.
- Spotify API error → prints `FAILED: Spotify returned <status> <msg>`.

## `batch-add`

Add many tracks to a single playlist in batches of 100 (Spotify API max). The **preferred path** whenever a skill or workflow adds more than one track to the same target — one API call per 100 URIs instead of one per track.

```bash
# Dry-run from a file (one URI/URL/ID per line; '#' lines and blanks are skipped)
python playlist_manager.py batch-add "Metal" candidates.txt

# Execute from stdin
cat candidates.txt | python playlist_manager.py batch-add "Metal" - --execute
```

### Arguments

| Argument | Description |
|----------|-------------|
| `playlist` | Target playlist name — must match a key under `"playlists"` in [playlists.json](../playlists.json) or an alias under `"aliases"` (case-insensitive) |
| `source` | Path to a file with one Spotify track URI/URL/ID per line, or `-` to read from stdin. Blank lines and lines starting with `#` are ignored. |
| `--execute` | Without this flag, nothing is written |

### Behaviour

- Input is de-duplicated before sending to Spotify (same URI listed twice → counted once).
- The combined set of URIs already in the playlist (from `.tracks_log.json` plus a live `playlist_items` fetch) is filtered out — URIs already present are reported as `SKIP {N} URIs already in playlist (will not re-add)` and not sent.
- Remaining URIs are sent to `playlist_add_items` in chunks of up to 100. Each chunk is one Spotify API call.
- On a successful chunk, every URI in the chunk is logged via `log_successful_add` so `.tracks_log.json` stays current.
- On a 429 (rate limit), the script honours `Retry-After` (see [architecture.md](architecture.md)).

### Why batch instead of `add` in a loop

- Each `add` invocation pays the Python + spotipy + auth bootstrap cost (~1-2s) and calls `playlist_contains_uri`, which paginates the playlist. 150 tracks via per-track `add` ≈ 150 bootstraps + 150 pagination calls + 150 add calls ≈ 600 API calls and several minutes.
- `batch-add` paginates the playlist once, then sends 1 API call per 100 tracks. 150 tracks ≈ 1 pagination + 2 add calls ≈ ~3 API calls and ~10 seconds.

### Exit behaviour

- No URIs in input (empty file, only comments) → prints `No URIs to add. Nothing to do.` and exits.
- All URIs already in the playlist → prints `Nothing new to add. Done.` and exits.
- Chunk fails → prints `FAILED batch of {N}: <status> <msg>`, increments the failed counter, continues with remaining chunks.
- Spotify returns no `snapshot_id` for a chunk → prints `WARN: no snapshot_id ...`, increments failed counter, continues.

Final line summarises: `DONE: added {A}, failed {F}, skipped {S} (already in playlist).`

## `batch-remove`

Remove many tracks from a single playlist in batches of 100 (Spotify API max). The **preferred path** whenever a skill or workflow removes more than one track from the same playlist.

```bash
# Dry-run from a file
python playlist_manager.py batch-remove "Rock" to_remove.txt

# Execute from stdin
cat to_remove.txt | python playlist_manager.py batch-remove "Rock" - --execute
```

### Arguments

| Argument | Description |
|----------|-------------|
| `playlist` | Target playlist name — must match a key under `"playlists"` in [playlists.json](../playlists.json) or an alias under `"aliases"` (case-insensitive) |
| `source` | Path to a file with one Spotify track URI/URL/ID per line, or `-` to read from stdin. Blank lines and lines starting with `#` are ignored. |
| `--execute` | Without this flag, nothing is written |

### Behaviour

- Input is de-duplicated before sending to Spotify.
- URIs not in the playlist (per `.tracks_log.json` + live `playlist_items`) are reported as `SKIP {N} URIs not in playlist` and dropped — `playlist_remove_all_occurrences_of_items` is idempotent on non-present URIs, but skipping makes the log line accurate.
- Remaining URIs are sent in chunks of up to 100 via `playlist_remove_all_occurrences_of_items`. Each chunk is one Spotify API call.
- On a successful chunk, every URI is removed from `.tracks_log.json` via `remove_from_log`.

### When NOT to use this command

- **One track from many playlists** — Spotify's API removes from one playlist per call. There is no batch equivalent. Use a `remove --execute` loop or call the relevant skill (`/playlist-remove`) instead.

### Exit behaviour

- No URIs in input → prints `No URIs to remove. Nothing to do.` and exits.
- All URIs absent from the playlist → prints `Nothing to remove. Done.` and exits.
- Chunk failure handling is identical to `batch-add`.

Final line summarises: `DONE: removed {R}, failed {F}, skipped {S} (not in playlist).`

## `smart-add`

Classify a track with OpenAI, confirm interactively, then add it to the suggested playlists.

```bash
# Dry-run — classify and prompt for confirmation, write nothing
python playlist_manager.py smart-add "https://open.spotify.com/track/<id>"

# Real run — writes to Spotify after y/N (per playlist by default)
python playlist_manager.py smart-add "https://open.spotify.com/track/<id>" --execute

# Single bulk y/N for the whole set instead of confirming per playlist
python playlist_manager.py smart-add "https://open.spotify.com/track/<id>" --execute --accept-all

# Cap to 3 suggestions and drop anything below 75% confidence
python playlist_manager.py smart-add "https://open.spotify.com/track/<id>" --max-playlists 3 --min-confidence 75
```

### Flow

1. Look up rich track metadata on Spotify (artists, album, release date, popularity, explicit flag, URL).
2. Ask OpenAI to pick playlists that fit the track. The prompt is assembled from [playlists.json](../playlists.json): `"categories"` groups playlists into buckets (genre/mood/theme), `"special_rules"` adds per-playlist semantics, and the `--min-playlists` / `--max-playlists` flags control how many suggestions to ask for. The catch-all playlist is **not** shown to the classifier — it's a script-side fallback (see step 4).
3. Sort the model's suggestions by confidence (highest first) and truncate to `--max-playlists`.
4. **Catch-all check**: if `playlists.json -> "catch_all"` is configured AND no remaining match has confidence >= `catch_all.threshold` (default 85), append the catch-all playlist to the suggestions with confidence 100. This may push the total to `max-playlists + 1`.
5. **Confidence filter**: drop any suggestion below `--min-confidence` (default 0 = no filter). The catch-all has confidence 100 so it always survives.
6. Print the recommendation (track header, summary, genres, final suggested playlists).
7. Compute **Pending actions** — for each suggestion, the script checks the duplicate guard and labels it `ADD` or `SKIP` before any confirmation.
8. Prompt for confirmation:
   - **Default**: ask `y/N` separately for each `ADD` action. Rejecting one keeps the rest of the run going.
   - **`--accept-all`**: single `y/N` that accepts all `ADD` actions at once.
9. For each accepted playlist: either dry-run print or POST the add (under `--execute`).

`y`, `yes`, `j`, and `ja` are all accepted as confirmation.

### Example output

```
============================================================
Track: Bakermat, Nic Hanson - Walk That Walk
Album: Walk That Walk
Spotify: https://open.spotify.com/track/1W5mUuAOQSSKUbLOt7cDhq
============================================================

Summary:
Bright, uplifting deep-house track with festival energy.

Genres:
- deep house — 88% — driving bassline with vocal hook
- tropical house — 64% — bright melodies, summery vibe

Suggested playlists:
- House — 92% — uplifting deep-house with vocals
- Party — 84% — high-energy festival vibe
- Happy tunes — 78% — bright, major key

Pending actions:
- ADD: House (92%)
- SKIP: already in Party
- ADD: Happy tunes (78%)

Add to 'House' (92%)? [y/N]: y
Add to 'Happy tunes' (78%)? [y/N]: y

- House: ADDED
- Happy tunes: ADDED
```

### Arguments

| Argument | Description |
|----------|-------------|
| `track` | Spotify track URL, URI, or ID |
| `--execute` | Without this flag, accepted suggestions print `DRY RUN (would add)` instead of writing |
| `--accept-all` | Ask one bulk y/N for the whole set instead of the default per-playlist y/N |
| `--max-playlists` | Cap on classifier suggestions (1-5, default 5). The catch-all fallback may add one more on top when triggered. |
| `--min-playlists` | Minimum number of suggestions to ask the classifier for (1-5, default 3). Must not exceed `--max-playlists`. |
| `--min-confidence` | Drop suggestions below this confidence (0-100, default 0 = no filter). The catch-all always survives (confidence 100). |

### Requirements

- `OPENAI_API_KEY` set in `.env` — see [setup.md](setup.md).
- [playlists.json](../playlists.json) populated. `"categories"`, `"special_rules"`, and `"catch_all"` are optional but heavily recommended — without `"categories"` the classifier sees one flat list of playlist names and has to guess at the structure.
- Spotify's `/v1/tracks/{id}` endpoint must respond. If it times out, classification cannot proceed and the script aborts cleanly. Fall back to plain `add` in that case.

### Cost

`gpt-4.1-mini` (the default) costs roughly $0.0001–$0.0003 per `smart-add` call, depending on the size of the JSON prompt. Override the model via `OPENAI_MODEL` in `.env` if you want better classifications and don't mind the cost.

## `analyze-only`

Same classification pipeline as `smart-add`, but stops after printing the suggestions. No prompts, no writes — useful for quickly seeing "where would this track go?" without committing to anything.

```bash
python playlist_manager.py analyze-only "https://open.spotify.com/track/<id>"

# Same tuning flags as smart-add
python playlist_manager.py analyze-only "https://open.spotify.com/track/<id>" --max-playlists 5 --min-confidence 75
```

### Flow

1. Look up rich track metadata on Spotify.
2. Ask OpenAI to pick playlists (same prompt as `smart-add`).
3. Sort, truncate to `--max-playlists`, apply catch-all and `--min-confidence` (same filtering as `smart-add`).
4. Print the recommendation and exit. No duplicate guard check, no `Pending actions`, no confirmation prompt.

### Arguments

| Argument | Description |
|----------|-------------|
| `track` | Spotify track URL, URI, or ID |
| `--max-playlists` | Cap on classifier suggestions (1-10, default 10). The catch-all fallback may add one more on top when triggered. |
| `--min-playlists` | Minimum number of suggestions to ask the classifier for (1-10, default 5). Must not exceed `--max-playlists`. |
| `--min-confidence` | Drop suggestions below this confidence (0-100, default 0 = no filter). The catch-all always survives (confidence 100). |

### Requirements

Same as `smart-add`: `OPENAI_API_KEY` in `.env` and a populated [playlists.json](../playlists.json).

## `review-playlist`

Walk every track in a source playlist, classify each with OpenAI, and decide per track whether to add it to its suggested playlists. Useful for sorting a messy "to triage" playlist into your genre/mood playlists in one sitting.

```bash
# Dry-run — classify every track and show what would happen
python playlist_manager.py review-playlist "https://open.spotify.com/playlist/<id>"

# Real run — actually add accepted tracks to suggested playlists
python playlist_manager.py review-playlist "https://open.spotify.com/playlist/<id>" --execute

# Tune the classifier the same way as smart-add
python playlist_manager.py review-playlist "https://open.spotify.com/playlist/<id>" --execute --max-playlists 3 --min-confidence 75

# Read tracks from a local exportify CSV instead of Spotify
python playlist_manager.py review-playlist exportify-exports/House.csv

# Same — by bare name (resolved against exportify-exports/)
python playlist_manager.py review-playlist House
```

### Source input

The `playlist` argument accepts any of:

- A Spotify playlist URL, URI, or 22-char ID.
- A path to an [Exportify](https://exportify.net) CSV (e.g. `exportify-exports/House.csv`).
- A bare name that matches a CSV in [exportify-exports/](../exportify-exports/) (e.g. `House` → `exportify-exports/House.csv`, or `"Drum & Bass"` → `exportify-exports/Drum_&_Bass.csv`). Matching is case-insensitive and treats spaces, underscores, and `/` separators as equivalent so the Spotify display name maps to exportify's filename mangling.

When a URL is given but Spotify returns no readable tracks (dev-tier strips playlist contents), the script looks for a CSV in `exportify-exports/` whose name matches the source playlist and prompts you to use it instead. Answer `y` to fall back to the local export; `N` exits with the usual Exportify pointer.

### Per-track prompt

For each track the script prints the track header, the classifier's suggested playlists, and asks:

```
Add this track to these playlists? [y/N/s/q]:
```

| Input | Meaning |
|-------|---------|
| `y` / `yes` / `j` / `ja` | Accept — add to every suggested playlist (skipping any the duplicate guard flags) |
| `n` / `no` / `nee` / empty | Reject — leave Spotify untouched, move on |
| `s` / `skip` | Same as reject |
| `q` / `quit` / `exit` / Ctrl-D | Stop the whole review immediately |

Unlike `smart-add`, accept is **all-or-nothing per track** — `y` adds to every suggested playlist. If you want per-playlist control, use `smart-add` on that one track instead.

### Flow

1. Load the source playlist by URL/URI/ID and list its tracks via `playlist_items`.
2. For each track: run the same classification pipeline as [smart-add](#smart-add) (catch-all fallback and `--min-confidence` filter included).
3. Show suggestions, prompt `y/N/s/q`.
4. On `y`: for each suggested playlist, check the duplicate guard, then either dry-run print or `playlist_add_items` under `--execute`.
5. Print a summary: accepted, skipped, total.

### Arguments

| Argument | Description |
|----------|-------------|
| `playlist` | Spotify playlist URL/URI/ID, path to an exportify CSV, or a name matching a file in [exportify-exports/](../exportify-exports/). See [Source input](#source-input). |
| `--execute` | Without this flag, accepted suggestions print `DRY RUN (would add)` instead of writing |
| `--max-playlists` | Cap on classifier suggestions per track (1-5, default 3). The catch-all fallback may add one more on top when triggered. |
| `--min-playlists` | Minimum number of suggestions to ask the classifier for (1-5, default 1). Must not exceed `--max-playlists`. |
| `--min-confidence` | Drop suggestions below this confidence (0-100, default 80). The catch-all always survives (confidence 100). |

### Limits and caveats

- Each track costs one OpenAI classification call plus a few Spotify reads — reviewing a 50-track playlist is a few minutes of API time and pennies of OpenAI credit.
- If the app is in Spotify Developer Mode and `playlist_items` returns stripped data (no track URIs), the script offers a matching CSV in [exportify-exports/](../exportify-exports/) as a fallback. Decline (or have no matching file) and it exits with the same Exportify pointer as [log-import](#log-import).
- The duplicate guard runs per suggestion, so accepting a track that's already in some of its suggested playlists is safe — those playlists just print `SKIP (already in playlist)`.

## `bulk-playlist`

Classify every track in a source playlist, show a per-target tally, and add them all after **one** y/N. Use this when you have a big triage playlist and want a quick "send it" workflow instead of `review-playlist`'s per-track prompt.

```bash
# Dry-run — classify all tracks, show the tally, no writes
python playlist_manager.py bulk-playlist "https://open.spotify.com/playlist/<id>"

# Real run — apply everything after the y/N
python playlist_manager.py bulk-playlist "https://open.spotify.com/playlist/<id>" --execute

# Same tuning flags as smart-add
python playlist_manager.py bulk-playlist "https://open.spotify.com/playlist/<id>" --execute --min-confidence 75

# Read tracks from a local exportify CSV instead of Spotify
python playlist_manager.py bulk-playlist exportify-exports/House.csv

# Same — by bare name (resolved against exportify-exports/)
python playlist_manager.py bulk-playlist House
```

The `playlist` argument accepts the same three forms as [review-playlist → Source input](#source-input) (URL/URI/ID, CSV path, or bare name in `exportify-exports/`), and applies the same CSV fallback when a URL returns no readable tracks.

### Flow

1. Load the source by URL/URI/ID **or** parse an exportify CSV — see [Source input](#source-input).
2. For each track: run the same classification pipeline as [smart-add](#smart-add) (catch-all fallback and `--min-confidence` filter included).
3. Build a plan: for every (track → target playlist) pair, skip anything already in the local adds log so the tally reflects real additions.
4. Print a per-target tally sorted by count.
5. Ask one `y/N`. On `y`, write every planned addition (or dry-run print).

### Example output

```
Reading source playlist: To triage (3aBcDeFgHiJkLmNoPqRsTu)
Found 132 tracks. Classifying...

  [1/132] Bakermat - Walk That Walk
  [2/132] Charlotte de Witte - Doppler
  ...

Found 132 tracks.

Recommendations:
- 23 → House
- 18 → Techno
- 11 → Funny meme
- 7 → Ket420

Proceed? [y/N]: y

- House: ADDED Bakermat - Walk That Walk (snapshot AbCdEfGhIj…)
...

============================================================
Bulk add complete (EXECUTED): 59 added, 0 failed.
```

### Arguments

| Argument | Description |
|----------|-------------|
| `playlist` | Spotify playlist URL/URI/ID, path to an exportify CSV, or a name matching a file in [exportify-exports/](../exportify-exports/). See [Source input](#source-input). |
| `--execute` | Without this flag, planned additions print `DRY RUN (would add)` instead of writing |
| `--max-playlists` | Cap on classifier suggestions per track (1-5, default 3). The catch-all fallback may add one more on top when triggered. |
| `--min-playlists` | Minimum number of suggestions to ask the classifier for (1-5, default 1). Must not exceed `--max-playlists`. |
| `--min-confidence` | Drop suggestions below this confidence (0-100, default 80). The catch-all always survives (confidence 100). |

### Limits and caveats

- Each track costs one OpenAI classification call — a 132-track playlist is a few minutes of API time and ~$0.01–$0.05 of credit on `gpt-4.1-mini`.
- Duplicate detection here uses **only** the local adds log (`.tracks_log.json`), not a per-target Spotify scan. For untracked target playlists, seed the log first with [log-import](#log-import) or the script will happily re-add tracks the playlist already contains.
- Single y/N — there's no per-track override. Use [review-playlist](#review-playlist) when you need to vet tracks individually.
- If `playlist_items` returns stripped data (Spotify Developer Mode), the script offers a matching CSV in [exportify-exports/](../exportify-exports/) as a fallback — same behavior as [review-playlist](#review-playlist).

## `scan-for`

Pick one of your target playlists and scan a source playlist for tracks that would fit it. Each source track is classified, and any track whose classification includes the target (above `--min-confidence`) becomes a candidate. One `y/N` adds them all.

```bash
# Dry-run — list every source track that fits "House"
python playlist_manager.py scan-for "House" "https://open.spotify.com/playlist/<id>"

# Real run — add the candidates after the y/N
python playlist_manager.py scan-for "House" "https://open.spotify.com/playlist/<id>" --execute

# Stricter — only candidates the classifier scored at >= 75% for "House"
python playlist_manager.py scan-for "House" "https://open.spotify.com/playlist/<id>" --execute --min-confidence 75

# Scan a local exportify CSV instead of a Spotify URL
python playlist_manager.py scan-for "House" exportify-exports/Random_sht.csv

# Same — by bare name (resolved against exportify-exports/)
python playlist_manager.py scan-for "House" "Random sht"
```

The `source` argument accepts the same three forms as [review-playlist → Source input](#source-input) (URL/URI/ID, CSV path, or bare name in `exportify-exports/`), and applies the same CSV fallback when a URL returns no readable tracks.

### Flow

1. Resolve the target name (accepts the same aliases as [add](#add)) against [playlists.json](../playlists.json).
2. Load the source by URL/URI/ID **or** parse an exportify CSV — see [Source input](#source-input).
3. For each source track: skip if already in the target (per the local adds log); otherwise run the same classification pipeline as [smart-add](#smart-add).
4. If the target playlist appears in the track's matches (after `--min-confidence` filtering), record it as a candidate with the classifier's confidence for that target.
5. Sort candidates by confidence (desc), print them, and ask one `y/N`.
6. On `y`: add every candidate to the target (or dry-run print).

### Example output

```
Target playlist: House (0BEX4bI5xtkEVA4BfYTKg2)
Scanning source:  To triage (3aBcDeFgHiJkLmNoPqRsTu)
Found 132 tracks. Classifying...

  [1/132] Bakermat - Walk That Walk
  ...

Found 132 tracks.
  Already in House: 4
  Not a fit for House: 105

23 candidate(s) for House:
- 92% — Bakermat - Walk That Walk
    uplifting deep-house with vocals
- 88% — Honey Dijon - Show Me Some Love
    classic house groove with vocal stabs
...

Add all 23 to 'House'? [y/N]: y

- ADDED Bakermat - Walk That Walk (snapshot AbCdEfGhIj…)
...

============================================================
Scan complete (EXECUTED): 23 added, 0 failed.
```

### Arguments

| Argument | Description |
|----------|-------------|
| `target` | Target playlist name — must match a key under `"playlists"` or an alias in [playlists.json](../playlists.json) |
| `source` | Spotify playlist URL/URI/ID, path to an exportify CSV, or a name matching a file in [exportify-exports/](../exportify-exports/). See [Source input](#source-input). |
| `--execute` | Without this flag, the y/N prompt still runs but accepted candidates print `DRY RUN` |
| `--min-confidence` | Drop matches below this confidence before checking for the target (0-100, default 80). |

The classifier is always asked for its full top-5 matches per track so the target has the maximum chance to appear — there's no `--max-playlists` / `--min-playlists` here. Use `--min-confidence` to require a strong fit; the default of 80 keeps the candidate list to confident matches.

### How it differs from `bulk-playlist`

| | `bulk-playlist` | `scan-for` |
|--|--|--|
| Target playlists | All matches the classifier returns | One playlist you choose |
| Output | Per-target tally across the whole source | A single list of fitting tracks for the target |
| Use case | "Sort this triage playlist into all my buckets" | "Which of these would fit my House playlist?" |

### Limits and caveats

- The classifier is invoked once per source track, same cost profile as [bulk-playlist](#bulk-playlist).
- Duplicate detection uses the local adds log only — seed via [log-import](#log-import) if the target playlist isn't already tracked there, or the script may re-add tracks already in it.
- If a track somewhat fits the target but the classifier didn't include it in its top-5 matches at all, it won't be flagged. Lower `--min-confidence` for more lenient scans, or fall back to per-track [smart-add](#smart-add).
- If `playlist_items` returns stripped data (Spotify Developer Mode), the script offers a matching CSV in [exportify-exports/](../exportify-exports/) as a fallback — same behavior as [review-playlist](#review-playlist).

## `list-tracks`

Print every track in a playlist as tab-separated `URI<TAB>Artist - Title`. Useful for feeding a track list to the `/playlist-audit` or `/playlist-triage` skills without running a full classification.

```bash
# From a playlist name in playlists.json
python playlist_manager.py list-tracks "House"

# From a Spotify playlist URL
python playlist_manager.py list-tracks "https://open.spotify.com/playlist/<id>"

# From an exportify CSV (works without Spotify auth)
python playlist_manager.py list-tracks exportify-exports/House.csv
```

### Arguments

| Argument | Description |
|----------|-------------|
| `playlist` | Playlist name from `playlists.json`, Spotify playlist URL/URI/ID, or path to an exportify CSV |

### Output format

```
Playlist: House (42 tracks)
spotify:track:abc123	Martin Garrix - Animals
spotify:track:def456	Dua Lipa - Levitating
...
```

The first line is a summary header. Every subsequent line is `<spotify_uri>\t<Artist - Title>`.

### Empty output

If the Spotify API returns no tracks (Spotify Developer Mode strips `playlist_items`), pass an exportify CSV path instead. The command does not auto-fallback in this path — that fallback is handled by `review-playlist`, `bulk-playlist`, and `scan-for`.

## `audit-playlist`

Classify every track in one of your playlists against that playlist's own expected genre or theme using OpenAI, and print a confidence score per track. Tracks below `--min-confidence` are listed as removal candidates with their Spotify URIs.

> **Note**: For Claude AI + live web-search classification (more accurate, no OpenAI required), use the `/playlist-audit` skill instead. This command is the faster OpenAI-based fallback for larger playlists.

```bash
# Audit House playlist (reads tracks from Spotify API, uses default --min-confidence 60)
python playlist_manager.py audit-playlist "House"

# With exportify CSV fallback (needed in Spotify Developer Mode)
python playlist_manager.py audit-playlist "House" --csv exportify-exports/House.csv

# Lower the removal-candidate threshold to 40%
python playlist_manager.py audit-playlist "House" --min-confidence 40
```

### Arguments

| Argument | Description |
|----------|-------------|
| `playlist` | Playlist name or alias to audit — must be in `playlists.json` |
| `--csv PATH` | Path to an exportify CSV — workaround when Spotify dev-tier strips playlist contents |
| `--min-confidence N` | Tracks below this confidence (0–100, default 60) are listed as removal candidates |

### How classification works

The command fetches the track list (from Spotify API or CSV), then classifies each track with OpenAI against all playlists in your config. It reports the confidence score for the target playlist specifically. If the target playlist doesn't appear in the top-10 OpenAI results for a track, the track scores 0%.

This is the same OpenAI classifier used by `smart-add`, `review-playlist`, `bulk-playlist`, and `scan-for`.

### Example output

```
Auditing 'House' — 12 tracks
Source: 0BEX4bI5xtkEVA4BfYTKg2
============================================================

[1/12] Martin Garrix - Animals
  92% — progressive house anthem; AllMusic confirms house genre

[2/12] Dua Lipa - Levitating
  38% — disco-pop with mild house elements; primarily mainstream pop
...

============================================================

Audit complete: House
  Classified:              11/12
  High match   (≥80%): 9 tracks
  Medium match (60-79%): 1 track
  Low match    (<60%): 1 track
  Classification failed:   1 track

Tracks below 60% — candidates for removal:
   38% — Dua Lipa - Levitating
          URI: spotify:track:463CkQjx2Zk1yXoBuierM9
```

### What to do with the candidates

Copy the URIs from the output and pass them to [`remove`](#remove) one by one, or use the `/playlist-audit` skill which automates the whole flow (audit → threshold → confirmation → removal).

## `tests/test_spotify.py`

Not a subcommand — a standalone smoke test that authenticates with Spotify and lists all your playlists. Useful for confirming OAuth works.

```bash
python tests/test_spotify.py
```

The first run opens a browser tab for consent; subsequent runs reuse the cached token.
