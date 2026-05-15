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

Then call **AskUserQuestion** with the four uncertainty options from `templates/uncertainty.md` — ordered by accuracy, with web-driven lookups before training-only recall:
- "Breder zoeken (artiestpagina's)" — broaden WebFetch/WebSearch to artist-level pages on AllMusic / Wikipedia / RYM / Last.fm.
- "Zwakkere webbronnen" — fall back to Last.fm tags / SoundCloud / Bandcamp via WebFetch.
- "Sla genres over" — no genre claim, playlist matching only.
- "Inschatten zonder internet (Claude + OpenAI)" — last resort: Claude training recall combined with OpenAI's `analyze-only` (read-only, no Spotify writes) as a second opinion. Falls back to Claude-only with an explicit notification when OpenAI is unavailable. Never `smart-add`.

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

The **"Inschatten zonder internet (Claude + OpenAI)"** option is the true last resort. Full step-by-step flow is in `templates/uncertainty.md`. Summary of response shapes:

- **Claude + OpenAI both available, agree:** `bron: Claude + OpenAI (interne kennis)`, `betrouwbaarheid: middel`, confidence averaged and capped at **75%**.
- **One source only:** `bron: Claude (interne kennis)` or `bron: OpenAI (interne kennis)`, capped at **65%**, note the other source didn't mention it.
- **Both present but disagree:** two rows, each capped at **60%**, disagreement noted.
- **OpenAI unavailable:** prepend `⚠️ OpenAI was niet beschikbaar ({reden}).` then render Claude-only rows: `bron: Claude (interne kennis)`, `betrouwbaarheid: laag` (or `middel` for well-known tracks), cap at **70%**, one-line AI-only caveat.

The "Breder zoeken (artiestpagina's)" and "Zwakkere webbronnen" options still use **WebFetch / WebSearch** — they just broaden the source. Genre entries from those paths get a real source name (e.g. `bron: Last.fm tags via WebFetch`, `bron: AllMusic artist page`) and `betrouwbaarheid: middel` or `laag` depending on how strong the source was.

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
