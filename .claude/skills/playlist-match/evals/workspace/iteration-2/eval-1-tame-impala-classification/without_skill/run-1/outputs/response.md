**Tame Impala - The Less I Know The Better** (album *Currents*, 2015)
Spotify: `spotify:track:6K4t31amVTZDgR3sKmwUJJ`

### Genre read

| Genre / feel | Confidence |
|---|---|
| Psychedelic pop / neo-psychedelia | 95% |
| Indie / alternative | 90% |
| Pop (crossover hit, huge streaming numbers) | 75% |
| Disco/funk-tinged groove (that bassline) | 50% |
| Electronic (synth-heavy, but band-based) | 30% |

Feel: upbeat and groovy (danceability 0.64, energy 0.74, valence 0.79, ~117 BPM), while the lyrics are about jealousy and heartbreak.

### Playlist matches

| Playlist | Fit | Note |
|---|---|---|
| Alternative / Indie | 95% | **already in it** (according to your local log) |
| Pop / Mainstream | 75% | **already in it** (according to your local log) |
| Ket420 | 70% | dreamy, psychedelic production fits the "spacey/mellow" rule; it's more groovy than mellow, though |
| Happy tunes | 60% | sounds happy, but the lyrics are bittersweet |
| Party | 55% | works at an indie/alt party; not a peak-time banger |
| Jazz / Funk / Soul | 25% | funky bassline, but not really the genre |

Since it's already in its two strongest matches, there's nothing obvious left to add. The only real extra candidate is **Ket420**, with Happy tunes / Party as optional add-ons.

Note: the "already in" check comes from `.tracks_log.json`. Your Alternative / Indie export dates from 28 August and doesn't include the track, so if you added it by hand outside this tool, you may want to check Spotify to be sure.

**Do you want me to add it anywhere?** Options:
1. Ket420 only
2. Ket420 + Happy tunes
3. Ket420 + Happy tunes + Party
4. Nothing, it's fine where it is

If you pick one, this is the dry run for option 3 (leave out the lines you don't want, then add `--execute` to actually write):

```bash
python playlist_manager.py add spotify:track:6K4t31amVTZDgR3sKmwUJJ "Ket420"
python playlist_manager.py add spotify:track:6K4t31amVTZDgR3sKmwUJJ "Happy tunes"
python playlist_manager.py add spotify:track:6K4t31amVTZDgR3sKmwUJJ "Party"
```
