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
- **2026-05-16**: When the empty-CSV branch is hit and `.tracks_log.json` has URIs for the playlist, the workflow "resolve URIs via `sp.track()` → synthetic exportify-style CSV → audit-playlist --csv" works cleanly. Worth surfacing as a documented fallback in SKILL.md step 3 (in addition to "ask for CSV path").
  - superseded 2026-10-20: `list-tracks` / `audit-playlist` read playlists in `playlists.json` live, so the empty-CSV branch no longer arises for them.
- **2026-05-16**: Heavy `sp.track()` lookups (107 + 96 = 203 single-track calls in one run) can exhaust the Spotify app's daily quota and trigger a ~22h Retry-After. Both `audit-playlist` (label fetches) and the `remove` CLI's pretty-print `get_track()` were affected. Workarounds: (a) skip `get_track()` in the audit CSV-build path when the resolved URI is enough, (b) make `remove` graceful when `get_track()` fails (continue with URI-only label), (c) a `remove --batch` that takes a list of URIs and skips label lookups.
  - resolved 2026-10-20: (b) `get_track()` now continues with a URI-only label on lookup failure; (c) shipped as `batch-remove`.

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
