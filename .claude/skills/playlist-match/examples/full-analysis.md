# Example — full analysis

Worked example to anchor the output format. The user's message in this scenario:

> "Tame Impala - The Less I Know The Better"

The artist has not appeared earlier in the chat, so the artist info block **is** included.

Note: the chat output ends after **Playlist match**. After printing the analysis, the skill calls **AskUserQuestion** with the follow-up menu from `templates/followup.md` — that prompt is rendered in the UI, not as chat text.

---

## Tame Impala - The Less I Know The Better

**Artiestinformatie:**
Tame Impala is het soloproject van de Australische multi-instrumentalist Kevin Parker en staat bekend om psychedelische pop met dreamy synths en falsetto-zang.

**Nummeromschrijving:**
Een groovy disco-pop track met droomzware synths, melancholische lyrics en een onmiskenbare bassline die het nummer draagt.

**Genres:**
- Psychedelic Pop — 92% — AllMusic + Wikipedia consensus; falsetto-vocals over droomzware synths
- Disco — 78% — onmiskenbare bassline, four-on-the-floor groove
- Indie / Alternative — 71% — productie en context passen bij indie-rock canon van begin 2010s

**Playlist match:**
- Alternative / Indie — 88% — past binnen het indie-pop canon, productiestijl Tame Impala
- Pop / Mainstream — 74% — radio-vriendelijke disco-pop hook
- Happy tunes — 62% — opgewekte groove, ondanks melancholische lyrics
- Ket420 — 58% — droomzware synths en spacey vibe lenen zich voor mellow listening

*(Skill calls AskUserQuestion: "Wat wil je hierna doen?" — buttons: Voeg toe aan playlists / Meer over de artiest / Meer over het nummer / Uitgebreide playlist-analyse.)*

---

## Variant — artist already covered earlier in the chat

The user's *second* message is "Tame Impala - Borderline". The artist info block is **skipped**:

## Tame Impala - Borderline

**Nummeromschrijving:**
Dromerige synth-pop met een aanstekelijke fluit-hook en typische Tame Impala falsetto.

**Genres:**
- Psychedelic Pop — 90% — consistent met Parker's productiestijl, AllMusic + RYM eens
- Synth-pop — 76% — fluit-hook en synth-arrangement leunen meer richting synth-pop dan disco
- Indie / Alternative — 70% — canon-context indie-rock 2020

**Playlist match:**
- Alternative / Indie — 87% — indie-pop canon, Tame Impala productiestijl
- Pop / Mainstream — 72% — radio-vriendelijke pop-hook
- Ket420 — 60% — dromerige synths, mellow vibe

*(Skill calls AskUserQuestion as above.)*

---

## Variant — electronic subgenre includes Electronic Music umbrella

For "Charlotte de Witte - Doppler" (techno):

**Playlist match:**
- Techno — 94% — strakke industrial techno, vier-op-de-vloer kick, hypnotiserende synth
- Electronic Music — 90% — umbrella-regel: alle elektronische tracks komen hier ook
- Party — 82% — peak-time festival-energie
- Angry tunes — 41% — donker, agressief — past randvoorwaardelijk

Note `Electronic Music` listed **alongside** Techno, not instead of.
