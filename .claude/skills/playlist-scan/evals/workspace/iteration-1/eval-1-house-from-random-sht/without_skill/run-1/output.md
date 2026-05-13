Goeie vraag. Ik kan dat zelf niet direct beantwoorden — ik heb in deze sessie geen live verbinding met je Spotify-account, dus ik kan de tracks in `Random sht` niet ophalen en classificeren. Maar deze repo heeft daar precies een command voor: `scan-for`.

## Wat `scan-for` doet

`scan-for` neemt één doel-playlist (in dit geval `House`), loopt door alle tracks van een bronlijst (in dit geval `Random sht`), classificeert elke track via de OpenAI-pipeline, en print de tracks die binnen je `--min-confidence` als House gescoord worden. Daarna één `y/N` om alles toe te voegen.

Bron: [docs/commands.md → scan-for](../../docs/commands.md#scan-for).

## Command om te draaien

Uit `playlists.json` zie ik dat `Random sht` ID `1PMqc20PYGO1nqOeqY0zRe` heeft en `House` ID `0BEX4bI5xtkEVA4BfYTKg2`. Je kunt de bron op drie manieren opgeven (URL, CSV-pad, of bare naam die in `exportify-exports/` staat).

Dry-run eerst (geen schrijfacties, alleen kandidaten zien):

```bash
python playlist_manager.py scan-for "House" "https://open.spotify.com/playlist/1PMqc20PYGO1nqOeqY0zRe"
```

Of korter, via de bare naam (als er een `exportify-exports/Random_sht.csv` bestaat — dat is ook de aangeraden fallback als Spotify in Developer Mode de items stript):

```bash
python playlist_manager.py scan-for "House" "Random sht"
```

Wil je strenger zijn dan de default van 80% confidence:

```bash
python playlist_manager.py scan-for "House" "https://open.spotify.com/playlist/1PMqc20PYGO1nqOeqY0zRe" --min-confidence 85
```

Echt toevoegen na de y/N: zet `--execute` erachter.

```bash
python playlist_manager.py scan-for "House" "https://open.spotify.com/playlist/1PMqc20PYGO1nqOeqY0zRe" --execute
```

## Wat je terug krijgt

Een gesorteerde lijst (hoogste confidence eerst) met per track een korte motivatie van de classifier, bv:

```
23 candidate(s) for House:
- 92% — Bakermat - Walk That Walk
    uplifting deep-house with vocals
- 88% — Honey Dijon - Show Me Some Love
    classic house groove with vocal stabs
...

Add all 23 to 'House'? [y/N]:
```

Run de dry-run gerust en plak de output hier terug — dan kan ik meekijken naar de grensgevallen (de 80–85% range) of helpen beslissen of er nog tracks tussen zitten die je liever in `Electronic Music`, `Techno` of `Party` zou willen.
