# Command Reference

Reference for slash commands (skills) available in this repository. Each command is a folder under [.claude/skills/](../skills/) with a `SKILL.md` entry point — click through for the full instructions.

For the end-user CLI reference (`python playlist_manager.py …`), see [docs/commands.md](../../docs/commands.md). This file lists Claude Code skills, not Python subcommands.

---

## Skills

| Command | Category | Description |
|---------|----------|-------------|
| [`/playlist-match`](#playlist-match) | Workflow | Classifies a shared song's genres with confidence scores, recommends matching playlists from `playlists.json`, and can invoke `add` to write the result |
| [`/playlist-triage`](#playlist-triage) | Workflow | Triages a source playlist into target playlists via `review-playlist` (per-track y/N) or `bulk-playlist` (single y/N) |
| [`/playlist-scan`](#playlist-scan) | Workflow | Scans a source playlist for tracks that fit a chosen target playlist via `scan-for` |
| [`/playlist-remove`](#playlist-remove) | Workflow | Removes a track from one or more playlists via `remove` |
| [`/playlist-audit`](#playlist-audit) | Workflow | Audits a playlist's genre/theme fit with confidence scores per track and offers to remove low-confidence tracks |
| [`/playlist-log-import`](#playlist-log-import) | Workflow | Seeds the local duplicate-guard log (`.tracks_log.json`) from an Exportify CSV via `log-import` |
| [`/playlist-config`](#playlist-config) | Workflow | Bootstraps or extends `playlists.json` from your Spotify account via `list-playlists --all` |

All seven skills produce **Dutch** user-facing prose (the user's preference); their `SKILL.md`, `references/`, `templates/`, and `examples/` stay in English so triggers and steering remain model-readable. See [writing-docs.md → Language](writing-docs.md) for the convention.

---

### `/playlist-match`

**Category:** Workflow

Analyzes any song the user shares — `Artist - Title`, a Spotify track URL/URI/ID, or a Dutch ask like *"welke playlist past hierbij"* — identifies its genres with confidence scores, recommends 1–5 playlists from [`playlists.json`](../../playlists.json), and on request adds the track via the project's CLI.

**Usage:**

```
# Trigger phrases (Dutch or English work)
Welke playlist past bij Daft Punk - Around the World?
https://open.spotify.com/track/<id>
Artist - Title
```

**What it does:**

1. Detects input type — new analysis, natural-language follow-up, or out-of-scope (routed to a sibling skill).
2. Reads `playlists.json` each run so user edits to the taxonomy are honored.
3. Identifies the song and resolves it to `Artist - Title` (preserving the URL/URI/ID when given, for later `add` invocations).
4. Determines genres via live web lookup (AllMusic, Wikipedia, RYM, Discogs, Last.fm) as the primary source; training-data recall is the last resort only.
5. Matches 1–5 playlists from `playlists.json` categories, each scored with a confidence percentage and a short reason.
6. Renders a Dutch analysis (artist info, song description, genres, playlist matches), then calls `AskUserQuestion` with a standard follow-up menu.
7. On "Voeg toe aan playlists", uses `AskUserQuestion` to pick playlists from the recommended set, shows the exact `playlist_manager.py add` commands, asks for one final confirmation, then runs them via Bash.

**Guardrails:**

- **Never** recommends `Random sht` — it is the script-side catch-all under `playlists.json -> catch_all` and must not appear in user-facing output.
- **Never** recommends a playlist that is not currently present in `playlists.json -> categories` (the file is read each run).
- **Never** invokes `add` with `--execute` without explicit confirmation in the same turn.
- **Never** invents or guesses a Spotify track ID. If only `Artist - Title` was given, asks the user to paste a URL before invoking `add`.
- **Never** uses old letter-shortcut menus (`A`–`F` etc.) — all follow-ups go through `AskUserQuestion`.
- User-facing prose is **Dutch**; playlist names stay verbatim from `playlists.json` (no translation).

**Source:** [.claude/skills/playlist-match/SKILL.md](../skills/playlist-match/SKILL.md). Maturity in the [Skill Level Overview](../skills/skill-level-overview.html) dashboard.

---

### `/playlist-triage`

**Category:** Workflow

Sorts a whole source playlist into many target playlists in one sitting. Wraps the project's [`review-playlist`](../../docs/commands.md#review-playlist) (per-track `y/N/s/q`) and [`bulk-playlist`](../../docs/commands.md#bulk-playlist) (single `y/N` for the whole plan) CLI subcommands.

**Usage:**

```
# Trigger phrases
sorteer mijn 'to triage'
review this playlist
haal mijn triage leeg
https://open.spotify.com/playlist/<id>
```

**What it does:**

1. Resolves the source — Spotify URL/URI/ID, a CSV path under `exportify-exports/`, or a bare playlist name matched against that folder.
2. Asks via `AskUserQuestion` which workflow to use: **Claude + web** (per-track, ≤20 tracks default), **Review CLI** (per-track y/N, 20–50 tracks), or **Bulk CLI** (single y/N, >50 tracks).
3. **Web-first path**: uses `list-tracks` + Claude AI + live WebSearch per track (same methodology as `/playlist-match`); confirms each track via `AskUserQuestion` before running `add --execute`.
4. **CLI paths**: surfaces the classifier defaults (`--max-playlists 3 --min-playlists 1 --min-confidence 80`), defaults to dry-run, renders the exact `playlist_manager.py review-playlist` / `bulk-playlist` command, and runs it via Bash after confirmation.
5. For `bulk-playlist --execute`, offers a `yes |` pipe option; for `review-playlist --execute`, always recommends the user's own terminal (per-track stdin cannot be driven from chat).

**Guardrails:**

- Defaults to dry-run; `--execute` requires explicit confirmation in the same turn.
- Won't guess a missing source — asks via `AskUserQuestion`.
- Sticks to CSV filenames listed in `exportify-exports/`; never invents a filename.
- User-facing prose is **Dutch**.

**Source:** [.claude/skills/playlist-triage/SKILL.md](../skills/playlist-triage/SKILL.md).

---

### `/playlist-scan`

**Category:** Workflow

Picks one target playlist and mines a source playlist for tracks that fit it. Wraps the project's [`scan-for`](../../docs/commands.md#scan-for) CLI subcommand — the source-to-one-target counterpart to `/playlist-triage` (source-to-many).

**Usage:**

```
# Trigger phrases
welke tracks in random sht passen in House?
scan random_sht.csv op Techno
find house-fitting tracks in my triage
```

**What it does:**

1. Resolves the target name against `playlists.json` (aliases honored). Refuses the catch-all (`Random sht`) without an explicit second confirmation.
2. Resolves the source — Spotify URL/URI/ID, CSV path, or bare name in `exportify-exports/`.
3. Asks via `AskUserQuestion` which mode to use: **Claude + web** (per-track, ≤20 source tracks default) or **scan-for CLI** (OpenAI-backed, faster for larger sources).
4. **Web-first path**: uses `list-tracks` + Claude AI + live WebSearch per track; presents candidates via `AskUserQuestion` multiSelect; runs `add --execute` per confirmed candidate.
5. **CLI path**: defaults to dry-run; renders the exact `playlist_manager.py scan-for` command and runs it via Bash after confirmation.

**Guardrails:**

- Refuses `Random sht` as a target unless the user re-confirms — almost never their actual intent.
- Defaults to dry-run; `--execute` requires explicit confirmation.
- User-facing prose is **Dutch**.

**Source:** [.claude/skills/playlist-scan/SKILL.md](../skills/playlist-scan/SKILL.md).

---

### `/playlist-remove`

**Category:** Workflow

Removes a track from one or more playlists. Wraps the project's [`remove`](../../docs/commands.md#remove) CLI subcommand.

**Usage:**

```
# Trigger phrases
Verwijder https://open.spotify.com/track/<id> uit House
remove spotify:track:<id> from Techno
haal dit nummer weg uit mijn playlists
verwijder Dua Lipa - Levitating uit Drum & Bass
```

**What it does:**

1. Parses the track input — accepts Spotify URL, URI, or ID directly. If only `Artist - Title` is given, asks for a URL/URI/ID via `AskUserQuestion` (never guesses or invents a track ID).
2. Resolves the target playlist(s) against `playlists.json`. Accepts a single playlist name or asks via `AskUserQuestion` with `multiSelect: true` for multiple targets.
3. Flags `Random sht` with an extra confirmation — removing from the catch-all is almost never the intent.
4. Shows the exact `playlist_manager.py remove "<url>" "<Playlist>" --execute` command(s) and confirms via `AskUserQuestion` before running anything.
5. Reports the script's output verbatim (`DONE`, `SKIP: track not found in playlist`, etc.) and explains SKIP in Dutch when the track was likely added through the Spotify UI.

**Guardrails:**

- Never runs `remove --execute` without explicit confirmation in the same turn.
- Never invents or guesses a Spotify track ID.
- Warns explicitly when `Random sht` is the target and requires a second confirmation.
- User-facing prose is **Dutch**.

**Source:** [.claude/skills/playlist-remove/SKILL.md](../skills/playlist-remove/SKILL.md).

---

### `/playlist-audit`

**Category:** Workflow

Audits every track in a playlist against its genre/theme, shows a confidence score per track, and offers to remove low-confidence tracks. Uses Claude AI + live web search as the primary classifier (same methodology as `/playlist-match`), with the OpenAI-backed `audit-playlist` CLI as the faster fallback for large playlists.

**Usage:**

```
# Trigger phrases
controleer mijn House playlist — welke nummers passen er niet in?
audit mijn Techno playlist
welke nummers in House passen er eigenlijk niet in?
audit House, gebruik de snelle mode
```

**What it does:**

1. Resolves the playlist from `playlists.json`. Refuses to audit `Random sht` (it's the catch-all by design).
2. Runs `list-tracks "<playlist>"` to get the track list. Falls back to an exportify CSV when the API returns empty (Spotify Dev Mode).
3. Offers two audit modes via `AskUserQuestion`: **web-first** (Claude + WebSearch per track, default for ≤20 tracks) or **quick** (OpenAI `audit-playlist` CLI, faster for larger playlists).
4. Produces a Dutch audit report with ✅/⚠️/❌ per track and a score distribution summary.
5. Asks for a removal threshold via `AskUserQuestion`, presents low-confidence candidates via `multiSelect`, confirms, then runs `remove --execute` for each accepted track.

**Guardrails:**

- Never audits `Random sht`.
- Never removes a track without explicit confirmation.
- Never fabricates confidence scores — if a source is unavailable, says so.
- User-facing prose is **Dutch**.

**Source:** [.claude/skills/playlist-audit/SKILL.md](../skills/playlist-audit/SKILL.md).

---

### `/playlist-log-import`

**Category:** Workflow

Seeds the local duplicate-guard log (`.tracks_log.json`) for one playlist from an Exportify CSV (or any file containing Spotify track URIs/URLs/IDs). Wraps the project's [`log-import`](../../docs/commands.md#log-import) CLI subcommand.

**Usage:**

```
# Trigger phrases
seed mijn log voor House
log-import House exportify-exports/house.csv
House CSV importeren
registreer deze export voor Techno
```

**What it does:**

1. Resolves the target against `playlists.json -> playlists` / `aliases`. Renders the canonical name in the planned command.
2. Resolves the file path. Accepts absolute paths, relative paths, or bare names against `exportify-exports/`. Verifies the file exists before running.
3. Confirms target + file (and line count when cheap) via `AskUserQuestion` — this is the **only** safety gate (no `--execute` flag exists because no Spotify API call is made).
4. Renders the exact `playlist_manager.py log-import "<TARGET>" "<FILE>"` command and runs it via Bash.

**Guardrails:**

- Local-only. No Spotify side-effect, no `--execute` flag — the AskUserQuestion gate is the safety net.
- Never invents a filename; if the file isn't found, asks the user to correct the path.
- User-facing prose is **Dutch**; canonical playlist names are quoted verbatim from `playlists.json`.

**Source:** [.claude/skills/playlist-log-import/SKILL.md](../skills/playlist-log-import/SKILL.md).

---

### `/playlist-config`

**Category:** Workflow

Bootstraps or extends [`playlists.json`](../../playlists.json) from the user's Spotify account. Wraps the project's [`list-playlists`](../../docs/commands.md#list-playlists) CLI subcommand (with and without `--all`). The CLI itself only reads; **the skill is what mutates `playlists.json`** under an `AskUserQuestion` gate.

**Usage:**

```
# Trigger phrases
welke playlists ken ik?
list-playlists
add my new playlist to the config
sync mijn playlists.json met Spotify
```

**What it does:**

1. Detects intent (inspect / bootstrap / extend) and asks via `AskUserQuestion` if ambiguous.
2. Runs `list-playlists` (no flags) for inspect, or `list-playlists --all` for bootstrap / extend. Output is printed verbatim.
3. For bootstrap / extend: parses the `Untracked` block, surfaces it to the user, and walks them through which entries to add — plus optional `aliases`, `categories`, `special_rules`, and (for bootstrap) `catch_all`.
4. Edits `playlists.json` only after an explicit `AskUserQuestion` confirmation; surfaces the resulting diff.

**Guardrails:**

- The CLI is read-only — the `playlists.json` edit is what requires confirmation.
- Validates every entry against the schema enforced by `_validate_config` (22-char Spotify IDs, alias targets that resolve, category members that resolve, etc.). See [setup.md → Configure your playlists](../../docs/setup.md#configure-your-playlists).
- Stops cleanly when the Spotify OAuth call fails — never tries to invent IDs.
- User-facing prose is **Dutch**.

**Source:** [.claude/skills/playlist-config/SKILL.md](../skills/playlist-config/SKILL.md).

---

## Maintaining this list

When you add a new skill under `.claude/skills/<name>/`:

1. Add a row to the table above with the slash command, category, and a one-line description sourced from the skill's `description` frontmatter
2. Add a short subsection beneath it covering usage, what it does, and guardrails
3. Run `bash .claude/skills/update-skill-overview.sh` to refresh [skill-level-overview.html](../skills/skill-level-overview.html)

See [writing-skills.md](writing-skills.md) for the full skill authoring guide.
