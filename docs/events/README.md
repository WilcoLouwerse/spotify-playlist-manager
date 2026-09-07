# Events — concerten & festivals

Deze map bevat **gegenereerde event-aanbevelingen** voor de gebruiker, gebaseerd op Spotify-playlists, woonplaats en agenda-blokkades.

> **Inhoud is persoonlijk** — de daadwerkelijke `.md`-bestanden (lijsten + index) zijn **gitignored** omdat ze locatie, vakantiedata en muzieksmaak-derivaten bevatten. Alleen deze README staat in git.

---

## Waar is deze map voor?

Wanneer je de [`event-radar`](../../.claude/skills/event-radar/SKILL.md) skill aanroept, worden hier gedateerde markdown-bestanden weggeschreven met:

- **Hoofdlijst** (`<YYYY-MM-DD>-favs.md`) — concerten/festivals met artiesten die je al luistert
- **Discovery** (`<YYYY-MM-DD>-discovery.md`) — kleinere venues + adjacent-unknown artiesten
- **EDM-genres** (`<YYYY-MM-DD>-edm-genres.md`) — pure subgenre-nights (DnB/Techno/Hardstyle/etc.)
- **Tribute** (`<YYYY-MM-DD>-tribute.md`) — tribute-bands voor overleden/inactieve favs (optioneel, standaard uit)

Vraag je om een **genre- of format-gefilterde run**, dan schrijft de skill een extra bestand met een
beschrijvend suffix in plaats van de bovenstaande vaste namen — bijvoorbeeld
`2026-06-26-metal-festivals.md` (alleen metal-festivals, aug t/m dec). Zelfde metadata-blok en
hype-rating, alleen een smallere scope.

Het `<YYYY-MM-DD>`-prefix in de filename is de **generation date** — elke run produceert nieuwe gedateerde bestanden zodat oude runs blijven bestaan als historische snapshots.

Een **lokale `INDEX.md`** in deze map (gitignored) houdt een chronologische TOC bij van alle runs. Open die voor het overzicht.

## Hoe gebruik je de skill?

Roep aan via slash-command of natuurlijke taal:

```
/event-radar
```

of

> *"Welke concerten/festivals zou ik leuk vinden de komende maanden?"*
> *"Find me events for the rest of the year based on my taste."*
> *"Discovery-run voor herfst, alleen kleine venues."*

De skill leest [`event-radar.config.json`](../../event-radar.config.example.json) (sample in repo, jouw versie is gitignored) voor je defaults:

- Woonplaats + radii
- Voorkeuren (taal, venue-tier, confidence-floor, budget, travel-mode, etc.)
- Lievelings-genres + do-not-recommend artiesten
- Distance-cache (self-learned over tijd)
- Ticket-history (bought / attended / wishlist)
- Vaste jaarlijkse blokkades (kerst, verjaardag, etc.)

Voor parameters die niet in de config staan vraagt de skill via AskUserQuestion. Tijdvenster + ad-hoc blokkades worden altijd actief gevraagd, zodat agenda-wijzigingen meegenomen worden.

## Privacy & gitignore

`.gitignore` ignoret:
- `docs/events/*.md` (alle gegenereerde lijsten + de lokale INDEX)
- `!docs/events/README.md` (uitzondering: deze file)
- `event-radar.config.json` (jouw config met persoonlijke defaults)

Wat **wel** in git staat:
- Deze README
- [`event-radar.config.example.json`](../../event-radar.config.example.json) — schema-template, geen persoonlijke data
- De skill zelf in `.claude/skills/event-radar/`

## Skill-documentatie

| Bestand | Doel |
|---|---|
| [`.claude/skills/event-radar/SKILL.md`](../../.claude/skills/event-radar/SKILL.md) | Hoofdlogica, stappen, guardrails |
| [`.claude/skills/event-radar/references/config-schema.md`](../../.claude/skills/event-radar/references/config-schema.md) | Schema voor `event-radar.config.json` |
| [`.claude/skills/event-radar/references/agent-prompts.md`](../../.claude/skills/event-radar/references/agent-prompts.md) | Templates voor research-agents |
| [`.claude/skills/event-radar/references/venue-list.md`](../../.claude/skills/event-radar/references/venue-list.md) | Seed venue-catalog (config takes precedence) |
| [`.claude/skills/event-radar/references/distance-table.md`](../../.claude/skills/event-radar/references/distance-table.md) | Seed distance-table (config takes precedence) |
| [`.claude/skills/event-radar/references/caveats.md`](../../.claude/skills/event-radar/references/caveats.md) | Seed van fake-news / cancelled / skip-NL artiesten |
| [`.claude/skills/event-radar/templates/`](../../.claude/skills/event-radar/templates/) | Output-scaffolds (`favs.md`, `discovery.md`, `edm-genres.md`, `tribute.md`, `index.md`) |
| [`.claude/skills/event-radar/examples/run-2026-06.md`](../../.claude/skills/event-radar/examples/run-2026-06.md) | Voorbeeld van een volledige run incl. agent-dispatch |
| [`.claude/skills/event-radar/learning-candidates.md`](../../.claude/skills/event-radar/learning-candidates.md) | Dated observaties die nog niet gepromoveerd zijn |
| [`.claude/skills/event-radar/learnings.md`](../../.claude/skills/event-radar/learnings.md) | Self-improvement pipeline (L6) |
| [`.claude/skills/event-radar/evals/evals.json`](../../.claude/skills/event-radar/evals/evals.json) | Eval-scenarios + trigger-tests |

## Algemene caveats

> De **canonieke** en meest actuele lijst staat in
> [`references/caveats.md`](../../.claude/skills/event-radar/references/caveats.md) plus
> `research_caveats` in je config — die worden elke run bijgewerkt. Onderstaande punten zijn een
> samenvatting, laatst geverifieerd op **2026-09-07**.

- **Fake tour-news**: posters op socials zijn vaak AI-gegenereerd. Verifieer altijd op de officiële venue- of artiestenpagina.
- **Aggregator vs primary source**: Songkick / aesplora.com / musicfestivalwizard zijn vaak speculatief. Officiële venue-agendas zijn authoritative.
- **ADE drop (oktober)**: veel NL House/Techno/DnB datums voor herfst worden pas in **eind augustus** aangekondigd. Re-run de skill in september voor de meest complete autumn lijst. *(Per 2026-09-07: deze re-run staat open — de nieuwste lijsten dateren van juni 2026.)*
- **Mysteryland 2026**: afgeblazen (pauze, terug 2027).
- **Qlimax**: definitief gestopt sinds 2024.

## Maturity

De skill staat per laatste meting op **M7** (zie [skill-level-overview.html](../../.claude/skills/skill-level-overview.html)) — boven de **L6**-target. Die meting is deels structureel gedetecteerd; de baseline-delta over herhaalde runs is nog niet gemeten.
