Ik heb verder gezocht in zwakkere bronnen: streamingstatistieken, blogs en artiestprofielen. Over het nummer zelf staat daar nog steeds geen genre-tag. Wat ik wel vond:

**Wat de zwakkere bronnen zeggen**

- **Het nummer zelf:** "Victory" verscheen op 6 oktober 2023 en heeft ongeveer 2,7 miljoen streams. Het is Michael Wilburs op één na populairste nummer, na "SMASH". Deze cijfers komen van een statistieksite van derden ([musicmetricsvault](https://www.musicmetricsvault.com/artists/michael-wilbur/4xa7ht9m5Uj0YhGWIm0K9n)) zonder genre-tag op trackniveau.
- **Michael Wilbur:** musicmetricsvault tagt hem als *jazz funk*. Volgens de bio daar mengt hij EDM, jazz, house en hiphop. Viberate noemt *Jazz, Jazz Fusion, Avant-garde Jazz* ([viberate](https://www.viberate.com/artist/michael-wilbur/overview/)). Solo speelt hij live loops op bassax, tenorsax, trompet en stem ([Moe's Alley](https://moesalley.com/tm-attraction/michael-wilbur/)).
- **Tonio Sagan:** hij is producer en MC en heeft eerder met Moon Hooch gewerkt (de *Light It Up* EP en "Acid Mountain"). Een eerdere samenwerking met Wilbur, "Luna Moths", wordt omschreven als *jazz en hiphop met experimentele randjes*, met Sagans raps en Wilburs sax ([The Word Is Bond](https://www.thewordisbond.com/tonio-sagan-drops-luna-moths-feat-michael-wilbur-erick-t-coomes/), [Wikipedia: Moon Hooch](https://en.wikipedia.org/wiki/Moon_Hooch)).

**Genre-inschatting (op basis van de artiesten, niet van het nummer)**

| Genre | Zekerheid |
|---|---|
| Jazz fusion / jazz funk (sax-gedreven) | 70% |
| Electronic / EDM-productie | 55% |
| Hiphop / beats | 45% |
| House | 25% |

**Playlist-matches**

| Playlist | Score | Waarom |
|---|---|---|
| Jazz / Funk / Soul | 70% | Wilbur is consequent jazz(-funk/-fusion) getagd |
| Electronic Music | 55% | Elektronische productie (Sagan, Wilburs EDM-crossover) |
| Rap | 40% | Alleen als Sagan erop rapt, wat ik niet kon bevestigen |
| Party | 40% | Wilburs populaire werk ("SMASH") is energiek en dansbaar |
| **Random sht** | **100% (catch-all)** | Geen enkele playlist haalt de drempel van 85% |

De scores liggen dicht bij elkaar en geen ervan komt boven de 85%. Volgens de catch-all-regel in `playlists.json` gaat het nummer dan naar **Random sht**, dus dat is nu de sterkste match. Jazz / Funk / Soul is de beste genrekandidaat, maar die steunt alleen op artiestgegevens en niet op het nummer zelf.

**Waar wil je hem aan toevoegen?**

1. **Random sht** (de catch-all-match)
2. **Jazz / Funk / Soul**
3. **Random sht + Jazz / Funk / Soul**
4. Eerst zelf luisteren en daarna kiezen (bijvoorbeeld ook Electronic Music of Rap)

Laat het me weten, dan voer ik het uit. Hieronder de dry-run voor optie 1. Die schrijft nog niets weg; vervang de playlistnaam voor een andere keuze:

```bash
python playlist_manager.py add "https://open.spotify.com/track/3q5pd71UVh8jPbAfpjgBzM" "Random sht"
```
