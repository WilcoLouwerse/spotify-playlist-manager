Leuk, een obscure track! Voordat ik iets doe wil ik even zeker weten dat we het over hetzelfde nummer hebben en wat je ermee wilt.

## Wat ik (niet) weet

"Spook & Mr Vague - aufdemwegnach" ken ik niet uit mijn trainingsdata. Dat zegt op zich niks — het kan prima een echte release zijn (klinkt als iets uit een Duitse/Nederlandse electronic/lo-fi hoek, gezien `aufdemwegnach` = "auf dem Weg nach" = "onderweg naar"). Ik ga het dus niet verzinnen.

## Wat ik nodig heb om iets nuttigs te doen

Heb je een Spotify-link voor de track? Iets in de vorm van:

```
https://open.spotify.com/track/<id>
```

Met die URI kan ik via dit project een paar dingen doen:

1. **`smart-add`** — laat de OpenAI-classifier een suggestie doen voor welke van jouw playlists in `playlists.json` passen, jij bevestigt:
   ```bash
   python playlist_manager.py smart-add "https://open.spotify.com/track/<id>" --execute
   ```
2. **`add`** — als je zelf al weet in welke playlist 'ie moet (bijv. een "Obscure", "Electronic" of "Lo-fi" lijst die je hebt geconfigureerd):
   ```bash
   python playlist_manager.py add "https://open.spotify.com/track/<id>" "PlaylistNaam" --execute
   ```
3. **Eerst dry-run** — laat `--execute` weg om te zien wat er zou gebeuren zonder echt te schrijven.

## Als je geen link hebt

Spotify zelf is de beste plek om te zoeken — als de track daar niet staat kan deze CLI er ook niks mee (we werken via de Spotify Web API). Mocht 'ie er wel staan maar moeilijk te vinden: probeer de exacte string `Spook Mr Vague aufdemwegnach` in de Spotify-zoekbalk, of zoek op artiest en filter op nummer.

Plak de Spotify-track-URL hier en ik help je 'm op de juiste plek krijgen.
