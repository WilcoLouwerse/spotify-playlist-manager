"""Manage Spotify playlists via CLI.

Default is dry-run: nothing is changed unless --execute is passed.
"""

import argparse
import json
import os
import re
import socket
import sys

from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# WSL's IPv6 route to api.spotify.com is broken (connect hangs until read
# timeout). Force IPv4 resolution so requests reliably reach Spotify.
_orig_getaddrinfo = socket.getaddrinfo


def _ipv4_only_getaddrinfo(*args, **kwargs):
    return [info for info in _orig_getaddrinfo(*args, **kwargs) if info[0] == socket.AF_INET]


socket.getaddrinfo = _ipv4_only_getaddrinfo

load_dotenv()

SCOPE = (
    "playlist-read-private "
    "playlist-read-collaborative "
    "playlist-modify-private "
    "playlist-modify-public "
    "user-library-read "
    "user-read-private"
)

PLAYLISTS = {
    "Rap": "0IKLWWkZTJ0zk9mX8BatJC",
    "Pop / Mainstream": "6Z28iv4DlEyMYytBb8bjKd",
    "Alternative / Indie": "4cXn8rebxCzVvsK0XxYU8S",
    "K-pop": "4RXXB8PxXK7Jm3Ysoi4EiC",
    "Metal & Rock": "22jVRahS7rhanx3pmIwWCD",
    "Instrumental Metal": "2imtHkNm6dZIj8xc0i2n2F",
    "Jazz / Funk / Soul": "64VfxKOeVr1noBgNPqZCWQ",
    "House": "0BEX4bI5xtkEVA4BfYTKg2",
    "Techno": "7lRL294p8uvOOXTxNPIBhn",
    "Trance": "3eh9PL5diEtYoxxAmIUh38",
    "Drum & Bass": "0jECuEhrsvUJCkVy9fmGmN",
    "Dubstep / Bass": "4kxvCA0xRslKisr9kA5y2y",
    "Hardstyle & Hardcore": "3jGm3qv2QQXmB6lxrgdDoR",
    "Synthwave": "5BFG9XBUWoYfPek8CcL3ea",
    "Electronic Music": "3Y6OleDjCBkDtjlQC1JC4S",
    "Party": "5UxXh0fjJzKCLY8DMNzWy5",
    "Happy tunes": "3nupbERYJs4woq5dOAFUCj",
    "Sad tunes": "5FLVYNGAqBLmrhFoD3ItbV",
    "Angry tunes": "6n9atJab6utXK1SRHoixSp",
    "Rustig / 'anders'": "1ALotvr2UUPqWUHKTmEQdp",
    "Funny meme": "3ks35C34IFNPhW3Clw9zym",
    "Ket420": "3viX7Yo3jzYVZ4a6WMIR3S",
    "Hooyah": "2e4z5WbyQEsZ6I4YXkd5Np",
}

ALIASES = {
    "electronic music": "Electronic Music",
    "edm": "Electronic Music",
    "dnb": "Drum & Bass",
    "drum and bass": "Drum & Bass",
    "dubstep": "Dubstep / Bass",
    "bass": "Dubstep / Bass",
    "hardcore": "Hardstyle & Hardcore",
    "hardstyle": "Hardstyle & Hardcore",
    "indie": "Alternative / Indie",
    "alternative": "Alternative / Indie",
    "pop": "Pop / Mainstream",
    "jazz": "Jazz / Funk / Soul",
    "funk": "Jazz / Funk / Soul",
    "soul": "Jazz / Funk / Soul",
    "rock": "Metal & Rock",
    "metal": "Metal & Rock",
    "calm": "Rustig / 'anders'",
    "chill": "Rustig / 'anders'",
    "meme": "Funny meme",
}


def get_spotify_client():
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope=SCOPE,
            cache_path=".spotify_token_cache",
            open_browser=True,
        ),
        requests_timeout=30,
        retries=5,
    )


def normalize_playlist_name(name):
    if name in PLAYLISTS:
        return name

    key = name.strip().lower()
    if key in ALIASES:
        return ALIASES[key]

    matches = [p for p in PLAYLISTS if p.lower() == key]
    if matches:
        return matches[0]

    raise ValueError(f"Unknown playlist: {name}")


