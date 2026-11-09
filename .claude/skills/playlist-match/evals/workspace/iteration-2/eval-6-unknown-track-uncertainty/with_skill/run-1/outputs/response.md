Sorry, ik heb moeite om de genres voor dit nummer te vinden. Ik heb via WebSearch/WebFetch gezocht op Last.fm (track- én artiestpagina geven 404), Discogs, RYM, Bandcamp, SoundCloud en Spotify, maar 'Spook & Mr Vague' en 'aufdemwegnach' komen nergens voor, ook niet als artiestbrede tags. Ik kan dus niets staven en verzin geen genres. Heb je een Spotify-link, of weet je hoe het klinkt? Typ dat dan via 'Other'.

```AskUserQuestion
question: "Web-lookups gaven geen duidelijk antwoord. Hoe wil je dat ik hiermee verder ga?"
header:   "Genre-aanpak"
multiSelect: false
options:
  - label:       "Breder zoeken (artiestpagina's)"
    description: "Verbreed de WebFetch/WebSearch naar artiestbrede pagina's (artiestpagina op AllMusic/Wikipedia/RYM/Last.fm). Scope wordt artiestgebaseerd."
  - label:       "Zwakkere webbronnen"
    description: "Val terug op zwakkere webbronnen (Last.fm tags, SoundCloud-tag, Bandcamp-tag) via WebFetch. Lagere precisie, hogere recall."
  - label:       "Sla genres over"
    description: "Alleen playlist matching, geen harde genreclaim."
  - label:       "Inschatten zonder internet (Claude + OpenAI)"
    description: "Laatste redmiddel: Claude én OpenAI schatten in op basis van hun trainingsdata. OpenAI wordt via analyze-only (read-only, geen Spotify writes) aangeroepen. Als OpenAI niet beschikbaar is wordt dit gemeld en valt de skill terug op Claude alleen."
```
