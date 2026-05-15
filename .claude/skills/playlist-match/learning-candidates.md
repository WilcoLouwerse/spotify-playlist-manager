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

- 2026-05-15 — Een meme-y / absurde **tracktitel** is op zichzelf niet genoeg voor `Funny meme`. Bij Sickmode - WHAAAT?? (YES!!! THE KICK IS ANVIL FROM M1N3CR4FT) scoorde ik Funny meme 70% op basis van de titel + anvil-kick gimmick, maar de user koos alleen Hardstyle & Hardcore + Electronic Music. Hypothese: `Funny meme` is bedoeld voor tracks waar het *muzikale materiaal* (lyrics, melodie, vocal hook) de grap is — niet voor reguliere genretracks met een grappige naam. Bij twijfel: scoor lager (≤50%) of laat weg.

## Open Questions

*(empty)*

---

## Maintenance

- **Sweep**: every ~30 days, drop entries older than 30 days that haven't been confirmed.
- **Promote**: when a single entry has 3+ "+ confirmed" lines, move it (minus the confirmations log) to the matching section of `learnings.md` and clear it from this file.
- **Demote**: if an entry in `learnings.md` is contradicted by a new observation here, leave the candidate, mark the `learnings.md` entry with "⚠️ contradicted YYYY-MM-DD — see candidates" and re-promote after re-validation.
