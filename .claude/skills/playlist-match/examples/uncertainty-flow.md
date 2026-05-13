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
> - **Schat op basis van artiest** — Gebruik artiestbrede tags / reputatie als bron, scope = artiestgebaseerd.
> - **Minder betrouwbare bron** — Vertrouw op Last.fm tags, SoundCloud-tag of vergelijkbare losse signalen.
> - **Combineer beide** — Artiestbron én minder-betrouwbare bron samen wegen.
> - **Sla genres over** — Alleen playlist matching, geen harde genreclaim.

Stop. Wait for the user.

---

## Step 2 — user picks "Combineer beide"

Response (note the per-genre fields required by `references/output-rules.md`):

```
Oké! Op basis van je keuze ('Combineer beide') zou ik zeggen dat dit nummer de volgende genres en playlist matches heeft:

Genres:
- Future Bass — 62% — chopped vocal samples, supersaw stabs, snare-roll buildups (bron: Last.fm + soundcloud genre-tag, betrouwbaarheid: middel, scope: nummerspecifiek)
- Chillwave — 55% — dromerige synthtexturen, mid-tempo, lo-fi-productie (bron: Last.fm tags + artiestbreed, betrouwbaarheid: laag, scope: artiestgebaseerd)
- Alternative R&B — 48% — vocal-driven, gevoelig songschrijven, hybride met electronica (bron: Last.fm + artiestbreed, betrouwbaarheid: laag, scope: artiestgebaseerd)
  Tegenstrijdigheid: bronnen zijn het niet eens — geen consensus tussen Last.fm tags en SoundCloud-tag.

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
