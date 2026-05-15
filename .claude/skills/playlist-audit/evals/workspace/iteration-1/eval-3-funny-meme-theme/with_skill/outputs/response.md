# User-Facing Response — eval-3-funny-meme-theme

> This is the exact Dutch response the skill would present to the user for the prompt:
> "welke nummers passen er niet in mijn Funny meme playlist?"

---

Ik heb `list-tracks` uitgevoerd voor de **Funny meme** playlist, maar Spotify geeft in Development Mode geen nummers terug. Heb je een Exportify CSV-export van deze playlist?

- **Ja, ik heb een CSV** — deel het pad en ik herstart de audit
- **Nee** — exporteer je playlist op https://exportify.net en kom daarna terug

---

> *(Assuming the user provides a CSV or we simulate the track list for demonstration — the response below shows what the skill produces after obtaining the track list.)*

---

De **Funny meme** playlist is een thema-playlist. Ik beoordeel elk nummer op **meme-status, internetklassieker-status en absurde/grappige teksten** — niet op muziekgenre. De `special_rules` voor deze playlist zijn: *"Only for meme songs, internet classics, absurd/funny lyrics."*

[1/12] Rick Astley - Never Gonna Give You Up  
[2/12] Smash Mouth - All Star  
[3/12] Rebecca Black - Friday  
[4/12] PSY - Gangnam Style  
[5/12] Ylvis - What Does the Fox Say?  
[6/12] William Hung - She Bangs  
[7/12] OK Go - Here It Goes Again  
[8/12] Ed Sheeran - Shape of You  
[9/12] Doja Cat - Say So  
[10/12] Crazy Frog - Axel F  
[11/12] MGMT - Electric Feel  
[12/12] Mr. Oizo - Flat Beat  

---

**Funny meme — 12 nummers geauditeerd**

✅  7 nummers  ≥80% match (past goed)
⚠️  1 nummer   60–79% match (twijfelachtig)
❌  4 nummers  <60% match (past slecht)

Score-methode: thema-gebaseerd — criteria zijn meme-status, internetklassieker-status en absurde/grappige teksten, NIET genre.

**Nummers met lage match (kandidaten voor verwijdering):**
— 8% — Ed Sheeran - Shape of You
       Reden: mainstream pophit zonder meme-karakter of absurde elementen; past niet in Funny meme
       URI: spotify:track:0eGsygTp906u18L0Oimnem
— 18% — MGMT - Electric Feel
       Reden: serieuze psychedelische pop; incidenteel in memes maar geen meme-song
       URI: spotify:track:6K4t31amVTZDgR3sKmwUJJ
— 22% — Doja Cat - Say So
       Reden: retro-pophit met TikTok-populariteit maar geen meme-song of absurde teksten
       URI: spotify:track:3n69KToLBJFRjJHGOHxF59
— 52% — OK Go - Here It Goes Again
       Reden: beroemde loopband-video ging viraal maar het nummer zelf is een serieus indie-rocklied, geen meme-song
       URI: spotify:track:0u2P5u6lvoDfwTYjAADbn4

**Twijfelachtig (⚠️):**
— 68% — Mr. Oizo - Flat Beat
       Reden: Flat Eric-pop was vroege internetmeme (1999) maar minder herkenbaar voor jongere generaties
       URI: spotify:track:0nrRP5dpqRi08e34VxlA3g

---

**Welke drempel wil je gebruiken voor verwijdering?**

- Verwijder alles onder 60% (standaard) — 4 nummers
- Verwijder alles onder 70% — 4 nummers (zelfde)
- Verwijder alles onder 80% — 5 nummers (ook Flat Beat erbij)
- Niks verwijderen — alleen het overzicht bekijken
