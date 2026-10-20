# Audit Report Template

Use this format when rendering the audit results in step 6 of the skill. All prose is **Dutch**. Playlist names stay verbatim.

---

## Format

```
**{Playlist} — {N} nummers geauditeerd**

✅ {high}  nummers  ≥80% match (past goed)
⚠️ {med}   nummers  60–79% match (twijfelachtig)
❌ {low}   nummers  <60% match (past slecht)
{skipped}  nummers  geen data (niet gevonden)   ← omit line if 0

**Nummers met lage match (kandidaten voor verwijdering):**
— {confidence}% — {Artist} - {Title}
       Reden: {one-line reason in Dutch}
       URI: {uri}                               ← show URI so skill can build the remove command
— {confidence}% — {Artist} - {Title}
       Reden: {one-line reason in Dutch}
       URI: {uri}
```

**Notes:**
- Omit the "geen data" line when `skipped` is 0.
- Order low-confidence tracks by ascending confidence (lowest first).
- Include ⚠️ tracks in the candidate list only if the user picks a threshold above 60% (70% or 80%) — by default show ❌ only.
- For the quick mode (OpenAI CLI), map the CLI output directly into this format rather than re-formatting from scratch.
- Never show the `Random sht` playlist in reasons or comparisons.

---

## Example (web-first, House playlist, 12 tracks)

```
**House — 12 nummers geauditeerd**

✅ 9  nummers  ≥80% match (past goed)
⚠️ 2  nummers  60–79% match (twijfelachtig)
❌ 1  nummer   <60% match (past slecht)

**Nummers met lage match (kandidaten voor verwijdering):**
— 38% — The Weeknd - Blinding Lights
       Reden: synth-pop en dark R&B; geen house-kenmerken (AllMusic: synth-pop, Wikipedia: dark pop)
       URI: spotify:track:0VjIjW4GlUZAMYd2vXMi3b
```

---

## After the report

Immediately follow the report with the threshold question (step 7 of the skill). Do not add commentary between the report block and the AskUserQuestion call.