def extract_track_id(track_input):
    if "open.spotify.com/track/" in track_input:
        part = track_input.split("open.spotify.com/track/")[1]
        return part.split("?")[0].split("/")[0]
    if track_input.startswith("spotify:track:"):
        return track_input.split(":")[-1]
    return track_input


def get_track(sp, track_input):
    track_id = extract_track_id(track_input)
    uri = f"spotify:track:{track_id}"
    fallback = {
        "id": track_id,
        "uri": uri,
        "name": "",
        "artists": [],
        "album": "",
        "release_date": None,
        "popularity": None,
        "duration_ms": None,
        "explicit": None,
        "spotify_url": f"https://open.spotify.com/track/{track_id}",
        "label": uri,
        "metadata_available": False,
    }
    try:
        track = sp.track(track_id)
    except Exception as exc:  # noqa: BLE001 — best-effort lookup
        print(f"(track lookup failed: {exc.__class__.__name__}; continuing with URI only)")
        return fallback

    artist_names = [a["name"] for a in track["artists"]]
    album = track["album"]
    label = f"{artist_names[0]} - {track['name']}" if artist_names else track["name"]
    return {
        "id": track["id"],
        "uri": track["uri"],
        "name": track["name"],
        "artists": artist_names,
        "album": album["name"],
        "release_date": album.get("release_date"),
        "popularity": track.get("popularity"),
        "duration_ms": track.get("duration_ms"),
        "explicit": track.get("explicit"),
        "spotify_url": track["external_urls"]["spotify"],
        "label": label,
        "metadata_available": True,
    }


ADDS_LOG_PATH = ".adds_log.json"
_WARNED_ABOUT_STRIPPED_DATA = False


def _load_adds_log():
    try:
        with open(ADDS_LOG_PATH) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_adds_log(log):
    with open(ADDS_LOG_PATH, "w") as f:
        json.dump(log, f, indent=2)


def log_successful_add(playlist_id, track_uri):
    log = _load_adds_log()
    uris = log.setdefault(playlist_id, [])
    if track_uri not in uris:
        uris.append(track_uri)
        _save_adds_log(log)


def playlist_contains_uri(sp, playlist_id, track_uri):
    # First check the local log — Spotify's development-tier API strips
    # track URIs from playlist_items responses (Nov 2024 restrictions),
    # so we cannot rely on it alone.
    log = _load_adds_log()
    if track_uri in log.get(playlist_id, []):
        return True

    # Best-effort Spotify check. Will only catch items added before the
    # log existed if the API returns real URIs (Extended Quota Mode).
    results = sp.playlist_items(
        playlist_id,
        fields="items(track(uri)),next",
        additional_types=("track",),
        limit=100,
    )
    api_returned_any_uri = False
    while results:
        for item in results["items"]:
            t = item.get("track") or {}
            uri = t.get("uri")
            if uri:
                api_returned_any_uri = True
            if uri == track_uri:
                return True
        results = sp.next(results) if results.get("next") else None

    global _WARNED_ABOUT_STRIPPED_DATA
    if not api_returned_any_uri and not _WARNED_ABOUT_STRIPPED_DATA:
        print(
            "WARN: Spotify returned no track URIs from playlist_items — the app is "
            "in Development Mode and the API does not expose playlist contents. "
            "Duplicate detection relies on .adds_log.json; use `log-import` to "
            "seed it from a CSV export (e.g. https://exportify.net)."
        )
        _WARNED_ABOUT_STRIPPED_DATA = True

    return False


def add_track(sp, track_input, playlist_name, execute):
    canonical_name = normalize_playlist_name(playlist_name)
    playlist_id = PLAYLISTS[canonical_name]
    track = get_track(sp, track_input)
    track_uri = track["uri"]

    print(f"Track: {track['label']}")
    print(f"Target playlist: {canonical_name}")
    print(f"Playlist ID: {playlist_id}")

    if playlist_contains_uri(sp, playlist_id, track_uri):
        print("\nSKIP: track already in playlist. No changes made.")
        return

    if not execute:
        print("\nDRY RUN: no changes made. Add --execute to actually add the track.")
        return

    try:
        resp = sp.playlist_add_items(playlist_id, [track_uri])
    except spotipy.SpotifyException as exc:
        print(f"\nFAILED: Spotify returned {exc.http_status} {exc.msg or exc.code}")
        return
    snapshot = (resp or {}).get("snapshot_id") if isinstance(resp, dict) else None
    if not snapshot:
        print(f"\nWARN: Spotify returned no snapshot_id (response={resp!r}); add may not have persisted.")
        return
    log_successful_add(playlist_id, track_uri)
    print(f"\nDONE: track added (snapshot {snapshot[:10]}…)")


