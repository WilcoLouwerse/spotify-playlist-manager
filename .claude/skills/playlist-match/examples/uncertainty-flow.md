# Example — uncertainty flow

User message:

> "kun je iets zeggen over Galimatias - In My Head"

The song is on Bandcamp / SoundCloud, the artist is on the edge of multiple electronic micro-genres. AllMusic has no track-level entry; Last.fm tags are all over the place ("future bass", "chillwave", "alternative R&B", "experimental"); Wikipedia has no article. **Genres can't be pinned down confidently.**

---

## Step 1 — print the lead-in line (Dutch), then call AskUserQuestion

Chat output:

```
Sorry, ik heb moeite om de genres voor dit nummer te vinden. AllMusic en Wikipedia hebben geen track-level info, en de Last.fm-tags spreken elkaar tegen (future bass, chillwave, alternative R&B, experimental).
```

Then the skill calls **AskUserQuestion**:

> "Hoe wil je dat ik hiermee verder ga?"
> - **Laat Claude inschatten** — Claude AI doet een best-effort schatting op basis van interne kennis, met expliciete betrouwbaarheidscaveats. Geen OpenAI / smart-add.
> - **Schat op basis van artiest** — Gebruik artiestbrede tags / reputatie als bron, scope = artiestgebaseerd.
> - **Minder betrouwbare bron** — Vertrouw op Last.fm tags, SoundCloud-tag of vergelijkbare losse signalen.
> - **Sla genres over** — Alleen playlist matching, geen harde genreclaim.

Stop. Wait for the user.

---

## Step 2 — user picks "Laat Claude inschatten"

Claude AI is the named fallback source — **not** OpenAI / `smart-add`. Genre confidences are capped at 70% and every row labels `bron: Claude (interne kennis)`.

```
Oké! Op basis van je keuze ('Laat Claude inschatten') doe ik een best-effort schatting op basis van mijn eigen kennis. Let op: dit is een AI-only inschatting, niet gestaafd door externe bronnen — neem de percentages met een korreltje zout.

Genres:
- Future Bass — 65% — chopped vocal samples, supersaw stabs, snare-roll buildups passen bij Galimatias' bekende sound (bron: Claude (interne kennis), betrouwbaarheid: middel, scope: nummerspecifiek)
- Alternative R&B — 55% — vocaal-gedreven, hybride met electronica, past bij het bredere oeuvre (bron: Claude (interne kennis), betrouwbaarheid: laag, scope: artiestgebaseerd)
- Chillwave — 45% — dromerige synthtexturen en lo-fi-productie, maar minder eenduidig (bron: Claude (interne kennis), betrouwbaarheid: laag, scope: artiestgebaseerd)
  Caveat: alleen interne kennis als bron — geen cross-check tegen AllMusic / RYM / Wikipedia.

Playlist matches:
- Electronic Music — 78% — past in de elektronische umbrella, ongeacht welke micro-genre wint
- Rustig / 'anders' — 64% — mid-tempo, dromerig, niet evident dansbaar
- Ket420 — 58% — psychedelische textuur, mellow tempo
```

Then the skill calls **AskUserQuestion** again (per `templates/followup.md`) so the user can pick a follow-up or "Klaar".

---

## Step 3 — if the user had picked "Sla genres over" instead

"Sla genres over" = playlist matching **only**, no genre claim. Response:

```
Oké! Op basis van je keuze ('Sla genres over') sla ik harde genreclaims over en doe ik alleen playlist matching.

Playlist matches:
- Electronic Music — 76% — past in de elektronische umbrella ongeacht subgenre
- Rustig / 'anders' — 64% — mid-tempo, dromerig
- Ket420 — 58% — psychedelische textuur, mellow tempo
```

Then call **AskUserQuestion** again.
