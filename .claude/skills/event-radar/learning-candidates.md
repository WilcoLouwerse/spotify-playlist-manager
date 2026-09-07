# Learning candidates — event-radar

Unverified observations from individual runs. Two-stage buffer that prevents single-run noise from polluting `learnings.md`.

```
learning-candidates.md  ->  (3+ confirmations OR fixes a measured eval failure)  ->  learnings.md  ->  SKILL.md rules
       ↓ (no)
    discarded after 30 days
```

Each entry is dated. One insight per bullet. Include source (which user message / which eval). When the same candidate recurs, append `+ confirmed YYYY-MM-DD (context)` rather than duplicating.

---

## Patterns That Work

*(empty — strongest patterns from 2026-06-01 already promoted to learnings.md after user-confirmation during the same run)*

## Mistakes to Avoid

*(empty — strongest patterns from 2026-06-01 already promoted to learnings.md)*
- **2026-09-07**: **Filling a TBA line-up with expected headliners produces confident-looking wrong data.** The 2026-06-01 edm-genres/favs runs listed Awakenings ADE (21-25 okt) with "Adam Beyer, Amelie Lens, Charlotte de Witte, Reinier Zonneveld" while the line-up was still TBA. Verified 2026-09-07: only Adam Beyer is on it (Drumcode, do 22 okt); the other three are absent, and the whole event moved from Gashouder to the SugarFactory. The entry read as researched fact, not as a guess — nothing in the output signalled it was extrapolated. Rule candidate: when a line-up is TBA, write `line-up TBA` and name **zero** artists; the hype-rating may still be an estimate but artist names must be sourced. Source: 2026-09-07 verify-run.
- **2026-09-07**: **Aggregator-sourced entries were the ones that rotted.** Of the 9 events that fell away, the two with a Songkick/aggregator source URL (Daniel Caesar @ Ziggo Dome) or no official venue link were dead, while every entry carrying an official venue-agenda URL survived. Reinforces the existing guardrail — but the useful sharpening is: an entry whose *only* obtainable source is an aggregator should get an explicit `⚠️ aggregator-only` marker in the output, not just a lower rating. Source: 2026-09-07 verify-run.

## Domain Knowledge

- **2026-06-01**: Theme/mood playlists hide world-music / reggae favs. The user has a `Landjuweel '26` playlist (121 tracks) suggesting they attend Landjuweel festival; this taste is invisible in genre playlists. → **Hypothesis to validate**: detect "festival-name" playlists (titles that match known festival names like "Landjuweel", "Lowlands", "DGTL") and treat as strong signal that the user attends. Needs 2 more confirmations before promotion. Source: 2026-06-01 first full run.
- **2026-09-07**: **A skip-NL entry has a shelf life of roughly one quarter.** Three of the June skip-NL entries (Slipknot, Muse, Polyphia) were all wrong by September — each announced an NL date *after* the June runs (Muse announced 12 jun 2026, i.e. 11 days after the 2026-06-01 run). Moved to `research_caveats.corrected_skip_nl` in the config and to a "Corrected on re-verify" section in `references/caveats.md`. Rule candidate: date-stamp every skip-NL entry and re-verify any entry older than ~3 months instead of trusting it. Source: 2026-09-07 verify-run.
- **2026-09-07**: **Several major NL venue sites are unreadable by WebFetch.** Ziggo Dome and AFAS Live render their agenda entirely client-side (WebFetch returns "0 Resultaten"), and TivoliVredenburg returns HTTP 403. Working fallbacks: Songkick's venue *calendar* page for a rough list, then confirm each hit against the official tour announcement (Knotfest, Live Nation, Ticketmaster). Venues that *do* fetch cleanly: 013, Doornroosje, Patronaat, Melkweg, Effenaar, Baroeg. Source: 2026-09-07 verify-run.
- **2026-09-07**: **Gashouder was closed for renovation through 2026**, reopening only with ADE pre-opening shows. Awakenings ADE 2026 relocated to the SugarFactory. Don't treat "Awakenings" and "Gashouder" as synonyms. Source: 2026-09-07 verify-run.

## Open Questions

- **2026-06-01**: Five parallel agents (Metal/Rock + Electronic + Rap + Indie/Alt/Pop/Jazz + Supplementary) was the sweet spot for the 2026-06-01 run. Question: does this hold for narrow-taste users (only metal, or only electronic)? Probably should scale agent count down for narrow tastes. Source: 2026-06-01 run, single observation.
- **2026-06-01**: User pushed back on "only big arenas" (Ziggo Dome / AFAS Live / Ahoy). After moving to `venue_tier: mix`, the user was happy. Question: should `mix` always be the default in the example config, or is this user-specific? Source: 2026-06-01 run — converted to a Consolidated Principle if confirmed across users.
- **2026-06-01**: Should the skill auto-detect "festival-named playlists" as STRONG signals? Currently a heuristic — needs formalizing as a rule once the pattern recurs.
- **2026-06-01**: When the user has bought tickets, omit the event from recommendations or flag it as "you're going!"? Leaning toward flag-with-emoji. Source: 2026-06-01 architectural decision, awaits user feedback on a future run.

## Consolidated Principles

*(populated from learnings.md after promotion-stage entries reach standing-rule status; mirrored back here so anyone reading candidates sees the full pipeline picture.)*

---

## Maintenance

- **Sweep**: every ~30 days, drop entries older than 30 days that haven't been confirmed.
- **Promote**: 3+ confirmations → move to `learnings.md`, clear from this file.
- **Demote**: a contradiction in here → mark the `learnings.md` entry "⚠️ contradicted YYYY-MM-DD".
- **Last sweep**: 2026-06-01 — restructured to canonical 5-section format; de-duplicated entries already present in `learnings.md`; left only entries that need more confirmations.
