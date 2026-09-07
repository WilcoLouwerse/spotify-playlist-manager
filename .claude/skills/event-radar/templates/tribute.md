# Tribute & legacy — {{date_window_human}}

Tribute-bands en legacy-acts voor favs die overleden, gestopt of inactief zijn. Gefilterd op je geblokkeerde datums ({{blocked_ranges_short}}).

**Bron**: scan van alle {{n_playlists}} playlists → {{n_inactive_favs}} inactieve/overleden favs → onderzoek door de tribute-agent.

## 🎯 Hype-rating legenda

Elk event start met een inschatting van hoe leuk je dit waarschijnlijk gaat vinden. Voor tributes weegt **kwaliteit van de act** zwaarder dan adjacency — een middelmatige tribute van een top-fav is minder waard dan een uitstekende van een mid-fav:

- 🔥 **95–100%** — officieel geëndorseerd of met oud-bandleden; zo dicht bij het origineel als het wordt
- 🟢 **80–94%** — gevestigde tribute met sterke live-reputatie
- 🟡 **65–79%** — solide act, goede reviews, de moeite waard
- 🟠 **50–64%** — lokale/kleinere act, wisselende reviews
- 🔵 **<50%** — niche of onbekende kwaliteit, hit-or-miss

---

## ⭐ Top-picks (beste act-kwaliteit voor je sterkste inactieve favs)

| # | Datum | Tribute-act | Voor wie | Waarom |
|---|---|---|---|---|
{{top_picks_table}}

---

## 📅 Per maand

{{#each month}}
### {{month_name}} {{year}}

{{#each event}}
- {{hype_glyph}} **{{hype_pct}}%** — **{{date}}** {{star_if_top}} — [{{tribute_act}}]({{url}}) → tribute aan **{{original_artist}}** ({{detail}}) — {{venue}}, {{city}} (~{{distance}}km) {{endorsement_marker}} {{caveat_marker}}
{{/each}}

{{/each}}

---

## 🎸 Inactieve favs zonder tribute-optie in dit venster

Voor deze favs is niets gevonden binnen je radius en datumvenster — ter info, zodat je weet dat er gezocht is:

{{no_tribute_found_list}}

---

## ❌ Geblokkeerd door je agenda (ter info)

{{blocked_events_list}}

## ⚠️ Belangrijk om te weten

Tribute-scene-specifieke caveats: naamsverwarring tussen concurrerende tributes van dezelfde band, acts die zonder aankondiging van line-up wisselen, en "officieel" dat niet altijd door de rechthebbenden bevestigd is. Verifieer altijd op de venue-agenda.

{{caveats_section}}

## 🛒 Drie tickets om eerst te kopen

{{top_three_to_buy}}
