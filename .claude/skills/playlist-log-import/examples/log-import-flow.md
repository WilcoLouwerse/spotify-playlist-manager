# Example — log-import flow

User message:

> "kan je mijn House export importeren in de log?"

---

## Step 1-3 — detect, resolve target, resolve file

- Target: "House" → matches `playlists.json -> playlists.House` directly. Use canonical name `House`.
- File: bare playlist name "House" → resolve against `exportify-exports/`. Skill finds `exportify-exports/House.csv` (143 lines).

## Step 4 — confirmation

Plan rendered (per `templates/plan.md`):

```
Je wilt de log voor House seeden met exportify-exports/House.csv (143 regels).

Dit is een lokale operatie — er wordt niets naar Spotify geschreven. Alleen `.adds_log.json` wordt bijgewerkt.

Ik ga dit commando draaien vanuit de repo-root:

.venv/bin/python playlist_manager.py log-import "House" "exportify-exports/House.csv"
```

**AskUserQuestion**:

> "Doorgaan?"
> - **Ja, importeer**
> - **Nee, andere target/file** *(handmatig)*
> - **Annuleren**

User picks **Ja, importeer**.

## Step 6 — run

Skill runs the command. Output verbatim:

```
Playlist: House (0BEX4bI5xtkEVA4BfYTKg2)
  Imported new URIs: 142
  Already in log:    0
  Duplicate in file: 0
  Unparseable lines: 1
  Total URIs logged: 142
```

## Step 7 — summary

```
Klaar! 142 nieuwe URIs toegevoegd aan de log voor House (totaal nu 142).
```

(The single `Unparseable lines: 1` is the CSV header row — normal, no need to flag it.)

---

## Variant — alias resolution

User says "seed mijn dnb log met `exportify-exports/Drum_&_Bass.csv`".

- Target: "dnb" → `playlists.json -> aliases.dnb = "Drum & Bass"`. Skill confirms canonical via **AskUserQuestion**:

  > "Target opgelost: **Drum & Bass** (alias `dnb`). Klopt?"
  > - **Ja**
  > - **Nee, ik bedoelde iets anders**

- File: explicit path `exportify-exports/Drum_&_Bass.csv` — verify exists (note the `&` is fine in the filename; quote the argument).

Command rendered:

```bash
.venv/bin/python playlist_manager.py log-import "Drum & Bass" "exportify-exports/Drum_&_Bass.csv"
```

---

## Variant — file not found

User says "log-import House van house_export.csv".

- Target: "House" → resolved.
- File: `house_export.csv` — doesn't exist at repo root or `exportify-exports/`.

Skill lists `exportify-exports/` contents (e.g. `House.csv`, `Techno.csv`, `Random_sht.csv`) and asks via **AskUserQuestion**:

> "Ik kan `house_export.csv` niet vinden. Welk bestand bedoel je?"
> - **`exportify-exports/House.csv`** *(meest waarschijnlijke match)*
> - **Ander pad** *(typ zelf)*
> - **Annuleren**

User picks the first option. Skill loops back to step 4 with the corrected file.

---

## Variant — re-seed (file already imported)

User runs the same House CSV again a week later, after adding a few more tracks manually.

Output:

```
Playlist: House (0BEX4bI5xtkEVA4BfYTKg2)
  Imported new URIs: 3
  Already in log:    142
  Duplicate in file: 0
  Unparseable lines: 1
  Total URIs logged: 145
```

Summary:

```
Klaar! 3 nieuwe URIs toegevoegd aan de log voor House (totaal nu 145).
```

---

## Variant — empty / wrong-format file

User runs `log-import House notes.txt` where `notes.txt` has 50 lines of plain text and no Spotify URIs.

Output:

```
Playlist: House (0BEX4bI5xtkEVA4BfYTKg2)
  Imported new URIs: 0
  Already in log:    0
  Duplicate in file: 0
  Unparseable lines: 50
  Total URIs logged: 0
```

Summary:

```
Geen Spotify-URIs gevonden in notes.txt — check of dit een exportify CSV is.
```

---

## Variant — user asks for `--execute` or `--dry-run`

User says "doe een dry-run van log-import House".

Skill explains (without invoking):

> "`log-import` heeft geen dry-run modus — het is een lokale operatie en raakt Spotify niet aan. Het schrijft alleen naar `.adds_log.json`. Wil je `m gewoon draaien? Je kunt achteraf de wijziging zien in `.adds_log.json`."

Then **AskUserQuestion** to proceed or cancel.

---

## Variant — user asks to seed multiple playlists

User says "seed mijn House, Techno en DnB logs van hun csvs".

Skill clarifies via **AskUserQuestion** that `log-import` is one-playlist-per-run and asks which to do first:

> "`log-import` doet één playlist tegelijk. Met welke wil je beginnen?"
> - **House** (`exportify-exports/House.csv`)
> - **Techno** (`exportify-exports/Techno.csv`)
> - **Drum & Bass** (`exportify-exports/Drum_&_Bass.csv`)

After the first run completes, the skill loops back and offers the next.
