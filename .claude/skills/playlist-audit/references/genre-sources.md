# Genre Sources for Playlist Audit

How to determine whether a specific track fits a specific playlist's genre or theme. This is the same methodology as [`/playlist-match`](../../playlist-match/references/genre-sources.md) — consult that file for the complete reference. This page is a quick summary scoped to the audit context.

---

## Primary approach: Claude + live web lookup (web-first mode)

Use **WebSearch** + **WebFetch** against 2–3 independent sources per track before publishing a confidence score. Never publish a score from training-data recall when web tools are available.

| Source | What to look up | Strength |
|--------|----------------|----------|
| AllMusic | `"<artist> <track> site:allmusic.com"` | Editorial genre tagging, often track-level |
| RateYourMusic | `"<artist> <track> rateyourmusic"` | Crowdsourced, granular subgenres |
| Wikipedia | `"<artist> <track> wikipedia"` | Genre listed in infobox; fall back to album page |
| Discogs | `"<artist> <track> discogs"` | Release-level genre + style tags |
| Last.fm | WebFetch `https://www.last.fm/music/<artist>/_/<track>` | User tags (high recall, lower precision) |

**Rules of thumb:**
- 2+ strong sources agree → confidence ≥ 80%
- Only Last.fm tags agree → confidence ≤ 65%
- Sources conflict → list both; lower the headline number; note conflict in reason
- All lookups fail → mark track as "geen data"; **do not fabricate a score**

---

## Scoring against the target playlist

After sourcing genres from the web, compare them to what the playlist expects:

1. **Check `playlists.json → categories`** — is this playlist under `genre`, `mood`, or `theme`?
2. **Genre playlists** (House, Techno, Drum & Bass, …): match the sourced genre tags against the playlist name. Use domain knowledge for subgenre relationships (progressive house ≈ house, hardstyle ≈ hardstyle & hardcore, etc.).
3. **Mood playlists** (Happy tunes, Sad tunes, Rustig / 'anders'): check lyrical sentiment and musical mood from web sources; BPM and energy are secondary signals.
4. **Theme playlists** (Funny meme, Ket420, Hooyah): apply the playlist's `special_rules` literally. These are contextual; genre match alone is insufficient.
5. **Electronic Music umbrella**: if sourced genres include any electronic subgenre, the track fits `Electronic Music` in addition to its specific subgenre.

---

## Confidence bands (same as `/playlist-match`)

| Band | Use when |
|------|----------|
| 90–100% | Multiple strong sources agree the track is squarely in this playlist's genre |
| 75–89% | Strong sources mostly agree; one minor disagreement |
| 60–74% | Mixed signals; some stylistic overlap but not a strong fit |
| 40–59% | Plausible but contested; likely a secondary genre |
| < 40% | Weak or no match — recommend for removal candidates |

---

## Training-data recall (last resort only)

Use only when all web lookups fail (404s, no entries, or sharp unresolved conflict). Cap confidence at 70% for well-known tracks, 60% otherwise. Label the reason with `bron: Claude (interne kennis)` so the user understands the limitation. Never use as the default path.
