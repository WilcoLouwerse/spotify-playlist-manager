Je hebt gelijk, niemand kent hem, ik ook niet. Eerlijk antwoord dus: ik kan niet betrouwbaar zeggen welk genre **Spook & Mr Vague - aufdemwegnach** is.

**Wat ik heb gecontroleerd**
- Zoeken op het web naar "Spook & Mr Vague", "Mr Vague" en "aufdemwegnach" (ook via Bandcamp/SoundCloud/Discogs) leverde niets op dat bij deze artiest of titel hoort. Wel andere artiesten met "Spook" of "Vague" in de naam, maar daar hoort dit nummer niet bij.
- Het nummer staat niet in je lokale log (`.tracks_log.json`) en ook niet in de exportify-exports. Het zit dus waarschijnlijk nog in geen enkele playlist.

**Wat ik zou gokken (lage zekerheid)**
De naam ("Spook & Mr Vague", een Duitse titel als één woord aan elkaar) doet denken aan een kleine elektronische of lo-fi/ambient-release. Maar dat is puur afgeleid uit de naam, dus het is geen classificatie:

| Playlist | Zekerheid | Waarom |
|---|---|---|
| Random sht | hoogste | Vangnet uit `playlists.json`: geen enkele andere playlist haalt de drempel van 85% |
| Electronic Music | ~30% | Alleen een gok op basis van de naam |
| Rustig / 'anders' | ~25% | Alleen een gok op basis van de naam |
| Ket420 | ~15% | Alleen als het spacey/psychedelisch klinkt |

Op basis hiervan zou ik hem **niet** in een genre-playlist zetten. Random sht is de enige veilige keuze.

**Hoe we het wel goed krijgen**
1. Stuur me de Spotify-link van het nummer. Dan kan de classifier van het script ernaar kijken (alleen analyse, er verandert niets):
   ```bash
   python playlist_manager.py analyze-only "<spotify-track-url>"
   ```
2. Of vertel kort hoe het klinkt (tempo, instrumenten, vocals, sfeer), dan maak ik een echte inschatting.

Wil je hem nu meteen in Random sht zetten, of stuur je eerst de link of een beschrijving?
