# Add-confirmation template (add flow)

Render after the user has chosen playlists. Substitute placeholders. Show **before** the mandatory `AskUserQuestion` confirmation, which itself comes **before** any Bash call.

```
Je wilt {TRACK_TITLE} toevoegen aan {N} playlist(s):

{LIST_OF_PLAYLISTS}

Ik ga deze commando's draaien vanuit de repo-root:

{CODE_BLOCK_WITH_COMMANDS}
```

## Placeholder reference

- `{TRACK_TITLE}` — `Artiestnaam - Nummernaam` (same as the analysis title).
- `{N}` — count of selected playlists.
- `{LIST_OF_PLAYLISTS}` — bulleted list, one playlist per line, with the confidence score from the analysis:
  ```
  - House — 92%
  - Party — 84%
  ```
- `{CODE_BLOCK_WITH_COMMANDS}` — fenced bash block, one command per playlist, in the user's selection order, **always with `--execute`**:
  ```bash
  .venv/bin/python playlist_manager.py add "<URL>" "House" --execute
  .venv/bin/python playlist_manager.py add "<URL>" "Party" --execute
  ```
  Quote every playlist name with double quotes.

## Confirmation step (mandatory)

After rendering the plan, call **AskUserQuestion**:

> "Klaar om deze commando's uit te voeren?"
> - Ja, voer uit
> - Nee, annuleren

Only run the commands when the user picks **Ja, voer uit**. This is the single safety gate — the skill never invokes the python script without it.

## After the user confirms

Run each command via Bash. Print the script's output verbatim, in order. Don't paraphrase the duplicate-guard messages — `SKIP: track already in playlist` and `ADDED ...` come from the script and should appear as-is.

End with one Dutch summary line:

```
Klaar! {ADDED} toegevoegd, {SKIPPED} overgeslagen (al in playlist).
```

Then call **AskUserQuestion** again (per `templates/followup.md`) so the user can chain another action or pick "Klaar".

## If the user cancels

```
Oké, niets gewijzigd.
```

Then call **AskUserQuestion** again (per `templates/followup.md`) so the user can pick another action or stop.
