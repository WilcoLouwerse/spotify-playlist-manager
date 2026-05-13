# Genre Sources & Confidence

How to decide what genres a song is. The output goes into the **Genres** block of the analysis with a percentage and a one-line reason per genre.

---

## Sources, ranked

Use multiple independent sources per song. Cross-check before publishing a confidence percentage.

| Source | Strength | Track-scoped? |
|--------|----------|---------------|
| AllMusic | Editorial genre tagging, often track-level via the album page. | Album / track |
| RateYourMusic (RYM) | Crowdsourced but heavily moderated; granular subgenres. | Album / song |
| Wikipedia | Track or album infobox usually lists genres explicitly. | Track / album |
| Discogs | Release-level genre + style tags. | Release |
| Last.fm | User tags — high recall, low precision (treat as signal, not truth). | Track |
| Label or artist site | Sometimes the label's own categorisation, especially for niche electronic. | Track / release |
| Spotify's own genres | Artist-level only; weak signal. | Artist |
| **Claude AI (internal knowledge)** | **Source of last resort.** Use only when no external source is reachable or all sources contradict, **and** the user has picked "Laat Claude inschatten" in the uncertainty fork. Cap confidence at 70%. Never OpenAI / `smart-add`. | Track if Claude knows it, else artist |

**Rules of thumb:**
- If 2+ "strong" sources (AllMusic, RYM, Wikipedia, Discogs) agree on a genre → confidence ≥ 80%.
- If only Last.fm user tags agree → confidence ≤ 65% and call out the source weakness in the reason.
- If sources contradict (e.g. AllMusic says "indie rock", RYM crowd says "post-punk") → list both with the higher-confidence one first, lower the headline number, and add the conflict to the reason.
- If **all** external sources fail (no entries, or sharp unresolved conflict) → enter the uncertainty fork (`templates/uncertainty.md`). When the user picks "Laat Claude inschatten", Claude AI's own training knowledge is the named fallback source — never `smart-add` (OpenAI). Cap individual genre confidences at 70% and label `bron: Claude (interne kennis)` with `betrouwbaarheid: laag` (or `middel` only for well-known tracks).

---

## Track-level vs. artist-level

A genre that fits the artist overall doesn't have to fit the specific track. Sleep Token's catalogue spans alt-metal, post-rock, R&B, and pop; "The Summoning" leans djent + prog, "Granite" leans alt-R&B. Always scope sources to the song first; back off to the album, then the artist, only if track-level info isn't available — and **say so** in the reason ("track-level info unavailable, scored from album").

---

## Conflict thresholds and the uncertainty fork

| Situation | What to do |
|-----------|------------|
| All sources align | Single-genre confidence ≥ 85%. |
| Two strong genres compete | Two entries in the list with confidences distributed between them (often 70%-ish each). |
| Sources conflict sharply, no clear winner | Don't fabricate — print the uncertainty lead-in and call **AskUserQuestion** with the four options per `templates/uncertainty.md`. |
| Song or artist not discoverable | Say so plainly. Don't invent. Offer the uncertainty flow only if the *song* is identified but its *genre* is the unknown part. |

---

## Confidence bands

Use these bands so percentages are consistent run-to-run:

| Band | Use when |
|------|----------|
| 90-100% | Multiple strong sources agree, including the artist's own labelling. |
| 75-89% | Strong sources mostly agree; one minor disagreement. |
| 60-74% | Mixed signals; mostly Last.fm tags; track-level info partial. |
| 40-59% | Plausible but contested; usually a secondary genre. |
| ≤ 39% | Don't publish — drop the genre or surface it via the uncertainty menu. |

Round to the nearest integer percent. Don't use decimals.

---

## Reason line — what to write

Each genre's reason is one short clause (≤ 12 words). It should justify the percentage. Pick from:

- production detail (e.g. "saw-lead drops, 174 BPM half-time DnB structure")
- instrumentation (e.g. "djent guitars + clean vocal hooks")
- consensus note (e.g. "AllMusic + Wikipedia agree; RYM users add post-punk")
- track-scope note (e.g. "track-level info partial, scored from album")
- conflict flag (e.g. "Last.fm tags lean trance, AllMusic says progressive house")

Avoid: artist-only justifications ("the artist usually makes X"), genre name repetition ("it sounds like metal because it's metal"), vague vibe statements.
