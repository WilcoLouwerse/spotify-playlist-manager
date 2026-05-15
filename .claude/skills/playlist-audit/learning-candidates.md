# Learning candidates — playlist-audit

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

- **2026-05-15**: Ambiguous short artist names (e.g. "ASM") risk a false-match against the wrong genre. ASM in this Techno playlist turned out to be the French hip-hop group "A State of Mind" on Chinese Man Records, not a techno producer. Always verify the *album/label* context (Chinese Man Records, sample sources like Black Moon) before assigning a genre — don't trust the artist-name-on-techno-playlist signal alone.

## Domain Knowledge

- **2026-05-15**: BENNETT's signature is "pop/classical source + techno mix" branding (Vois sur ton chemin, Lullaby, Mamma Mia, Silence). All four scored ≥75% as Techno because the production methodology (Peak Time Techno kick + bassline under the source vocal) is consistent. Treat any "<source> (Techno Mix) — BENNETT" as a likely fit for Techno even when the source material is non-electronic.
- **2026-05-15**: "Bass house" tracks (WILL K - Sun Is Dark, Picco - Hesitate, Zeds Dead - One Three Nine, Sean Paul - Get Busy/Odd Mob mix) score very low (~30%) against pure Techno because they belong to the *house* family, not techno — despite being high-energy electronic. Default-route these to House + Electronic Music, not Techno.
- **2026-05-15**: The 55%-band ("Melodic House & Techno", "Hypertechno", "Scouse House") are genuine crossover genres — they fit both House and Techno legitimately. Leaving them in Techno *and* adding to House is the cleanest treatment; removing them from Techno would be wrong.

## Open Questions

*(empty)*

---

## Maintenance

- **Sweep**: every ~30 days, drop entries older than 30 days that haven't been confirmed.
- **Promote**: 3+ confirmations → move to `learnings.md`, clear from this file.
- **Demote**: a contradiction in here → mark the `learnings.md` entry "⚠️ contradicted YYYY-MM-DD".
