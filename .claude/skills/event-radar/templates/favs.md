# Favorites — concerten & festivals {{date_window_human}}

Concerten en festivals met artiesten die je al luistert. Gefilterd op je geblokkeerde datums ({{blocked_ranges_short}}).

**Bron**: scan van alle {{n_playlists}} playlists + onderzoek door {{n_agents}} specialist-agents.

## 🎯 Hype-rating legenda

Elk event start met een inschatting van hoe leuk je dit waarschijnlijk gaat vinden (adjacency aan favs + venue/format fit + scene-buzz + listen-frequency):

- 🔥 **95–100%** — lock-it-in, top-tier, drop-everything
- 🟢 **80–94%** — sterke match, hoge kans op enthousiasme
- 🟡 **65–79%** — solide match, de moeite waard
- 🟠 **50–64%** — stretch / interessante experimentele uitstap
- 🔵 **<50%** — niche wildcard, hit-or-miss

---

## ⭐ Top-picks (must-see, hoogste match-dichtheid)

| # | Datum | Event | Waarom |
|---|---|---|---|
{{top_picks_table}}

---

## 📅 Per maand

{{#each month}}
### {{month_name}} {{year}}

{{#each event}}
- {{hype_glyph}} **{{hype_pct}}%** — **{{date}}** {{star_if_top}} — [{{artist_or_festival}}]({{url}}) ({{detail}}) — {{venue}}, {{city}} (~{{distance}}km) {{caveat_marker}}
{{/each}}

{{/each}}

---

## ❌ Geblokkeerd door je agenda (ter info)

{{blocked_events_list}}

## ⚠️ Belangrijk om te weten

{{caveats_section}}

## 🛒 Drie tickets om eerst te kopen

{{top_three_to_buy}}
