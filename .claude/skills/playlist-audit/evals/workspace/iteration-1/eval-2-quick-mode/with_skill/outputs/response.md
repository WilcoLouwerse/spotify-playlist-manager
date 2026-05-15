Oké, ik ga de **House** playlist auditen in de snelle modus (OpenAI CLI).

Eerst haal ik de tracklist op:

```bash
.venv/bin/python playlist_manager.py list-tracks "House"
```

Zodra ik de tracks heb, voer ik de audit uit met het volgende commando:

```bash
.venv/bin/python playlist_manager.py audit-playlist "House"
```

Dit stuurt alle tracks in één batch naar OpenAI voor genre-classificatie. De CLI gebruikt standaard `--min-confidence 60`.

---

**(Commando wordt niet uitgevoerd — OpenAI API niet beschikbaar in deze omgeving.)**

Als het commando zou draaien, zou de output er ongeveer zo uitzien:

**House — 42 nummers geauditeerd**

✅ 35 nummers  ≥80% match (past goed)
⚠️  5 nummers  60–79% match (twijfelachtig)
❌  2 nummers  <60% match (past slecht)

**Nummers met lage match (kandidaten voor verwijdering):**
— 42% — Dua Lipa - Levitating
       Reden: disco-pop met lichte house-elementen; voornamelijk mainstream pop
       URI: spotify:track:voorbeeld1
— 38% — The Weeknd - Blinding Lights
       Reden: synth-pop / dark R&B; geen house-kenmerken
       URI: spotify:track:voorbeeld2

---

Na het rapport zou ik vragen welke drempel je wilt gebruiken voor verwijdering:

**Welke drempel wil je gebruiken voor verwijdering?**
- Verwijder alles onder 60% (standaard)
- Verwijder alles onder 70%
- Verwijder alles onder 80%
- Niks verwijderen — alleen het overzicht bekijken
