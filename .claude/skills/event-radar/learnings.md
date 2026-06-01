# Learnings — event-radar

Dated, atomic insights captured from real runs. Promote candidates from `learning-candidates.md` here after 3+ run confirmations or explicit user confirmation. Consolidate at ~80-100 entries.

## Patterns That Work

- 2026-06-01: **Scan all playlists, not just genre-specific.** Liked Songs (4838 tracks) revealed Iron Maiden (154), Papa Roach (96), Linkin Park (73) — top-tier favs that were not in the top 15 of any genre playlist. Always scan Favorieten + Liked Songs + theme playlists alongside genre playlists.
- 2026-06-01: **Five parallel agents = sweet spot for breadth.** Metal/Rock + Electronic + Rap + Indie/Alt/Pop/Jazz + Supplementary-missing-favs. Discovery + EDM-genres run in a later round once the main list is back.
- 2026-06-01: **AskUserQuestion for blocked dates before any research.** Filtering after research wastes agent cycles.
- 2026-06-01: **Cap agent report length at ~500-700 words.** Forces prioritization and makes consolidation manageable.

## Mistakes to Avoid

- 2026-06-01: **Don't trust aggregator sites for ticket URLs.** Songkick / aesplora.com / musicfestivalwizard are often speculative or outdated. Always use the official venue / artist page for the link. Aggregators are fine for discovery, bad for "buy a ticket".
- 2026-06-01: **Don't include multi-day festivals that overlap any blocked day.** Even if day 1 is free, the user may not want to be there. Default = exclude unless single-day tickets exist and user opts in.
- 2026-06-01: **Don't assume Düsseldorf/Brussel are inside 100 km of Houten.** Both are ~150 km. Common mistake when the agent sees "close to NL".
- 2026-06-01: **Don't recommend dead-or-inactive artists without flagging.** Caro Emerald is inactive in 2026, no tour. Skip silently or flag explicitly — don't mention without context.

## Domain Knowledge

- 2026-06-01: **Eminem 2026 fake-tour posters** circulating on socials are AI-generated. Cross-referenced with ad-hoc-news.de + absence of Live Nation / eminem.com confirmation. Worth keeping in `research_caveats.fake_news` permanently.
- 2026-06-01: **Mysteryland 2026 = cancelled** (festival on break, returns 2027 with new concept). Save in `research_caveats.cancelled_events`.
- 2026-06-01: **Landjuweel = LATE JULY (23-26 jul 2026)**, not late August — common confusion since Ruigoord runs multiple summer events. Verify against ruigoord.nl every year.
- 2026-06-01: **ADE (Amsterdam Dance Event, October) lineup drop ≈ late August.** Most NL/BE House/Techno/DnB autumn club dates only announce post-ADE. Advise user to re-run skill in early September for the most complete autumn picture.
- 2026-06-01: **Qlimax ended permanently in 2024.** Reverze is February-only (2027 = next). Stop suggesting these as future hardstyle options.
- 2026-06-01: **Wacken Open Air (Wacken, DE) is at the 470 km edge** of the festival radius. Include but flag the travel.

## Open Questions

- Should the skill auto-detect "festival-named playlists" (like `Landjuweel '26`) as STRONG signals that the user is going to that festival? Currently a manual heuristic — formalize as a rule?
- When the user has bought tickets, should the skill **omit** the event from recommendations or **flag it** as "you're going!" for context? Currently leaning toward flag-with-emoji for context.
- Should the skill ever override `confidence_floor: confirmed_only` for top-tier favs (e.g., if Metallica announces a rumored NL date, include it with caveat even when confidence is low)?
- How aggressive should the `do_not_recommend_artists` auto-detection be? Right now manual list only.

## Consolidated Principles

(Promoted after 3+ confirmations or explicit user agreement)

- **Always read `event-radar.config.json` first.** It holds the user's authoritative defaults (home city, radii, language, preferences). The seed reference files (venue-list.md, distance-table.md) are fallbacks only.
- **Always write back to the config** after a successful run. Distance cache, new venues discovered, fake-news / cancelled / skip-NL caveats — all go into config so the next run is faster and smarter.
- **Filename = creation date.** Format `YYYY-MM-DD-<list-type>.md`. Different days = different snapshots, never overwrites.
- **Metadata block is mandatory** in every output file: generation date + search period + blocked dates + location/radii.
