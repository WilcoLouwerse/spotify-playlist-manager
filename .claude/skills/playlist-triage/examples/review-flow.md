# Example — review-playlist flow

User message:

> "kun je deze playlist voor me reviewen? https://open.spotify.com/playlist/3aBcDeFgHiJkLmNoPqRsTu"

The user said "reviewen" → route to `review-playlist`.

---

## Step 1-3 — detect, resolve, pick workflow

Source resolved: `https://open.spotify.com/playlist/3aBcDeFgHiJkLmNoPqRsTu` (URL form, pass verbatim).

Workflow chosen automatically: **review-playlist** (user said "reviewen"). No AskUserQuestion needed at this step — but the skill can confirm via a single AskUserQuestion if it wants to be defensive.

## Step 4 — tuning

No tuning hints in the user's message. Use defaults: `--max-playlists 3 --min-confidence 80` (these are the script defaults, so they don't need to appear on the command line).

## Step 5 — mode

**AskUserQuestion**:

> "Hoe wil je dit draaien?"
> - **Dry-run** *(aanbevolen)* — toon het plan, schrijf niets.
> - **Execute** — schrijf direct, met per-nummer y/N in je terminal.

User picks **Dry-run**.

## Step 6 — plan

```
Je wilt https://open.spotify.com/playlist/3aBcDeFgHiJkLmNoPqRsTu triëren via review-playlist (dry-run).

Ik ga dit commando draaien vanuit de repo-root:

yes | .venv/bin/python playlist_manager.py review-playlist "https://open.spotify.com/playlist/3aBcDeFgHiJkLmNoPqRsTu"

Dit is een dry-run — ik beantwoord de prompts automatisch met y, maar zonder --execute wordt er niets geschreven.
```

## Step 8 — run

Skill runs the command. Output (script's own format, verbatim):

```
Reviewing source: To triage (3aBcDeFgHiJkLmNoPqRsTu)

============================================================
Track 1/22: Bakermat - Walk That Walk
============================================================

Suggested playlists:
- House — 92% — uplifting deep-house with vocals
- Party — 84% — high-energy festival vibe

Add this track to these playlists? [y/N/s/q]:
- House: DRY RUN (would add)
- Party: DRY RUN (would add)

...

============================================================
Review complete (DRY RUN): accepted 22, skipped 0, reviewed 22/22.
```

The `yes |` pipe answered every prompt with `y`; without `--execute` nothing was written.

## Step 9 — summary

```
Dry-run klaar — 22 kandidaten verdeeld over verschillende playlists. Niets geschreven.
```

## Variant — user wants to execute

After dry-run, user says "OK voer 'm uit". The skill goes back to step 5 (mode = execute) and step 6 (plan), then step 7:

**AskUserQuestion**:

> "Hoe wil je 'm draaien?"
> - **Run vanuit mijn terminal** — review-playlist heeft per-track y/N prompts; ik kan die niet vanuit chat invullen.
> - **Annuleren** — terug.

Skill shows:

```
Draai dit zelf vanuit de repo-root:

.venv/bin/python playlist_manager.py review-playlist "https://open.spotify.com/playlist/3aBcDeFgHiJkLmNoPqRsTu" --execute

Per nummer krijg je een prompt: y = toevoegen aan alle suggesties, N = overslaan, s = skip (gelijk aan N), q = stoppen.
```

Skill does NOT run the command — it's terminal-only for review-playlist.
