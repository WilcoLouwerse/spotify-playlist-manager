# Example — add flow

Following the analysis in `examples/full-analysis.md` (Tame Impala - The Less I Know The Better), the skill has called the follow-up `AskUserQuestion`. The user picks:

> **Voeg toe aan playlists**

The user originally pasted only `Tame Impala - The Less I Know The Better` — no Spotify URL. Walk through the full flow.

---

## Step 1 — ask for the Spotify URL (no URL yet)

The skill calls **AskUserQuestion** (the user will paste the URL via the "Other" free-text field):

> "Voor 'Voeg toe aan playlists' heb ik een Spotify-link, URI of track-ID nodig. Plak die via 'Other', of kies 'Annuleren'."
> - **Annuleren** — sluit de add-flow af zonder iets te doen.

User pastes `https://open.spotify.com/track/6K4t31amVTZDgR3sKmwUJJ`.

---

## Step 2 — pick playlists (only from the recommended list)

The skill recommended `Alternative / Indie`, `Pop / Mainstream`, `Happy tunes`, `Ket420`. **AskUserQuestion** with `multiSelect: true`:

> "Naar welke playlist(s) moet ik dit nummer toevoegen?"
> - **Alternative / Indie — 88%**
> - **Pop / Mainstream — 74%**
> - **Happy tunes — 62%**
> - **Ket420 — 58%**

User selects `Alternative / Indie` and `Pop / Mainstream`. **This multi-select is the
confirmation gate** — the selection authorizes the write.

---

## Step 3 — show the plan (via `templates/add-confirmation.md`)

Commands are always rendered with `--execute` — the dry-run/execute question is gone; the playlist multi-select in step 2 is the safety gate.

```
Je wilt Tame Impala - The Less I Know The Better toevoegen aan 2 playlist(s):

- Alternative / Indie — 88%
- Pop / Mainstream — 74%

Ik draai deze commando's vanuit de repo-root:

.venv/bin/python playlist_manager.py add "https://open.spotify.com/track/6K4t31amVTZDgR3sKmwUJJ" "Alternative / Indie" --execute
.venv/bin/python playlist_manager.py add "https://open.spotify.com/track/6K4t31amVTZDgR3sKmwUJJ" "Pop / Mainstream" --execute
.venv/bin/python playlist_manager.py like "https://open.spotify.com/track/6K4t31amVTZDgR3sKmwUJJ" --execute
```

The `like` line is always appended — no extra question — so the track also lands in Liked Songs.

---

## Step 4 — run, print verbatim

Immediately after rendering the plan — no extra confirmation prompt — the skill runs each
command via Bash. The script output, verbatim:

```
Track: Tame Impala - The Less I Know The Better
Target playlist: Alternative / Indie
Playlist ID: <playlist-id>

DONE: track added (snapshot 5vQ8bX2kLm…)
Track: Tame Impala - The Less I Know The Better
Target playlist: Pop / Mainstream
Playlist ID: <playlist-id>

SKIP: track already in playlist. No changes made.
Track: Tame Impala - The Less I Know The Better
Target: Liked Songs

DONE: track added to Liked Songs
```

---

## Step 5 — summarise + re-offer the follow-up menu

```
Klaar! 1 toegevoegd, 1 overgeslagen (al in playlist). Liked Songs: toegevoegd.
```

Then call **AskUserQuestion** again (per `templates/followup.md`) so the user can chain another action or pick "Klaar".

---

## Variant — user selected zero playlists

If the step-2 multi-select comes back empty, the skill skips the plan render and the Bash
calls, and prints:

```
Oké, niets gewijzigd.
```

…and immediately calls **AskUserQuestion** again with the follow-up menu so the user can pick another action or "Klaar". No plan is rendered and no python script runs.

---

## Variant — user pasted a Spotify URL originally

If the user's original message was `https://open.spotify.com/track/6K4t31amVTZDgR3sKmwUJJ`, the skill **skips step 1** and goes straight to step 2 (playlist selection). The URL is already known.

---

## Variant — natural-language add follow-up

User says "voeg toe aan House en Techno" instead of clicking the **Voeg toe aan playlists** button. The skill:
1. Treats this as the add action with `House` and `Techno` pre-selected.
2. Validates that both playlists were in the recommendations from `SKILL.md` step 6 (*Match playlists*) — if not, asks for confirmation via **AskUserQuestion** before adding to a playlist that wasn't on the recommended list.
3. Skips to step 3 (render the plan) and then runs the commands in step 4.
