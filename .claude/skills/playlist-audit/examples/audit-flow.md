# Example — Audit Flow (web-first, small playlist)

A worked example for `/playlist-audit`. Illustrates a web-first audit on a small playlist followed by track removal.

---

**User input:**
> "Controleer mijn House playlist — welke nummers passen er eigenlijk niet in?"

**Step 1** — Intent detected: audit of "House" playlist.

**Step 2** — Resolve "House" → `playlists.json` → ID `0BEX4bI5xtkEVA4BfYTKg2`. Category: `genre`. No special_rules.

**Step 3** — Run `list-tracks`:
```bash
.venv/bin/python playlist_manager.py list-tracks "House"
```
Output:
```
Playlist: House (8 tracks)
spotify:track:abc1	Martin Garrix - Animals
spotify:track:abc2	Dua Lipa - Levitating
spotify:track:abc3	Tiësto - The Business
spotify:track:abc4	Calvin Harris - Summer
spotify:track:abc5	David Guetta - Titanium
spotify:track:abc6	Avicii - Levels
spotify:track:abc7	The Weeknd - Blinding Lights
spotify:track:abc8	Swedish House Mafia - One
```

8 tracks → web-first recommended.

**Step 4** — AskUserQuestion: "Welke auditmodus wil je gebruiken?"
- **Web-first (Claude + web, nauwkeuriger)** ← recommended
- Quick (OpenAI CLI, sneller)

User picks **Web-first**.

**Step 5a** — Web-first audit:

```
[1/8] Martin Garrix - Animals
  AllMusic: progressive house, big room house; RYM: big room house / EDM
  → 92% match — klassiek progressive house; AllMusic + RYM bevestigen

[2/8] Dua Lipa - Levitating
  Wikipedia: disco-pop, synth-pop; AllMusic: pop
  → 38% match — disco-pop met lichte house-invloeden; voornamelijk mainstream pop

[3/8] Tiësto - The Business
  AllMusic: electro house, pop; RYM: big room house
  → 78% match — electro house met pop-randje; valt net buiten de kern

[4/8] Calvin Harris - Summer
  AllMusic: dance-pop, progressive house; Wikipedia: dance-pop
  → 72% match — dance-pop met progressive house elements; meer dance-pop dan house

[5/8] David Guetta - Titanium
  AllMusic: dance-pop, electro house; Wikipedia: dance-pop, electro-house
  → 65% match — electro-pop met house-productie; vergelijkbaar met Calvin Harris

[6/8] Avicii - Levels
  AllMusic: progressive house, dance; RYM: progressive house
  → 95% match — canoniek progressive house; meerdere sterke bronnen

[7/8] The Weeknd - Blinding Lights
  AllMusic: synth-pop; Wikipedia: dark pop, new wave
  → 35% match — synth-pop en dark R&B; geen house-kenmerken

[8/8] Swedish House Mafia - One
  AllMusic: progressive house; Wikipedia: progressive house
  → 94% match — progressive house; bevestigd door meerdere bronnen
```

**Step 6** — Audit report (Dutch):

```
House — 8 nummers geauditeerd

✅ 4 nummers  ≥80% match (past goed)
⚠️ 3 nummers  60–79% match (twijfelachtig)
❌ 2 nummers  <60% match (past slecht)

Nummers met lage match (kandidaten voor verwijdering):
— 35% — The Weeknd - Blinding Lights
       Reden: synth-pop en dark R&B; geen house-kenmerken (AllMusic: synth-pop)
       URI: spotify:track:abc7
— 38% — Dua Lipa - Levitating
       Reden: disco-pop; lichte house-invloeden maar voornamelijk mainstream pop
       URI: spotify:track:abc2
```

**Step 7** — AskUserQuestion: threshold.
User picks **Verwijder alles onder 60%**.

**Step 8** — AskUserQuestion multiSelect:
"Welke van deze nummers wil je verwijderen uit House?"
- ✓ The Weeknd - Blinding Lights (35%)
- ✓ Dua Lipa - Levitating (38%)

User selects both.

**Step 9** — Show planned commands + confirm:
```bash
.venv/bin/python playlist_manager.py remove "spotify:track:abc7" "House" --execute
.venv/bin/python playlist_manager.py remove "spotify:track:abc2" "House" --execute
```

AskUserQuestion: "Klaar om deze nummers te verwijderen?" → **Ja, verwijder**.

**Step 10** — Bash output:
```
Track: The Weeknd - Blinding Lights
Target playlist: House
Playlist ID: 0BEX4bI5xtkEVA4BfYTKg2
DONE: track removed (snapshot 4kqBJD…)

Track: Dua Lipa - Levitating
Target playlist: House
Playlist ID: 0BEX4bI5xtkEVA4BfYTKg2
DONE: track removed (snapshot 7mxQPR…)
```

**Step 11** — Summary:
> "Audit klaar! 2 verwijderd, 0 overgeslagen. House heeft nu 6 nummers."
