# Example — uncertainty flow

User message:

> "kun je iets zeggen over Galimatias - In My Head"

The song is on Bandcamp / SoundCloud, the artist is on the edge of multiple electronic micro-genres. **The skill first ran the default flow: WebSearch + WebFetch on AllMusic, Wikipedia, RYM, Discogs.** AllMusic returns 404 for the track; Wikipedia has no article; RYM has the album but no track-level genre; Discogs lists the release with sparse tags. Last.fm has tags but they're all over the place ("future bass", "chillwave", "alternative R&B", "experimental"). **Web lookups failed to converge — that's what triggers the uncertainty fork.**

---

## Step 1 — print the lead-in line (Dutch), then call AskUserQuestion

The lead-in always names the web sources that were tried, so the user understands this menu only appears *after* live lookup failed.

```
Sorry, ik heb moeite om de genres voor dit nummer te vinden. Ik heb AllMusic, Wikipedia, RYM en Discogs opgezocht (WebFetch/WebSearch), maar AllMusic en Wikipedia geven geen track-level info, en de Last.fm-tags spreken elkaar tegen (future bass, chillwave, alternative R&B, experimental).
```

Then the skill calls **AskUserQuestion**:

> "Web-lookups gaven geen duidelijk antwoord. Hoe wil je dat ik hiermee verder ga?"
> - **Breder zoeken (artiestpagina's)** — Verbreed de WebFetch/WebSearch naar artiestbrede pagina's (AllMusic / Wikipedia / RYM / Last.fm artist). Scope wordt artiestgebaseerd.
> - **Zwakkere webbronnen** — Val terug op zwakkere webbronnen (Last.fm tags, SoundCloud-tag, Bandcamp-tag) via WebFetch. Lagere precisie, hogere recall.
> - **Sla genres over** — Alleen playlist matching, geen harde genreclaim.
> - **Inschatten zonder internet (Claude + OpenAI)** — Laatste redmiddel: Claude én OpenAI schatten in op basis van trainingsdata. OpenAI wordt via analyze-only (read-only, geen Spotify-wijzigingen) aangeroepen. Als OpenAI niet beschikbaar is wordt dit gemeld en valt de skill terug op Claude alleen.

Stop. Wait for the user.

---

## Step 2 — user picks "Breder zoeken (artiestpagina's)"

The skill broadens the WebFetch/WebSearch to artist-level pages and reports back.

```
Oké! Ik heb de WebFetch-sweep verbreed naar artiestbrede pagina's (AllMusic, Last.fm, RYM artist).

Genres:
- Future Bass — 70% — Galimatias' artiestpagina op AllMusic plaatst hem rond future bass en alt-electronica (bron: AllMusic artist page via WebFetch, betrouwbaarheid: middel, scope: artiestgebaseerd)
- Alternative R&B — 60% — RYM artist tags noemen alt-R&B als secundair (bron: RYM artist page via WebFetch, betrouwbaarheid: middel, scope: artiestgebaseerd)
- Chillwave — 50% — Last.fm artist tags overlappen met chillwave (bron: Last.fm artist via WebFetch, betrouwbaarheid: laag, scope: artiestgebaseerd)
  Caveat: scores zijn artiestbreed, niet trackspecifiek — track op AllMusic en Wikipedia bleef onvindbaar.

Playlist matches:
- Electronic Music — 78% — past in de elektronische umbrella, ongeacht welke micro-genre wint
- Rustig / 'anders' — 64% — mid-tempo, dromerig, niet evident dansbaar
- Ket420 — 58% — psychedelische textuur, mellow tempo
```

Then the skill calls **AskUserQuestion** again (per `templates/followup.md`) so the user can pick a follow-up or "Klaar".

---

## Step 3 — if the user had picked "Inschatten zonder internet (Claude + OpenAI)" instead

The skill needs a Spotify URL/ID to run `analyze-only`. In this example the user originally typed a name only — no URL. So the skill asks:

> "Voor de OpenAI-check heb ik een Spotify-link of track-ID nodig. Plak die via 'Other', of kies 'Alleen Claude' om OpenAI over te slaan."
> - **Alleen Claude**

User pastes `https://open.spotify.com/track/3MKCzCnpzw3TjFzes5ci1L`.

The skill runs its own Claude training-recall classification (held internally), then:

```bash
.venv/bin/python playlist_manager.py analyze-only "https://open.spotify.com/track/3MKCzCnpzw3TjFzes5ci1L"
```

OpenAI returns successfully. The skill merges the two sources:

```
Oké! Ik heb Claude's interne kennis gecombineerd met OpenAI's analyze-only (read-only, geen Spotify-wijzigingen).

Genres:
- Future Bass — 68% — chopped vocal samples, supersaw stabs; Claude en OpenAI zijn het eens (bron: Claude + OpenAI (interne kennis), betrouwbaarheid: middel, scope: nummerspecifiek)
- Alternative R&B — 58% — vocaal-gedreven, hybride met electronica; alleen Claude noemde dit, OpenAI niet (bron: Claude (interne kennis), betrouwbaarheid: laag, scope: artiestgebaseerd)
- Chillwave — 45% — dromerige synthtexturen; bronnen zijn het niet eens (Claude: 55%, OpenAI: 35%) (bron: Claude + OpenAI (interne kennis), betrouwbaarheid: laag, scope: artiestgebaseerd)
  Caveat: beide bronnen gebruiken trainingsdata, geen live webcheck.

Playlist matches:
- Electronic Music — 75% — Claude én OpenAI noemen dit als eerste keuze (bron: Claude + OpenAI (interne kennis), betrouwbaarheid: middel)
- Rustig / 'anders' — 63% — Claude noemt dit, OpenAI niet (bron: Claude (interne kennis), betrouwbaarheid: laag)
- Ket420 — 55% — OpenAI noemt dit, Claude niet (bron: OpenAI (interne kennis), betrouwbaarheid: laag)
```

---

### Variant — OpenAI unavailable (e.g. no API key)

Same user pick, same URL, but `analyze-only` prints `OPENAI_API_KEY not set in .env`. The skill falls back to Claude-only and notifies the user:

```
⚠️ OpenAI was niet beschikbaar (geen API key). Alleen Claude's interne kennis is gebruikt.

Genres:
- Future Bass — 65% — chopped vocal samples, supersaw stabs, snare-roll buildups passen bij Galimatias' bekende sound (bron: Claude (interne kennis), betrouwbaarheid: middel, scope: nummerspecifiek)
- Alternative R&B — 55% — vocaal-gedreven, hybride met electronica, past bij het bredere oeuvre (bron: Claude (interne kennis), betrouwbaarheid: laag, scope: artiestgebaseerd)
- Chillwave — 45% — dromerige synthtexturen en lo-fi-productie, maar minder eenduidig (bron: Claude (interne kennis), betrouwbaarheid: laag, scope: artiestgebaseerd)
  Caveat: alleen Claude's interne kennis als bron — geen cross-check tegen live webbronnen of OpenAI.

Playlist matches:
- Electronic Music — 70% — past in de elektronische umbrella, ongeacht welke micro-genre wint (bron: Claude (interne kennis), betrouwbaarheid: middel)
- Rustig / 'anders' — 62% — mid-tempo, dromerig, niet evident dansbaar (bron: Claude (interne kennis), betrouwbaarheid: laag)
- Ket420 — 55% — psychedelische textuur, mellow tempo (bron: Claude (interne kennis), betrouwbaarheid: laag)
```

---

## Step 4 — if the user had picked "Sla genres over"

"Sla genres over" = playlist matching **only**, no genre claim. Response:

```
Oké! Op basis van je keuze ('Sla genres over') sla ik harde genreclaims over en doe ik alleen playlist matching.

Playlist matches:
- Electronic Music — 76% — past in de elektronische umbrella ongeacht subgenre
- Rustig / 'anders' — 64% — mid-tempo, dromerig
- Ket420 — 58% — psychedelische textuur, mellow tempo
```

Then call **AskUserQuestion** again.
