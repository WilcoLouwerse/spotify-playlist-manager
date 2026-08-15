# Add-plan template (add flow)

Render after the user has chosen playlists via the `AskUserQuestion` multi-select in step 10.b. That selection **is** the confirmation gate — do **not** call `AskUserQuestion` again to confirm the commands. Render the plan, then run the commands directly.

```
Je wilt {TRACK_TITLE} toevoegen aan {N} playlist(s):

{LIST_OF_PLAYLISTS}

Ik draai deze commando's vanuit de repo-root:

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

## Execute the commands

Immediately after rendering the plan, run each command via Bash sequentially. No extra confirmation prompt — the multi-select in step 10.b already authorized the write. Print the script's output verbatim, in order. Don't paraphrase the duplicate-guard messages — `SKIP: track already in playlist` and `ADDED ...` come from the script and should appear as-is.

End with one Dutch summary line:

```
Klaar! {ADDED} toegevoegd, {SKIPPED} overgeslagen (al in playlist).
```

Then call **AskUserQuestion** again (per `templates/followup.md`) so the user can chain another action or pick "Klaar".

## If the user selected zero playlists

If the multi-select came back empty, skip the plan render and the Bash calls:

```
Oké, niets gewijzigd.
```

Then call **AskUserQuestion** again (per `templates/followup.md`) so the user can pick another action or stop.
