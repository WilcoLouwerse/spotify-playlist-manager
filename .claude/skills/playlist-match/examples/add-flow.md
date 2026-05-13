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

User selects `Alternative / Indie` and `Pop / Mainstream`.

---

## Step 3 — show the plan (via `templates/add-confirmation.md`)

Commands are always rendered with `--execute` — the dry-run/execute question is gone; the next step's confirmation is the safety gate.

```
Je wilt Tame Impala - The Less I Know The Better toevoegen aan 2 playlist(s):

- Alternative / Indie — 88%
- Pop / Mainstream — 74%

Ik ga deze commando's draaien vanuit de repo-root:

.venv/bin/python playlist_manager.py add "https://open.spotify.com/track/6K4t31amVTZDgR3sKmwUJJ" "Alternative / Indie" --execute
.venv/bin/python playlist_manager.py add "https://open.spotify.com/track/6K4t31amVTZDgR3sKmwUJJ" "Pop / Mainstream" --execute
```

---

## Step 4 — mandatory confirmation

**AskUserQuestion**:

> "Klaar om deze commando's uit te voeren?"
> - **Ja, voer uit**
> - **Nee, annuleren**

This step is **never skipped**. The skill only invokes Bash after the user picks **Ja, voer uit**.

User picks **Ja, voer uit**.

---

## Step 5 — run, print verbatim

The skill runs each command via Bash. The script output, verbatim:

```
Tame Impala - The Less I Know The Better -> Alternative / Indie: ADDED
Tame Impala - The Less I Know The Better -> Pop / Mainstream: SKIP: track already in playlist
```

---

## Step 6 — summarise + re-offer the follow-up menu

```
Klaar! 1 toegevoegd, 1 overgeslagen (al in playlist).
```

Then call **AskUserQuestion** again (per `templates/followup.md`) so the user can chain another action or pick "Klaar".

---

## Variant — user picks "Nee, annuleren"

The skill prints:

```
Oké, niets gewijzigd.
```

…and immediately calls **AskUserQuestion** again with the follow-up menu so the user can pick another action or "Klaar". No python script runs.

---

## Variant — user pasted a Spotify URL originally

If the user's original message was `https://open.spotify.com/track/6K4t31amVTZDgR3sKmwUJJ`, the skill **skips step 1** and goes straight to step 2 (playlist selection). The URL is already known.

---

## Variant — natural-language add follow-up

User says "voeg toe aan House en Techno" instead of clicking the **Voeg toe aan playlists** button. The skill:
1. Treats this as the add action with `House` and `Techno` pre-selected.
2. Validates that both playlists were in the step-6 recommendations — if not, asks for confirmation via **AskUserQuestion** before adding to a playlist that wasn't on the recommended list.
3. Skips to step 3 (render the plan) and then the mandatory confirmation in step 4.
