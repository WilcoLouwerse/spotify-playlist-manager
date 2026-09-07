# Example — follow-up responses

Following the analysis in `examples/full-analysis.md` (Tame Impala - The Less I Know The Better), the skill has just called **AskUserQuestion** with the follow-up menu. Below is what each follow-up looks like depending on the user's pick.

**Rules:**
- Answer **only** the chosen action. No full re-analysis.
- No printed "type a letter" footer.
- After the answer, call **AskUserQuestion** again (per `templates/followup.md`) so the user can chain another action or pick "Klaar".

---

## User picks "Meer over de artiest"

```
**Artiestinformatie — uitgebreid:**
Tame Impala is het soloproject van Kevin Parker, opgericht in 2007 in Perth (Australië). Parker speelt en produceert alle instrumenten zelf. Het project debuteerde met de neo-psychedelische rock-LP "Innerspeaker" (2010), en bewoog zich met "Lonerism" (2012) richting synthesizer-pop. Vanaf "Currents" (2015) — het album van dit nummer — verschoof Tame Impala definitief richting disco-, R&B- en pop-invloeden, terwijl de psychedelische productiestijl behouden bleef. Live opereert Tame Impala als vijfkoppige band.
```

*(Skill calls AskUserQuestion: "Wil je nog iets anders weten over dit nummer?" — buttons: Voeg toe aan playlists / Meer over het nummer / Uitgebreide playlist-analyse / Klaar.)*

---

## User picks "Meer over het nummer"

```
**Song-analyse — "The Less I Know The Better":**
Lyrisch is dit een nummer over jaloezie en de pijn van wanneer iemand waarop je verliefd bent kiest voor een ander. De verteller weet dat hij beter af is met afstand ("the less I know the better"), maar kan zichzelf er niet toe brengen los te laten. Cool en de jongen die Heather verovert worden tegenover elkaar geplaatst — de verteller verliest die strijd op alle fronten.

Muzikaal staat het in schril contrast met de tekst: de aanstekelijke basline, falsetto-vocals en disco-groove maken het tot een dansbare track. Die spanning tussen vrolijke productie en pijnlijke lyrics is karakteristiek voor Kevin Parker's songwriting.
```

*(Skill calls AskUserQuestion again with remaining options + Klaar.)*

---

## User types "album" via Other → Album & albumhoes

```
**Album:** Currents (2015)

**Albumhoes:** https://upload.wikimedia.org/wikipedia/en/9/9b/Tame_Impala_-_Currents.png
```

Note: only link to cover art if you have a verified URL. If you don't, say "Geen officiële linkbron beschikbaar — zoek 'Tame Impala Currents albumhoes' in een browser." rather than inventing one.

*(Skill calls AskUserQuestion again.)*

---

## User types "links" via Other → Streaming links

```
**Beluister "The Less I Know The Better":**
- Spotify: https://open.spotify.com/track/6K4t31amVTZDgR3sKmwUJJ
- YouTube: https://www.youtube.com/watch?v=sBzrzS1Ag_g
- Apple Music: https://music.apple.com/album/the-less-i-know-the-better/1440838039
- Tidal: search "Tame Impala — The Less I Know The Better"
- SoundCloud: search "Tame Impala — The Less I Know The Better"
```

Only paste links you are sure exist. Search prompts ("search '...'" on a given platform) are an acceptable fallback when you don't have a verified URL.

*(Skill calls AskUserQuestion again.)*

---

## User picks "Uitgebreide playlist-analyse"

```
**Uitgebreide playlist-analyse:**

✅ **Past goed:**
- **Alternative / Indie** — definitief het beste tehuis. Tame Impala is een hoeksteen van het indie-pop / psychedelische pop canon en dit nummer is een fanfavoriet uit dat canon.
- **Pop / Mainstream** — "Currents" was Parker's commerciële doorbraak en deze track is breed bekend buiten indie-luisterkringen.

⚠️ **Past randvoorwaardelijk:**
- **Happy tunes** — de muzikale productie is opgewekt en dansbaar, maar de lyrische thematiek is bitter — afhankelijk van wat de gebruiker met "happy" bedoelt.
- **Ket420** — droomzware synths en spacey vibe maken hem geschikt voor mellow listening, maar het is geen "stoner anthem" in enge zin.

❌ **Past niet:**
- **Party** — wel dansbaar maar geen festival-banger; te ingetogen voor een party-playlist.
- **House / Techno / Trance** — geen elektronische track in die zin; de disco-groove is acoustic-band, geen DAW-productie.

**Alternatieven die niet in de top-5 stonden:**
- *Sad tunes* zou kunnen op basis van de lyrische pijn, maar de productie verraadt dat niet — dus niet logisch.
```

*(Skill calls AskUserQuestion again with remaining options + Klaar.)*

---

## User picks "Klaar"

End the flow silently — no closing line, no summary. The user has indicated they're done.

---

## User types something ambiguous via Other

If the free-text doesn't map clearly to any action (e.g. "huh?"), the skill calls **AskUserQuestion** again to disambiguate — it does **not** guess. Example re-prompt:

> "Ik begreep dat niet helemaal. Wat wil je doen?"
> - Voeg toe aan playlists
> - Meer info (artiest of nummer)
> - Uitgebreide playlist-analyse
> - Klaar
