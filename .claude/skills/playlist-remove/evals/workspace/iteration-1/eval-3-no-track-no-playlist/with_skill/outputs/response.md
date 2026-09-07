# User-facing Response — eval-3-no-track-no-playlist (with_skill)

> This is the response the user would see. AskUserQuestion calls are shown inline as dialogue boxes.

---

## Eerste vraag — welk nummer?

Je wil een nummer verwijderen uit al je playlists, maar ik zie geen Spotify-link, URI of track-ID in je bericht.

**[AskUserQuestion]**
> Welk nummer wil je verwijderen? Plak een Spotify-link, URI of track-ID, of type Artiest – Titel.
>
> [ Other: plak hier je link/URI/ID of "Artiest – Titel" ] [ Annuleren ]

---

## Na antwoord: gebruiker plakt een Spotify-link

*(Voorbeeld: `https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC`)*

Ik heb de link. Je wil dit nummer uit **al je playlists** verwijderen. Ik heb alle 24 playlists uit je configuratie opgehaald. `Random sht` is standaard uitgesloten (dat is de catch-all; als je die ook wilt meenemen, kies dan 'Other').

**[AskUserQuestion — multiSelect]**
> Selecteer de playlists waaruit je het nummer wilt verwijderen:
>
> [x] Rap
> [x] Pop / Mainstream
> [x] Alternative / Indie
> [x] K-pop
> [x] Metal & Rock
> [x] Instrumental Metal
> [x] Jazz / Funk / Soul
> [x] House
> [x] Techno
> [x] Trance
> [x] Drum & Bass
> [x] Dubstep / Bass
> [x] Hardstyle & Hardcore
> [x] Synthwave
> [x] Electronic Music
> [x] Party
> [x] Happy tunes
> [x] Sad tunes
> [x] Angry tunes
> [x] Rustig / 'anders'
> [x] Funny meme
> [x] Ket420
> [x] Hooyah
> [ ] Other (voor Random sht of andere)
> [ ] Annuleren

---

## Na antwoord: gebruiker bevestigt alle 23 playlists

Dit ga ik uitvoeren:

```bash
.venv/bin/python playlist_manager.py remove "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC" "Rap" --execute
.venv/bin/python playlist_manager.py remove "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC" "Pop / Mainstream" --execute
.venv/bin/python playlist_manager.py remove "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC" "Alternative / Indie" --execute
.venv/bin/python playlist_manager.py remove "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC" "K-pop" --execute
.venv/bin/python playlist_manager.py remove "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC" "Metal & Rock" --execute
.venv/bin/python playlist_manager.py remove "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC" "Instrumental Metal" --execute
.venv/bin/python playlist_manager.py remove "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC" "Jazz / Funk / Soul" --execute
.venv/bin/python playlist_manager.py remove "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC" "House" --execute
.venv/bin/python playlist_manager.py remove "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC" "Techno" --execute
.venv/bin/python playlist_manager.py remove "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC" "Trance" --execute
.venv/bin/python playlist_manager.py remove "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC" "Drum & Bass" --execute
.venv/bin/python playlist_manager.py remove "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC" "Dubstep / Bass" --execute
.venv/bin/python playlist_manager.py remove "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC" "Hardstyle & Hardcore" --execute
.venv/bin/python playlist_manager.py remove "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC" "Synthwave" --execute
.venv/bin/python playlist_manager.py remove "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC" "Electronic Music" --execute
.venv/bin/python playlist_manager.py remove "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC" "Party" --execute
.venv/bin/python playlist_manager.py remove "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC" "Happy tunes" --execute
.venv/bin/python playlist_manager.py remove "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC" "Sad tunes" --execute
.venv/bin/python playlist_manager.py remove "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC" "Angry tunes" --execute
.venv/bin/python playlist_manager.py remove "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC" "Rustig / 'anders'" --execute
.venv/bin/python playlist_manager.py remove "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC" "Funny meme" --execute
.venv/bin/python playlist_manager.py remove "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC" "Ket420" --execute
.venv/bin/python playlist_manager.py remove "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC" "Hooyah" --execute
```

**[AskUserQuestion]**
> Klaar om dit nummer te verwijderen uit 23 playlists?
>
> [ Ja, verwijder ] [ Nee, annuleren ]

---

## Na bevestiging: uitvoer per playlist (voorbeeld)

*(Script output wordt verbatim getoond voor elke playlist, e.g.:)*

```
DONE: track removed (snapshot abc123...)
SKIP: track not found in playlist. No changes made.
...
```

*(Als er SKIPs zijn: "Dit nummer stond niet in [playlist]. Het is mogelijk via de Spotify-app toegevoegd buiten dit tool om — het staat dan niet in `.tracks_log.json`. Gebruik `log-import` om de log bij te vullen vanuit een Exportify CSV.")*

---

## Samenvatting

Klaar! 5 verwijderd, 18 overgeslagen (niet in playlist).

**[AskUserQuestion]**
> Wil je nog iets doen?
>
> [ Voeg toe aan andere playlist ] [ Klaar ]
