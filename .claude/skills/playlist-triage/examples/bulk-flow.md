# Example — bulk-playlist flow

User message:

> "leeg mijn 'Random sht' helemaal — ik vertrouw de classifier"

The user said "leeg" + "vertrouw" → route to `bulk-playlist`.

---

## Step 1-3 — detect, resolve, pick workflow

Source: bare name "Random sht" → resolve against `exportify-exports/`. Skill lists matching files:
- `exportify-exports/Random_sht.csv` (95-track export from 2026-05-12)

Skill confirms via **AskUserQuestion**:

> "Gevonden CSV: `exportify-exports/Random_sht.csv` (95 tracks, geëxporteerd 2026-05-12). Gebruik die?"
> - **Ja, gebruik die CSV**
> - **Nee, gebruik de Spotify URL** *(handmatig plakken)*

User picks **Ja**.

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
Je wilt 'Random sht' (exportify-exports/Random_sht.csv) triëren via bulk-playlist (execute).

Ik ga dit commando draaien vanuit de repo-root:

.venv/bin/python playlist_manager.py bulk-playlist "Random sht" --execute

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
yes | .venv/bin/python playlist_manager.py bulk-playlist "Random sht" --execute
```

Output verbatim:

```
Reading source playlist: Random sht (from exportify-exports/Random_sht.csv)
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

Proceed? [y/N]: y

- House: ADDED Bakermat - Walk That Walk (snapshot AbCdEfGhIj…)
...

============================================================
Bulk add complete (EXECUTED): 59 added, 0 failed.
```

## Step 9 — summary

```
Klaar! 59 toegevoegd, 0 overgeslagen (al in playlist).
```

---

## Variant — user wants dry-run first

After step 5 the user picked **Dry-run eerst**. Skill runs the dry-run via Bash (no `yes |` needed — dry-run skips the prompt). Then offers in step 9:

```
Dry-run klaar — 59 kandidaten verdeeld over 5 playlists. Niets geschreven.
```

Then **AskUserQuestion** to chain: "Nu echt executen, of stoppen?"
