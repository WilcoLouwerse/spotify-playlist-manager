# Learning candidates — playlist-match

Unverified observations from individual runs. The two-stage buffer that prevents single-run noise from polluting `learnings.md` (and from there, SKILL.md rules).

```
learning-candidates.md  ->  (3+ confirmations OR fixes a measured eval failure)  ->  learnings.md  ->  SKILL.md rules
       ↓ (no)
    discarded after 30 days
```

Each entry is dated. One insight per bullet. Include source: which song / which eval / which user message triggered the observation. If the same candidate recurs, **don't duplicate** — append a "+ confirmed YYYY-MM-DD (song)" line. Promote when the count hits 3.

---

## Patterns That Work

*(empty)*

## Mistakes to Avoid

*(empty)*

## Domain Knowledge

*(empty)*

## Open Questions

*(empty)*

---

## Maintenance

- **Sweep**: every ~30 days, drop entries older than 30 days that haven't been confirmed.
- **Promote**: when a single entry has 3+ "+ confirmed" lines, move it (minus the confirmations log) to the matching section of `learnings.md` and clear it from this file.
- **Demote**: if an entry in `learnings.md` is contradicted by a new observation here, leave the candidate, mark the `learnings.md` entry with "⚠️ contradicted YYYY-MM-DD — see candidates" and re-promote after re-validation.
