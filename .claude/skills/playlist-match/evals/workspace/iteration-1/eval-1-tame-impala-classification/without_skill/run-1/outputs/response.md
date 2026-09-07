"The Less I Know The Better" by Tame Impala — classic psych-pop / indie groove track from *Currents* (2015). Here's how I'd map it onto your `playlists.json`:

**Suggested playlists:**

- **Alternative / Indie** — Tame Impala is the textbook fit here. Kevin Parker's project sits squarely in modern psych-rock / indie. High confidence.
- **Ket420** — your special rule says "stoned, psychedelic, spacey, mellow." This track is dreamy, hazy, bass-driven psych-pop. Strong thematic fit.

**Probably not:**

- Not *Pop / Mainstream* despite its crossover success — your "Alternative / Indie" bucket is the better home given the artist's lane.
- Not *Happy tunes* / *Sad tunes* — it's groovy and bittersweet, doesn't lean hard either way.
- No electronic playlists — it's a band track, not EDM, so the "Electronic Music" umbrella rule doesn't apply.

**To actually add it**, grab the Spotify track URL and run:

```bash
python playlist_manager.py smart-add "https://open.spotify.com/track/<id>" --execute
```

That will run the OpenAI classifier and prompt you per-playlist. Or if you want to skip the AI and add manually:

```bash
python playlist_manager.py add "https://open.spotify.com/track/<id>" "Alternative / Indie" --execute
python playlist_manager.py add "https://open.spotify.com/track/<id>" "Ket420" --execute
```

Want me to look up the track URL and run `smart-add` in dry-run to see what the classifier picks?
