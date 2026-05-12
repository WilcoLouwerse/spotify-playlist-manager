"""Smoke test: authenticate with Spotify and list the current user's playlists."""

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

SCOPE = " ".join(
    [
        "playlist-read-private",
        "playlist-read-collaborative",
        "playlist-modify-private",
        "playlist-modify-public",
        "user-library-read",
        "user-read-private",
    ]
)


def main() -> int:
    load_dotenv()

    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

    if not (client_id and client_secret and redirect_uri):
        print(
            "Missing SPOTIPY_CLIENT_ID / SPOTIPY_CLIENT_SECRET / SPOTIPY_REDIRECT_URI."
            " Copy .env.example to .env and fill it in.",
            file=sys.stderr,
        )
        return 1

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=SCOPE,
            cache_path=".spotify_token_cache",
            open_browser=True,
        ),
        requests_timeout=30,
        retries=5,
    )

    me = sp.current_user()
    print(f"Connected as: {me['display_name']} ({me['id']})")

    print("\nYour playlists:")
    results = sp.current_user_playlists(limit=50)
    while results:
        for playlist in results["items"]:
            if not playlist:
                print("- <unavailable playlist (None entry)>")
                continue
            name = playlist.get("name", "<no name>")
            pid = playlist.get("id", "<no id>")
            tracks = playlist.get("tracks") or {}
            total = tracks.get("total", "?")
            print(f"- {name} | tracks: {total} | id: {pid}")
        results = sp.next(results) if results.get("next") else None

    return 0


if __name__ == "__main__":
    sys.exit(main())
