# Workflow choice — review vs bulk

Two commands cover the same source-to-many-targets workflow. The skill should pick the right one for the user's situation. See [`docs/commands.md`](../../../../docs/commands.md#review-playlist) and [`docs/commands.md → bulk-playlist`](../../../../docs/commands.md#bulk-playlist) for the authoritative behaviour.

---

## Quick comparison

|                       | `review-playlist`                       | `bulk-playlist`                                                  |
|-----------------------|-----------------------------------------|------------------------------------------------------------------|
| **Prompt cadence**    | Per-track `y/N/s/q`                     | Single `y/N` for the whole plan                                  |
| **Per-target control**| Yes — accept all suggested playlists for one track, or reject the whole track | No — a single y/N accepts the entire (track → playlist) plan     |
| **Cost**              | 1 OpenAI call per track + Spotify reads | Same                                                             |
| **Good for**          | 20–50 tracks where curation matters     | > 50 tracks where the user just wants them sorted                |
| **Default --max-playlists** | 3                                  | 3                                                                |
| **Default --min-playlists** | 1                                  | 1                                                                |
| **Default --min-confidence**| 80                                 | 80                                                               |

---

## How to recommend

Listen to the user's framing:

- "**review**", "**check**", "**curate**", "**een voor een**" → **review-playlist**
- "**sort**", "**drain**", "**empty**", "**leeghalen**", "**zet alles op de juiste plek**" → **bulk-playlist**
- "**triage**" / "**sorteer**" with no further qualifier → ask via **AskUserQuestion**. Default highlight: Claude + web for ≤ 20 tracks, review for 20–50, bulk for > 50 (see `SKILL.md` step 3).

If the source isn't loaded yet and the user hasn't framed it: ask via **AskUserQuestion** *after* the source is known, so the skill can include the track count in the question ("Je triage-playlist heeft 132 nummers — wil je per nummer beslissen of in één klap accepteren?").

---

## Interactive prompts and how the skill handles them

Both commands prompt on stdin. The skill can't drive those prompts from chat reliably:

| Command | Prompt | What the skill can do |
|---------|--------|------------------------|
| `review-playlist` (per-track) | `Add this track to these playlists? [y/N/s/q]:` | Dry-run via Bash with `yes \|` (nothing is written without `--execute`). For execute: tell the user to run it interactively from their terminal. |
| `bulk-playlist` (single y/N) | `Proceed? [y/N]:` | Dry-run via Bash with `yes \|`. For execute: offer the `yes \| ...` pipe (auto-accept). |

With `--execute`, the `yes |` pipe is safe **only** for `bulk-playlist`'s single y/N. Never pipe `y` into `review-playlist --execute` — it would accept every track without review, defeating the point. Without `--execute` the pipe is harmless for both: the Bash tool has no stdin, so without it the prompts read end-of-input and the dry-run stops early.

---

## When neither is right

If the user wants to add **one** track, route them to the [playlist-match](../../playlist-match/SKILL.md) skill (which wraps `add`). If they want to find tracks that fit a **specific** playlist out of a larger source, route them to [playlist-scan](../../playlist-scan/SKILL.md) (which wraps `scan-for`).
