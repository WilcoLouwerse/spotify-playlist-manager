"""Smoke test: authenticate with Spotify and list the current user's playlists."""

import os
import sys

from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

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
        )
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
