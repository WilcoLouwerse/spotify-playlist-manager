# Uncertainty prompt template

**Only fires after the default flow has failed.** The default is Claude + live web lookup via WebSearch/WebFetch on AllMusic, Wikipedia, RYM, Discogs, etc. (`references/genre-sources.md`). This menu appears only when those web lookups returned nothing usable or contradicted sharply — never as a shortcut to skip web lookup.

## Step 1 — print the lead-in line

Print only this line in chat (Dutch, with `{REASON}` filled in). The reason should make clear that **web lookups were tried** and what specifically failed.

```
Sorry, ik heb moeite om de genres voor dit nummer te vinden. {REASON}
```

`{REASON}` examples (one short sentence in Dutch — always reference the web lookups that were tried):
- "Ik heb AllMusic, Wikipedia en RYM opgezocht, maar de bronnen staan haaks op elkaar — geen consensus op trackniveau."
- "WebFetch op AllMusic/Wikipedia leverde geen track-level info op; alleen artiestbrede tags, en die overlappen meerdere genres."
- "Het nummer staat niet op de gangbare bronnen (AllMusic, RYM, Wikipedia geven 404); alleen Last.fm tags zijn beschikbaar, en die spreken elkaar tegen."

## Step 2 — call AskUserQuestion with the uncertainty options

The options are ordered by accuracy. The first three still use **WebFetch/WebSearch** — they just broaden or weaken the source. **"Inschatten zonder internet (Claude + OpenAI)" is the last resort** (Claude training recall plus the read-only `analyze-only` second opinion; confidence caps in the flow below). Never substitute `smart-add` for any of these.

```
question: "Web-lookups gaven geen duidelijk antwoord. Hoe wil je dat ik hiermee verder ga?"
header:   "Genre-aanpak"
multiSelect: false
options:
  - label:       "Breder zoeken (artiestpagina's)"
    description: "Verbreed de WebFetch/WebSearch naar artiestbrede pagina's (artiestpagina op AllMusic/Wikipedia/RYM/Last.fm). Scope wordt artiestgebaseerd."
  - label:       "Zwakkere webbronnen"
    description: "Val terug op zwakkere webbronnen (Last.fm tags, SoundCloud-tag, Bandcamp-tag) via WebFetch. Lagere precisie, hogere recall."
  - label:       "Sla genres over"
    description: "Alleen playlist matching, geen harde genreclaim."
  - label:       "Inschatten zonder internet (Claude + OpenAI)"
    description: "Laatste redmiddel: Claude én OpenAI schatten in op basis van hun trainingsdata. OpenAI wordt via analyze-only (read-only, geen Spotify writes) aangeroepen. Als OpenAI niet beschikbaar is wordt dit gemeld en valt de skill terug op Claude alleen."
```

Legacy label mapping (for internal reasoning only — never expose):
- "Breder zoeken (artiestpagina's)" ≡ old `Z` ("Schat op basis van artiest") — but now web-driven
- "Zwakkere webbronnen" ≡ old `Y` ("Minder betrouwbare bron") — but explicitly via WebFetch
- "Sla genres over" ≡ old `W`
- "Inschatten zonder internet (Claude + OpenAI)" — new, dual-training-data last resort

Wait for the user's reply before producing any genres or playlist matches. When the user picks an option, switch to the response format in `references/output-rules.md → "Uncertainty response"`.

### "Inschatten zonder internet (Claude + OpenAI)" — step-by-step flow

This option is the **true last resort** — chosen when even broadened web lookups fail or the user wants a fast offline answer. The skill combines two training-data sources for a cross-check. Never invokes `smart-add` (writes to Spotify); only the read-only `analyze-only` command is used.

**Step A — need a Spotify URL/URI/ID for analyze-only.**
If the original input included one, use it. If not, call **AskUserQuestion**:
> "Voor de OpenAI-check heb ik een Spotify-link of track-ID nodig. Plak die via 'Other', of kies 'Alleen Claude' om OpenAI over te slaan."
> - **Alleen Claude** — sla OpenAI over, gebruik Claude interne kennis.

If the user pastes a URL → proceed to Step B. If they pick "Alleen Claude" → skip to the Claude-only output shape below.

**Step B — run Claude's own training-recall classification first** (genres + playlist matches). Hold the result; do not render it yet.

**Step C — run analyze-only via Bash:**
```bash
.venv/bin/python playlist_manager.py analyze-only "<spotify-url-or-id>"
```
Run from the repo root.

**Step D — detect OpenAI failure.** If stdout contains any of these strings, OpenAI has failed:
- `OPENAI_API_KEY not set in .env`  → reason: "geen API key"
- `OpenAI: insufficient quota`       → reason: "quota op"
- `OpenAI rate-limited`              → reason: "rate limit"
- `OpenAI: authentication failed`    → reason: "API key ongeldig"
- `OpenAI: connection error`         → reason: "geen verbinding"
- `OpenAI API error`                 → reason: "API fout"
- `OpenAI returned invalid JSON`     → reason: "ongeldig JSON"
- `OpenAI classification rejected`   → reason: "classificatie afgewezen"

On failure → **fall back to Claude-only output shape** (below), prepend the failure notification.

**Step E — combine on success.** Parse OpenAI's genre and playlist rows from stdout. Drop any `Random sht` / catch-all row first: `analyze-only` appends it when no match reaches the catch-all threshold, and it is the script's fallback, not a classification. Merge with Claude's results:

- **Both agree on a genre/playlist (within ±15 pp)** → publish one row, average the confidences, cap at **75%**, label `bron: Claude + OpenAI (interne kennis), betrouwbaarheid: middel`.
- **One source has it, the other doesn't** → publish it with the single source's confidence, cap at **65%**, label `bron: Claude (interne kennis)` or `bron: OpenAI (interne kennis)` as appropriate, note the other source didn't mention it.
- **Both have it but strongly disagree (>15 pp gap or contradicting genre labels)** → publish both rows separately, each capped at **60%**, note the disagreement.

---

#### Claude-only output shape (OpenAI unavailable or skipped)

Add a notification line **before** the genre block:

```
⚠️ OpenAI was niet beschikbaar ({reden}). Alleen Claude's interne kennis is gebruikt.
```

Then render genres and playlists from Claude's training recall:
- `bron: Claude (interne kennis)`
- `betrouwbaarheid: laag` (default); `middel` only for well-known tracks
- `scope:` — `nummerspecifiek` if Claude knows this specific track; `artiestgebaseerd` otherwise
- One-line caveat: "AI-only inschatting, niet gestaafd door externe bronnen."
- Cap individual genre confidences at **70%**.
