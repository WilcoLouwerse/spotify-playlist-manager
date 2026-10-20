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
- `{CODE_BLOCK_WITH_COMMANDS}` — fenced bash block, one command per playlist, in the user's selection order, then always one `like` line for Liked Songs, **all with `--execute`**:
  ```bash
  .venv/bin/python playlist_manager.py add "<URL>" "House" --execute
  .venv/bin/python playlist_manager.py add "<URL>" "Party" --execute
  .venv/bin/python playlist_manager.py like "<URL>" --execute
  ```
  Quote every playlist name with double quotes. Liked Songs is not listed in `{LIST_OF_PLAYLISTS}` and has no confidence score — the `like` line in the code block is enough.

## Execute the commands

Immediately after rendering the plan, run each command via Bash sequentially. No extra confirmation prompt — the multi-select in step 10.b already authorized the write. Print the script's output verbatim, in order. Don't paraphrase the script's messages — `DONE: track added (snapshot …)`, `SKIP: track already in playlist. No changes made.` and, for the like line, `DONE: track added to Liked Songs` / `SKIP: track already in Liked Songs. No changes made.` come from the script and should appear as-is.

End with one Dutch summary line:

```
Klaar! {ADDED} toegevoegd, {SKIPPED} overgeslagen (al in playlist). Liked Songs: {LIKED}.
```

`{LIKED}` — `toegevoegd` on `DONE`, `stond er al` on `SKIP`, `mislukt` on `FAILED` (then add the token tip from `references/add-command.md`).

Then call **AskUserQuestion** again (per `templates/followup.md`) so the user can chain another action or pick "Klaar".

## If the user selected zero playlists

If the multi-select came back empty, skip the plan render and the Bash calls (including `like`):

```
Oké, niets gewijzigd.
```

Then call **AskUserQuestion** again (per `templates/followup.md`) so the user can pick another action or stop.
