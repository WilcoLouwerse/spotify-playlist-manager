# Example — bulk-playlist flow

User message:

> "leeg mijn 'Random sht' helemaal — ik vertrouw de classifier"

The user said "leeg" + "vertrouw" → route to `bulk-playlist`.

---

## Step 1-3 — detect, resolve, pick workflow

Source: bare name "Random sht" → a key in `playlists.json` (ID `7RaNdOmShTpLaYlIsTiD01`), so Spotify can read it live. A CSV snapshot also exists: `exportify-exports/Random_sht.csv` (95-track export from 2026-05-12). Per `references/source-resolution.md` → "Prefer the live playlist over a CSV", the skill asks via **AskUserQuestion**:

> "Voor Random sht staat een CSV-export klaar, maar Spotify kan deze playlist ook live uitlezen. Welke bron wil je gebruiken?"
> - **Live via Spotify (Recommended)** — meest actueel.
> - **Deze CSV** — momentopname van 2026-05-12.

User picks **Live via Spotify**. The source argument becomes the playlist ID `7RaNdOmShTpLaYlIsTiD01`.

Workflow: **bulk-playlist** (user said "leeg" + "vertrouw").

## Step 4 — tuning

User said "ik vertrouw de classifier" → leave defaults. The catch-all (`Random sht`) will pick up anything below the threshold, which is fine here because that's the source playlist anyway.

## Step 5 — mode

**AskUserQuestion**:

> "Dry-run eerst of direct executen?"
> - **Dry-run eerst** *(aanbevolen)* — toon het plan, schrijf niets.
> - **Direct execute** — schrijf direct na één y/N.

User picks **Direct execute**.

## Step 6 — plan

```
Je wilt 'Random sht' (live) triëren via bulk-playlist (execute).

Ik ga dit commando draaien vanuit de repo-root:

.venv/bin/python playlist_manager.py bulk-playlist "7RaNdOmShTpLaYlIsTiD01" --execute

Het script vraagt één y/N voor het hele plan. Draai 'm zelf in je terminal, of laat mij 'm draaien met automatisch 'y' via een pipe.
```

## Step 7 — confirmation for execute

**AskUserQuestion**:

> "Hoe wil je deze execute-run uitvoeren?"
> - **Vanuit mijn terminal** *(handmatige y/N)* — copy-paste het commando.
> - **Hier draaien met automatische 'y'** — `yes | ...` accepteert de single y/N automatisch.
> - **Annuleren** — terug.

User picks **Hier draaien met automatische 'y'**.

## Step 8 — run

Skill runs:

```bash
yes | .venv/bin/python playlist_manager.py bulk-playlist "7RaNdOmShTpLaYlIsTiD01" --execute
```

Output verbatim:

```
Reading source: Random sht (7RaNdOmShTpLaYlIsTiD01)
Found 95 tracks. Classifying...

  [1/95] Bakermat - Walk That Walk
  [2/95] Charlotte de Witte - Doppler
  ...

Found 95 tracks.

Recommendations:
- 23 → House
- 18 → Techno
- 14 → Electronic Music
- 11 → Funny meme
- 7 → Ket420

Proceed? [y/N]: 

- House: ADDED Bakermat - Walk That Walk (snapshot AbCdEfGhIj…)
...

============================================================
Bulk add complete (EXECUTED): 73 added, 0 failed.
```

## Step 9 — summary

```
Klaar! 73 toegevoegd, 0 mislukt.
```

---

## Variant — user wants dry-run first

After step 5 the user picked **Dry-run eerst**. Skill runs the dry-run via Bash as `yes | .venv/bin/python playlist_manager.py bulk-playlist "7RaNdOmShTpLaYlIsTiD01"` — without `--execute` the pipe only makes the script print each `DRY RUN (would add …)` line instead of stopping at `Proceed? [y/N]:` (the Bash tool has no stdin). Then offers in step 9:

```
Dry-run klaar — 73 kandidaten verdeeld over 5 playlists. Niets geschreven.
```

Then **AskUserQuestion** to chain: "Nu echt executen, of stoppen?"
