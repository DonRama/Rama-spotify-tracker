# app.py
import streamlit as st
import pandas as pd
from playlist_utils import analyze_playlist
from spotify_auth import get_spotify_client

st.set_page_config(page_title="Spotify Playlist Analyzer", layout="wide")
st.title("🎧 Spotify Playlist Analyzer")

# Authenticate Spotify
sp = get_spotify_client()

# Get user playlists
playlists = sp.current_user_playlists()['items']
playlist_options = {pl['name']: pl['id'] for pl in playlists}
selected_name = st.selectbox("Choose a playlist to analyze:", playlist_options.keys())

if selected_name:
    playlist_id = playlist_options[selected_name]
    with st.spinner("Analyzing playlist..."):
        df_summary, chart = analyze_playlist(sp, playlist_id)
        st.write("### Playlist Summary")
        st.dataframe(df_summary)
        st.altair_chart(chart, use_container_width=True)

    st.write("Rate this playlist:")
    rating = st.slider("Your Rating", 1, 5, 3)
    notes = st.text_area("Your Notes")
    st.success("Rating saved (in memory for now, persistent storage coming soon!)")
