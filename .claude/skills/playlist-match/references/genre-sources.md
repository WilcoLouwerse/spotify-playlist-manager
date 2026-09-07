# Genre Sources & Confidence

How to decide what genres a song is. The output goes into the **Genres** block of the analysis with a percentage and a one-line reason per genre.

**The default flow is Claude + live web lookup.** Use **WebSearch** and **WebFetch** to pull current data from the sources below. This is the most accurate and most up-to-date path — and the one always tried first. Training-data recall is **last resort only**.

---

## Sources, ranked (web-driven)

Cross-check across multiple independent sources before publishing a confidence percentage. For each, the mechanism is `WebSearch` (to find the right URL) followed by `WebFetch` (to read it).

| Source | Strength | Track-scoped? | How to look up |
|--------|----------|---------------|----------------|
| AllMusic | Editorial genre tagging, often track-level via the album page. | Album / track | WebSearch `"<artist> <track> site:allmusic.com"`, WebFetch the result. |
| RateYourMusic (RYM) | Crowdsourced but heavily moderated; granular subgenres. | Album / song | WebSearch `"<artist> <track> rateyourmusic"`, WebFetch the result. |
| Wikipedia | Track or album infobox usually lists genres explicitly. | Track / album | WebSearch `"<artist> <track> wikipedia"` (fall back to the album page if no track page exists), WebFetch the result. |
| Discogs | Release-level genre + style tags. | Release | WebSearch `"<artist> <track> discogs"`, WebFetch the release page. |
| Last.fm | User tags — high recall, low precision (treat as signal, not truth). | Track | WebFetch `https://www.last.fm/music/<artist>/_/<track>` (URL-encode names) or use WebSearch to find the right URL. |
| Label or artist site | Sometimes the label's own categorisation, especially for niche electronic. | Track / release | WebSearch the artist + release on the label domain, WebFetch the page. |
| Spotify's own genres | Artist-level only; weak signal. | Artist | WebFetch `https://open.spotify.com/artist/<id>` if an artist URL is in hand. |
| **Claude AI (internal knowledge)** | **Last resort.** Used only when every web lookup above fails and the user has picked "Inschatten zonder internet (Claude + OpenAI)" in the uncertainty fork. Combined with OpenAI as a second training-data source when available; falls back to Claude-only with an explicit reason if OpenAI is down. | Track if Claude knows it, else artist | No tool — recall from training data. Label `bron: Claude (interne kennis)` or `bron: Claude + OpenAI (interne kennis)` per row depending on whether OpenAI succeeded. |
| **OpenAI (via `analyze-only`)** | **Second-opinion-only.** Used only alongside Claude in the offline path above, via the read-only `analyze-only` command — never `smart-add`, never in the default web flow. Provides a second training-data classification to cross-check Claude's genres and playlists. Falls back gracefully on any OpenAI error. | Track-level | `Bash` → `.venv/bin/python playlist_manager.py analyze-only "<spotify-url-or-id>"`. Parse the printed genres + playlist matches from stdout. Check for OpenAI error strings listed in `templates/uncertainty.md` and fall back to Claude-only if any are present. |

**Rules of thumb:**
- **Always start with web lookup.** Run WebSearch / WebFetch against at least 2 strong sources (AllMusic, RYM, Wikipedia, Discogs) before publishing genres. Never publish a genre based on training recall when web tools are available.
- If 2+ "strong" web sources agree on a genre → confidence ≥ 80%.
- If only Last.fm user tags agree → confidence ≤ 65% and call out the source weakness in the reason.
- If sources contradict (e.g. AllMusic says "indie rock", RYM crowd says "post-punk") → list both with the higher-confidence one first, lower the headline number, and add the conflict to the reason.
- If **all** web lookups fail (404s, no entries, or sharp unresolved conflict) → enter the uncertainty fork (`templates/uncertainty.md`). From that menu the user can broaden the lookup (artist-wide pages, weaker sources) — all of which still use WebFetch/WebSearch. The "Laat Claude inschatten zonder internet" option is the true last resort: training-only, capped at 70%, labeled `bron: Claude (interne kennis)` with `betrouwbaarheid: laag` (or `middel` only for well-known tracks). Never `smart-add` (OpenAI).

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
