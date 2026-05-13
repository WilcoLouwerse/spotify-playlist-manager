# Adding the song via `playlist_manager.py`

When the user picks **Voeg toe aan playlists** in the follow-up `AskUserQuestion` (or asks naturally — "voeg toe aan House"), the skill invokes the project's existing CLI. **Read [`docs/commands.md`](../../../../docs/commands.md) for the authoritative reference.** This page is a fast index of what to call, with what flags, and why.

---

## Which command — `add` vs `smart-add`

Default: **`add`** (one track, one playlist, no classifier).

The skill has already produced a multi-source classification more rigorous than `smart-add`'s single OpenAI call. Re-running `smart-add` would discard your work and ask OpenAI to redo it. Use `add` once per chosen playlist instead.

Use `smart-add` **only** if the user explicitly says: "let the project's classifier decide", "use smart-add", or similar. Don't substitute it on your own initiative.

| Command | Picks playlists? | Confirmation | When the skill uses it |
|---------|------------------|--------------|------------------------|
| `add` | No — you pass the playlist name | None — writes immediately under `--execute` | Default. Loop once per playlist the user chose. |
| `smart-add` | Yes — OpenAI picks | Interactive per-playlist y/N (or single bulk y/N with `--accept-all`) | Only when the user explicitly asks for it. |
| `analyze-only` | Yes — classify only | None — no writes | Don't use from this skill; we did our own classification already. |

---

## `add` — exact invocation

From the repo root, with the venv. The skill always runs with `--execute` (it confirms with the user via **AskUserQuestion** before invoking Bash):

```bash
.venv/bin/python playlist_manager.py add "<track>" "<Playlist Name>" --execute
```

Dry-run (omitting `--execute`) still exists in the CLI, but the skill no longer asks the user to choose between dry-run and execute — the confirmation prompt is the safety gate.

Argument rules:

- `<track>` — Spotify track URL (`https://open.spotify.com/track/<id>`), URI (`spotify:track:<id>`), or bare 22-char ID. If the user gave you any of these in their original message, use it verbatim. Don't invent or guess one.
- `<Playlist Name>` — must match a key under `"playlists"` in [`playlists.json`](../../../../playlists.json) or an entry under `"aliases"`. Case-insensitive. **Quote** the name so spaces, slashes, and apostrophes don't break the shell.

Special playlist-name characters to handle:
- `Jazz / Funk / Soul` → `"Jazz / Funk / Soul"`
- `Rustig / 'anders'` → `"Rustig / 'anders'"` (single quotes inside double quotes are fine)
- `Pop / Mainstream` → `"Pop / Mainstream"`

---

## Behaviour the user will see

From [`docs/commands.md`](../../../../docs/commands.md):

- **Dry-run by default in the CLI.** Without `--execute`, the script prints the planned action and exits without writing. The skill always passes `--execute` because it has already confirmed with the user via **AskUserQuestion**.
- **Duplicate guard is always on.** Before writing, the script consults the local `.adds_log.json`. If the track is already logged for that playlist, the script prints `SKIP: track already in playlist` and exits. There is no override flag.
- **IPv4 only.** Spotify's IPv6 route is broken on WSL; the script forces IPv4. No skill action needed — just know that the first call may take a moment.
- **Unknown playlist** → `ValueError: Unknown playlist: ...`. The skill should have already validated names against `playlists.json`; if this fires, the file probably changed mid-flow — re-read it.

---

## The add flow, step by step

1. **Do we have a Spotify URL/URI/ID for this song?**
   - Yes → use it.
   - No → **AskUserQuestion**:

     > "Voor 'Voeg toe aan playlists' heb ik een Spotify-link, URI of track-ID nodig. Plak die via 'Other', of kies 'Annuleren'."

     If the user pastes a URL, continue. If they cancel, end the add flow gracefully and offer the follow-up menu again.

2. **Which playlists?** **AskUserQuestion** with `multiSelect: true`, listing **only the playlists you recommended in step 6**. Optionally add an "All recommended" shortcut. Honor the user's selection literally — never silently add a playlist they didn't pick.

3. **Render the plan** using `templates/add-confirmation.md`. One `add --execute` command per playlist, on its own line, in a code block.

4. **Mandatory confirmation before running.** **AskUserQuestion**:

   > "Klaar om deze commando's uit te voeren?"
   > - Ja, voer uit
   > - Nee, annuleren

   On *Nee*, end the add flow and re-offer the follow-up menu. This step is **never skipped** — it is the single safety gate before any python script runs.

5. **Run** each command via Bash, sequentially. Print the script's output verbatim. Order: same order the user selected the playlists.

6. **Summarise** with one Dutch sentence at the end:

   > "Klaar! N toegevoegd, M overgeslagen (al in playlist)."

   Then call **AskUserQuestion** again (per `templates/followup.md`) so the user can chain another action or pick "Klaar".

---

## When `add` exits with `SKIP: track already in playlist`

The duplicate guard caught it. Surface the message to the user as-is; don't retry, and don't pretend it was added. Continue with the next playlist in the loop.

---

## When `smart-add` is the right call

Only when the user explicitly opts in. Then:

```bash
# Dry-run, per-playlist confirmation
.venv/bin/python playlist_manager.py smart-add "<track>"

# Execute, single bulk y/N
.venv/bin/python playlist_manager.py smart-add "<track>" --execute --accept-all

# Filter the classifier's output
.venv/bin/python playlist_manager.py smart-add "<track>" --max-playlists 3 --min-confidence 75
```

The script handles its own y/N prompts on stdin. The skill should explain that the user will see interactive prompts in their terminal, and step back rather than scripting answers.

---

## What about the bulk commands?

`review-playlist`, `bulk-playlist`, and `scan-for` operate on a *source playlist*, not a single song. They're out of scope for this skill — when the user wants to triage a whole playlist, they should run those commands directly per [`docs/commands.md`](../../../../docs/commands.md).
