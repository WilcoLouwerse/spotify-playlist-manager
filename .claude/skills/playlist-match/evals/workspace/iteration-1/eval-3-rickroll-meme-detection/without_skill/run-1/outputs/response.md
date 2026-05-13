"Never Gonna Give You Up" by Rick Astley (1987) — classic 80s synth-pop / dance-pop. A staple of the era, but it's also become *the* internet meme song ("Rickroll").

Based on your `playlists.json`, here's how I'd classify it:

## Suggested playlists

- **Pop / Mainstream** — it's a quintessential 80s pop hit, charted #1 in multiple countries.
- **Funny meme** — per your `special_rules`: *"Only for meme songs, internet classics, absurd/funny lyrics."* Rickrolling is arguably *the* internet classic, so this fits squarely.
- **Happy tunes** — upbeat tempo, optimistic lyrics, major key.

Optional, weaker fits:
- **Party** — danceable, crowd-pleaser, but more "nostalgic singalong" than peak party energy. Judgment call.

## Suggested command

If you want to add it via the CLI (dry-run first, per your safety defaults):

```bash
# Dry-run
python playlist_manager.py smart-add "https://open.spotify.com/track/4PTG3Z6ehGkBFwjybzWkR8"

# Execute once you're happy
python playlist_manager.py smart-add "https://open.spotify.com/track/4PTG3Z6ehGkBFwjybzWkR8" --execute
```

Or skip the classifier and add directly:

```bash
python playlist_manager.py add "https://open.spotify.com/track/4PTG3Z6ehGkBFwjybzWkR8" "Funny meme" --execute
python playlist_manager.py add "https://open.spotify.com/track/4PTG3Z6ehGkBFwjybzWkR8" "Pop / Mainstream" --execute
```

Note: I'm assuming the standard 1987 album version (Spotify track id `4PTG3Z6ehGkBFwjybzWkR8`) — confirm before running `--execute` if you meant a remix/live version.

Want me to run the dry-run for you?
