# Uncertainty prompt template

Use when genre sources contradict sharply or the song's genre can't be pinned down.

## Step 1 — print the lead-in line

Print only this line in chat (Dutch, with `{REASON}` filled in):

```
Sorry, ik heb moeite om de genres voor dit nummer te vinden. {REASON}
```

`{REASON}` examples (one short sentence in Dutch):
- "AllMusic en Wikipedia staan haaks op elkaar — geen consensus op trackniveau."
- "Geen track-level info gevonden; alleen artiestbrede tags, en die overlappen meerdere genres."
- "Het nummer staat niet duidelijk op de gangbare bronnen — alleen Last.fm tags, en die spreken elkaar tegen."

## Step 2 — call AskUserQuestion with the uncertainty options

Use exactly this structure. **"Laat Claude inschatten" is listed first because it is the recommended fallback** when external genre sources have failed — Claude AI uses its own training knowledge to make a best-effort call, with explicit reliability caveats in the response. Never substitute OpenAI / `smart-add` here.

```
question: "Hoe wil je dat ik hiermee verder ga?"
header:   "Genre-aanpak"
multiSelect: false
options:
  - label:       "Laat Claude inschatten"
    description: "Claude AI doet een best-effort schatting op basis van interne kennis, met expliciete betrouwbaarheidscaveats. Geen OpenAI / smart-add."
  - label:       "Schat op basis van artiest"
    description: "Gebruik artiestbrede tags / reputatie als bron, scope = artiestgebaseerd."
  - label:       "Minder betrouwbare bron"
    description: "Vertrouw op Last.fm tags, SoundCloud-tag of vergelijkbare losse signalen."
  - label:       "Sla genres over"
    description: "Alleen playlist matching, geen harde genreclaim."
```

Note: the older "Combineer beide" option is gone — "Laat Claude inschatten" subsumes it (Claude AI combines whatever signals it has, weighted by its own reliability assessment). The labels for legacy reference (for internal reasoning only — never expose):
- "Laat Claude inschatten" — new, primary Claude-AI fallback
- "Schat op basis van artiest" ≡ old `Z`
- "Minder betrouwbare bron" ≡ old `Y`
- "Sla genres over" ≡ old `W`

Wait for the user's reply before producing any genres or playlist matches. When the user picks an option, switch to the response format in `references/output-rules.md → "Uncertainty response"`.

### "Laat Claude inschatten" — specific response shape

When the user picks this option, Claude AI produces the analysis from its own training knowledge. Each genre row must include:

- `bron: Claude (interne kennis)`
- `betrouwbaarheid: laag` (default) — only mark `middel` if the song / artist is well-known enough that Claude has high-confidence internal knowledge.
- `scope:` — `nummerspecifiek` if Claude knows this specific track; `artiestgebaseerd` otherwise.
- A one-line caveat noting this is an AI-only estimate, not a cross-checked source claim.

Cap individual genre confidences at **70%** when the only source is Claude's internal knowledge — never publish 80%+ without external corroboration.
