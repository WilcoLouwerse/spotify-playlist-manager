Je wilt House-kandidaten zoeken in 'Random sht' (dry-run).

Doel resolved tegen `playlists.json`: **House** (`0BEX4bI5xtkEVA4BfYTKg2`) — directe key-match.
Bron: `Random sht` — bare naam, resolvet tegen de playlist met diezelfde naam in `playlists.json` (`1PMqc20PYGO1nqOeqY0zRe`). Geen CSV nodig; als de API stripped data teruggeeft handelt het script zelf de CSV-fallback af.

Ik ga dit commando draaien vanuit de repo-root:

```bash
.venv/bin/python playlist_manager.py scan-for "House" "Random sht"
```

Dit is een dry-run — geen y/N prompt, niets wordt geschreven. Default `--min-confidence 80`; de classifier geeft per track z'n top-5 terug en alleen tracks waarvan House daarin zit komen op de lijst.

Na de dry-run laat ik de kandidatenlijst verbatim zien en geef ik een 1-regelige samenvatting. Als je daarna écht wilt toevoegen, draaien we 'm opnieuw met `--execute` (één y/N) — vanuit jouw terminal of hier met automatische 'y'.
