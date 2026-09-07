# Baseline response — eval-2: Artist-Title only (without_skill)

Baseline searched the web for the track ID, found ambiguous results, then offered two options:

```
python playlist_manager.py remove "39LLxExYz6ewLAcYrzQQyP" "Techno" --execute
# or
python playlist_manager.py remove "0v2boHmWtxMTD2REGN8MbK" "Techno" --execute
```

(Both returned SKIP in dev mode — playlist membership cannot be confirmed.)

**Key difference from with_skill:**
- Baseline: searched the web to guess the track ID (introduces ambiguity — multiple versions of Levitating exist)
- With skill: immediately asks user for a Spotify URL via AskUserQuestion — never guesses or invents an ID

The baseline's approach is riskier because searching the web for track IDs can return the wrong version.
