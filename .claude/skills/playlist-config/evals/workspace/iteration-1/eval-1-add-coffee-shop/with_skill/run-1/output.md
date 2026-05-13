Top, ik ga je nieuwe playlist `Coffee Shop` toevoegen aan `playlists.json` (sub-flow C: extend). Hieronder mijn plan.

**Stap 1 — Spotify ophalen (read-only)**

Eerst haal ik alle schrijfbare playlists op via de Spotify API, zodat we de officiële ID van `Coffee Shop` krijgen (nooit een ID verzinnen — die komt uit `list-playlists --all`):

```bash
.venv/bin/python playlist_manager.py list-playlists --all
```

Ik plak de output verbatim terug zodat je ziet dat de API-call werkte, en ik pak uit het `Untracked`-blok de regel `"Coffee Shop": "<22-char-id>"`.

**Stap 2 — Bevestigen welke key + ID**

Mocht de Spotify-naam licht afwijken (bv. `coffee shop` lowercase of `Coffee Shop ☕`), dan vraag ik via **AskUserQuestion**: "Welke display key wil je in `playlists.json`?"
- `Coffee Shop` (Spotify-naam, default)
- Custom key opgeven
- Annuleren

**Stap 3 — Optionele metadata per pick**

Drie korte **AskUserQuestion**-rondes, allemaal met "skip" als optie:

- Alias? bv. `"coffee"` → `"Coffee Shop"`
  - Ja, alias opgeven
  - Nee, geen alias
- Category bucket?
  - `genre`
  - `mood`
  - `theme`
  - Skip (uncategorised)
- Special rule? (alleen als het een strakke semantische bucket is)
  - Ja, regel opgeven
  - Nee, skip

`catch_all` sla ik over — die is alleen voor sub-flow B (bootstrap).

**Stap 4 — Diff tonen vóór schrijven**

```
Voorgestelde wijziging aan playlists.json:

  + "playlists" -> "Coffee Shop": "<id-uit-stap-1>"
  + "categories" -> "<bucket>" += "Coffee Shop"   (alleen als gekozen)
  + "aliases"    -> "<shorthand>": "Coffee Shop"  (alleen als gekozen)

Bestaande entries blijven ongewijzigd.
```

**Stap 5 — Schrijfbevestiging (enige safety gate)** via **AskUserQuestion**:
- Ja, schrijf naar `playlists.json`
- Pas eerst aan (terug naar pick-stap)
- Annuleren

**Stap 6 — Edit + verifiëren**

Na `Ja` doe ik een additieve **Edit** op `playlists.json` (key-volgorde + indentatie behouden), en daarna:

```bash
.venv/bin/python playlist_manager.py list-playlists
```

om te bevestigen dat `load_config` het bestand accepteert en `Coffee Shop` zichtbaar is. Bij een parse-error bied ik rollback aan.

Ik begin met de `list-playlists --all` call — momentje.
