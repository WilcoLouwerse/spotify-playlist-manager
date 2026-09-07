Je wilt de log voor **House** seeden met `exportify-exports/House.csv`.

Dit is een lokale operatie — er wordt niets naar Spotify geschreven. Alleen `.tracks_log.json` wordt bijgewerkt. Na deze import weet de duplicate-guard van `add`, `smart-add`, `review-playlist`, `bulk-playlist` en `scan-for` dat die tracks al in House zitten.

Ik ga dit commando draaien vanuit de repo-root:

```bash
.venv/bin/python playlist_manager.py log-import "House" "exportify-exports/House.csv"
```

Geen vlaggen — `log-import` accepteert alleen `<playlist>` en `<file>`, en is altijd lokaal (geen `--execute`/`--dry-run`).

**Bevestig je dit?**

- **Ja, importeer** — ik draai het commando en print de vijf tellers (Imported / Already in log / Duplicate in file / Unparseable lines / Total) verbatim.
- **Nee, andere target/file** — bijv. een ander pad (`exportify-exports/house.csv`?) of een andere playlist.
- **Annuleren** — dan doe ik niks en blijft `.tracks_log.json` ongewijzigd.
