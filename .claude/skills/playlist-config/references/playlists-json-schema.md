## playlists.json schema

Canonical reference: [`playlists.example.json`](../../../../playlists.example.json). What follows is the rule-by-rule contract `load_config` enforces, so the skill can validate proposed edits before writing.

---

## Top-level keys

| Key | Required | Shape | Notes |
|-----|:---:|-------|-------|
| `playlists` | **Yes** | `{ "<Display Name>": "<22-char Spotify ID>", ... }` | The registry of writable target playlists. Every other section references these keys. |
| `aliases` | No | `{ "<shorthand>": "<canonical key in playlists>", ... }` | Case-insensitive shorthand lookup for CLI commands. The **value** must be an exact key under `playlists`. |
| `categories` | No | `{ "genre": [...], "mood": [...], "theme": [...] }` | Buckets shown to the OpenAI classifier in `smart-add`. Each list entry must be an exact key under `playlists`. |
| `special_rules` | No | `{ "<playlist key>": "<rule prose>", ... }` | Per-playlist semantics injected into the classifier prompt. Keys must exist under `playlists`. |
| `catch_all` | No | `{ "playlist": "<key>", "threshold": <int 1-100>, "rule": "<prose>" }` | Programmatic fallback. `playlist` value must be a key under `playlists`. Default threshold: 85. |

If `playlists` is missing or empty, every CLI command fails at startup.

---

## Validation rules `load_config` enforces

These are the only rules the skill needs to pre-check before writing — anything else the script accepts.

1. **`aliases` values point to existing playlists.** Every value in `aliases` must be a key in `playlists`. Otherwise `load_config` raises and every CLI command refuses to run.
2. **`categories` entries point to existing playlists.** Same rule, per list under `genre` / `mood` / `theme`.
3. **`special_rules` keys point to existing playlists.** Same rule.
4. **`catch_all.playlist` points to an existing playlist.** Same rule.
5. **No duplicate IDs across `playlists`.** Two keys can point to the same ID, but it's almost always a copy-paste mistake — flag it via **AskUserQuestion** rather than silently accepting.
6. **IDs are 22 characters, base62-ish (alphanumeric).** Anything else is suspect; flag via **AskUserQuestion**.
7. **JSON is well-formed.** Trailing commas, smart quotes, or unquoted keys break the parser.

---

## Conventions (not enforced by `load_config`, but enforced by skill etiquette)

- **Key naming**: title-cased display names, with the natural punctuation the user uses in Spotify (`Drum & Bass`, `Rustig / 'anders'`, `Pop / Mainstream`). The key is what users see in `add` / `smart-add` output.
- **Alias lowercase**: keep alias keys lowercase. `load_config` lowercases at lookup time anyway, so mixed-case alias keys silently work but render inconsistently in diffs.
- **Categories are non-overlapping per axis**: a playlist usually belongs to exactly one of `genre` / `mood` / `theme`. Cross-listing is allowed but rarely helps the classifier.
- **`catch_all.playlist` is special**: it is **never** shown to the OpenAI classifier as a candidate. It's a script-side safety net. Don't add it to `categories` either — that would surface it as a regular target.
- **`special_rules` should be terse**: one or two sentences. The classifier prompt is already long.

---

## Things the skill should NOT do

- Don't reorder keys in `playlists` — preserve the user's hand-curated order so diffs stay readable.
- Don't rewrite `playlists.example.json` — it's the documented schema reference, not the live config.
- Don't add `categories` buckets beyond `genre` / `mood` / `theme` without asking — the `smart-add` prompt assumes these three.
- Don't auto-generate aliases from playlist names — wait for the user to offer one.
- Don't omit `aliases` / `categories` / `special_rules` / `catch_all` sections when they exist; only omit empty ones when **creating** a fresh file (sub-flow B).
