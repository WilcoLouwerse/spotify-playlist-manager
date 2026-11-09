**Rick Astley - Never Gonna Give You Up** (1987)
Spotify: https://open.spotify.com/track/4PTG3Z6ehGkBFwjybzWkR8 (I checked it with a dry-run: Spotify returns "Rick Astley - Never Gonna Give You Up")

This is *the* Rickroll, probably the best-known meme song there is. Musically it's upbeat 80s dance-pop (Stock Aitken Waterman production, Hi-NRG/synth-pop feel).

**Genre/vibe estimate**

| Aspect | Confidence |
|---|---|
| Internet meme / classic (Rickroll) | 99% |
| 80s pop / dance-pop | 95% |
| Upbeat, feel-good | 85% |
| Party / sing-along | 65% |
| Synth-pop (not synthwave) | 40% |

**Recommended playlists**

| Playlist | Confidence | Why |
|---|---|---|
| **Funny meme** | 98% | Matches the special rule exactly: "meme songs, internet classics". The Rickroll is the textbook example. |
| **Pop / Mainstream** | 90% | Classic 80s chart pop, a UK and US #1. |
| **Happy tunes** | 80% | Bright, major-key, bouncy. |
| Party | 60% | Works as a sing-along at a party, but it isn't really a party banger. |
| Synthwave | 15% | Not a match: synthwave is the modern retro-80s genre, and this is actual 80s pop. |

Random sht isn't needed as a fallback: two playlists score above the 85% threshold.

Duplicate check: the track is **not** in Funny meme, Pop / Mainstream, Happy tunes or Party yet. The dry-runs showed no SKIP.

**Which ones should I add it to?** My suggestion is **Funny meme + Pop / Mainstream + Happy tunes**. Let me know if you want Party too, or only Funny meme. Once you confirm, I'll run:

```bash
python playlist_manager.py add "https://open.spotify.com/track/4PTG3Z6ehGkBFwjybzWkR8" "Funny meme" --execute
python playlist_manager.py add "https://open.spotify.com/track/4PTG3Z6ehGkBFwjybzWkR8" "Pop / Mainstream" --execute
python playlist_manager.py add "https://open.spotify.com/track/4PTG3Z6ehGkBFwjybzWkR8" "Happy tunes" --execute
```

Do you also want it in your Liked Songs (`like ... --execute`)?
