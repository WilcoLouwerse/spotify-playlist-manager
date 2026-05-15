---
name: playlist-match
description: Classifies a shared song's genres with confidence scores, recommends matching playlists from playlists.json, and can add the track via the project's add command — fires on 'Artist - Title', Spotify URLs, or 'welke playlist past hierbij'.
metadata:
  category: Workflow
  tags: [music, genre-classification, playlist-matching, spotify, dutch]
---

# Playlist Match

Analyzes any song the user shares in the chat, identifies its musical genres with confidence scores, recommends 1-5 playlists from the project's playlist taxonomy, and — when the user asks — adds the track to one or more of the recommended playlists via the project's existing CLI ([playlist_manager.py](../../../playlist_manager.py)).

User-facing prose is **Dutch** (the user authored the format spec in Dutch). Keep this file, references, templates, and examples in English so triggers and steering stay model-readable.

**Input**: A song name (`Artist - Title`), a Spotify track URL/URI/ID, or any message asking "welke playlist past hierbij" / "wat voor genre is X" / "classify this track". May also be a follow-up message responding to the most recent analysis (a natural-language request like "voeg toe aan House", or an answer selected via `AskUserQuestion`).

**Source of truth**: The playlist list is [`playlists.json`](../../../playlists.json) at the repo root. Read it each run so user edits (added, renamed, removed playlists) are honored. **Never recommend `Random sht`** — it is the script-side catch-all under `catch_all` and must not appear in user-facing output.

**Conversation memory**: Track which songs and artists have already been covered in this chat so artist info isn't repeated, and so follow-up answers resolve against the most recent analysis.

**No single-letter shortcuts.** Older versions of this skill accepted `A`–`F` / `Z`/`Y`/`X`/`W` / `?` as shortcuts. That mechanic is gone — every follow-up is driven by **AskUserQuestion** instead. If the user types a single letter, treat it as an unrelated message (or ask via AskUserQuestion which follow-up they meant).

---

## Steps

1. **Detect input type**

   Classify the message:
   - **New analysis** — names a song, pastes a Spotify track URL, or asks which playlist fits.
   - **Natural-language follow-up** — references the prior analysis without going through AskUserQuestion, e.g. "voeg toe aan House" / "meer over de artiest" / "wat voor album is dit". Route directly to the matching follow-up step.
   - **Other** — out of scope. Hand back to the surrounding agent; do not produce an analysis. But before handing off, check whether a sibling skill is the right fit and mention it in Dutch:
     - User wants to **sort / triage a whole playlist** into target playlists → `/playlist-triage`
     - User wants to **find tracks in a playlist that fit one specific target** → `/playlist-scan`
     - User wants to **remove a track** from a playlist → `/playlist-remove`
     - User wants to **audit a playlist** (check if existing tracks match its genre/theme) → `/playlist-audit`
     - User wants to **add or sync playlists in the config** (`playlists.json`) → `/playlist-config`
     - User wants to **seed the duplicate guard** from an Exportify export → `/playlist-log-import`

   For follow-ups jump to step 9.

2. **Read the taxonomy**

   Read [`playlists.json`](../../../playlists.json). The legal recommendations are the union of `categories.genre`, `categories.mood`, and `categories.theme`. Honor `special_rules` (Funny meme / Ket420 / Hooyah / Electronic Music) literally. See `references/playlists.md`.

   If the user mentions a playlist that is not in the file, note it and suggest `/playlist-config` to add it before continuing with the analysis.

3. **Identify the song**

   Resolve the input to `Artist - Title`. If the user gave a Spotify URL/URI/ID, **remember it** for step 10 — you will need it to invoke `add`. If only a name was given, the URL is unknown for now.

4. **Check chat memory for the artist**

   Scan the conversation for prior analyses of the same artist. If covered, **skip** the artist info block in the output. Otherwise produce a 1-2 sentence artist description.

