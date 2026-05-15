# User-facing Response — Playlist Audit: House

*This is the response the skill would show to the user, in Dutch.*

---

## Stap 1–2: Playlist herkend

House gevonden in `playlists.json` — genre-playlist. Ik ga alle nummers controleren op house-kenmerken.

---

## Stap 3: Nummers ophalen

```
.venv/bin/python playlist_manager.py list-tracks "House"
```

> De Spotify API geeft geen nummers terug voor de House playlist — dit gebeurt in Development Mode.
> Heb je een exportify CSV export van House?
>
> - **Ja, ik heb een CSV** — geef het pad, dan gebruik ik dat
> - **Nee** — exporteer via https://exportify.net en geef het CSV-pad terug

*(Voor deze demo ga ik verder met een gesimuleerde lijst van 12 nummers.)*

---

## Stap 4: Auditmodus kiezen

> **Welke auditmodus wil je gebruiken?**
> House heeft 12 nummers.
>
> - **Web-first (Claude + web, nauwkeuriger)** ← aanbevolen voor ≤20 nummers
> - **Quick (OpenAI CLI, sneller)**

*(Gesimuleerde keuze: Web-first)*

---

## Stap 5: Nummers controleren...

```
[1/12]  Martin Garrix - Animals
[2/12]  Disclosure - Latch
[3/12]  Duke Dumont - I Got U
[4/12]  Dua Lipa - Levitating
[5/12]  Calvin Harris - Summer
[6/12]  The Weeknd - Blinding Lights
[7/12]  Fisher - Losing It
[8/12]  Chris Lake - High As Hope
[9/12]  Gorgon City - Ready For Your Love
[10/12] Peggy Gou - (It Goes Like) Nanana
[11/12] Daft Punk - One More Time
[12/12] Fred again.. - Marea (We've Lost Dancing)
```

---

## Stap 6: Auditrapport

**House — 12 nummers geauditeerd**

✅ 9  nummers  ≥80% match (past goed)
⚠️ 1  nummer   60–79% match (twijfelachtig)
❌ 2  nummers  <60% match (past slecht)

**Nummers met lage match (kandidaten voor verwijdering):**
— 18% — The Weeknd - Blinding Lights
       Reden: synth-pop en dark R&B; stijl sluit nauw aan bij 80s new wave, geen house-elementen (AllMusic: "synth-pop", Wikipedia: "synth-pop, new wave revival")
       URI: spotify:track:aaa006

— 42% — Dua Lipa - Levitating
       Reden: disco-pop / dance-pop; mainstream pop met nu-disco-invloeden, geen house-kenmerken (AllMusic: "dance-pop, disco-pop", Wikipedia: "pop, dance-pop")
       URI: spotify:track:aaa004

**Twijfelachtige nummers (⚠️):**
— 78% — Fred again.. - Marea (We've Lost Dancing)
       Reden: house / UK garage crossover; sterke dance-component maar niet puur house (Discogs: "house, UK garage")
       URI: spotify:track:aaa012

---

## Stap 7: Verwijderdrempel kiezen

> **Welke drempel wil je gebruiken voor verwijdering?**
>
> - **Verwijder alles onder 60% (standaard)** → verwijdert 2 nummers (The Weeknd 18%, Dua Lipa 42%)
> - **Verwijder alles onder 70%** → verwijdert 2 nummers (zelfde als boven)
> - **Verwijder alles onder 80%** → verwijdert 3 nummers (ook Fred again.. 78%)
> - **Niks verwijderen** — alleen het overzicht bekijken

---

## Stap 8: Bevestig te verwijderen nummers (gesimuleerd: onder 60%)

> **Welke van deze nummers wil je verwijderen uit House?**
> *(meerdere keuzes mogelijk)*
>
> - The Weeknd - Blinding Lights (18%)
> - Dua Lipa - Levitating (42%)

---

## Stap 9: Geplande commando's en definitieve bevestiging

```bash
.venv/bin/python playlist_manager.py remove "spotify:track:aaa006" "House" --execute
.venv/bin/python playlist_manager.py remove "spotify:track:aaa004" "House" --execute
```

> **Klaar om deze 2 nummers te verwijderen uit House?**
>
> - **Ja, verwijder**
> - **Nee, annuleren**

---

## Stap 10–11: Resultaat (gesimuleerd)

*(Commando's niet uitgevoerd in deze eval.)*

> Audit klaar! 2 verwijderd, 0 overgeslagen, 0 bewaard door jou. House heeft nu 10 nummers.
