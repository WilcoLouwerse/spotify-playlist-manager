# Venue catalog — SEED ONLY

**⚠️ This file is a seed/fallback. The skill's authoritative venue data lives in [`event-radar.config.json`](../../../../event-radar.config.json) under `venues.preferred` / `venues.avoid` / `venues.known_about`.** Read the config first; only fall back to this seed when the config is missing or empty.

This catalog assumes a Houten-based user. **If the config's `user.home_city` differs, this list is no longer authoritative** — use it as inspiration and rebuild a local catalog via WebSearch + WebFetch for the new home city.

**Self-learning**: when the skill discovers a new venue in a successful run (matches taste, within radius, has agenda online), append it to the config's `venues.known_about` array with `{name, city, country, agenda_url, capacity_tier, last_seen}`. Over time this grows into a personal catalog far richer than this seed.

---

## How tiers map to user preference

- `arenas only` → only "Arenas (large)" below
- `mid-sized` → "Mid-size" + selected arena shows
- `small / underground` → "Small / underground" + open-air theaters
- `mix` (default) → all tiers

## Arenas (large, ~10k–60k)

| Venue | City | Distance from Houten | Agenda |
|---|---|---|---|
| Ziggo Dome | Amsterdam | ~40 km | https://www.ziggodome.nl/agenda |
| AFAS Live | Amsterdam | ~40 km | https://www.afaslive.nl/en/agenda |
| Johan Cruijff ArenA | Amsterdam | ~40 km | https://www.johancruijffarena.nl/en/calendar |
| Ahoy | Rotterdam | ~60 km | https://www.ahoy.nl/en/events |
| GelreDome | Arnhem | ~55 km | https://www.gelredome.nl/ |
| Sportpaleis (AFAS Dome) | Antwerpen, BE | ~140 km | https://www.sportpaleis.be/en/agenda |
| Jaarbeurs | Utrecht | ~10 km | https://www.jaarbeurs.nl/ |
| Brabanthallen | Den Bosch | ~50 km | https://brabanthallen.nl/ |

## Mid-size (~1k–5k)

| Venue | City | Distance from Houten | Agenda |
|---|---|---|---|
| TivoliVredenburg (Grote Zaal, Ronda) | Utrecht | 10 km | https://www.tivolivredenburg.nl/agenda/ |
| 013 (Main Stage) | Tilburg | 50 km | https://www.013.nl/en/agenda |
| Paradiso (Grote Zaal) | Amsterdam | 40 km | https://www.paradiso.nl/en/program |
| Melkweg (Max) | Amsterdam | 40 km | https://www.melkweg.nl/en/agenda |
| Effenaar (Grote Zaal) | Eindhoven | 55 km | https://www.effenaar.nl/agenda |
| Doornroosje (Grote Zaal) | Nijmegen | 50 km | https://www.doornroosje.nl/agenda |
| Patronaat | Haarlem | 50 km | https://patronaat.nl/programma/ |
| Annabel | Rotterdam | 50 km | https://annabel.nu/agenda/ |
| Maassilo | Rotterdam | 50 km | https://dance.maassilo.com/agenda/ |
| AB (Ancienne Belgique) | Brussel, BE | ~165 km (festival rule) | https://www.abconcerts.be/ |

## Small / underground (~150–800)