def validate_classification(data):
    if not isinstance(data, dict):
        raise ValueError("response is not an object")

    matches = data.get("playlist_matches")
    if not isinstance(matches, list) or not matches:
        raise ValueError("playlist_matches must be a non-empty list")
    if len(matches) > 5:
        raise ValueError(f"too many playlist matches: {len(matches)}")

    for match in matches:
        playlist = match.get("playlist")
        confidence = match.get("confidence")
        if playlist not in PLAYLISTS:
            raise ValueError(f"unknown playlist: {playlist}")
        if not isinstance(confidence, int) or not 0 <= confidence <= 100:
            raise ValueError(f"invalid confidence for {playlist}: {confidence}")


def classify_track_with_openai(track):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY not set in .env — cannot run smart-add.")
        return None

    from openai import (
        APIConnectionError,
        APIError,
        AuthenticationError,
        OpenAI,
        RateLimitError,
    )

    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    track_payload = {k: v for k, v in track.items() if k not in ("metadata_available", "label")}

    available_playlists = {
        "genre": [
            "Rap", "Pop / Mainstream", "Alternative / Indie", "K-pop",
            "Metal & Rock", "Instrumental Metal", "Jazz / Funk / Soul",
            "House", "Techno", "Trance", "Drum & Bass", "Dubstep / Bass",
            "Hardstyle & Hardcore", "Synthwave", "Electronic Music",
        ],
        "mood": ["Party", "Happy tunes", "Sad tunes", "Angry tunes", "Rustig / 'anders'"],
        "theme": ["Funny meme", "Ket420", "Hooyah"],
    }

    prompt_data = {
        "task": "Classify this Spotify track for playlist placement.",
        "track": track_payload,
        "available_playlists": available_playlists,
        "rules": {
            "max_playlists": 5,
            "min_playlists": 1,
            "only_use_available_playlists": True,
            "use_only_listed_names_exact_spelling": True,
            "classification_signals": [
                "genre", "BPM", "energy", "mood", "lyrics", "production",
                "cultural context", "meme context", "listening scenario",
            ],
            "anti_shortcuts": [
                "Do not classify based on artist name alone — a single artist can span multiple genres and moods.",
                "Weigh track-specific signals (sound, BPM, lyrics, production) against artist tendencies.",
                "Use multiple independent signals; if signals conflict, lower confidence rather than picking one source.",
            ],
            "category_balance": (
                "Suggestions should usually combine at most one genre playlist with relevant mood "
                "or theme playlists; do not return multiple overlapping subgenres from the genre list."
            ),
            "special_playlists": {
                "Funny meme": "Only for meme songs, internet classics, absurd/funny lyrics.",
                "Ket420": "Only for stoned, psychedelic, spacey, mellow, ketamine/weed-friendly listening.",
                "Hooyah": "Only for sexually tinted, sensual, suggestive songs.",
            },
            "electronic_music": (
                "Use 'Electronic Music' as catch-all for electronic tracks that do "
                "not clearly fit House, Techno, Trance, Drum & Bass, Dubstep / Bass, "
                "Hardstyle & Hardcore, or Synthwave."
            ),
            "confidence": "0-100 integer; lower it when signals disagree or are weak.",
        },
        "required_json_schema": {
            "genres": [
                {"genre": "string", "confidence": "integer", "reason": "string"}
            ],
            "playlist_matches": [
                {"playlist": "string", "confidence": "integer", "reason": "string"}
            ],
            "short_summary": "string",
        },
    }

    system_msg = (
        "You are a strict music classification assistant. "
        "Return only valid JSON matching the required schema. "
        "Only use playlist names from available_playlists, spelled exactly as given. "
        "No markdown. No commentary."
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": json.dumps(prompt_data, ensure_ascii=False)},
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
        )
    except RateLimitError as exc:
        code = getattr(getattr(exc, "body", None), "get", lambda *_: None)("code")
        if code == "insufficient_quota" or "insufficient_quota" in str(exc):
            print(
                "OpenAI: insufficient quota. Add credit or a payment method at "
                "https://platform.openai.com/settings/organization/billing and retry."
            )
        else:
            print(f"OpenAI rate-limited the request. Try again in a moment. Detail: {exc}")
        return None
    except AuthenticationError:
        print(
            "OpenAI: authentication failed. Check OPENAI_API_KEY in .env "
            "(may have been revoked) — create a new key at "
            "https://platform.openai.com/api-keys."
        )
        return None
    except APIConnectionError as exc:
        print(f"OpenAI: connection error — {exc}")
        return None
    except APIError as exc:
        print(f"OpenAI API error: {exc}")
        return None

    content = response.choices[0].message.content
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        print(f"OpenAI returned invalid JSON:\n{content[:300]}")
        return None

    try:
        validate_classification(data)
    except ValueError as exc:
        print(f"OpenAI classification rejected: {exc}")
        return None

    return data


