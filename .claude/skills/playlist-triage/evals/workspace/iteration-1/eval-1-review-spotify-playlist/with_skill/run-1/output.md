Je gaf een Spotify-URL plus "reviewen" — dat mapt op `review-playlist` (per-track `y/N/s/q`). Ik start met een **dry-run** zodat we eerst het plan zien voor er iets geschreven wordt.

Je wilt `https://open.spotify.com/playlist/3aBcDeFgHiJkLmNoPqRsTu` triëren via `review-playlist` (dry-run).

Ik ga dit commando draaien vanuit de repo-root:

```bash
.venv/bin/python playlist_manager.py review-playlist "https://open.spotify.com/playlist/3aBcDeFgHiJkLmNoPqRsTu"
```

Dit is een dry-run — geen y/N prompts, niets wordt geschreven. Je ziet per nummer welke target-playlists de classifier voorstelt (defaults: `--max-playlists 3 --min-playlists 1 --min-confidence 80`).

Een paar dingen om te weten vóór we doorgaan:

- **Als de Spotify API niets leesbaars teruggeeft** (Developer Mode strip), biedt de CLI zelf een CSV-fallback aan uit `exportify-exports/`. Laat dat gebeuren — niet vooraf omzeilen.
- **Voor de echte run** (`--execute`) kan ik de per-track `y/N/s/q` prompts niet vanuit chat beantwoorden. Dan krijg je het commando met `--execute` erbij en draai je 'm zelf in je terminal.

Na de dry-run laat ik de output verbatim zien en geef ik één Dutch samenvattingsregel:

> Dry-run klaar — {N} kandidaten verdeeld over {M} playlists. Niets geschreven.

Wil je dat ik 'm zo draai, of eerst nog iets aanpassen (striktere classifier `--min-confidence 90`, meer suggesties per track `--max-playlists 5`, of direct over naar `bulk-playlist` als je gewoon wilt leeghalen)?
