#!/usr/bin/env python3
"""
Programmatic grader for the playlist-match eval suite.

Reads each eval-N/<config>/run-1/outputs/response.md and writes a grading.json
next to it. Each assertion is checked by a small Python predicate so the result
is reproducible across iterations.

Run from the skill root:
    python evals/grade.py [iteration-N]   # defaults to iteration-1
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
WORKSPACE = SKILL_DIR / "evals" / "workspace"


# --- check helpers -----------------------------------------------------------

DUTCH_TOKENS = (
    "Artiestinformatie",
    "Nummeromschrijving",
    "Playlist match",
    "Genres",
    "Voeg toe",
    "Sorry, ik heb moeite",
    "Wat wil je",
    "voor deze",
    "nummer",
    "geen",
    "playlist",
    "klaar",
    "playlists",
)

LETTER_MENU_RE = re.compile(
    r'(?m)^\s*"?[A-F]"?\s*:\s+',  # e.g.  "A": ...
)
ZYXW_MENU_RE = re.compile(
    r'(?m)^\s*"?[ZYXW]"?\s*:\s+',  # old Z/Y/X/W
)
PLAYLIST_BULLET_RE = re.compile(r"(?m)^\s*[-*]\s+(.+?)\s+—\s+(\d{1,3})\s*%\s*—\s*(.+?)$")


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def find_section(content: str, header: str) -> str | None:
    """Return the bulleted body following a bold Dutch section header, or None."""
    header_pat = re.compile(rf"\*\*{re.escape(header)}\s*:?\*\*", re.IGNORECASE)
    lines = content.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if header_pat.search(ln):
            start = i + 1
            break
    if start is None:
        return None
    body = []
    for ln in lines[start:]:
        if ln.startswith(("**", "#", "---")):
            break
        body.append(ln)
        # heuristic stop: blank line followed by another section is fine via above checks
    return "\n".join(body)


def playlist_entries(content: str) -> list[tuple[str, int, str]]:
    body = find_section(content, "Playlist match")
    if not body:
        return []
    entries = []
    for m in PLAYLIST_BULLET_RE.finditer(body):
        name = m.group(1).strip().strip("`*")
        # Strip trailing parenthetical confidence label like "(88%)"
        name = re.sub(r"\s*\(\s*\d+%\s*\)\s*$", "", name)
        try:
            conf = int(m.group(2))
        except ValueError:
            conf = 0
        reason = m.group(3).strip()
        entries.append((name, conf, reason))
    return entries


def genre_entries(content: str) -> list[tuple[str, int, str]]:
    body = find_section(content, "Genres")
    if not body:
        return []
    entries = []
    for m in PLAYLIST_BULLET_RE.finditer(body):
        entries.append((m.group(1).strip().strip("`*"), int(m.group(2)), m.group(3).strip()))
    return entries


def dutch_score(content: str) -> int:
    return sum(1 for t in DUTCH_TOKENS if t.lower() in content.lower())


# --- per-eval assertions -----------------------------------------------------


def grade_eval_1(content: str) -> list[dict]:
    pls = playlist_entries(content)
    pl_names = [n for n, _, _ in pls]
    pl_confs = {n: c for n, c, _ in pls}
    genres = genre_entries(content)
    title_ok = bool(
        re.search(
            r"(?m)^\s*#{0,3}\s*Tame Impala\s*[-–—]\s*The Less I Know The Better\s*$",
            content,
        )
    )
    return [
        {
            "text": "title line is exactly 'Tame Impala - The Less I Know The Better'",
            "passed": title_ok,
            "evidence": "found heading line" if title_ok else "no exact-match title line found",
        },
        {
            "text": "Artiestinformatie block is present (first occurrence in chat)",
            "passed": "**Artiestinformatie" in content,
            "evidence": ("Artiestinformatie header present" if "**Artiestinformatie" in content else "no Artiestinformatie header found"),
        },
        {
            "text": "Genres section has 2-4 bullets with percentage and short reason",
            "passed": 2 <= len(genres) <= 4,
            "evidence": f"found {len(genres)} genre bullets matching `name — XX% — reason`",
        },
        {
            "text": "Playlist match includes 'Alternative / Indie' with confidence >= 80%",
            "passed": pl_confs.get("Alternative / Indie", 0) >= 80,
            "evidence": (
                f"Alternative / Indie at {pl_confs.get('Alternative / Indie', 0)}%"
                if "Alternative / Indie" in pl_names
                else f"Alternative / Indie not in playlist match (found: {pl_names})"
            ),
        },
        {
            "text": "Playlist match does NOT include 'Random sht'",
            "passed": "Random sht" not in content,
            "evidence": "Random sht not mentioned" if "Random sht" not in content else "Random sht appears in response",
        },
        {
            "text": "Output does NOT print the old A-F / Z-Y-X-W letter menu",
            "passed": not LETTER_MENU_RE.search(content) and not ZYXW_MENU_RE.search(content),
            "evidence": (
                "no letter menu detected"
                if not LETTER_MENU_RE.search(content) and not ZYXW_MENU_RE.search(content)
                else "letter menu detected (A-F or Z-Y-X-W lines)"
            ),
        },
        {
            "text": "User-facing prose is in Dutch (Artiestinformatie, Nummeromschrijving, Genres, Playlist match)",
            "passed": all(h in content for h in ("Artiestinformatie", "Nummeromschrijving", "Genres", "Playlist match")),
            "evidence": (
                "Dutch section headers all present"
                if all(h in content for h in ("Artiestinformatie", "Nummeromschrijving", "Genres", "Playlist match"))
                else "one or more Dutch headers missing"
            ),
        },
    ]


def grade_eval_2(content: str) -> list[dict]:
    pls = playlist_entries(content)
    pl_names = [n for n, _, _ in pls]
    pl_confs = {n: c for n, c, _ in pls}
    genres_txt = (find_section(content, "Genres") or "").lower()
    techno_in_genres = any(g in genres_txt for g in ("techno", "industrial", "peak-time", "minimal"))
    return [
        {
            "text": "Playlist match includes 'Techno' with confidence >= 85%",
            "passed": pl_confs.get("Techno", 0) >= 85,
            "evidence": (f"Techno at {pl_confs.get('Techno', 0)}%" if "Techno" in pl_names else f"Techno not in playlist match (found: {pl_names})"),
        },
        {
            "text": "Playlist match also includes 'Electronic Music' alongside Techno (umbrella rule)",
            "passed": "Electronic Music" in pl_names and "Techno" in pl_names,
            "evidence": f"present={[n for n in pl_names if n in ('Techno', 'Electronic Music')]}",
        },
        {
            "text": "Playlist match does NOT include 'Random sht'",
            "passed": "Random sht" not in content,
            "evidence": "Random sht absent" if "Random sht" not in content else "Random sht appears",
        },
        {
            "text": "Genres section identifies Techno (or a Techno subgenre) as primary",
            "passed": techno_in_genres,
            "evidence": "techno-family keyword found in Genres" if techno_in_genres else "no techno-family keyword found in Genres section",
        },
        {
            "text": "Output does NOT print the old A-F / Z-Y-X-W letter menu",
            "passed": not LETTER_MENU_RE.search(content) and not ZYXW_MENU_RE.search(content),
            "evidence": "no letter menu detected"
            if (not LETTER_MENU_RE.search(content) and not ZYXW_MENU_RE.search(content))
            else "letter menu detected",
        },
    ]


def grade_eval_3(content: str) -> list[dict]:
    pls = playlist_entries(content)
    pl_names = [n for n, _, _ in pls]
    pl_confs = {n: c for n, c, _ in pls}
    meme_reason = next((r for n, _, r in pls if n == "Funny meme"), "")
    meme_keywords = ("rick roll", "rickroll", "meme", "internet", "cultural", "cultureel")
    genres_txt = (find_section(content, "Genres") or "").lower()
    pop_keywords = ("synth-pop", "synthpop", "dance-pop", "pop", "synth pop", "hi-nrg", "blue-eyed soul")
    pop_in_genres = any(k in genres_txt for k in pop_keywords) and "meme" not in genres_txt.split("\n")[0]
    return [
        {
            "text": "Playlist match includes 'Funny meme' with confidence >= 80% (Rick Roll cultural context)",
            "passed": pl_confs.get("Funny meme", 0) >= 80,
            "evidence": (
                f"Funny meme at {pl_confs.get('Funny meme', 0)}%"
                if "Funny meme" in pl_names
                else f"Funny meme not in playlist match (found: {pl_names})"
            ),
        },
        {
            "text": "Playlist match includes 'Pop / Mainstream' or 'Happy tunes'",
            "passed": "Pop / Mainstream" in pl_names or "Happy tunes" in pl_names,
            "evidence": f"present from set={[n for n in pl_names if n in ('Pop / Mainstream', 'Happy tunes')]}",
        },
        {
            "text": "Funny meme reason explicitly cites the meme / Rick Roll / cultural context, not just genre",
            "passed": any(k in meme_reason.lower() for k in meme_keywords),
            "evidence": f"reason='{meme_reason}'",
        },
        {
            "text": "Genres section identifies the track as 80s synth-pop / dance-pop / pop, not 'meme music'",
            "passed": pop_in_genres,
            "evidence": f"genres section text head='{genres_txt[:80]}...'",
        },
        {
            "text": "Output does NOT print the old A-F / Z-Y-X-W letter menu",
            "passed": not LETTER_MENU_RE.search(content) and not ZYXW_MENU_RE.search(content),
            "evidence": "no letter menu detected"
            if (not LETTER_MENU_RE.search(content) and not ZYXW_MENU_RE.search(content))
            else "letter menu detected",
        },
    ]


def grade_eval_4(content: str) -> list[dict]:
    cli_in_output = "playlist_manager.py add" in content and ("--execute" in content or "ADDED" in content)
    invented_id_pat = re.compile(r"spotify[:.]/?/?(open\.spotify\.com/track/|track[:/])\w{20,24}")
    has_id = bool(invented_id_pat.search(content))
    askq_hint = re.search(r"AskUserQuestion|spotify[- ]?(link|url|id)|\?$|annuleren|disambig", content, re.IGNORECASE)
    dutch = dutch_score(content) >= 3
    return [
        {
            "text": "Skill does NOT call '.venv/bin/python playlist_manager.py add' on the basis of 'F'",
            "passed": not cli_in_output,
            "evidence": "no executed add command" if not cli_in_output else "add command appears in output",
        },
        {
            "text": "Skill does NOT invent or guess a Spotify track ID",
            "passed": not has_id,
            "evidence": "no Spotify track id pattern" if not has_id else "appears to reference a Spotify track id",
        },
        {
            "text": "Skill either treats 'F' as unrelated OR uses AskUserQuestion-style disambiguation rather than executing the add flow",
            "passed": bool(askq_hint) and not cli_in_output,
            "evidence": "disambiguation/AskUserQuestion-style language present" if askq_hint else "no disambiguation language found",
        },
        {
            "text": "Response is in Dutch",
            "passed": dutch,
            "evidence": f"dutch token score={dutch_score(content)}/3 minimum",
        },
    ]


def grade_eval_5(content: str) -> list[dict]:
    cli_in_output = bool(re.search(r"\.venv/bin/python\s+playlist_manager\.py\s+add", content))
    # No actual execution: no ADDED / SKIP literal output lines
    no_execute = "ADDED" not in content and "SKIP: track already in playlist" not in content
    quoted_playlist = re.search(r'\.venv/bin/python\s+playlist_manager\.py\s+add\s+"https?://[^"]+"\s+"[^"]+"', content)
    dutch = dutch_score(content) >= 3
    return [
        {
            "text": "Skill does NOT actually run playlist_manager.py (no execute)",
            "passed": no_execute,
            "evidence": "no ADDED / SKIP execution markers in response" if no_execute else "looks like the command was executed",
        },
        {
            "text": "Skill does NOT treat 'F https://...' as the literal letter 'F' alone — the URL is acted on",
            "passed": "spotify.com/track" in content or "track/" in content or "open.spotify.com" in content,
            "evidence": "Spotify URL referenced in response" if "spotify.com/track" in content or "track/" in content else "URL not referenced",
        },
        {
            "text": "If add commands are rendered, each uses '.venv/bin/python playlist_manager.py add'",
            "passed": (cli_in_output if "playlist_manager.py" in content else True),
            "evidence": ("venv-prefixed add command present" if cli_in_output else "no add command rendered, vacuously true"),
        },
        {
            "text": "If add commands are rendered, each quotes the playlist name with double quotes",
            "passed": (bool(quoted_playlist) if cli_in_output else True),
            "evidence": (
                "quoted playlist name found"
                if quoted_playlist
                else ("no add command rendered, vacuously true" if not cli_in_output else "add command found but playlist name not double-quoted")
            ),
        },
        {
            "text": "Response is in Dutch",
            "passed": dutch,
            "evidence": f"dutch token score={dutch_score(content)}/3 minimum",
        },
    ]


def grade_eval_6(content: str) -> list[dict]:
    leadin_ok = "Sorry, ik heb moeite om de genres" in content
    no_old_menu = not ZYXW_MENU_RE.search(content) and '"Z":' not in content and '"Y":' not in content
    no_fab_genres = not find_section(content, "Genres") or len(genre_entries(content)) == 0
    no_playlist_match = not find_section(content, "Playlist match") or len(playlist_entries(content)) == 0
    return [
        {
            "text": "Output contains the Dutch uncertainty lead-in 'Sorry, ik heb moeite om de genres voor dit nummer te vinden'",
            "passed": leadin_ok,
            "evidence": "lead-in line present" if leadin_ok else "lead-in line not found",
        },
        {
            "text": "Output does NOT print the old Z/Y/X/W letter menu",
            "passed": no_old_menu,
            "evidence": "no Z/Y/X/W menu" if no_old_menu else "Z/Y/X/W letter menu detected",
        },
        {
            "text": "Skill does NOT produce a Genres section with fabricated entries",
            "passed": no_fab_genres,
            "evidence": "no Genres section / no fabricated bullets"
            if no_fab_genres
            else f"Genres section with {len(genre_entries(content))} bullets",
        },
        {
            "text": "Skill does NOT produce a Playlist match section (user has not picked an option yet)",
            "passed": no_playlist_match,
            "evidence": "no Playlist match section / no bullets"
            if no_playlist_match
            else f"Playlist match section with {len(playlist_entries(content))} bullets",
        },
    ]


GRADERS = {
    1: grade_eval_1,
    2: grade_eval_2,
    3: grade_eval_3,
    4: grade_eval_4,
    5: grade_eval_5,
    6: grade_eval_6,
}


def grade_run(eval_dir: Path, config: str) -> None:
    meta_path = eval_dir / "eval_metadata.json"
    meta = json.loads(meta_path.read_text())
    eval_id = meta["eval_id"]

    run_dir = eval_dir / config / "run-1"
    response_path = run_dir / "outputs" / "response.md"
    if not response_path.exists():
        print(f"  SKIP {eval_dir.name}/{config}: no response.md")
        return

    content = read(response_path)
    expectations = GRADERS[eval_id](content)
    passed = sum(1 for e in expectations if e["passed"])
    total = len(expectations)

    tokens = 0
    tool_uses = 0
    timing_path = run_dir / "timing.json"
    if timing_path.exists():
        timing_data = json.loads(timing_path.read_text())
        tokens = timing_data.get("total_tokens", 0)
        tool_uses = timing_data.get("tool_uses", 0)

    grading = {
        "expectations": expectations,
        "summary": {
            "passed": passed,
            "failed": total - passed,
            "total": total,
            "pass_rate": round(passed / total, 4) if total else 0.0,
        },
        "execution_metrics": {
            "total_tool_calls": tool_uses,
            "errors_encountered": 0,
            "output_chars": len(content),
            "tokens": tokens,
        },
        "timing": {},
    }
    grading_path = run_dir / "grading.json"
    grading_path.write_text(json.dumps(grading, indent=2))
    print(f"  {eval_dir.name}/{config}: {passed}/{total} passed")


def main():
    iteration = sys.argv[1] if len(sys.argv) > 1 else "iteration-1"
    iter_dir = WORKSPACE / iteration
    if not iter_dir.exists():
        print(f"missing iteration dir: {iter_dir}")
        sys.exit(1)

    for eval_dir in sorted(iter_dir.glob("eval-*")):
        if not (eval_dir / "eval_metadata.json").exists():
            continue
        for config in ("with_skill", "without_skill"):
            grade_run(eval_dir, config)


if __name__ == "__main__":
    main()
