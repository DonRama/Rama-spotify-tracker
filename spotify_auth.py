# spotify_auth.py
from spotipy.oauth2 import SpotifyOAuth
import spotipy

def get_spotify_client(secrets):
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=secrets["SPOTIPY_CLIENT_ID"],
        client_secret=secrets["SPOTIPY_CLIENT_SECRET"],
        redirect_uri=secrets["SPOTIPY_REDIRECT_URI"],
        scope="playlist-read-private playlist-read-collaborative user-library-read"
    ))
