# Config schema — `event-radar.config.json`

The authoritative source of user defaults + self-learned data for the event-radar skill. Lives at the repo root, gitignored. Sample is checked in as `event-radar.config.example.json`.

## Top-level keys

| Key | Type | Purpose |
|---|---|---|
| `_schema_version` | number | Bump when schema changes incompatibly |
| `user` | object | Home base + radius defaults |
| `preferences` | object | Per-run defaults the skill applies unless overridden |
| `favorite_genres` | array of strings | Default genre filter; used as `should_trigger` hint for agents |
| `do_not_recommend_artists` | array | Artists to filter out of all matching (false positives in playlists) |
| `venues` | object | Preferred / avoid / known_about lists |
| `distance_cache_km` | object | "City, Country" → km from `user.home_city`. Self-populated. |
| `ticket_history` | object | `bought` / `attended` / `wishlist` lists with date+event |
| `recurring_blocked_dates` | array | Yearly-recurring blocks (Christmas, etc.) |
| `research_caveats` | object | `fake_news` / `cancelled_events` / `skip_nl_artists` / `corrected_skip_nl` / `out_of_radius_high_match` / `lineup_format_notes` arrays. Self-populated. |
| `event_series_calendar_hints` | object | User-curated list of recurring annual festivals/events grouped by `spring_summer` / `autumn_winter`. Each entry: `{event, typical_dates, location, url, note?}`. Skill uses these as research seeds — "is the 2026 edition of this confirmed?" |

## `user` object

```json
{
  "name": "Wilco",
  "home_city": "Houten",
  "home_country": "NL",
  "default_concert_radius_km": 100,
  "default_festival_radius_km": 500
}
```

Both `home_city` and `home_country` are required for the distance-table to make sense. `default_concert_radius_km` and `default_festival_radius_km` are per-run overridable via AskUserQuestion.

## `preferences` object

All optional. Skill uses sane defaults when missing:

| Key | Type | Default | Notes |
|---|---|---|---|
| `language` | string | `"nl"` | Output language. `"en"` for English. |
| `list_types` | array | `["favs", "discovery", "edm-genres"]` | Which lists to generate |
| `venue_tier` | string | `"mix"` | `arenas_only` / `mid_size` / `small_underground` / `mix` |
| `confidence_floor` | string | `"confirmed_only"` | vs `"include_unconfirmed_with_flag"` |
| `travel_mode` | string | `"car"` | `"car"` or `"public_transport"` |
| `day_of_week_preference` | string | `"no_preference"` | `"weekends_only"` / `"weeknights_ok"` |
| `budget_tier` | string | `"any"` | `"under_50"` / `"under_100"` / `"any"` |
| `output_granularity` | string | `"split"` | `"split"` (one file per type) or `"single"` |
| `recency_weighting` | string | `"all_time_equal"` | vs `"weight_recent_more"` |
| `festival_camping_ok` | boolean | `true` | Affects multi-day festival weighting |
| `accessibility_notes` | string | `""` | Free text — kid-friendly, sober, mobility, etc. |
| `include_tribute_bands` | boolean | `false` | For deceased/inactive favs |

## `venues` object

```json
{
  "preferred": ["TivoliVredenburg", "De Helling", "Doornroosje"],
  "avoid": ["VenueX"],
  "known_about": [
    {
      "name": "dB's",
      "city": "Utrecht",
      "country": "NL",
      "agenda_url": "https://www.dbstudio.nl/agenda/",
      "capacity_tier": "small",
      "last_seen": "2026-06-01"
    }
  ]
}
```

- `preferred` → boost match weight
- `avoid` → exclude events at these venues
- `known_about` → auto-discovered venues; cached so the skill doesn't re-research them

## `distance_cache_km` object

Self-populated. Skill reads this BEFORE doing any distance lookups. Format: `"City, Country": <km>`.

```json
{
  "Amsterdam, NL": 35,
  "Utrecht, NL": 10,
  "Antwerpen, BE": 85
}
```

When the home city changes, this cache is invalidated and rebuilt over time.

## `ticket_history` object

```json
{
  "bought": [
    {"date": "2026-06-10", "event": "Iron Maiden Ziggo Dome", "marked_at": "2026-06-01"}
  ],
  "attended": [],
  "wishlist": []
}
```

The skill uses `bought` to mark "you're going!" in the output instead of re-recommending.

## `recurring_blocked_dates` array

```json
[
  {"yearly": "12-24/12-26", "label": "Christmas"},
  {"yearly": "07-15", "label": "Anniversary"}
]
```

Auto-applied to every run as default blocked dates. User can still add one-off blocks per run via AskUserQuestion.

## `research_caveats` object

```json
{
  "fake_news": [
    {"claim": "Eminem 2026 European Tour", "first_seen": "2026-05-29", "note": "AI-generated posters on socials; no official source."}
  ],
  "cancelled_events": [
    {"event": "Mysteryland 2026", "reason": "Festival on break, returns 2027", "first_seen": "2026-05-29"}
  ],
  "skip_nl_artists": [
    {"artist": "Metallica", "year": "2026", "reason": "M72 tour ends in London 5 jul; no NL date", "first_seen": "2026-05-29"}
  ],
  "corrected_skip_nl": [
    {"artist": "Slipknot", "year": "2026", "corrected_on": "2026-09-07", "was": "Wacken Aug 2026 only; no NL standalone", "now": "Ziggo Dome 5 dec 2026 (source: Knotfest)"}
  ],
  "out_of_radius_high_match": [
    {"event": "Summer Breeze Open Air 2026", "location": "Dinkelsbuhl, DE", "distance_km": 620, "lineup_strength": "high (In Flames + Alestorm + Lamb of God)", "status": "grotendeels uitverkocht", "first_seen": "2026-06-26", "note": "Flag if the user wants to stretch the 500 km radius for one of the strongest lineups"}
  ],
  "lineup_format_notes": [
    {"event": "Wacken Open Air", "note": "Default ticket is a 4-day weekend pass; single-day tickets historically uncertain. Verify day-ticket availability before recommending when only one festival day falls in the window.", "first_seen": "2026-06-26"}
  ]
}
```

Skill appends here when agents discover new entries. Read at the start of every run so agents don't waste time re-researching.

Key semantics:

- **`corrected_skip_nl`** — skip-NL entries later proven wrong. **Never re-add these to `skip_nl_artists`.** A skip-NL entry has a shelf life of roughly one quarter, so date-stamp every entry and re-verify anything older than ~3 months rather than trusting it. Mirror each correction into `references/caveats.md` under "Corrected on re-verify".
- **`out_of_radius_high_match`** — events outside the distance radius whose lineup is strong enough to be worth offering the user as an explicit radius-stretch, rather than silently dropping.
- **`lineup_format_notes`** — ticketing-format gotchas (weekend-pass-only festivals, day-ticket uncertainty) that change whether an in-window event is actually attendable.

## Read/write semantics

- **Read at**: step 2 (load config), step 3 (taxonomy + playlists), step 4 (agent briefing — pass relevant config to agents), step 5 (consolidation — apply `do_not_recommend_artists` + `venues.avoid`).
- **Write at**: step 9 (after successful run). Never write during agent execution — only after consolidation succeeds and output files are saved.
- **Atomic writes**: read full JSON → modify in memory → write back. Never partial-update.
- **Preserve unknown keys**: if the user added custom keys, leave them untouched.
- **Schema version bump**: if `_schema_version` in the example is newer than the user's config, log a warning and ask the user before migrating.
