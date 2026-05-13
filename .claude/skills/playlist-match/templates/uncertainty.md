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

## Step 2 — call AskUserQuestion with the four uncertainty options

Use exactly this structure:

```
question: "Hoe wil je dat ik hiermee verder ga?"
header:   "Genre-aanpak"
multiSelect: false
options:
  - label:       "Schat op basis van artiest"
    description: "Gebruik artiestbrede tags / reputatie als bron, scope = artiestgebaseerd."
  - label:       "Minder betrouwbare bron"
    description: "Vertrouw op Last.fm tags, SoundCloud-tag of vergelijkbare losse signalen."
  - label:       "Combineer beide"
    description: "Artiestbron én minder-betrouwbare bron samen wegen."
  - label:       "Sla genres over"
    description: "Alleen playlist matching, geen harde genreclaim."
```

The labels map to the old letter shortcuts as follows (for internal reasoning only — never expose):
- "Schat op basis van artiest" ≡ old `Z`
- "Minder betrouwbare bron" ≡ old `Y`
- "Combineer beide" ≡ old `X`
- "Sla genres over" ≡ old `W`

Wait for the user's reply before producing any genres or playlist matches. When the user picks an option, switch to the response format in `references/output-rules.md → "Uncertainty response"`.
