# Plan template

Render after the user has resolved a target + file (steps 2-3 of SKILL.md). Show **before** running any Bash, and **before** the AskUserQuestion confirmation in step 4.

```
Je wilt de log voor {TARGET} seeden met {FILE_LABEL} ({LINE_COUNT} regels).

Dit is een lokale operatie — er wordt niets naar Spotify geschreven. Alleen `.adds_log.json` wordt bijgewerkt.

Ik ga dit commando draaien vanuit de repo-root:

{CODE_BLOCK_WITH_COMMAND}
```

## Placeholder reference

- `{TARGET}` — canonical playlist name from `playlists.json` (not an alias).
- `{FILE_LABEL}` — full resolved path of the file (e.g. `exportify-exports/House.csv`). Show the path the CLI will actually receive — that's what will appear in `.adds_log.json`'s audit trail if something looks off later.
- `{LINE_COUNT}` — line count of the file, if cheaply available (`wc -l` is fine). If reading the file is awkward, omit this parenthetical.
- `{CODE_BLOCK_WITH_COMMAND}` — fenced bash block with **one** command. Both `<TARGET>` and `<FILE>` quoted with double quotes.

  ```bash
  .venv/bin/python playlist_manager.py log-import "<TARGET>" "<FILE>"
  ```

  No flags. `log-import` does not accept `--execute`, `--dry-run`, `--min-confidence`, or any other tuning knob.

---

## After the plan is shown — AskUserQuestion

Step 4 of SKILL.md. Use exactly these options (translate-friendly):

- **Ja, importeer** — proceed.
- **Nee, andere target/file** — re-resolve (loop back to step 2 or 3).
- **Annuleren** — end the flow with `Oké, niets gedaan.`.

---

## After the user confirms — run

Run via Bash. Print the script's output verbatim — five counter lines plus the playlist header. Don't paraphrase.

Then add a Dutch summary line (per SKILL.md step 7).

---

## If the user cancels

```
Oké, niets gedaan. `.adds_log.json` is niet aangepast.
```

Then call **AskUserQuestion** again so the user can change the target, file, or stop entirely.
