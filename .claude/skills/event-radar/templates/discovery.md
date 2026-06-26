# Discovery — kleinere venues + onbekende artiesten {{date_window_human}}

Concerten bij **kleinere venues** ({{small_venues_short}}) met artiesten die **je nog niet kent**, maar die in de adjacency-zone van je smaak vallen.

Geblokkeerde datums ({{blocked_ranges_short}}) al uitgefilterd. Elke entry uitgelegd: aan welke bekende fav grenst dit?

## 🎯 Hype-rating legenda

Elk event start met een inschatting van hoe leuk je dit waarschijnlijk gaat vinden (adjacency aan favs + venue/format fit + scene-buzz):

- 🔥 **95–100%** — lock-it-in, top-tier, drop-everything
- 🟢 **80–94%** — sterke match, hoge kans op enthousiasme
- 🟡 **65–79%** — solide match, de moeite waard
- 🟠 **50–64%** — stretch / interessante experimentele uitstap
- 🔵 **<50%** — niche wildcard, hit-or-miss

---

## 📅 Per maand

{{#each month}}
### {{month_name}} {{year}}

{{#each event}}
- {{hype_glyph}} **{{hype_pct}}%** — **{{date}}** — [{{artist}}]({{url}}) ({{genre_hint}}) — {{venue}}, {{city}}
  → *{{why_match}}*

{{/each}}

{{/each}}

---

## 📋 Browse zelf voor meer

Deze venues hebben veel meer waar je blij van wordt — agenda's vullen zich vaak pas later in het seizoen:

{{venue_agenda_links}}

## ⚠️ Caveats

{{caveats_section}}
