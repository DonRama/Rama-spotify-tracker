# spotify_auth.py
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_spotify_client(secrets):
    try:
        auth_manager = SpotifyOAuth(
            client_id=secrets["SPOTIPY_CLIENT_ID"],
            client_secret=secrets["SPOTIPY_CLIENT_SECRET"],
            redirect_uri=secrets["SPOTIPY_REDIRECT_URI"],
            scope="playlist-read-private playlist-read-collaborative"
        )
        return spotipy.Spotify(auth_manager=auth_manager)

    except spotipy.SpotifyException as e:
        st.error("❌ Spotify authentication failed. Check your credentials.")
        st.stop()
    except Exception as e:
        st.error(f"⚠️ Unexpected error: {e}")
        st.stop()
