# Favorites — concerten & festivals {{date_window_human}}

Concerten en festivals met artiesten die je al luistert. Gefilterd op je geblokkeerde datums ({{blocked_ranges_short}}).

**Bron**: scan van alle {{n_playlists}} playlists + onderzoek door {{n_agents}} specialist-agents.

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
- **{{date}}** {{star_if_top}} — [{{artist_or_festival}}]({{url}}) ({{detail}}) — {{venue}}, {{city}} (~{{distance}}km) {{caveat_marker}}
{{/each}}

{{/each}}

---

## ❌ Geblokkeerd door je agenda (ter info)

{{blocked_events_list}}

## ⚠️ Belangrijk om te weten

{{caveats_section}}

## 🛒 Drie tickets om eerst te kopen

{{top_three_to_buy}}
