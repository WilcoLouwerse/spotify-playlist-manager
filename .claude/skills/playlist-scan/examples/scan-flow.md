# Example — scan-for flow

User message:

> "welke tracks uit 'Random sht' zouden in House passen?"

---

## Step 1-3 — detect, resolve target, resolve source

- Target: "House" → matches `playlists.json -> playlists.House` directly. Use canonical name `House`.
- Source: bare name "Random sht" → resolve against `exportify-exports/`. Skill finds `exportify-exports/Random_sht.csv`.

Skill confirms via **AskUserQuestion**:

> "Bevestig:"
> - Target: **House**
> - Source: `exportify-exports/Random_sht.csv` (95 tracks)
>
> Klopt dit?
> - **Ja, ga door**
> - **Nee, andere source/target** *(handmatig)*

User picks **Ja**.

## Step 4 — tuning

No tuning hint. Use default `--min-confidence 80`. Don't show flags unless deviating.

## Step 5 — mode

**AskUserQuestion**:

> "Hoe wil je dit draaien?"
> - **Dry-run** *(aanbevolen)* — toon de kandidaten, schrijf niets.
> - **Execute** — voeg de kandidaten direct toe na één y/N.

User picks **Dry-run**.

## Step 6 — plan

```
Je wilt House kandidaten zoeken in 'Random sht' (exportify-exports/Random_sht.csv) (dry-run).

Ik ga dit commando draaien vanuit de repo-root:

.venv/bin/python playlist_manager.py scan-for "House" "Random sht"

Dit is een dry-run — geen y/N prompt, niets wordt geschreven.
```

## Step 8 — run

Skill runs the command. Output verbatim:

```
Target playlist: House (0BEX4bI5xtkEVA4BfYTKg2)
Scanning source:  Random sht (from exportify-exports/Random_sht.csv)
Found 95 tracks. Classifying...

  [1/95] Bakermat - Walk That Walk
  ...

Found 95 tracks.
  Already in House: 4
  Not a fit for House: 68

23 candidate(s) for House:
- 92% — Bakermat - Walk That Walk
    uplifting deep-house with vocals
- 88% — Honey Dijon - Show Me Some Love
    classic house groove with vocal stabs
- 86% — Disclosure - Latch
    deep-house-leaning electronic pop
...
- 81% — Kerri Chandler - Bar A Thym
    classic NY garage house

DRY RUN: would prompt [y/N] to add all 23 to 'House'
```

## Step 9 — summary

```
Dry-run klaar — 23 kandidaten voor House. Niets geschreven.
```

## Variant — user wants to execute after seeing the list

User says "ja prima, voeg ze allemaal toe". Skill goes back to step 5 (mode = execute), step 6 (plan with `--execute`), step 7:

**AskUserQuestion**:

> "Hoe wil je deze execute-run uitvoeren?"
> - **Vanuit mijn terminal** — copy-paste het commando en typ `y`.
> - **Hier draaien met automatische 'y'** — `yes | ...` accepteert de prompt automatisch.
> - **Annuleren** — terug.

User picks **Hier draaien met automatische 'y'**.

Skill runs:

```bash
yes | .venv/bin/python playlist_manager.py scan-for "House" "Random sht" --execute
```

Output:

```
... (same scan output as dry-run) ...

Add all 23 to 'House'? [y/N]: y

- ADDED Bakermat - Walk That Walk (snapshot AbCdEfGhIj…)
- ADDED Honey Dijon - Show Me Some Love (snapshot ...)
...

============================================================
Scan complete (EXECUTED): 23 added, 0 failed.
```

## Step 9 — summary (execute path)

```
Klaar! 23 toegevoegd aan House, 0 overgeslagen (al in playlist).
```

---

## Variant — alias resolution

User says "welke dnb-tracks passen in mijn triage?".

- Target: "dnb" → `playlists.json -> aliases.dnb = "Drum & Bass"`. Skill confirms canonical via **AskUserQuestion**:

  > "Target opgelost: **Drum & Bass** (alias `dnb`). Klopt?"
  > - **Ja**
  > - **Nee, ik bedoelde iets anders**

Source missing — skill asks for it via **AskUserQuestion**.

---

## Variant — user picks `Random sht` as target

User says "scan op Random sht in mijn triage". Highly unusual.

Skill confirms via **AskUserQuestion**:

> "`Random sht` is de catch-all playlist in `playlists.json`, niet bedoeld als scan-target. Weet je zeker dat je daar tracks aan wilt toevoegen?"
> - **Nee, ik bedoelde iets anders**
> - **Ja, scan toch op Random sht** *(zeldzaam)*

Only proceed if the user confirms.
