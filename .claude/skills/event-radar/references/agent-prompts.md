# Agent prompt templates

Each agent is a `general-purpose` agent with WebSearch + WebFetch access. Brief them like smart colleagues who haven't seen the surrounding conversation. **Dispatch in parallel** (one message, multiple Agent tool calls).

---

## Universal preamble (paste at top of every agent prompt)

```
You are researching concerts and festivals for a user based in {{home_city}}, {{home_country}}.

Today's date: {{today_iso}}. Search window: {{date_window}}.

LOCATION RULES:
- CONCERTS: within {{concert_radius}} km of {{home_city}}.
- FESTIVALS: within {{festival_radius}} km of {{home_city}}.

BLOCKED DATES (skip events overlapping these):
{{blocked_ranges_bulleted}}

VENUE-TIER PREFERENCE: {{venue_tier}}
CONFIDENCE FLOOR: {{confidence_floor}}

OUTPUT LANGUAGE: {{output_language}}
```

---

## Metal / Rock agent

After preamble, add:

```
USER TASTE — Metal & Rock:
{{top_artists_metal_rock}}

VENUES TO CHECK (sized appropriately for tier preference):
{{venue_list_metal}}

FESTIVALS TO CHECK:
{{festival_list_metal}}

YOUR JOB:
1. Use WebSearch / WebFetch on artist tour pages and venue agendas.
2. Verify date, city, country, venue, distance, which user-fav plays.
3. Filter to radius + date window + blocked dates.
4. Report: group by month. Each entry: `**Date** — Artist/Festival — Venue, City (distance) — [link](url) — Why match`.
5. End with "Skipped because…" section.
6. Be honest about unconfirmed dates — flag them.
```

---

## Electronic agent (broad: House/Techno/DnB/Hardstyle/Synthwave)

Same structure. Emphasize:
- Sub-genre coverage spread across the report
- Per festival, list 3–5 lineup matches from the user's favs
- For multi-stage festivals, note which stage(s) the favs play

---

## Rap / Hip-hop agent

Same structure. Emphasize:
- Distinguish US / UK / NL rap
- Arena-tier tours (Eminem, Kendrick, J. Cole) deserve extra verification — check `eminem.com` / `kendricklamar.com` / venue site, not just aggregators
- Watch for known fake-news (see `caveats.md`)

---

## Indie / Alt / Pop / Jazz agent

Same structure. Emphasize:
- North Sea Jazz, Le Guess Who?, Le Mini Who, Festival Mundial — jazz/world fests often missed
- Smaller theater venues (Caprera openluchttheater, BIMHUIS, Het Wapen)

---

## Supplementary "missing favs" agent

Use when Liked Songs reveals top-50 artists not present in genre-specific playlists. Same structure. Emphasize:
- Tour-cycle artists (Iron Maiden, Linkin Park From Zero, etc.)
- Old-favs nostalgia tours
- Reggae/dub if user has a Landjuweel-type playlist

---

## Discovery agent (small venues + unknown adjacent artists)

```
This is DISCOVERY research — the OPPOSITE of the main list. Find smaller venues with LESS-KNOWN acts the user would probably love but DOESN'T listen to yet.

USER TASTE PROFILE (so you know what's "adjacent"):
{{taste_profile_with_adjacency_hints}}

SMALL VENUES TO SCAN (CORE of the task — read their agendas):
{{small_venue_list}}

YOUR JOB:
1. WebFetch each venue's June–Dec agenda.
2. Find shows by acts in the user's adjacent-taste zone that are NOT by the famous favs (since those are in the main list).
3. Filter blocked dates rigorously.
4. Each entry: `**Date** — Artist — Venue, City — [link](url) — Why match (which user-fav this is adjacent to)`.
5. Aim for 12–20 discoveries.
6. End with a "Browse these venues' agendas yourself" section.
```

---

## EDM genre-specific agent

```
This is PURE genre-night research. The main list already has the mega-fests (Tomorrowland, Defqon.1, Liquicity, etc.) — this round focuses on pure genre-specific nights/parties:
- Pure Drum & Bass nights
- Pure techno parties (club nights, raves)
- Pure hardstyle/hardcore events
- Pure trance events
- Pure dubstep/bass events

USER'S EDM FAVS:
{{edm_favs_by_subgenre}}

VENUES TO SCAN:
{{edm_venue_list}}

EVENT SERIES TO CHECK:
- Verknipt, Rampage, Liquicity NL, Q-dance one-offs, Strafwerk, Loveland, KNTXT, Drumcode, Reverze, Project Hardcore

YOUR JOB:
1. WebFetch venue agendas + event-series pages.
2. Find PURE genre nights (skip the mega-fests).
3. Filter blocked dates.
4. Report grouped BY GENRE first (DnB / Techno / Hardstyle / House / Dubstep / Trance / Other), then chronologically within each.
5. End with "Series to watch" — recurring nights to bookmark.
```

---

## Tribute / legacy agent (optional, only if `tribute` list type requested)

For deceased / inactive favs (Pink Floyd, Queen, Michael Jackson, 2Pac, etc.) — find quality tribute acts in the user's region.

```
This round is TRIBUTE and LEGACY acts only. The user has favs who are deceased, disbanded, or
have not toured in years — the original act is not an option, so a high-quality tribute is.

INACTIVE / DECEASED FAVS (with why they're unavailable):
{{inactive_favs_with_reason}}

VENUES TO SCAN:
{{venue_list}}

YOUR JOB:
1. For each inactive fav, WebFetch venue agendas + the tribute act's own site/socials.
2. Judge ACT QUALITY, not just adjacency — this is the axis that matters here. A mediocre
   tribute to a top fav is worth less than an excellent tribute to a mid fav. Rank by:
   official endorsement or ex-members in the line-up > established act with a strong live
   reputation > good reviews > local/unknown quality.
3. Filter blocked dates.
4. Report chronologically, grouped by month. Per entry give: tribute act name, which original
   artist it covers, venue + city + distance, date, source URL, and an endorsement marker
   (`officieel geëndorseerd` / `met oud-bandleden` / `-`) so the writer can render it.
5. Name every inactive fav you found NOTHING for, so the output can say it was searched.
6. Flag tribute-scene traps explicitly: two competing tributes with near-identical names,
   acts that swap line-ups without announcing, and "officieel" claims not confirmed by the
   rights holders. Verify on the venue agenda before asserting.
```

---

## Tips for all agents

- **Cap report length** — ~500-700 words. Force prioritization.
- **Require sources** — every entry needs a URL, prefer official.
- **End with caveats** — honest "skipped because" + "not yet confirmed".
- **Group consistently** — by month for favs/discovery, by genre for EDM.
- **Cross-check** — if two sources conflict on a date, flag it.
