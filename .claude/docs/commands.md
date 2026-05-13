# Command Reference

Reference for slash commands (skills) available in this repository. Each command is a folder under [.claude/skills/](../skills/) with a `SKILL.md` entry point — click through for the full instructions.

For the end-user CLI reference (`python playlist_manager.py …`), see [docs/commands.md](../../docs/commands.md). This file lists Claude Code skills, not Python subcommands.

---

## Skills

| Command | Category | Description |
|---------|----------|-------------|
| `/playlist-match` | Workflow | Classifies a shared song's genres with confidence scores, recommends matching playlists from `playlists.json`, and can invoke `add` / `smart-add` to write the result |

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

1. Detects input type — new analysis, single-letter follow-up (`A`–`F`, `Z`/`Y`/`X`/`W`, `?`), or a natural-language add request
2. Reads `playlists.json` each run so user edits to the taxonomy are honored
3. Identifies the song and resolves it to `Artist - Title` (preserving the URL/URI/ID when given, for later `add` invocations)
4. Determines genres from multiple independent sources (Last.fm, AllMusic, Wikipedia, RYM, Discogs, label sites) — never genre-by-artist-reputation alone
5. Matches 1–5 playlists from `playlists.json` categories, each scored with a confidence percentage and a short reason
6. Renders a Dutch analysis (artist info, song description, genres, playlist matches, and the fixed `A`–`F` choice menu)
7. On follow-up `F` (or a natural-language add request), uses `AskUserQuestion` to pick playlists from the recommended set, defaults to **dry-run**, shows the exact `playlist_manager.py add` commands, asks for one final confirmation, then runs them via Bash

**Guardrails:**

- **Never** recommends `Random sht` — it is the script-side catch-all under `playlists.json -> catch_all` and must not appear in user-facing output.
- **Never** recommends a playlist that is not currently present in `playlists.json -> categories` (the file is read each run).
- **Never** invokes `add` (or `smart-add`) with `--execute` without explicit confirmation in the same turn. Dry-run first whenever in doubt.
- **Never** invents or guesses a Spotify track ID. If only `Artist - Title` was given, asks the user to paste a URL before invoking `add`.
- User-facing prose is **Dutch**; playlist names stay verbatim from `playlists.json` (no translation).

**Maturity:** See the [Skill Level Overview](../skills/skill-level-overview.html) dashboard, or [.claude/skills/playlist-match/SKILL.md](../skills/playlist-match/SKILL.md) for the source.

---

## Maintaining this list

When you add a new skill under `.claude/skills/<name>/`:

1. Add a row to the table above with the slash command, category, and a one-line description sourced from the skill's `description` frontmatter
2. Add a short subsection beneath it covering usage, what it does, and guardrails
3. Run `bash .claude/skills/update-skill-overview.sh` to refresh [skill-level-overview.html](../skills/skill-level-overview.html)

See [writing-skills.md](writing-skills.md) for the full skill authoring guide.
