# Full analysis output template

Fill the placeholders with the values you produced in steps 3-6 of `SKILL.md`. **Do not** print the leading numbers in `## 1.`, `## 2.`, etc. — they are authoring labels only. Omit the artist info block entirely if the artist was already covered earlier in the chat.

There is **no longer a printed choice menu** at the bottom of the analysis. After the Playlist match block, the skill calls **AskUserQuestion** (see `templates/followup.md`) to offer the next action. Do not print A-F letters, do not echo the AskUserQuestion options into the chat output.

---

## 1. Title

```
{ARTIST} - {TITLE}
```

## 2. Artist info — *only if the artist is new in this chat*

```
**Artiestinformatie:**
{1-2 zinnen over de artiest in het Nederlands. Genre / herkomst / kort iets karakteristieks.}
```

## 3. Song description — *always*

```
**Nummeromschrijving:**
{Eén zin in het Nederlands die het nummer beschrijft: vibe + opvallende productie- of compositiekeuze.}
```

## 4. Genres — *always*

```
**Genres:**
- {Genre 1} — {XX}% — {korte reden, ≤14 woorden}
- {Genre 2} — {XX}% — {korte reden}
- ...
```

Use 1-4 genres. Confidence per the bands in `references/genre-sources.md`. Reasons in English or Dutch; whichever is more natural for the source signal (musical terms like "djent" stay verbatim).

## 5. Playlist match — *always*

```
**Playlist match:**
- {Playlistnaam} — {XX}% — {korte reden}
- {Playlistnaam} — {XX}% — {korte reden}
- ...
```

1-5 entries. Playlist names verbatim from `playlists.json`. If you suggest any electronic subgenre, also include `Electronic Music`. Never include `Random sht`.

If genuinely nothing fits:

```
**Playlist match:**
Geen van de opgegeven playlists past hier echt — dit nummer valt buiten het bereik van de huidige lijst.
```

## 6. Follow-up — *always, via AskUserQuestion (not printed)*

Immediately after the analysis, call **AskUserQuestion** with the menu in `templates/followup.md`. Do not also print the menu in the chat — the user sees it in the UI prompt.

---

## Assembly order in the response

1. Title (no header — just the line `Artist - Title` as the section heading)
2. Artist info (if new)
3. Song description
4. Genres
5. Playlist match
6. AskUserQuestion call (not chat text)

No greeting, no closing line, no summary, no letter menu.