5. **Determine genres**

   Follow `references/genre-sources.md`. In short:
   - **Default = Claude + live web lookup.** Use **WebSearch** and **WebFetch** to pull current data from **multiple independent sources** (AllMusic, Wikipedia, RateYourMusic, Discogs, Last.fm, label / artist sites). This is the most accurate and up-to-date path and is always tried first — never skip straight to training recall when web tools are available.
   - Score each genre with a confidence percentage and a short reason; always note which web source(s) corroborated it.
   - Training-data recall is the **last resort**, only after web lookups fail or contradict sharply — and only via the explicit "Inschatten zonder internet (Claude + OpenAI)" path in the uncertainty fork. That path runs the project's read-only `analyze-only` command to get an OpenAI training-data second opinion and combines it with Claude's own training recall (capped at 75% on agreement, 60% on disagreement). If OpenAI is unavailable (no API key / quota / auth / network) the skill falls back to Claude-only and tells the user explicitly which OpenAI failure mode triggered the fallback.
   - If sources strongly conflict and no clear winner emerges, treat as **uncertain** and jump to step 7.

6. **Match playlists**

   Pick **1 to 5** playlists from the taxonomy. For each, output `name — X% — reason`. Match on genre, BPM/energy, vibe, mood, lyrics, production, cultural/meme context, listening scenario. **Never match purely on artist name.**

   - Special playlists (Funny meme / Ket420 / Hooyah) only when the song clearly meets the rule.
   - When you suggest any electronic subgenre (House, Techno, Trance, Drum & Bass, Dubstep / Bass, Hardstyle & Hardcore, Synthwave), **also** suggest `Electronic Music` — it is an inclusive umbrella, not a fallback (`special_rules` in `playlists.json`).
   - If no playlist sensibly fits, say so plainly in the output — do not force a low-confidence match.

7. **Uncertainty fork**

   If you cannot confidently determine genres, render the prefix message from `templates/uncertainty.md`, then call **AskUserQuestion** with the four uncertainty options (estimate from artist / use less-reliable source / combine both / skip genres, match playlists only). Wait for the user's reply before continuing. When the user answers, use the response format in `references/output-rules.md` (the "Uncertainty response" section).

8. **Render the analysis, then ask the follow-up question**

   Use `templates/full-analysis.md`. The numbered scaffolding (1./2./...) is internal; never print step numbers. Sections in order:

   1. Title — `Artiestnaam - Nummernaam`
   2. **Artiestinformatie** — only if the artist is new in this chat
   3. **Nummeromschrijving** — one sentence
   4. **Genres** — bulleted, each `— X% — reason`
   5. **Playlist match** — bulleted, each `— X% — reason`

   **Immediately after** the analysis text, call **AskUserQuestion** with the standard follow-up menu. The four button options are the most-frequent actions; less common asks go through the free-text "Other" field. See `templates/followup.md` for the exact wording.

   For a worked example, see `examples/full-analysis.md`.

9. **Handle follow-up choices**

   When the user picks an option (or types a natural-language request), answer **only** that one — never re-render the full analysis. After the answer, call **AskUserQuestion** again with the follow-up menu (including a "Klaar" option) so the user can pick another action or end the flow. See `templates/followup.md`.

   Supported follow-up actions:
   - **Meer over de artiest** — extended bio
   - **Meer over het nummer** — deeper song analysis (lyrics, meaning, message)
   - **Album & albumhoes** — album name + link to the cover-art image
   - **Streaming links** — links to YouTube, Spotify, and other platforms
   - **Uitgebreide playlist-analyse** — why each playlist does / does not fit + alternatives
   - **Voeg toe aan playlists** — add this song to one or more of the recommended playlists (step 10)

   If the user's free-text reply doesn't map clearly to one of the actions, call **AskUserQuestion** again to disambiguate; do not guess.

