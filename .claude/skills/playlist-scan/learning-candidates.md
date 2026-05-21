# Learning candidates — playlist-scan

Unverified observations from individual runs. The two-stage buffer that prevents single-run noise from polluting `learnings.md`.

```
learning-candidates.md  ->  (3+ confirmations OR fixes a measured eval failure)  ->  learnings.md  ->  SKILL.md rules
       ↓ (no)
    discarded after 30 days
```

Each entry is dated. One insight per bullet. Include source (which user message / which eval). When the same candidate recurs, append `+ confirmed YYYY-MM-DD (context)` rather than duplicating.

---

## Patterns That Work

*(empty)*

## Mistakes to Avoid

*(empty)*

## Domain Knowledge

*(empty)*

## Open Questions

- **2026-05-15**: User wanted to scan **multiple source CSVs** in one go (Random_sht + Favorieten + Electronic_Music + Party + Rustig_'anders' → Alternative / Indie). Current AskUserQuestion offers a single-select bron. Consider making the source question `multiSelect: true` when the CSV option is chosen, then loop `scan-for` per CSV. Source: direct user feedback during run.
  - + confirmed 2026-05-18 (Trance scan, 7 sources at once: Random sht + Favorieten + Electronic Music + Party + Rustig / 'anders' + fire-water + Your All-Time Top Songs)
- **2026-05-15**: Web-first-in-batches as an option for **>20 track** sources. User asked to do WebSearch classification in chunks of 100 tracks, surfacing candidates and confirming additions after each chunk before continuing. Current matrix only offers web-first ≤20 / CLI >20. Consider a third mode: "web-first batched (100/turn, confirm between batches)" — slower per track but gives the user precision + control over very long source playlists. Source: direct user feedback during run.
  - + confirmed 2026-05-18 (Trance scan: user explicitly said "Claude + WebSearch (per track)" + "in batches" for ~1594-track multi-source scan, after I defaulted to CLI without asking)

## Mistakes to Avoid

- **2026-05-18**: Defaulted to `scan-for` CLI for a 560-track source without offering the classifier choice via AskUserQuestion. SKILL.md step 4 says "the user can always override the default" — taking the default silently is a missed override point. Always offer both Claude+WebSearch and `scan-for` CLI in step 4, even when source >20 tracks. Source: user pushback "zou je mij niet moeten vragen of ik niet alsnog websearch wil doen?"

## Patterns That Work

- **2026-05-18**: For narrow-genre scans (e.g. Trance) via web-first batched mode, **pre-filter each batch using artist/title knowledge before WebSearching**. ~85-95% of tracks in a typical source are obviously not the target narrow genre (rock, pop, rap, etc.) and don't need web verification. Only WebSearch the plausible candidates (~5-15%) and the borderline electronic tracks. Saves time and context dramatically. Validated across 7 sources / 1594 tracks for Trance scan: ~30 WebSearches needed instead of 1594. Source: 2026-05-18 Trance multi-source scan.
- **2026-05-18**: For target playlists with a clearly narrow genre definition (Trance, Synthwave, K-pop, Instrumental Metal), the ≥80% confidence threshold is conservative-correct. Borderline electronic tracks (progressive house, big room, melodic dubstep, future garage, viking-trance fusion) consistently fall in the 40-60% range — should be skipped, not added. Source: 2026-05-18 Trance scan rejected Tiësto-Drifting (Future Garage), Avicii-Levels (Prog House), Alfons-Meet Her (Hard Dance cover), Age Of Love CDW Remix (Techno), Eihwar (Pagan/Folk).

## Domain Knowledge

- **2026-05-18**: When a Spotify playlist is shown in Development Mode (Spotify API returns no track URIs), `list-tracks` errors with "No readable tracks returned". Always retry with the CSV path under `exportify-exports/` (e.g. `exportify-exports/Random_sht.csv`). The skill should detect dev-mode error and auto-suggest the CSV fallback rather than failing.

---

## Maintenance

- **Sweep**: every ~30 days, drop entries older than 30 days that haven't been confirmed.
- **Promote**: 3+ confirmations → move to `learnings.md`, clear from this file.
- **Demote**: a contradiction in here → mark the `learnings.md` entry "⚠️ contradicted YYYY-MM-DD".
