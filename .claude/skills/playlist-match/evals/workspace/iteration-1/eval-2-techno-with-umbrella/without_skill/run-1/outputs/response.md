"Doppler" by Charlotte de Witte is a hard, driving peak-time techno track — pure Belgian techno, no vocals, relentless kick. Classic CdW.

Suggested playlists from your `playlists.json`:

- **Techno** — obvious fit, this is textbook modern techno.
- **Electronic Music** — per your `special_rules`, the umbrella goes alongside the subgenre, not instead of it.

Optional, depending on mood:
- **Party** — it's a club-floor weapon, works if you tag energetic tracks here.
- **Angry tunes** — it's aggressive/intense; skip if that playlist is more about lyrical anger than sonic intensity.

If you want me to actually add it, drop the Spotify track URL and I'll run:

```bash
python playlist_manager.py smart-add "<track-url>" --execute --accept-all
```

Or to target specifically:

```bash
python playlist_manager.py add "<track-url>" "Techno" --execute
python playlist_manager.py add "<track-url>" "Electronic Music" --execute
```
