Top, ik heb genoeg context. Hier is mijn plan voor "Coffee Shop" toevoegen aan `playlists.json`.

**Plan**

1. Spotify ID van je nieuwe "Coffee Shop" playlist ophalen via `list-playlists --all`. Dat commando print alle writable playlists in paste-ready JSON, gesplitst in tracked / untracked.
2. Het regeltje `"Coffee Shop": "<id>"` uit de untracked-sectie pakken en in `playlists.json` plakken onder `"playlists"`.
3. Omdat je `playlists.json` ook `"categories"` (genre / mood / theme) en eventueel `"aliases"` heeft, "Coffee Shop" daar ook netjes inhangen — anders ziet `smart-add` 'm wel als target maar weet de classifier niet in welke bucket 'ie hoort.
4. Verifiëren met `list-playlists` (zonder `--all`) — Coffee Shop hoort dan in de lijst te staan.

**Commands die ik wil draaien**

```bash
# stap 1 — Spotify ID ophalen
python playlist_manager.py list-playlists --all
```

```bash
# stap 4 — verifiëren na de edit
python playlist_manager.py list-playlists
```

De edit op `playlists.json` doe ik zelf met het Edit-tool zodra ik de ID heb — ongeveer zo:

```json
"playlists": {
  ...
  "Random sht": "1PMqc20PYGO1nqOeqY0zRe",
  "Coffee Shop": "<id-uit-stap-1>"
}
```

**Wat ik ga aannemen (zeg het als het anders moet)**

Je zei expliciet "geen verhelderingsvragen", dus ik maak deze keuzes:

- **Categorie**: "Coffee Shop" klinkt als sfeer/mood (chill, lo-fi, jazzy achtergrond). Ik zet 'm bij `"categories" -> "mood"`, naast `Rustig / 'anders'` en `Happy tunes`. Niet bij `genre`, want het is geen muzikaal genre.
- **Alias**: ik voeg `"coffee": "Coffee Shop"` toe onder `"aliases"` zodat je 'm met shorthand kan aanspreken (bv. `add ... coffee`). Geen `"shop"` alias — te dubbelzinnig.
- **`special_rules` / `catch_all`**: laat ik onaangeroerd. Coffee Shop is geen exclusieve niche zoals `Ket420` / `Hooyah`, en de catch-all blijft `Random sht`.

Als je 'm liever onder `theme` wil, of zonder alias, of met een andere alias (`koffie`, `lofi`, etc.) — zeg het, dan pas ik 'm aan voor ik save.
