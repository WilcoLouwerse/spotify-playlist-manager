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
- **2026-05-15**: Web-first-in-batches as an option for **>20 track** sources. User asked to do WebSearch classification in chunks of 100 tracks, surfacing candidates and confirming additions after each chunk before continuing. Current matrix only offers web-first ≤20 / CLI >20. Consider a third mode: "web-first batched (100/turn, confirm between batches)" — slower per track but gives the user precision + control over very long source playlists. Source: direct user feedback during run.

---

## Maintenance

- **Sweep**: every ~30 days, drop entries older than 30 days that haven't been confirmed.
- **Promote**: 3+ confirmations → move to `learnings.md`, clear from this file.
- **Demote**: a contradiction in here → mark the `learnings.md` entry "⚠️ contradicted YYYY-MM-DD".
