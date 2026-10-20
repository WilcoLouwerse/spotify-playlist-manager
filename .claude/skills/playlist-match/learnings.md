# Learnings — playlist-match

Dated, atomic observations promoted from `learning-candidates.md` after they've been confirmed across 3+ analyses or have fixed a measured eval failure. Consolidate when this file passes ~80 entries: remove outdated lines, merge duplicates, extract cross-entry patterns, promote validated principles to `SKILL.md` guardrails.

See [writing-skills.md → Level 6](../../docs/writing-skills.md#level-6-self-improvement--skills-that-learn-from-experience) for the learnings-to-rules pipeline.

---

## Patterns That Work

*(empty — populate after first run)*

## Mistakes to Avoid

*(empty — populate after first run)*

## Domain Knowledge

- 2026-05-13: `playlists.json -> catch_all -> playlist` resolves to `Random sht`. This is the script-side safety net for `smart-add` / `bulk-playlist`. The skill must never include it in user-facing recommendations — promoted to guardrail in SKILL.md.
- 2026-05-13: `special_rules.Electronic Music` mandates that `Electronic Music` is recommended *alongside* any electronic subgenre (House, Techno, Trance, DnB, Dubstep / Bass, Hardstyle & Hardcore, Synthwave), not as a fallback. Promoted to guardrail.
- 2026-05-13: `playlist_manager.py` is dry-run by default; only `--execute` writes. The duplicate guard is always on and cannot be overridden. Promoted to guardrail (never run `--execute` without explicit confirmation).
- 2026-06-23: Voor deze user is `Ket420` (en in mindere mate `Funny meme`) een **persoonlijke vibe-bucket** voor energieke meme- / hardstyle- / hardcore-tracks, niet strikt de literale "stoned / psychedelic / spacey / mellow"-special_rule. Drie observaties over twee artiestencombo's bevestigden dit: Jerome Molnar & XEDOX - Sidequest → Funny meme, Jerome Molnar & XEDOX - Horse Power → Funny meme + Ket420, MCR-T & horsegiirL - My Barn My Rules (147 BPM gabber farm-meme banger) → Ket420. Praktijk: bij meme-leaning hardstyle/hardcore tracks **structureel óók `Ket420` overwegen** in de aanbeveling met lagere confidence (~50-60%), in plaats van strikt vasthouden aan de spacey/mellow-special_rule. De confirmation-stap moet de mismatch met de literale special_rule nog wel neutraal flaggen, maar zonder weerstand te bieden.
- 2026-09-04: Voor de "Meer over het nummer" follow-up hebben **band-quote-bronnen voorrang** boven interpretatie-aggregators. Zoekvolgorde: eerst `<artist> <song> interview meaning` / `<artist> <album> press release` / label- of artist-site / Belgische/genre-muziekbladen (FrontView-achtig) — pas als daar niets uit komt, terugvallen op Lyreka / SongMeanings / Genius-annotations, en die dan expliciet labelen als interpretatie in plaats van als feit. Triggered by Balthazar - Losers (2026-09-04): leunde eerst op één Lyreka-lezing (romantische partner, unpacked suitcase-metafoor), user pushte terug, diepere search vond de door-de-band-geciteerde kernregel "we are losers on the verge of something great" + album-thema *waiting/restlessness* (Sand = zand in de zandloper) + pandemie-productie-context (eerste keer drum samples / bass synths). Gepromoveerd na 1 observatie op expliciet user-verzoek — niet via de standaard 3-confirmations-drempel. Verwerkt in SKILL.md step 9 (bullet "Meer over het nummer").

## Open Questions

- Does `add` accept playlist *aliases* in the same way `smart-add` does? Spec says yes ("must match a key under `"playlists"` or an alias under `"aliases"`"), but we render canonical names in output — should we also accept user-typed aliases in step-2 of the F flow without normalizing?
- For the Spotify Developer-Mode CSV fallback in `bulk-playlist` / `review-playlist`, is there a useful analog for the per-track skill? Probably not — we're operating on one track at a time.
- 2026-10-20: Resolved — the CSV fallback only applies to source playlists owned by someone else (the items endpoint answers 403); a single-track add never needs it.

## Consolidated Principles

*(empty — populate after 3+ confirmations of a candidate)*
