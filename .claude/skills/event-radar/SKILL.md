---
name: event-radar
description: Generates personalized concert/festival recommendations from the user's Spotify playlists with date-availability filtering, genre filtering, venue-tier filtering, and discovery mode — fires on 'welke concerten zou ik leuk vinden', 'wat is er te doen de komende maanden', 'event-radar', 'concert recommendations', or 'find festivals for me'.
metadata:
  category: Workflow
  tags: [music, events, concerts, festivals, recommendations, spotify, dutch]
---

# Event Radar

Reads the user's playlists (via Exportify CSVs in [`exportify-exports/`](../../../exportify-exports/) + [`playlists.json`](../../../playlists.json)), extracts top artists per genre, then dispatches specialist research agents to find concerts and festivals matching the user's taste, location, availability, and other preferences. Outputs structured markdown files under [`docs/events/`](../../../docs/events/).

User-facing prose is **Dutch**. Skill internals (this file, references, templates) stay in English.

**Input**: a free-text request to find events. May include hints (year, genres, dates). The skill collects missing parameters via **AskUserQuestion**.

**Output**: writes 1–4 `.md` files into `docs/events/<YYYY-MM-DD>-<list-type>.md` where `YYYY-MM-DD` is the **generation date** (today). Updates `docs/events/INDEX.md` (gitignored local index) with a new TOC row for the run. **Never write to `docs/events/README.md`** — that file is tracked in git and describes the folder's purpose generically; the TOC with personal run-metadata lives in `INDEX.md` instead.

**Config**: [`event-radar.config.json`](../../../event-radar.config.json) at repo root (gitignored). Sample in [`event-radar.config.example.json`](../../../event-radar.config.example.json). The skill **reads** this every run for user defaults (home city, radii, language, preferred venues, favorite genres, distance cache) and **writes back** to it after a successful run (new distances learned, new venues discovered, ticket history additions). See `references/config-schema.md`.

---

## Steps

### 1. Detect intent

User triggers include:
- "welke concerten/festivals zou ik leuk vinden de komende maanden"
- "wat is er te doen [de komende maanden / dit jaar / in [maand]]"
- "/event-radar"
- "find events / concerts / festivals based on my taste"
- "kun je een lijst maken van shows die bij mijn smaak passen"

If the message is **not** event-discovery, hand back to the surrounding agent. Mention adjacent skills if relevant (e.g. `/playlist-match` for single-song classification).

### 2. Load config + collect missing parameters via AskUserQuestion

**First — load the config**:

