# Follow-up template (AskUserQuestion-driven)

Replaces the old A-F letter menu. There are two places this fires:

1. **Right after the full analysis** (end of step 8 in `SKILL.md`).
2. **Right after answering a follow-up** (end of step 9), so the user can chain another action or stop.

In both cases, call **AskUserQuestion** with the menu below. There is **no chat-printed footer**, no letter menu, no "*Wil je een andere optie proberen?*" line — those were artifacts of the old letter mechanic.

---

## After the full analysis (first call)

`AskUserQuestion` allows 4 button options + an automatic "Other" free-text field. Use the four most common actions as buttons; uncommon ones (album + cover, streaming links) go via free-text. The skill must accept both — see "Routing the answer" below.

```
question: "Wat wil je hierna doen?"
header:   "Vervolg"
multiSelect: false
options:
  - label:       "Voeg toe aan playlists"
    description: "Voeg dit nummer toe aan één of meer van de aanbevolen playlists — je playlist-keuze daarna bevestigt meteen de write."
  - label:       "Meer over de artiest"
    description: "Uitgebreidere artiestinformatie — geschiedenis, stijl, context."
  - label:       "Meer over het nummer"
    description: "Diepere analyse: lyrics, betekenis, boodschap."
  - label:       "Uitgebreide playlist-analyse"
    description: "Waarom elke playlist wel of niet past, plus alternatieven."
```

Less common actions reachable via "Other":
- `"album"` / `"albumhoes"` → Album & albumhoes follow-up
- `"links"` / `"spotify link"` / `"youtube"` → Streaming-links follow-up
- `"klaar"` / `"stop"` / `"niks"` → end the flow without doing anything

If the user's free-text reply maps to a follow-up, run that follow-up. If it doesn't map clearly, call `AskUserQuestion` again to disambiguate; do not guess.

---

## After a follow-up reply (subsequent calls)

Same menu, but **add a "Klaar" button** so the user can exit cleanly without typing. Drop whichever button is least useful for this song to make room (usually "Uitgebreide playlist-analyse" if it was already done):

```
question: "Wil je nog iets anders weten over dit nummer?"
header:   "Volgende keuze"
multiSelect: false
options:
  - label:       "Voeg toe aan playlists"
    description: "Voeg dit nummer toe aan één of meer van de aanbevolen playlists."
  - label:       "Meer over de artiest"
    description: "Uitgebreidere artiestinformatie."
  - label:       "Meer over het nummer"
    description: "Diepere analyse: lyrics, betekenis, boodschap."
  - label:       "Klaar"
    description: "Sluit deze flow af — geen verdere actie."
```

If the user already used one of the three info-options, swap that button for whichever info-option they haven't seen yet ("Uitgebreide playlist-analyse", "Album & albumhoes", or "Streaming links"). The "Klaar" option always stays.

When the user picks **Klaar** (or types something like "nee" / "stop" / "niks"), end the flow without a closing summary — the user moves on.

---

## Routing the answer

Map the chosen label (button or free-text) to one of the follow-up actions in `SKILL.md` step 9:

| User picked / typed                                              | Action                                |
|------------------------------------------------------------------|---------------------------------------|
| "Voeg toe aan playlists", "voeg toe aan {playlist}", "add"       | Add flow (`SKILL.md` step 10)         |
| "Meer over de artiest", "wie is X", "artiest info"               | Extended bio                          |
| "Meer over het nummer", "lyrics", "betekenis", "wat gaat dit over" | Deeper song analysis               |
| "Album & albumhoes", "album", "albumhoes", "cover"               | Album name + cover-art link           |
| "Streaming links", "links", "spotify", "youtube"                 | Platform links                        |
| "Uitgebreide playlist-analyse", "waarom deze playlists", "uitleg" | Pros/cons per playlist               |
| "Klaar", "stop", "nee", "niks"                                   | End flow silently                     |
| Anything ambiguous                                                | Re-prompt via `AskUserQuestion`       |

When you produce the answer to a follow-up, **answer only the chosen action** — never re-render the full analysis.
