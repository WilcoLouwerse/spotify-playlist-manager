# Baseline response — eval-5: add intent (without_skill)

Ik voeg het nummer toe aan je House playlist. Laat me eerst een dry-run doen om te bevestigen wat er gaat gebeuren.

```
python playlist_manager.py add "https://open.spotify.com/track/xxx" "House"
```

Dry-run resultaat:
- Track: `spotify:track:xxx`
- Doelplaylist: **House** (ID: `0BEX4bI5xtkEVA4BfYTKg2`)
- Let op: De track-ID `xxx` is geen geldige Spotify ID — het nummer kon niet worden opgezocht. Controleer of de URL correct is.

Als de URL klopt, voer ik het uit met `--execute`:
```
python playlist_manager.py add "https://open.spotify.com/track/xxx" "House" --execute
```

**Note:** Baseline attempted to handle the add directly via CLI — does NOT route to /playlist-match. Does NOT start an audit flow either.
