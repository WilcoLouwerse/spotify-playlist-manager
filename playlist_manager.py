"""Manage Spotify playlists via CLI.

Default is dry-run: nothing is changed unless --execute is passed.
"""

import argparse
import json
import os
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
    '"Electronic Music"': "3Y6OleDjCBkDtjlQC1JC4S",
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
    "electronic music": '"Electronic Music"',
    "edm": '"Electronic Music"',
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
    try:
        track = sp.track(track_id)
        label = f"{track['artists'][0]['name']} - {track['name']}"
        return track["uri"], label
    except Exception as exc:  # noqa: BLE001 — best-effort lookup
        print(f"(track lookup failed: {exc.__class__.__name__}; continuing with URI only)")
        return uri, uri


def playlist_contains_uri(sp, playlist_id, track_uri):
    results = sp.playlist_items(
        playlist_id,
        fields="items(track(uri)),next",
        additional_types=("track",),
        limit=100,
    )
    while results:
        for item in results["items"]:
            t = item.get("track") or {}
            if t.get("uri") == track_uri:
                return True
        results = sp.next(results) if results.get("next") else None
    return False


def add_track(sp, track_input, playlist_name, execute):
    canonical_name = normalize_playlist_name(playlist_name)
    playlist_id = PLAYLISTS[canonical_name]
    track_uri, label = get_track(sp, track_input)

    print(f"Track: {label}")
    print(f"Target playlist: {canonical_name}")
    print(f"Playlist ID: {playlist_id}")

    if playlist_contains_uri(sp, playlist_id, track_uri):
        print("\nSKIP: track already in playlist. No changes made.")
        return

    if not execute:
        print("\nDRY RUN: no changes made. Add --execute to actually add the track.")
        return

    sp.playlist_add_items(playlist_id, [track_uri])
    print("\nDONE: track added.")


def suggest_playlists_from_openai(track_label):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY not set in .env — cannot run smart-add.")
        return []

    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    playlist_names = list(PLAYLISTS.keys())
    system_msg = (
        "You are a music classifier. Given a track and a list of available "
        "playlist names, choose between 1 and 5 playlists from the list that "
        "best fit the track. Only return playlist names from the provided list, "
        "spelled exactly as given. Return JSON."
    )
    user_msg = (
        f"Track: {track_label}\n\n"
        "Available playlists:\n"
        + "\n".join(f"- {name}" for name in playlist_names)
        + "\n\n"
        'Return JSON with this schema: {"suggestions": [{"playlist": "<exact name>", '
        '"confidence": <0-100 integer>, "reason": "<short reason>"}]}'
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
    )

    content = response.choices[0].message.content
    data = json.loads(content)
    suggestions = data.get("suggestions", [])

    valid = [s for s in suggestions if s.get("playlist") in PLAYLISTS][:5]
    return valid


def _prompt_yes(prompt):
    try:
        answer = input(prompt).strip().lower()
    except EOFError:
        answer = ""
    return answer in ("y", "yes")


def _process_suggestion(sp, name, track_uri, execute):
    playlist_id = PLAYLISTS[name]
    if playlist_contains_uri(sp, playlist_id, track_uri):
        print(f"- {name}: SKIP (already in playlist)")
        return
    if not execute:
        print(f"- {name}: DRY RUN (would add)")
        return
    sp.playlist_add_items(playlist_id, [track_uri])
    print(f"- {name}: ADDED")


def smart_add(sp, track_input, execute, per_playlist):
    track_uri, label = get_track(sp, track_input)
    if label == track_uri:
        print("Cannot classify: track metadata lookup failed. Try again later.")
        return

    print(f"Track: {label}\n")

    suggestions = suggest_playlists_from_openai(label)
    if not suggestions:
        print("No playlist suggestions returned.")
        return

    print("Suggested playlists:")
    for s in suggestions:
        confidence = s.get("confidence", "?")
        reason = s.get("reason", "")
        suffix = f" — {reason}" if reason else ""
        print(f"- {s['playlist']} — {confidence}%{suffix}")

    if per_playlist:
        print()
        any_accepted = False
        for s in suggestions:
            name = s["playlist"]
            confidence = s.get("confidence", "?")
            if not _prompt_yes(f"Add to '{name}' ({confidence}%)? [y/N]: "):
                print(f"- {name}: SKIPPED (rejected)")
                continue
            any_accepted = True
            _process_suggestion(sp, name, track_uri, execute)
        if not any_accepted:
            print("\nNo playlists accepted. No changes made.")
        return

    if not _prompt_yes("\nAdd this track to these playlists? [y/N]: "):
        print("Cancelled. No changes made.")
        return

    print()
    for s in suggestions:
        _process_suggestion(sp, s["playlist"], track_uri, execute)


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

    args = parser.parse_args()

    if args.command == "list-playlists":
        list_target_playlists()
        return 0

    sp = get_spotify_client()

    if args.command == "add":
        add_track(sp, args.track, args.playlist, args.execute)
    elif args.command == "smart-add":
        smart_add(sp, args.track, args.execute, args.per_playlist)

    return 0


if __name__ == "__main__":
    sys.exit(main())