1. Try to read [`event-radar.config.json`](../../../event-radar.config.json) at the repo root.
2. **If missing — interactive first-run setup**:
   - Load `event-radar.config.example.json` into memory as a scaffold (don't write it to disk yet).
   - Tell the user in Dutch: *"Het lijkt erop dat dit je eerste run is. Ik maak een config voor je aan — laten me eerst wat basics opvragen."*
   - Call **AskUserQuestion** to gather the **essential identity fields**, batched:
     - `user.home_city` + `user.home_country` (one combined free-text field, e.g. "Houten, NL")
     - `user.default_concert_radius_km` (options: 25 / 50 / 100 / 150 / custom)
     - `user.default_festival_radius_km` (options: 300 / 500 / 750 / custom)
     - `preferences.language` (nl / en)
   - Then a second AskUserQuestion call for **taste/preferences**:
     - `favorite_genres` (multi-select from a curated list: metal, rock, hardstyle, hardcore, techno, house, drum_and_bass, dubstep, synthwave, rap, hip-hop, indie, alt, jazz, funk, soul, reggae, pop, electroswing, classical, world, other — with Other for custom additions). **Default to all** but let the user uncheck what they don't want.
     - `preferences.venue_tier` (arenas_only / mid_size / small_underground / mix)
     - `preferences.list_types` (multi-select: favs / discovery / edm-genres / tribute — tribute off by default)
     - `preferences.travel_mode` (car / public_transport)
   - For everything not asked, keep the example defaults (confidence_floor: confirmed_only, day_of_week_preference: no_preference, budget_tier: any, output_granularity: split, recency_weighting: all_time_equal, festival_camping_ok: true, accessibility_notes: "", include_tribute_bands: false).
   - Merge the answers into the scaffold and **write `event-radar.config.json` to disk**.
   - Tell the user: *"Config opgeslagen in `event-radar.config.json` (gitignored). Je kunt het later met de hand bijwerken — woonplaats, voorkeuren, ticket-history, vaste blokkades, do-not-recommend artiesten."*
   - Continue with the rest of step 2 using the freshly-saved config.
3. **If present**: read it. No notification needed.

**Never ask the user to manually create the config from outside the skill.** First-run interactive setup is part of the skill flow. After auto-creation, the user can edit manually for fine-tuning, AND the skill's write-back step 9 keeps `distance_cache_km`, `venues.known_about`, `research_caveats`, and (with confirmation) `ticket_history` up to date over time.

Use config values as defaults for every parameter below — only ask via **AskUserQuestion** for what's missing or what the user explicitly wants to override **for this run**.

**Batch related questions into one call** when possible (AskUserQuestion supports up to 4 questions per call). Skip any parameter the user already provided in the message or config.

**Required parameters** (must always be known before research starts):

1. **Time window** — e.g. "rest of 2026", "summer 2026", "June–August 2026", "Q4 2026", or specific date range. Default: "next 6 months".
2. **Blocked dates** — date ranges where the user is unavailable (vacations, other festivals, work). Format: `YYYY-MM-DD` to `YYYY-MM-DD`. Multiple ranges allowed. **Always ask** — don't skip even if user gave dates earlier.
3. **Home base & radius** — default is the address from memory (currently: Houten, NL). Defaults: 100 km for concerts, 500 km for festivals. User can override.
4. **List types to generate** (multi-select):
   - `favs` — known artists from playlists
   - `discovery` — adjacent unknown artists at smaller venues
   - `edm-genres` — pure subgenre nights (DnB / Techno / Hardstyle / etc.)
   - `tribute` — tribute bands for deceased/inactive favs (optional, off by default)

**Optional refinements** (ask if user hasn't specified):

5. **Genre filter** — limit to specific genres (e.g. "only metal + electronic", "only hip-hop"). Default: all genres from playlists.
6. **Venue-tier preference** — `arenas only` (Ziggo Dome / AFAS Live / Ahoy), `mid-sized` (Paradiso / 013 / Effenaar), `small / underground` (Doornroosje / dB's / Paard / ACU / Tivoli Pandora), or `mix`. Default: `mix`.
7. **Language of the output file** — Dutch (default) or English.
8. **Output destination** — default `docs/events/`. Override if user wants a different folder.

**Quality / scope preferences** (ask once, remember in memory for later runs):

9. **Confidence floor** — `confirmed only` (official venue/artist source) vs `include rumored/unconfirmed` with flag. Default: `confirmed only`.
10. **Day-of-week preference** — `weekends only`, `weeknights ok`, `no preference`. Default: `no preference`.
11. **Budget tier** — `any`, `under €50 only`, `under €100 only`. Default: `any`. (Affects venue-tier weighting.)
12. **Travel mode** — `car ok` (full radius), `public transport only` (NL-rail + IC, narrower radius). Default: `car ok`.
13. **Social filter** — should the skill ask "who do you want to go with?" so it can flag friend-friendly vs solo-friendly shows. Default: skip.
14. **Recency weighting** — `weight recent listens more` (use Liked Songs adds in last 6 months) vs `treat all-time equally`. Default: `treat all-time equally` (current playlists already capture taste).
15. **Output granularity** — `one file per list type` (default — one file per selected list type) or `single combined file`.

**Extra refinements** (ask only if user signals interest):

16. **Already-bought tickets** — list of events the user already has tickets for, so the skill marks them ✅ "you're going!" rather than re-recommending them. Stored as `<!-- user-note: ticket-bought -->` annotations in the output file so future runs preserve them.
17. **Artist do-not-include list** — artists that show up in playlists but the user actually dislikes (e.g. they got there from a one-off shared song). Filter these out of all matching.
18. **Festival camping vs hotel preference** — affects multi-day festival weighting (camping people are more flexible on remote sites; hotel-only folks weigh urban festivals higher).
19. **Companion / accessibility constraints** — partner with mobility limit, bringing kids, sober events only, etc. Affects venue/festival recommendations.
20. **Pit / seated / VIP preference** — affects which arena tour dates and which seat tiers to mention.
21. **Re-run cadence** — should the skill self-schedule via `/schedule` to re-run monthly so the user gets fresh recommendations as tours announce? Default: no.
22. **Past-events filter** — should the skill mark events that are now in the past (since last run) so the user can see what they missed (or didn't go to)?

### 3. Read taxonomy + playlists

Read:
- [`playlists.json`](../../../playlists.json) — for the user's genre taxonomy and known playlist names
- All CSV files in [`exportify-exports/`](../../../exportify-exports/) — for the actual track + artist data

Build an in-memory map of top artists per playlist (Counter of artist appearances). Pay special attention to:
- **Liked Songs** — often biggest, may contain favs not in genre-specific playlists
- **Favorieten** — explicit user-curated favorites
- **Your All-Time Top Songs** — Spotify's own ranking
- Mood/theme playlists (Party, Sad tunes, etc.) — for context but not primary discovery
- **fire-water**, **Random sht** — broader exposure, useful for discovery seeds

### 4. Dispatch specialist research agents

Dispatch **parallel agents** (one per genre cluster). Each agent gets:
- The user's top artists in that cluster (from step 3)
- Location + radius rules
- Date window + blocked dates
- List type (favs vs discovery vs edm-genres vs tribute)
- Venue-tier preference
- Confidence floor + other refinements

Default agent set (adjust based on user's actual playlists):
- **Metal/Rock** — Iron Maiden, Metallica, Korn, Slipknot, etc.
- **Electronic** (broad) — House, Techno, DnB, Hardstyle, Synthwave
- **Rap/Hip-hop** — US, UK, NL rap
- **Indie/Alt/Pop/Jazz** — Gorillaz, Lana Del Rey, jazz, etc.
- **Supplementary** — any major Liked-Songs artists missed by genre playlists
- **Discovery** (if `discovery` list type requested) — small venues + adjacent unknown artists
- **EDM-genres** (if `edm-genres` requested) — pure genre-night clubs
- **Tribute / legacy** (if `tribute` requested) — tribute acts for deceased/inactive favs

Use the prompts in `references/agent-prompts.md` as templates. Each agent should:
- Use **WebSearch** + **WebFetch** aggressively (artist tour pages, venue agendas, festival lineups)
- Verify dates against blocked windows
- Provide official URLs (venue or artist tour page, NOT aggregator-only)
- Flag unconfirmed/rumored dates explicitly
- Return structured markdown by month or by genre

Run agents **in parallel** (single message with multiple Agent tool calls) — they're independent.

### 5. Consolidate + filter

Once all agents return:
- **Filter blocked dates** rigorously. A multi-day festival overlapping any blocked day → mark as ❌ blocked unless single-day tickets exist.
- **Deduplicate** events appearing in multiple agent results.
- **Rank top picks** — events with multiple top-fav artists, or single-only-NL-date for a top-3 artist.
- **Cross-check** caveats — flag known fake-news (e.g. Eminem 2026 fake tour posters), cancelled events (Mysteryland 2026 break), and tours that skip NL/BE.

### 6. Write output files

**Filename format**: `<YYYY-MM-DD>-<list-type>.md` under `docs/events/` where `YYYY-MM-DD` is **today** (the generation date), NOT the event year. The event year lives in the file header. This way:
- Multiple runs in the same year don't overwrite each other (you get historical snapshots)
- Sorting by filename = sorting by recency
- Filename answers "when did I generate this?"

Default outputs:
- `<YYYY-MM-DD>-favs.md` — known artists list
- `<YYYY-MM-DD>-discovery.md` — small venues + unknown adjacent artists
- `<YYYY-MM-DD>-edm-genres.md` — pure subgenre nights
- `<YYYY-MM-DD>-tribute.md` — tribute bands for deceased/inactive favs. Written only when `tribute` is in the run's `list_types`. The `preferences.include_tribute_bands` boolean is the *default seed* for that — `true` pre-selects `tribute` in the list-type question; the per-run selection is always authoritative.
- `INDEX.md` (gitignored, always update) — table of contents + per-run metadata. Prepend the new run's row at the top so newest runs are first.
- `README.md` — **do not touch**. It's the tracked, generic folder-description with no per-run data.

**Filtered runs**: when the user asks for a genre- or format-filtered run, write one file with a
**descriptive** `<list-type>` slug instead of the fixed names above — e.g.
`2026-06-26-metal-festivals.md` (metal festivals only, aug–dec), `2026-09-07-verify.md`. Same
metadata block and hype-rating, narrower scope.

**Required metadata block at top of every output file** (quote block):
```markdown
> **Gegenereerd op**: <YYYY-MM-DD>
> **Zoekperiode**: <YYYY-MM-DD> t/m <YYYY-MM-DD>
> **Uitgesloten datums (jouw blokkades)**:
> - <YYYY-MM-DD> t/m <YYYY-MM-DD>
> - …
>
> **Locatie**: <home_city>, <home_country> — concerten ≤<concert_radius>km, festivals ≤<festival_radius>km
> **Skill**: `/event-radar` — zie [`.claude/skills/event-radar/`](../../.claude/skills/event-radar/)
```

Use templates from `templates/`:
- `templates/favs.md` — favorites list scaffold
- `templates/discovery.md` — discovery list scaffold
- `templates/edm-genres.md` — EDM genres scaffold
- `templates/tribute.md` — tribute list scaffold
- `templates/index.md` — local `INDEX.md` scaffold (gitignored TOC, NOT the tracked README)

**Never overwrite existing run files** (different filename per day prevents this naturally). If the user re-runs on the same day, prompt: overwrite, suffix `-v2`, or merge.

**Preserve user annotations** marked with HTML comments `<!-- user-note: ... -->` or `<!-- ticket-bought -->` in any previous run files — when adding a new run, scan the latest run file for these markers and re-apply them to matching events in the new file.

Always include in each file:
- Metadata block (above)
- **Hype-rating prefix** on every event (see *Hype rating* below)
- Per-event: date, artist/festival name, venue, city, distance (rounded km), why-match note, **official URL**
- A "Geblokkeerd door je agenda (ter info)" section listing events the user couldn't make
- A "Caveats" section listing fake-news / cancelled / skip-NL findings

#### Hype rating (mandatory on every event)

Every event entry must begin with a **rating glyph + percentage** (e.g. `🟢 82%`) representing the skill's estimate of how much the user will enjoy it. The score combines four signals:

- **Adjacency** to known top favs (closer = higher)
- **Format/venue fit** with the user's preferences
- **Artist quality / buzz** in the relevant scene
- **Listen-frequency proxy** — for known artists, weight by playlist appearances

Bands of the score:

| Glyph | Range | Meaning |
|---|---|---|
| 🔥 | 95–100% | Lock-it-in, top-tier, drop-everything |
| 🟢 | 80–94% | Sterke match, hoge kans op enthousiasme |
| 🟡 | 65–79% | Solide match, de moeite waard |
| 🟠 | 50–64% | Stretch / interessante experimentele uitstap |
| 🔵 | <50% | Niche wildcard, hit-or-miss |

Format: `- 🟢 82% — **DD mmm** — [Artist](URL) (genre) — Venue, City`

Include a **Hype-rating legenda** section near the top of each output file (just below the metadata block) that explains the glyphs in Dutch so the user can read the file standalone.

The rating is a **judgement call** — not a deterministic formula. State the rating as the skill's estimate, not as ground truth. The user may push back, in which case capture it as a learning candidate.

### 7. Update INDEX (NOT README)

Update `docs/events/INDEX.md` (gitignored local index):

- Prepend a new section for this run titled `## Run <YYYY-MM-DD>`
- Inside: a markdown table with columns `Bestand | Wat erin staat | Periode | Blokkades`
- One row per file written in this run
- Preserve all previous run sections below — never overwrite history

`docs/events/README.md` is **read-only for the skill**. It's the public-facing folder description and is tracked in git. If the skill ever needs to update it (rare — only for skill-version-related content changes), warn the user first and confirm before touching.

### 8. Show the user a summary + next steps

Render in Dutch:
- One-line summary per file written ("Hoofdlijst met X events", "Discovery met Y events", "EDM-genres met Z events")
- Top 3 picks across all lists
- Then call **AskUserQuestion** with:
  - Open the README in the editor
  - Refine one of the lists (re-run an agent with stricter filters)
  - Add more blocked dates
  - Regenerate with different parameters
  - Klaar

### 9. Write back to config

After a successful run, **update `event-radar.config.json`** with anything new the skill learned:

- **`distance_cache_km`**: any new "City, Country → km" pairs resolved during the run via WebSearch or driving-time lookup
- **`venues.known_about`**: new venues encountered with confirmed events. Format: `{name, city, country, agenda_url, capacity_tier, last_seen: "<YYYY-MM-DD>"}`
- **`research_caveats`**: confirmed fake-news, cancelled events, skip-NL artists worth remembering across runs
- **`ticket_history`**: if the user marked anything as "ticket bought" during the follow-up Q&A

Use the JSON utilities in your toolset; never silently drop existing keys.

### 10. Capture Learnings

If anything was non-obvious this run (a venue not on the default list, a series the user mentioned, a confidence flag that was wrong, a genre cluster that returned thin, an agent prompt that needed tweaking), append a **dated atomic** entry to `learning-candidates.md` under the matching section.

Promote a candidate to `learnings.md` only after **the same observation recurs across 3+ runs** OR after the user explicitly confirms the rule should stand. `learnings.md` has 5 sections:

- **Patterns That Work** — moves that consistently produced good output
- **Mistakes to Avoid** — moves that consistently caused problems
- **Domain Knowledge** — facts about the user's taste / scene / venues that only emerged from real runs
- **Open Questions** — unresolved tensions that need a future decision
- **Consolidated Principles** — promoted rules that should eventually become SKILL.md guardrails

When `learnings.md` reaches ~80-100 entries, **consolidate**: remove outdated, merge duplicates, extract cross-entry patterns, promote validated principles to SKILL.md guardrails.

Skip this step entirely if nothing new came up.

---

## Guardrails

- **Always** ask about blocked dates via **AskUserQuestion** even if the user mentioned dates earlier — they may have new ones since last run.
- **Always** use **WebSearch + WebFetch** for current tour/festival data. Never rely on training-data recall for event dates — they go stale in weeks.
- **Always** prefer the **official venue page** or **artist tour page** for URLs over aggregators (Songkick, aesplora.com, musicfestivalwizard). Aggregators are useful as discovery but the source link should be authoritative.
- **Never** invent dates. If unconfirmed, mark "(unverified)" or omit.
- **Never** include events on user's blocked dates without explicit ❌ blocked annotation in the "blocked" section.
- **Never** dump raw agent output. Always consolidate, deduplicate, and rank before writing files.
- **Never** silently overwrite existing event files — read first, merge, preserve user annotations marked with `<!-- user-note: -->`.
- **User-facing text is Dutch.** File contents in Dutch unless user requested English.
- Run agents **in parallel** when independent — saves significant time.
- **Verify radius math**: 100 km from Houten includes Amsterdam (35km), Rotterdam (50km), Den Haag (60km), Eindhoven (70km), Tilburg (50km), Nijmegen (50km), Arnhem (50km), Antwerpen (~85km — barely). Brussels (~150km) and Düsseldorf (~150km) are **outside** the concert radius.

---

## File outputs

Default tree after a successful run:

```
docs/events/
├── README.md                       # tracked in git: folder description + skill usage; no personal data
├── INDEX.md                        # gitignored: chronological TOC of all runs (per-run metadata)
├── 2026-06-01-favs.md              # gitignored: known artists — generated 2026-06-01
├── 2026-06-01-discovery.md         # gitignored: adjacent unknowns, small venues — generated 2026-06-01
├── 2026-06-01-edm-genres.md        # gitignored: pure subgenre nights — generated 2026-06-01
└── 2026-09-15-favs.md              # gitignored: a later run for autumn
```

Each run produces NEW dated files; old runs become historical snapshots (never overwritten). README's TOC groups runs by generation date.

---

## References & templates

- `references/config-schema.md` — schema for `event-radar.config.json` (the authoritative user data)
- `references/agent-prompts.md` — template prompts for each specialist agent
- `references/venue-list.md` — **seed-only** venue catalog (config takes precedence)
- `references/distance-table.md` — **seed-only** distance table from Houten (config takes precedence)
- `references/caveats.md` — seed of known fake-news, cancelled events, skip-NL artists (config's `research_caveats` extends this over time)
- `templates/favs.md`, `templates/discovery.md`, `templates/edm-genres.md`, `templates/tribute.md`, `templates/index.md` — output scaffolds
- `examples/run-2026-06.md` — example of a full run including agent dispatch
- `learning-candidates.md` + `learnings.md` — self-improvement pipeline (L6)