| Venue | City | Distance from Houten | Agenda |
|---|---|---|---|
| TivoliVredenburg Pandora / Hertz / Cloud Nine | Utrecht | 10 km | https://www.tivolivredenburg.nl/agenda/ |
| De Helling | Utrecht | 10 km | https://www.tivolivredenburg.nl/de-helling/ |
| dB's | Utrecht | 10 km | https://www.dbstudio.nl/agenda/ |
| EKKO | Utrecht | 10 km | https://www.ekko.nl/ |
| ACU | Utrecht | 10 km | https://acu.nl/ |
| TrapOp! | Utrecht | 10 km | (check social media; small underground) |
| RASA | Utrecht | 10 km | https://www.rasa.nl/ |
| Paradiso Upstairs / Tolhuistuin | Amsterdam | 40 km | https://www.paradiso.nl/en/program |
| Bitterzoet | Amsterdam | 40 km | https://www.bitterzoet.com/ |
| OCCII | Amsterdam | 40 km | https://occii.org/ |
| OT301 | Amsterdam | 40 km | https://ot301.nl/ |
| BIMHUIS | Amsterdam (jazz) | 40 km | https://www.bimhuis.nl/agenda/ |
| RADION | Amsterdam (techno) | 40 km | https://radion.amsterdam/ |
| Shelter | Amsterdam (techno) | 40 km | https://shelteramsterdam.nl/ |
| Thuishaven | Amsterdam | 40 km | https://thuishaven.nl/ |
| SkateCafe | Amsterdam | 40 km | https://www.skatecafe.nl/ |
| Q-Factory | Amsterdam | 40 km | https://q-factory.nl/ |
| Merleyn | Nijmegen | 50 km | https://www.doornroosje.nl/agenda (Doornroosje runs it) |
| Effenaar small hall | Eindhoven | 55 km | https://www.effenaar.nl/agenda |
| 013 Stage 01 (small) | Tilburg | 50 km | https://www.013.nl/programma |
| Paard | Den Haag | 60 km | https://www.paard.nl/en/event/ |
| PIP | Den Haag | 60 km | https://pip.nl/ |
| Luxor Live | Arnhem | 55 km | https://www.luxorlive.nl/agenda/ |
| Willemeen | Arnhem | 55 km | https://willemeen.nl/ |
| BIRD | Rotterdam | 50 km | https://www.bird-rotterdam.nl/ |
| Toffler | Rotterdam | 50 km | https://toffler.nl/ |
| Hedon | Zwolle | 90 km | https://hedon-zwolle.nl/ |

## Open-air / theatres

| Venue | City | Distance from Houten | Agenda |
|---|---|---|---|
| Caprera Openluchttheater | Bloemendaal | 60 km | https://www.caprera.com/programma |
| Gashouder | Amsterdam | 40 km | https://www.gashouder.nl/agenda/ |
| Beekse Bergen (festival site) | Hilvarenbeek | 65 km | (festival-only) |
| Walibi terrein | Biddinghuizen | 65 km | (Lowlands etc.) |
| Megaland | Landgraaf | 180 km | (Pinkpop) |

## Out-of-radius (festival rule only, from Houten)

| Venue | City | Distance |
|---|---|---|
| Werchter | Werchter, BE | ~140 km |
| Boom (Tomorrowland site) | Boom, BE | ~140 km |
| Kortrijk (Alcatraz) | Kortrijk, BE | ~220 km |
| Dessel (Graspop) | Dessel, BE | ~150 km |
| Hasselt (Pukkelpop) | Hasselt, BE | ~155 km |
| Ferropolis (Splash!) | Gräfenhainichen, DE | ~600 km — **outside 500 km festival radius** |
| Wacken | Wacken, DE | ~470 km — at edge |
| Dinkelsbühl (Summer Breeze) | Dinkelsbühl, DE | ~620 km — **outside** |
| Frauenfeld (Openair Frauenfeld) | Frauenfeld, CH | ~650 km — **outside** |

---

## When the home city is NOT Houten

This seed assumes Houten. If `event-radar.config.json -> user.home_city` is set to a different city:

1. **Recompute distances**. Use a distance-API or WebSearch ("driving distance from X to Y"). Cache results in config's `distance_cache_km`.
2. **Re-tier venues**. A venue that's 40 km from Houten might be 150 km from Maastricht.
3. **Add local venues**. Every Dutch / Belgian / German city has its own venue ecosystem. Examples:
   - Maastricht: Muziekgieterij, AINSI, Het Gouvernement
   - Groningen: SPOT De Oosterpoort, Vera, USVA
   - Hamburg (DE): Docks, Markthalle, Große Freiheit 36
   - Berlin: Festsaal Kreuzberg, Berghain, Astra Kulturhaus
   - Paris: Le Bataclan, Olympia, Élysée Montmartre
4. **Update config**. Add discovered venues to `venues.known_about`.
