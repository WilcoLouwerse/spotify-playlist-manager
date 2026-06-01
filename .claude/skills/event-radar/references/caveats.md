# Known caveats — fake news, cancellations, skip-NL artists

This file accumulates findings across runs so future runs don't re-research them. Update on every run when something is verified.

## Fake / unreliable

- **Eminem 2026 World Tour** — Viral German posters (Berlin / Munich / Hamburg) circulating on socials are **AI-generated fakes**. Confirmed by ad-hoc-news.de and the absence of any official announcement on eminem.com or Live Nation. Do **not** trust aggregator listings claiming Eminem 2026 dates.
- **aesplora.com** — aggregator that publishes speculative / unverified dates. Cross-check before trusting. (Example: Rammstein Amsterdam Aug 25 2026 listed only by aesplora, not by Rammstein's official channels.)

## Cancelled / on break

- **Mysteryland 2026** — cancelled; festival on break, planned return 2027 with new concept.
- **Qlimax** — ended permanently in 2024.
- **Reverze 2026** — already happened (Feb 27–28); next edition Feb 2027.

## Skip-NL artists (confirmed no NL/BE date in 2026)

These artists toured Europe in 2026 but skipped NL/BE. Don't waste agent time on them unless re-verifying.

- **Metallica** (M72 European leg) — Frankfurt + Berlin + Hamburg + London; no NL. Tour ends 5 jul.
- **System Of A Down** — Berlin (8 jul) + Düsseldorf (10 jul); no NL.
- **Red Hot Chili Peppers** — Berlin (15 jul) + Munich (18 jul); no NL.
- **Avenged Sevenfold** — North America only with Good Charlotte; no Europe.
- **Pierce The Veil** — Aggregator sites mention "Amsterdam 2026" but Songkick official calendar shows no 2026 European dates. Unverified.
- **Bullet For My Valentine + Trivium co-headline** — Ended May 2025 in NA; no 2026 EU leg.
- **Slipknot** — Wacken Aug 2026 only; no NL standalone (Dec 2025 Ziggo Dome was last NL).
- **Polyphia** — no 2026 tour dates anywhere per Songkick.
- **Muse, Lana Del Rey, Måneskin, AURORA, alt-J, Norah Jones** — no NL/BE 2026 dates verified.
- **Caro Emerald** — appears inactive in 2026.
- **Woodkid** — not touring 2026.
- **Andreas Vollenweider** — only Switzerland dates.
- **BLACKPINK / (G)I-DLE / K/DA** — no NL dates; K-pop rarely routes through NL outside arena tours.

## Border / edge cases

- **Düsseldorf** — common assumption is "close to NL", but actually ~150 km from Houten, **outside the 100 km concert radius**. Treat as festival-only.
- **Brussel** — also ~150 km from Houten, **outside concert radius**. Antwerpen (~85–140km) is the BE concert edge.
- **Antwerpen** — distance varies by route (85–140km). Treat as **concert-eligible** since user explicitly includes it.
- **Frauenfeld (CH)** — ~650 km, **outside 500 km festival radius**. Skip.
- **Splash! Festival (Ferropolis, DE)** — ~600 km, **outside 500 km festival radius**. Skip even if lineup matches.

## Recurring re-check items

These are time-sensitive and need re-checking on every run:

- **ADE (Amsterdam Dance Event, October)** lineup drops late August. Many House/Techno/DnB NL club dates for autumn only announce post-ADE.
- **Q-dance autumn calendar** (X-Qlusive Holland, Project Hardcore, etc.) often only publishes in summer.
- **Imagine Dragons LOOM Tour NL** — flagged but unverified; check Johan Cruijff ArenA calendar.
- **Rammstein 2026 Amsterdam** — only aesplora.com listed; not on official channels. Re-verify.

## Lessons learned

- **Always prefer official venue/artist source over aggregators** for the final URL. Aggregators are fine for discovery but bad for "buy a ticket".
- **Wacken (470 km) is on the edge** of the 500 km festival radius — fine to include but flag the travel.
- **Multi-day festivals overlapping any blocked day** must be excluded unless single-day tickets exist for non-blocked days. Don't quietly include a 3-day festival because day 1 is free.
