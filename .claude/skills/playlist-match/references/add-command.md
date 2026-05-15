# Adding the song via `playlist_manager.py`

When the user picks **Voeg toe aan playlists** in the follow-up `AskUserQuestion` (or asks naturally — "voeg toe aan House"), the skill invokes the project's existing CLI. **Read [`docs/commands.md`](../../../../docs/commands.md) for the authoritative reference.** This page is a fast index of what to call, with what flags, and why.

---

## Which command — only `add`

This skill always uses **`add`** (one track, one playlist, no Python-side classifier). Claude AI is the classifier — steps 5–6 of `SKILL.md` produce a multi-source classification, and step 10 loops `add` once per playlist the user picked.

The project's `smart-add` and `analyze-only` commands call OpenAI to pick playlists. **This skill never invokes them.** If the user asks for "the classifier", "AI-picked playlists", or "use smart-add", re-do Claude AI's classification with whatever framing they want (stricter confidence band, different scope, etc.) and then loop `add` over the picks — never shell out to OpenAI.

| Command | Picks playlists? | This skill | Why |
|---------|------------------|------------|-----|
| `add` | No — you pass the playlist name | **Yes — only command used.** Loop once per playlist the user chose. | Claude AI already classified; `add` just executes the write. |
| `smart-add` | Yes — OpenAI picks | **Never.** | Claude AI replaces the OpenAI classifier; re-do the analysis instead. |
| `analyze-only` | Yes — OpenAI classifies, no write | **Only** in the "Inschatten zonder internet (Claude + OpenAI)" fallback path. Read-only, no Spotify changes. Never in the default web-lookup flow. | Provides a second training-data opinion to cross-check Claude's offline estimate. Falls back to Claude-only on any OpenAI error. |

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
- **Duplicate guard is always on.** Before writing, the script consults the local `.tracks_log.json`. If the track is already logged for that playlist, the script prints `SKIP: track already in playlist` and exits. There is no override flag.
- **Development Mode WARN.** When the script prints `WARN: Spotify returned no track URIs from playlist_items — the app is in Development Mode...`, surface it verbatim and add a Dutch tip: *"Gebruik `/playlist-log-import` om `.tracks_log.json` te seeden vanuit een Exportify CSV-export, zodat de duplicate-guard weet welke tracks al in je playlists zitten."* The WARN does not mean the add failed — check the line after it for `DONE` or `SKIP`.
- **IPv4 only.** Spotify's IPv6 route is broken on WSL; the script forces IPv4. No skill action needed — just know that the first call may take a moment.
- **Unknown playlist** → `ValueError: Unknown playlist: ...`. The skill should have already validated names against `playlists.json`; if this fires, the file probably changed mid-flow — re-read it. If the playlist the user wants genuinely isn't in the config yet, mention `/playlist-config` to add it.

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

## When the user asks for "the classifier" / "smart-add" / "let AI pick"

The skill **does not** call `smart-add` (OpenAI). Instead, Claude AI is the classifier — and a more thorough one (multiple independent sources vs. one OpenAI call). When the user asks for a classifier-driven flow, do this:

1. Acknowledge briefly in Dutch — e.g. "Ik ben hier zelf de classifier; ik doe een verse analyse met de framing die je wil."
2. Ask via **AskUserQuestion** what framing to use, so the user can steer the re-analysis:
   - **Strenger** — alleen playlists boven een hogere drempel (bv. ≥ 80%).
   - **Breder** — lagere drempel, meer kandidaten (bv. ≥ 50%).
   - **Beperkt tot een categorie** — alleen genre / mood / theme.
   - **Standaard opnieuw** — zelfde sweep, andere bron-weging.
3. Re-run steps 5–6 with that framing, render the playlist match block, and loop step 10's `add` calls over the picks the user selects.

Do **not** invoke `smart-add`. `analyze-only` is used **only** in the "Inschatten zonder internet (Claude + OpenAI)" fallback path of the uncertainty fork — never here in the add flow. The `add` command is the only Python entry point used when adding tracks to playlists.

---

## What about the bulk commands?

`review-playlist`, `bulk-playlist`, and `scan-for` operate on a *source playlist*, not a single song. They're out of scope for this skill — when the user wants to triage a whole playlist, they should run those commands directly per [`docs/commands.md`](../../../../docs/commands.md).
