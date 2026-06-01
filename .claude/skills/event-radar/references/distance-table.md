# Distance table — SEED ONLY (Houten home base)

**⚠️ This file is a seed/fallback. The skill's authoritative distance data lives in [`event-radar.config.json`](../../../event-radar.config.json) under `distance_cache_km`.** Read the config first; only fall back to this seed when the config is missing or has no entry for the city in question.

This table assumes a Houten-based user. **If the config's `user.home_city` differs, this table is no longer authoritative**.

**Self-learning**: when the skill resolves a distance via WebSearch or driving-time API, it MUST write the result back to the config's `distance_cache_km` keyed by `"City, Country"`. Future runs read from cache → no token cost.

---

## Default radii (from config)

The config's `user.default_concert_radius_km` and `user.default_festival_radius_km` drive the filtering. For Houten, defaults are:

- **Concerts**: 100 km
- **Festivals**: 500 km

Users can override on a per-run basis via AskUserQuestion.

## NL — inside 100 km concert radius (from Houten)

| City | Distance (km) |
|---|---|
| Utrecht | 10 |
| Amsterdam | 35 |
| Hilversum | 30 |
| Amersfoort | 25 |
| Arnhem | 55 |
| Nijmegen | 50 |
| Tilburg | 50 |
| Den Bosch | 30 |
| Eindhoven | 70 |
| Rotterdam | 50 |
| Den Haag | 60 |
| Haarlem | 50 |
| Leiden | 55 |
| Delft | 55 |
| Almere | 40 |
| Lelystad | 60 |
| Biddinghuizen | 65 |
| Hilvarenbeek | 65 |
| Ysselsteyn | 110 — **outside, but commonly used festival site (Jera On Air)** |
| Eersel | 95 |
| Leeuwarden | 165 — outside |
| Groningen | 195 — outside |

## BE — concert radius edge & festival range (from Houten)

| City | Distance (km) |
|---|---|
| Antwerpen | 85–140 (depending on route) — **borderline concert OK** |
| Hasselt | 155 — festival only |
| Brussel | 150 — festival only |
| Gent | 180 — festival only |
| Kortrijk | 220 — festival only |
| Werchter | 140 — festival only |
| Boom | 140 — festival only |
| Dessel | 150 — festival only |
| Geel | 110 — festival only |
| Lommel | 80 — **borderline concert** |

## DE — festival range (from Houten)

| City | Distance (km) |
|---|---|
| Düsseldorf | 150 — outside concert radius (despite being "close") |
| Köln | 225 — festival only |
| Frankfurt | 350 — festival only |
| Hamburg | 400 — festival only, edge |
| Berlin | 600 — **outside 500 km festival radius** |
| Mannheim (Time Warp) | 400 — festival only |
| Wacken | 470 — at edge of 500 km |
| Gräfenhainichen (Splash!) | 600 — **outside** |

## FR — festival range (from Houten)

| City | Distance (km) |
|---|---|
| Paris | 450 — festival only |
| Lille | 280 — festival only |
| Marseille | 1000 — outside |
| Clisson (Hellfest) | 700 — outside |

## CH / AT / CZ — outside (from Houten)

| City | Distance (km) |
|---|---|
| Zürich | 700 — outside |
| Vienna | 1000 — outside |
| Prague (Let It Roll) | 900 — outside |
| Budapest (Sziget) | 1300 — outside |

## UK — outside (from Houten)

The English Channel makes most UK festivals impractical despite "as the crow flies" distances being under 500 km. London is ~360 km but adds ferry/Eurotunnel time. **Skip UK by default** unless user explicitly opts in.

---

## How to use when home city is NOT Houten

1. **Don't trust this table.** Distances are anchored to Houten.
2. **Look up distance**: use WebSearch ("driving distance from {home_city} to {target_city}") or Google Maps. Round to nearest 5 km.
3. **Write back to config**: append `"{Target City}, {Country}": <km>` to `distance_cache_km` so future runs hit the cache.
4. **Apply radii**: compare against `user.default_concert_radius_km` / `user.default_festival_radius_km` from config.

## How to use when changing radii

If the user passes a different radius for one run (e.g. "but festivals can go to 700 km this time"):
- **Don't overwrite the config defaults** unless the user says "save this as my new default".
- Use the one-shot radius for filtering this run only.
- All cached distances remain valid (they're absolute km, not radii).
