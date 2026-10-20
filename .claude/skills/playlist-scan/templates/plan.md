# Plan template

Render after the user has chosen target + source + dry-run/execute. Substitute placeholders. Show **before** running any Bash.

```
Je wilt {TARGET} kandidaten zoeken in {SOURCE_LABEL} ({MODE_LABEL}).

Ik ga dit commando draaien vanuit de repo-root:

{CODE_BLOCK_WITH_COMMAND}

{INTERACTIVE_HINT}
```

## Placeholder reference

- `{TARGET}` — canonical playlist name from `playlists.json` (not an alias; the CLI accepts aliases but the rendered command should use the canonical name so it reads unambiguously).
- `{SOURCE_LABEL}` — display name of the source: the Spotify playlist name (if known), the CSV filename, or the bare name the user typed.
- `{MODE_LABEL}` — `dry-run` or `execute`.
- `{CODE_BLOCK_WITH_COMMAND}` — fenced bash block with **one** command. Both `<TARGET>` and `<SOURCE>` quoted with double quotes.

  ```bash
  yes | .venv/bin/python playlist_manager.py scan-for "<TARGET>" "<SOURCE>"   # dry-run (pipe is harmless without --execute)
  .venv/bin/python playlist_manager.py scan-for "<TARGET>" "<SOURCE>" --execute  # execute, single y/N
  yes | .venv/bin/python playlist_manager.py scan-for "<TARGET>" "<SOURCE>" --execute   # execute + auto-accept
  ```

  Append `--min-confidence N` only when the user asked to deviate from the default of `80`.

- `{INTERACTIVE_HINT}` — one Dutch sentence:
  - Dry-run: `"Dit is een dry-run — ik beantwoord de y/N-prompt automatisch, maar zonder --execute wordt er niets geschreven."`
  - Execute (terminal path): `"Het script toont een kandidatenlijst en vraagt één y/N in je terminal. Draai 'm zelf en typ y om alles aan {TARGET} toe te voegen."`
  - Execute (`yes |` path): `"Ik draai 'm voor je met automatisch 'y' — alle kandidaten worden toegevoegd aan {TARGET}."`

---

## After the user confirms

Run via Bash. Print the script's output verbatim, then a Dutch summary line (per SKILL.md step 10). Don't paraphrase the candidate list, the `Already in …` / `Not a fit for …` counts, `ADDED ...`, `DRY RUN (would add ...)`, or `Scan complete (…): N added, M failed.`

---

## If the user cancels

```
Oké, niets gedaan.
```

Then call **AskUserQuestion** again so the user can change the target, source, mode, or stop.