10. **Add the song to recommended playlists**

    Triggered when the user picks **Voeg toe aan playlists** or sends a natural-language add request. Follow `references/add-command.md`. Compressed flow:

    a. **Need a Spotify URL/URI/ID.** If the original input was a URL/URI/ID, use it. If not, use **AskUserQuestion** to ask the user to paste one. Do not invent or guess a track ID.

    b. **Pick playlists.** Use **AskUserQuestion** with `multiSelect: true` listing the playlists you recommended in step 6 (only those — not the full taxonomy). Optionally let the user choose **all recommended**.

    c. **Show the commands you are about to run** using `templates/add-confirmation.md`. One `add` invocation per playlist, always with `--execute`:

       ```bash
       .venv/bin/python playlist_manager.py add "<url>" "<Playlist Name>" --execute
       ```

       Run from the repo root. Quote playlist names verbatim from `playlists.json` (the script accepts aliases too, but exact names are unambiguous).

    d. **Confirm before running.** Use **AskUserQuestion** ("Klaar om deze commando's uit te voeren?"). Only proceed on explicit yes. This confirmation is **mandatory** — it replaces the old dry-run safety net.

    e. **Run** each command via **Bash** sequentially. Report the script's output back to the user verbatim — it tells them `ADD` or `SKIP (already in playlist)`. Do not paraphrase the script's own messages.

    f. **No `smart-add` fallback — Claude AI is the classifier.** The project's `smart-add` command calls OpenAI to pick playlists. This skill does **not** invoke it. Claude AI already classified the song in steps 5–6 with multi-source analysis that is more rigorous than `smart-add`'s single OpenAI call. If the user says "let the classifier decide", "use smart-add", or "let AI pick the playlists", explain that Claude AI is the classifier here and re-do the analysis with whatever framing they want (different sources, stricter confidence band, only electronic subgenres, broader sweep, etc.) — then loop step 10's `add` calls over the resulting picks. Never shell out to `smart-add` (or any OpenAI-driven command) from this skill.

11. **Capture Learnings**

    If anything was non-obvious this run (a tricky classification, a source disagreement, a playlist edge case, a follow-up that revealed a missing rule, an `add` invocation that surprised the user), append a dated entry to `learning-candidates.md` under the matching section. Promote a candidate to `learnings.md` only after the same observation recurs across 3+ analyses or fixes a measured eval failure. Skip if nothing new came up.

---

## Guardrails

- **Always** start genre identification with live web lookup via **WebSearch** + **WebFetch** against the sources in `references/genre-sources.md`. This is the most accurate and most up-to-date path and is the first thing tried — never skip to training-data recall when web tools are available.
- **Never** base a genre claim solely on the artist's overall reputation. Cross-check with multiple sources, scoped to the specific track when possible.
- **Never** recommend `Random sht`. It is the script-side fallback under `playlists.json -> catch_all` and must not appear in user-facing output.
- **Never** recommend a playlist that is not currently present in `playlists.json -> categories`. Read the file each run; user edits are authoritative.
- **Never** print the internal step numbers (1./2./3./...) from the templates in user-facing output. They are an authoring scaffold only.
- **Never** invoke `playlist_manager.py add` without explicit user confirmation in the same turn — call **AskUserQuestion** to confirm before running any python script.
- **Never** invoke `smart-add` from this skill. `smart-add` writes to Spotify after classifying with OpenAI; Claude AI is the writer's classifier here, so use `add` directly.
- **May** invoke the read-only `analyze-only` command **only** in the "Inschatten zonder internet (Claude + OpenAI)" path of the uncertainty fork. It calls OpenAI for a training-data second opinion without touching Spotify. Always combine the result with Claude's own training recall; fall back to Claude-only with an explicit reason message when OpenAI fails (no API key, quota, auth, connection, invalid JSON, validation rejection). Never use it as the default classifier — web lookup is still primary.
- **Never** invent or guess a Spotify track ID. If the user only gave you `Artist - Title`, ask for a URL via **AskUserQuestion** before invoking `add`.
- **Never** invoke `add` for a playlist that was not in the list you recommended in step 6 — unless the user explicitly typed a different one.
- **Never** print the old letter-shortcut menu (A-F / Z/Y/X/W / ?). All follow-ups go through **AskUserQuestion**.
- When genre sources disagree strongly, default to the **uncertainty flow** via **AskUserQuestion**. Do not silently pick a single source.
- User-facing text is **Dutch**. Playlist names stay verbatim from `playlists.json` (don't translate them).
- Follow-up answers reply to **only** the chosen action — never re-render the full analysis.
- If you cannot identify the song at all, say so plainly; do not invent a track.