def print_recommendation(track, classification):
    artists = ", ".join(track["artists"]) if track["artists"] else "(unknown artist)"
    print("\n" + "=" * 60)
    print(f"Track: {artists} - {track['name']}")
    if track["album"]:
        print(f"Album: {track['album']}")
    if track.get("spotify_url"):
        print(f"Spotify: {track['spotify_url']}")
    print("=" * 60)

    summary = classification.get("short_summary")
    if summary:
        print("\nSummary:")
        print(summary)

    genres = classification.get("genres") or []
    if genres:
        print("\nGenres:")
        for g in genres:
            print(f"- {g.get('genre')} — {g.get('confidence')}% — {g.get('reason')}")

    print("\nSuggested playlists:")
    for m in classification["playlist_matches"]:
        print(f"- {m['playlist']} — {m['confidence']}% — {m['reason']}")


def _prompt_yes(prompt):
    try:
        answer = input(prompt).strip().lower()
    except EOFError:
        answer = ""
    return answer in ("y", "yes", "j", "ja")


def smart_add(sp, track_input, execute, per_playlist):
    track = get_track(sp, track_input)
    if not track["metadata_available"]:
        print("Cannot classify: track metadata lookup failed. Try again later.")
        return

    classification = classify_track_with_openai(track)
    if not classification:
        return

    print_recommendation(track, classification)

    print("\nPending actions:")
    actions = []
    for match in classification["playlist_matches"]:
        name = match["playlist"]
        playlist_id = PLAYLISTS[name]
        confidence = match.get("confidence", "?")
        if playlist_contains_uri(sp, playlist_id, track["uri"]):
            print(f"- SKIP: already in {name}")
        else:
            print(f"- ADD: {name} ({confidence}%)")
            actions.append((name, playlist_id, confidence))

    if not actions:
        print("\nNo changes needed.")
        return

    if per_playlist:
        accepted = []
        print()
        for name, playlist_id, confidence in actions:
            if _prompt_yes(f"Add to '{name}' ({confidence}%)? [y/N]: "):
                accepted.append((name, playlist_id))
            else:
                print(f"- {name}: rejected")
        if not accepted:
            print("\nNo playlists accepted. No changes made.")
            return
    else:
        if not _prompt_yes("\nAdd this track to the listed playlists? [y/N]: "):
            print("Cancelled. No changes made.")
            return
        accepted = [(name, pid) for name, pid, _ in actions]

    print()
    for name, playlist_id in accepted:
        if not execute:
            print(f"- {name}: DRY RUN (would add)")
            continue
        try:
            resp = sp.playlist_add_items(playlist_id, [track["uri"]])
        except spotipy.SpotifyException as exc:
            print(f"- {name}: FAILED ({exc.http_status} {exc.msg or exc.code})")
            continue
        snapshot = (resp or {}).get("snapshot_id") if isinstance(resp, dict) else None
        if not snapshot:
            print(f"- {name}: WARN — Spotify returned no snapshot_id (response={resp!r})")
            continue
        log_successful_add(playlist_id, track["uri"])
        print(f"- {name}: ADDED (snapshot {snapshot[:10]}…)")


