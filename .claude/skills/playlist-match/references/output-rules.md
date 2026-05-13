# Output Rules

Formatting contract for the analysis, the uncertainty fork, and follow-up answers. All user-facing prose is **Dutch**.

---

## Headers and bullet format

- Section headers use bold Dutch labels: **Artiestinformatie:**, **Nummeromschrijving:**, **Genres:**, **Playlist match:**.
- Bullets use ` - ` (single hyphen + space).
- Confidence rendering: `Name — XX% — reason`. Use an em-dash (`—`), not a hyphen, between fields.
- Round percentages to integers; never use decimals.
- Keep reasons under ~14 words.

---

## Title format

```
Artiestnaam - Nummernaam
```

Use the artist's real / commonly-cited name and the official track title. Don't translate. Don't add quotes.

---

## When the song's genres can't be determined confidently

Print **only** this lead-in line in chat (Dutch):

```
Sorry, ik heb moeite om de genres voor dit nummer te vinden. [korte uitleg waarom]
```

Then call **AskUserQuestion** with the four uncertainty options from `templates/uncertainty.md`:
- "Schat op basis van artiest"
- "Minder betrouwbare bron"
- "Combineer beide"
- "Sla genres over"

Do not print the option list as chat text — the user picks via the UI prompt. Wait for the user's reply before continuing.

---

## Uncertainty response

When the user picks one of the four uncertainty options, respond with:

```
Oké! Op basis van je keuze ('[gekozen label]') zou ik zeggen dat dit nummer de volgende genres en playlist matches heeft:

Genres:
- [genre] — [confidence]% — [korte uitleg], bron: [bron], betrouwbaarheid: [hoog/middel/laag], scope: [nummerspecifiek/artiestgebaseerd]
  [eventuele tegenstrijdigheden tussen bronnen]

Playlist matches:
- [playlist] — [confidence]% — [reden]
```

Then call **AskUserQuestion** again (per `templates/followup.md`) so the user can pick another action or stop.

For each genre entry, **always include**: confidence %, source, reliability level, scope (track-specific or artist-based), and any source disagreement noted in `references/genre-sources.md`.

The "Sla genres over" option is special: skip the Genres section entirely and only render Playlist matches with a one-line note that no hard genre claim was made.

---

## Choice menu (after every full analysis)

There is no printed letter menu. After the Playlist match block, the skill calls **AskUserQuestion** with the menu in `templates/followup.md`. The user picks a button or types a free-text reply.

---

## Follow-up rules

- Answer **only** the chosen action — never re-paste the full analysis.
- No closing footer in chat — after the answer, call **AskUserQuestion** again (per `templates/followup.md`) so the user can chain another action or pick "Klaar".
- For the add action, follow the detailed flow in `references/add-command.md`.

---

## What never to print

- The internal step numbers (1./2./3./...) from the analysis template — those are scaffolding only.
- The old A-F / Z/Y/X/W / `?` letter menus — they are removed; every follow-up goes through **AskUserQuestion**.
- The old footer line "*Wil je een andere optie proberen? Reageer dan met de bijbehorende letter...*" — gone with the letter mechanic.
- `Random sht` as a playlist suggestion.
- A playlist not in `playlists.json -> categories`.
- Guessed track IDs or invented Spotify URLs.
- A "confidence: high/medium/low" qualifier *instead of* a percentage — always show the number.
