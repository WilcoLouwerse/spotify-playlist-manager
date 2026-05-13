# Plan template

Use this shape when rendering the planned edit in step 6 of SKILL.md. Render only the sections that actually change. Quote names verbatim. Always show the IDs the user is committing to — they have to live with them.

---

## Sub-flow C: extend an existing playlists.json

```
Voorgestelde wijziging aan playlists.json:

  + "playlists" -> "<Display Name>": "<22-char-id>"
  + "playlists" -> "<Display Name 2>": "<22-char-id-2>"

  (optional, only if user offered an alias)
  + "aliases" -> "<shorthand>": "<Display Name>"

  (optional, only if user chose a category bucket)
  + "categories" -> "<genre|mood|theme>" += "<Display Name>"

  (optional, only if user offered a special rule)
  + "special_rules" -> "<Display Name>": "<rule prose verbatim>"

Bestaande entries blijven ongewijzigd.
```

---

## Sub-flow B: bootstrap a new playlists.json

```
Voorgestelde nieuwe playlists.json (gebaseerd op playlists.example.json):

  "playlists":      {N} entries  — <comma-separated names>
  "aliases":        {M} entries  — <comma-separated shorthand→canonical>
  "categories":
    genre:          {K} entries
    mood:           {K} entries
    theme:          {K} entries
  "special_rules":  {S} entries
  "catch_all":      "<Display Name>" (threshold {T})

Volledig bestand: {N_lines} regels. Wil je een preview zien voor je commit?
```

If the user asks to see the full file, render it as a fenced JSON block. Otherwise keep the structural summary — full pastes clutter chat.

---

## Verification step (step 9)

After the edit, surface `list-playlists` output verbatim:

```
Verificatie:
$ .venv/bin/python playlist_manager.py list-playlists
- <Display Name>
- <Display Name 2>
- ...
```

If `load_config` errors out instead, render the error verbatim and offer rollback via **AskUserQuestion**:

- **Rol terug** — revert `playlists.json` to the prior state (use the original Read content captured before the Edit).
- **Ik fix het zelf** — leave the file as-is, end the flow.
