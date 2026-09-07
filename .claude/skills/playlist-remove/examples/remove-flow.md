# Example — Remove Flow

A worked example for `/playlist-remove`. Illustrates a direct remove request with a Spotify URL.

---

**User input:**
> "Verwijder https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC uit House"

**Step 1** — Input detected: track URL + playlist "House". Both present, proceed.

**Step 2** — Track URL given: `https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC`. Use verbatim.

**Step 3** — Resolve "House" in `playlists.json` → canonical name `House`, ID `0BEX4bI5xtkEVA4BfYTKg2`. Valid.

**Step 4** — No uncertainty expressed; skip web genre check.

**Step 5** — Show planned command:

```
Ik ga dit nummer verwijderen uit House:

.venv/bin/python playlist_manager.py remove "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC" "House" --execute
```

**Step 6** — AskUserQuestion: "Klaar om dit nummer te verwijderen?"
- Ja, verwijder → proceed
- Nee, annuleren → end

User picks **Ja, verwijder**.

**Step 7** — Bash output:
```
Track: Nelly Furtado - Say It Right
Target playlist: House
Playlist ID: 0BEX4bI5xtkEVA4BfYTKg2

DONE: track removed (snapshot 3oqAUMV…)
```

**Step 8** — Summary:
> "Klaar! 1 verwijderd, 0 overgeslagen."

AskUserQuestion: "Wil je nog iets anders doen?"
- Voeg toe aan andere playlist → handoff to `/playlist-match`
- Klaar → end

---

## Example — Track not in playlist (SKIP)

**User input:**
> "Verwijder spotify:track:4uLU6hMCjMI75M1A2tKUQC uit Techno"

**Step 7** — Bash output:
```
Track: Nelly Furtado - Say It Right
Target playlist: Techno
Playlist ID: 7lRL294p8uvOOXTxNPIBhn

SKIP: track not found in playlist. No changes made.
```

The skill surfaces this verbatim and explains in Dutch:
> "Het nummer staat niet in de lokale log voor Techno. Dit kan betekenen dat het via de Spotify-app is toegevoegd (niet via dit script). In Development Mode kan de Spotify API ook geen bevestiging geven. Gebruik `/playlist-log-import` om de log te seeden vanuit een Exportify CSV als je dat wil corrigeren."

---

## Example — Only "Artist - Title" given (needs URL)

**User input:**
> "Verwijder Dua Lipa - Levitating uit House"

**Step 2** — No Spotify URL given. AskUserQuestion:
> "Om het nummer te verwijderen heb ik een Spotify-link, URI of track-ID nodig. Plak die via 'Other', of kies 'Annuleren'."

User pastes: `https://open.spotify.com/track/463CkQjx2Zk1yXoBuierM9`

Continue from step 3 as normal.
