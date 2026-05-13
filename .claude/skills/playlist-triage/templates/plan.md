# Plan template

Render after the user has chosen workflow (review / bulk) + source + dry-run/execute. Substitute placeholders. Show **before** running any Bash.

```
Je wilt {SOURCE_LABEL} triëren via {COMMAND_LABEL} ({MODE_LABEL}).

Ik ga dit commando draaien vanuit de repo-root:

{CODE_BLOCK_WITH_COMMAND}

{INTERACTIVE_HINT}
```

## Placeholder reference

- `{SOURCE_LABEL}` — display name of the source: a Spotify playlist name (if known from the URL), the CSV filename, or the bare name the user typed.
- `{COMMAND_LABEL}` — `review-playlist` or `bulk-playlist`.
- `{MODE_LABEL}` — `dry-run` or `execute`.
- `{CODE_BLOCK_WITH_COMMAND}` — fenced bash block with **one** command. Quote the source verbatim. Append `--execute` only in execute mode. Append `--max-playlists N --min-confidence X` only when the user asked to deviate from defaults.

  ```bash
  .venv/bin/python playlist_manager.py review-playlist "<source>"            # dry-run
  .venv/bin/python playlist_manager.py review-playlist "<source>" --execute  # execute
  .venv/bin/python playlist_manager.py bulk-playlist "<source>" --execute    # execute, single y/N
  yes | .venv/bin/python playlist_manager.py bulk-playlist "<source>" --execute   # execute + auto-accept (bulk only)
  ```

- `{INTERACTIVE_HINT}` — one Dutch sentence telling the user what to expect:
  - Dry-run: `"Dit is een dry-run — geen y/N prompts, niets wordt geschreven."`
  - `review-playlist` execute (terminal path): `"Het script vraagt per nummer y/N/s/q in je terminal. Draai 'm zelf, ik kan die prompts niet via chat beantwoorden."`
  - `bulk-playlist` execute (terminal path): `"Het script vraagt één y/N voor het hele plan. Draai 'm zelf in je terminal, of laat mij 'm draaien met automatisch 'y' via een pipe."`
  - `bulk-playlist` execute (`yes |` path): `"Ik draai 'm voor je met automatisch 'y' — geen handmatige prompt."`

---

## After the user confirms

Run via Bash. Print the script's output verbatim, then a Dutch summary line (per `SKILL.md` step 9). Don't paraphrase `ADDED`, `SKIP`, `DRY RUN: would add`, or the final `... complete (EXECUTED): N added, M failed` line.

---

## If the user cancels

```
Oké, niets gedaan.
```

Then call **AskUserQuestion** again so the user can tweak the source, the workflow, the mode, or stop.
