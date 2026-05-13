# Playlist Taxonomy

The single source of truth is [`playlists.json`](../../../../playlists.json) at the repo root. Read it on every run; the lists below are reference, not authority.

---

## Genre playlists

`categories.genre` (15 entries at time of writing):

| Playlist | When it fits |
|----------|--------------|
| Rap | Hip-hop, rap, trap, drill, conscious / mumble / cloud rap, boom-bap. |
| Pop / Mainstream | Top-40 pop, radio pop, mainstream singer-songwriter, dance-pop. |
| Alternative / Indie | Indie rock, indie pop, dream pop, lo-fi indie, post-punk revival, art rock. |
| K-pop | Korean pop, K-R&B, K-hip-hop, J-pop adjacents only when clearly K-pop-styled. |
| Metal & Rock | All rock and metal with vocals: classic, hard, prog, nu, alt, metalcore, death, black, doom. |
| Instrumental Metal | Rock/metal without vocals — djent, post-rock, instrumental prog. Separate from Metal & Rock. |
| Jazz / Funk / Soul | Jazz of any era, funk, soul, neo-soul, R&B with strong jazz/funk DNA. |
| House | Deep, tech, future, tropical, French, classic Chicago — all house subgenres. |
| Techno | Industrial, melodic, peak-time, minimal, acid techno. |
| Trance | Uplifting, progressive, psytrance, vocal trance. |
| Drum & Bass | DnB, jungle, neurofunk, liquid DnB, jump-up. |
| Dubstep / Bass | Dubstep, riddim, bass music, bass house when leaning heavy. |
| Hardstyle & Hardcore | Hardstyle, hardcore, rawstyle, gabber, frenchcore, uptempo, terror. |
| Synthwave | Synthwave, retrowave, outrun, darksynth, vaporwave when synthwave-styled. |
| Electronic Music | **Umbrella for all electronic music.** See "Electronic Music umbrella rule" below. |

## Mood playlists

`categories.mood`:

| Playlist | When it fits |
|----------|--------------|
| Party | High-energy, dance-floor, festival, banger feel — regardless of genre. |
| Happy tunes | Bright, major key, feel-good, uplifting lyrics. |
| Sad tunes | Melancholic, heartbreak, grief, slow + minor key. |
| Angry tunes | Aggressive, confrontational, breakup-anger, heavy lyrics or production. |
| Rustig / 'anders' | Calm, chill, ambient, "different" / left-field that needs a slower listen. |

## Theme / special playlists

`categories.theme`. Use only when the song clearly fits the rule in `special_rules`:

| Playlist | Rule |
|----------|------|
| Funny meme | Meme songs, internet classics (Rick Roll), absurd / funny lyrics, intentionally bad in a fun way. |
| Ket420 | Stoned / psychedelic / spacey / mellow / ketamine-or-weed listening. Often shoegaze, ambient, psy, slow-DnB. |
| Hooyah | Sexually tinted / sensual / suggestive lyrics or production. |

---

## Electronic Music umbrella rule

From `playlists.json -> special_rules -> "Electronic Music"`:

> Suggest 'Electronic Music' for ALL electronic tracks — house, techno, trance, drum & bass, dubstep, hardstyle, synthwave, ambient electronic, etc. It is an inclusive umbrella, not a fallback: include it ALONGSIDE the matching electronic subgenre, not instead of it.

In practice: whenever you recommend any of House / Techno / Trance / Drum & Bass / Dubstep / Bass / Hardstyle & Hardcore / Synthwave, **also** recommend `Electronic Music`. Both go in the playlist match list — count as separate recommendations toward the 1-5 cap.

---

## What `Random sht` is — and why it stays hidden

`playlists.json -> catch_all`:

```
"catch_all": {
  "playlist": "Random sht",
  "threshold": 85,
  "rule": "Programmatic fallback ... NOT shown to the OpenAI classifier; it is a script-side safety net for tracks that don't fit anywhere."
}
```

`Random sht` is the script's safety net for `smart-add`/`bulk-playlist`. **The skill must never recommend it.** If nothing else fits, the correct user-facing answer is "geen van de playlists past hier echt" — not a `Random sht` suggestion.

---

## Aliases

`playlists.json -> aliases` maps shorthand to canonical names (e.g. `dnb` → `Drum & Bass`, `chill` → `Rustig / 'anders'`). The `add` command accepts aliases. The skill itself should **render** canonical names in its output (so the user reads `Drum & Bass`, not `dnb`), but may **accept** aliases when the user types a follow-up like "voeg toe aan dnb".

---

## When user-edited the file

If `playlists.json` contains playlists not on the lists above (the user added a new one, or renamed one), trust the file. Reference these tables only when something looks off — if the file says a playlist exists, recommend from the file.
