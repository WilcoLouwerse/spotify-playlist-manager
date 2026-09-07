# Claude Development Docs

Documentation for Claude Code and contributors working in this repository. Site documentation for end users of the CLI lives in [docs/](../../docs/); this folder is the runtime context Claude reads when assisting with the codebase.

## Guides

### Writing

#### [Writing Docs](writing-docs.md)
Documentation principles for every `.md` file in this project — the core rule (reference, don't duplicate), sources of truth per concern, audience/location mapping, link structure, formatting, and the staleness signals to watch for.

#### [Writing Skills](writing-skills.md)
How to create and structure skills under `.claude/skills/<name>/` — folder layout (`templates/`, `references/`, `examples/`, `evals/`), `SKILL.md` format, the 7-level skill maturity framework, and the local skill-overview tooling.

### Doing work

#### [Command Reference](commands.md)
Index of slash commands (skills) available in this repo. Each row links to the skill's `SKILL.md` for the full reference.

---

## Quick Reference

### Skill tooling

- [.claude/skills/skill-level-overview.html](../skills/skill-level-overview.html) — visual maturity dashboard for every skill in this repo.
- [.claude/skills/update-skill-overview.sh](../skills/update-skill-overview.sh) — auto-refreshes the dashboard from each skill's `SKILL.md` and folder structure.

### Source-of-truth files (developer-facing)

| File | Purpose |
|------|---------|
| [playlist_manager.py](../../playlist_manager.py) | The single-file CLI — argparse subcommands, OAuth, OpenAI classifier, duplicate guard |
| [playlists.json](../../playlists.json) | Local playlist taxonomy (gitignored). Schema in [playlists.example.json](../../playlists.example.json) |
| [requirements.txt](../../requirements.txt) | Pinned Python dependencies |
| [docs/setup.md](../../docs/setup.md) | Credentials, `.env`, venv setup |
| [docs/commands.md](../../docs/commands.md) | End-user CLI reference (every subcommand, dry-run behavior, duplicate guard) |
| [docs/architecture.md](../../docs/architecture.md) | Code structure, OAuth flow, OpenAI classifier, IPv4-only WSL workaround |
| [tests/](../../tests/) | `pytest` unit tests + OAuth smoke test |

See [docs/architecture.md → File layout](../../docs/architecture.md#file-layout) for the full repository map.