_TRACK_REF_RE = re.compile(r"(?:spotify:track:|open\.spotify\.com/track/)([A-Za-z0-9]{22})")
_BARE_ID_RE = re.compile(r"\b([A-Za-z0-9]{22})\b")


def _extract_uri_from_line(line):
    line = line.strip()
    if not line:
        return None
    m = _TRACK_REF_RE.search(line)
    if m:
        return f"spotify:track:{m.group(1)}"
    # Try the line as a bare 22-char ID, or as the first CSV/TSV field.
    candidates = [line, line.split(",", 1)[0].strip(), line.split("\t", 1)[0].strip()]
    for candidate in candidates:
        if _BARE_ID_RE.fullmatch(candidate):
            return f"spotify:track:{candidate}"
    return None


def log_import(playlist_name, file_path):
    canonical_name = normalize_playlist_name(playlist_name)
    playlist_id = PLAYLISTS[canonical_name]

    try:
        with open(file_path, encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return

    log = _load_adds_log()
    existing = list(log.get(playlist_id, []))
    pre_existing = set(existing)
    seen_in_file = set()
    added = 0
    duplicates_in_file = 0
    already_in_log = 0
    invalid = 0

    for raw in lines:
        uri = _extract_uri_from_line(raw)
        if uri is None:
            if raw.strip():
                invalid += 1
            continue
        if uri in pre_existing:
            already_in_log += 1
            continue
        if uri in seen_in_file:
            duplicates_in_file += 1
            continue
        seen_in_file.add(uri)
        existing.append(uri)
        added += 1

    log[playlist_id] = existing
    _save_adds_log(log)

    print(f"Playlist: {canonical_name} ({playlist_id})")
    print(f"  Imported new URIs: {added}")
    print(f"  Already in log:    {already_in_log}")
    print(f"  Duplicate in file: {duplicates_in_file}")
    print(f"  Unparseable lines: {invalid}")
    print(f"  Total URIs logged: {len(existing)}")


def list_target_playlists():
    for name in PLAYLISTS:
        print(f"- {name}")


def main():
    parser = argparse.ArgumentParser(description="Spotify playlist manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a track to a playlist")
    add_parser.add_argument("track", help="Spotify track URL, URI, or ID")
    add_parser.add_argument("playlist", help="Target playlist name")
    add_parser.add_argument("--execute", action="store_true", help="Actually perform the change")

    smart_parser = subparsers.add_parser(
        "smart-add",
        help="Classify a track with OpenAI, confirm, then add to suggested playlists",
    )
    smart_parser.add_argument("track", help="Spotify track URL, URI, or ID")
    smart_parser.add_argument(
        "--execute", action="store_true", help="Actually perform the change after confirmation"
    )
    smart_parser.add_argument(
        "--per-playlist",
        action="store_true",
        help="Ask y/N for each suggested playlist individually instead of one prompt for all",
    )

    subparsers.add_parser("list-playlists", help="List configured target playlists")

    import_parser = subparsers.add_parser(
        "log-import",
        help="Import Spotify track URIs/URLs/IDs from a file into the local adds log "
             "for a playlist (workaround for Spotify dev-tier API restrictions)",
    )
    import_parser.add_argument("playlist", help="Target playlist name")
    import_parser.add_argument(
        "file",
        help="Path to a text/CSV/JSON file. Any line containing a Spotify track URI, "
             "open.spotify.com/track URL, or bare 22-char ID is imported; other lines "
             "are ignored.",
    )

    args = parser.parse_args()

    if args.command == "list-playlists":
        list_target_playlists()
        return 0

    if args.command == "log-import":
        log_import(args.playlist, args.file)
        return 0

    sp = get_spotify_client()

    if args.command == "add":
        add_track(sp, args.track, args.playlist, args.execute)
    elif args.command == "smart-add":
        smart_add(sp, args.track, args.execute, args.per_playlist)

    return 0


if __name__ == "__main__":
    sys.exit(main())
