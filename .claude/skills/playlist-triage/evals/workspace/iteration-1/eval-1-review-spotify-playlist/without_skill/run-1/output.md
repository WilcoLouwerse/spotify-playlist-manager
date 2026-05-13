Zeker! Deze repo heeft daar twee commands voor — afhankelijk van hoe je wilt reviewen:

## Optie 1: per-track review (`review-playlist`)

Voor elke track in de playlist krijg je een y/N prompt om hem toe te voegen aan een doel-playlist:

```bash
python playlist_manager.py review-playlist "https://open.spotify.com/playlist/3aBcDeFgHiJkLmNoPqRsTu"
```

Voeg `--execute` toe als je de adds daadwerkelijk wilt schrijven (zonder die flag is het dry-run):

```bash
python playlist_manager.py review-playlist "https://open.spotify.com/playlist/3aBcDeFgHiJkLmNoPqRsTu" --execute
```

## Optie 2: bulk review (`bulk-playlist`)

Eén keer y/N voor de hele playlist tegelijk — handig als je al weet dat het allemaal naar dezelfde target moet:

```bash
python playlist_manager.py bulk-playlist "https://open.spotify.com/playlist/3aBcDeFgHiJkLmNoPqRsTu" --execute
```

## Of: scannen voor een specifiek genre

Als je alleen wilt zien welke tracks uit deze playlist in bv. je House-playlist passen:

```bash
python playlist_manager.py scan-for "House" "https://open.spotify.com/playlist/3aBcDeFgHiJkLmNoPqRsTu" --execute
```

---

Wil je dat ik er één voor je uitvoer? Zeg dan even welke (review per-track, bulk, of scan-for + genre), dan draai ik 'm. De duplicate-guard staat altijd aan, dus tracks die je eerder al hebt toegevoegd worden automatisch overgeslagen.
