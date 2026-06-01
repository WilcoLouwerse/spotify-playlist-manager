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

## Domain Knowledge

- **2026-06-01**: Theme/mood playlists hide world-music / reggae favs. The user has a `Landjuweel '26` playlist (121 tracks) suggesting they attend Landjuweel festival; this taste is invisible in genre playlists. → **Hypothesis to validate**: detect "festival-name" playlists (titles that match known festival names like "Landjuweel", "Lowlands", "DGTL") and treat as strong signal that the user attends. Needs 2 more confirmations before promotion. Source: 2026-06-01 first full run.

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
