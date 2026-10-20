# Adding the song via `playlist_manager.py`

When the user picks **Voeg toe aan playlists** in the follow-up `AskUserQuestion` (or asks naturally — "voeg toe aan House"), the skill invokes the project's existing CLI. **Read [`docs/commands.md`](../../../../docs/commands.md) for the authoritative reference.** This page is a fast index of what to call, with what flags, and why.

---

## Which commands — `add`, then `like`

This skill uses **`add`** for playlists (one track, one playlist, no Python-side classifier). Claude AI is the classifier — steps 5–6 of `SKILL.md` produce a multi-source classification, and step 10 loops `add` once per playlist the user picked. After the loop it always runs **`like`** once, so the track also lands in the user's Liked Songs.

The project's `smart-add` and `analyze-only` commands call OpenAI to pick playlists. **This skill never invokes them.** If the user asks for "the classifier", "AI-picked playlists", or "use smart-add", re-do Claude AI's classification with whatever framing they want (stricter confidence band, different scope, etc.) and then loop `add` over the picks — never shell out to OpenAI.

| Command | Picks playlists? | This skill | Why |
|---------|------------------|------------|-----|
| `add` | No — you pass the playlist name | **Yes.** Loop once per playlist the user chose. | Claude AI already classified; `add` just executes the write. |
| `like` | No — always Liked Songs | **Yes — always, once,** after the `add` loop, whenever at least one playlist was selected. | Standing user preference: every track that goes into a playlist is also liked. |
| `smart-add` | Yes — OpenAI picks | **Never.** | Claude AI replaces the OpenAI classifier; re-do the analysis instead. |
| `analyze-only` | Yes — OpenAI classifies, no write | **Only** in the "Inschatten zonder internet (Claude + OpenAI)" fallback path. Read-only, no Spotify changes. Never in the default web-lookup flow. | Provides a second training-data opinion to cross-check Claude's offline estimate. Falls back to Claude-only on any OpenAI error. |

---

## `add` — exact invocation

From the repo root, with the venv. The skill always runs with `--execute`. The confirmation gate is the multi-select in step 10.b — the user's playlist choice authorizes the write, so no extra "Klaar om deze commando's uit te voeren?" prompt is needed afterwards:

```bash
.venv/bin/python playlist_manager.py add "<track>" "<Playlist Name>" --execute
```

Dry-run (omitting `--execute`) still exists in the CLI, but the skill no longer uses it — the playlist multi-select is the safety gate.

Argument rules:

- `<track>` — Spotify track URL (`https://open.spotify.com/track/<id>`), URI (`spotify:track:<id>`), or bare 22-char ID. If the user gave you any of these in their original message, use it verbatim. Don't invent or guess one.
- `<Playlist Name>` — must match a key under `"playlists"` in [`playlists.json`](../../../../playlists.json) or an entry under `"aliases"`. Case-insensitive. **Quote** the name so spaces, slashes, and apostrophes don't break the shell.

Special playlist-name characters to handle:
- `Jazz / Funk / Soul` → `"Jazz / Funk / Soul"`
- `Rustig / 'anders'` → `"Rustig / 'anders'"` (single quotes inside double quotes are fine)
- `Pop / Mainstream` → `"Pop / Mainstream"`

---

## `like` — exact invocation

Once per add flow, after the last `add`, same `<track>` value, always with `--execute`:

```bash
.venv/bin/python playlist_manager.py like "<track>" --execute
```

- **No extra gate.** Liking is a standing preference of the user, so the step 10.b multi-select covers it. It is never offered as a checkbox and Liked Songs never appears in the playlist match — it is the Spotify library, not a playlist in `playlists.json`.
- **Not when nothing was selected.** An empty multi-select means no writes at all, `like` included.
- **Duplicate guard** asks Spotify directly (`.tracks_log.json` is not involved): `SKIP: track already in Liked Songs. No changes made.` is normal and not a failure.
- **`FAILED: Spotify returned 403`** almost always means the cached token was granted before the `user-library-modify` scope existed in this project. Tell the user in Dutch: *"Je Spotify-token mist nog de rechten voor Liked Songs. Verwijder `.spotify_token_cache` en draai het commando opnieuw; Spotify vraagt dan eenmalig opnieuw toestemming."* The playlist adds that already ran are unaffected.

---

## Behaviour the user will see

From [`docs/commands.md`](../../../../docs/commands.md):

- **Dry-run by default in the CLI.** Without `--execute`, the script prints the planned action and exits without writing. The skill always passes `--execute` because the user has already authorized the write by picking the playlist(s) in step 10.b's `AskUserQuestion` multi-select.
- **Duplicate guard is always on.** Before writing, the script reads the playlist's current contents from Spotify (falling back to the local `.tracks_log.json` only when Spotify hides them). If the track is already there, it prints `SKIP: track already in playlist` and exits. There is no override flag.
- **Hidden-contents WARN.** When the script prints `WARN: Spotify returned playlist entries without track URIs...`, surface it verbatim and add a Dutch tip: *"Spotify laat de inhoud van deze playlist nu niet zien, dus de duplicate-guard valt terug op `.tracks_log.json`. Gebruik `/playlist-log-import` om dat log aan te vullen vanuit een Exportify CSV-export."* The WARN does not mean the add failed — check the line after it for `DONE` or `SKIP`.
- **IPv4 only.** Spotify's IPv6 route is broken on WSL; the script forces IPv4. No skill action needed — just know that the first call may take a moment.
- **Unknown playlist** → `ValueError: Unknown playlist: ...`. The skill should have already validated names against `playlists.json`; if this fires, the file probably changed mid-flow — re-read it. If the playlist the user wants genuinely isn't in the config yet, mention `/playlist-config` to add it.

---

## The add flow, step by step

1. **Do we have a Spotify URL/URI/ID for this song?**
   - Yes → use it.
   - No → **AskUserQuestion**:

     > "Voor 'Voeg toe aan playlists' heb ik een Spotify-link, URI of track-ID nodig. Plak die via 'Other', of kies 'Annuleren'."

     If the user pastes a URL, continue. If they cancel, end the add flow gracefully and offer the follow-up menu again.

2. **Which playlists?** **AskUserQuestion** with `multiSelect: true`, listing **only the playlists you recommended in step 6**. Optionally add an "All recommended" shortcut. Honor the user's selection literally — never silently add a playlist they didn't pick. **This selection is the confirmation gate** for the write; do not add a second `AskUserQuestion` afterwards.

3. **Render the plan** using `templates/add-confirmation.md`. One `add --execute` command per playlist, on its own line, followed by one `like --execute` line, in a code block.

4. **Run** each command via Bash, sequentially — immediately after rendering the plan, no extra confirmation prompt. Print the script's output verbatim. Order: the `add` commands in the order the user selected the playlists, then `like`.

5. **Summarise** with one Dutch sentence at the end, plus the Liked Songs result:

   > "Klaar! N toegevoegd, M overgeslagen (al in playlist). Liked Songs: toegevoegd / stond er al / mislukt."

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

Do **not** invoke `smart-add`. `analyze-only` is used **only** in the "Inschatten zonder internet (Claude + OpenAI)" fallback path of the uncertainty fork — never here in the add flow. `add` (playlists) and `like` (Liked Songs) are the only Python entry points used in the add flow.

---

## What about the bulk commands?

`review-playlist`, `bulk-playlist`, and `scan-for` operate on a *source playlist*, not a single song. They're out of scope for this skill — route the user to `/playlist-triage` (`review-playlist` / `bulk-playlist`) or `/playlist-scan` (`scan-for`).
