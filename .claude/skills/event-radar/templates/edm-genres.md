# EDM genre-specifiek — pure genre-nights {{date_window_human}}

Pure subgenre-events (alleen DnB, alleen techno, alleen hardstyle, etc.) bij {{edm_venues_short}}. **Geen multi-genre festivals** — die staan in [{{year}}-favs.md]({{year}}-favs.md).

Geblokkeerde datums ({{blocked_ranges_short}}) al uitgefilterd.

## 🎯 Hype-rating legenda

Elk event start met een inschatting van hoe leuk je dit waarschijnlijk gaat vinden:

- 🔥 **95–100%** — lock-it-in, top-tier, drop-everything
- 🟢 **80–94%** — sterke match, hoge kans op enthousiasme
- 🟡 **65–79%** — solide match, de moeite waard
- 🟠 **50–64%** — stretch / interessante experimentele uitstap
- 🔵 **<50%** — niche wildcard, hit-or-miss

---

{{#each genre}}
## {{genre_name}}

{{#each event}}
- {{hype_glyph}} **{{hype_pct}}%** — **{{date}}** — [{{event_name}}]({{url}}) ({{lineup_short}}) — {{venue}}, {{city}} — *{{why_match}}*
{{/each}}

{{/each}}

---

## 🔔 Series om te volgen (recurring agendas om te bookmarken)

{{series_to_watch}}

## ⚠️ Key flags

{{key_flags}}
