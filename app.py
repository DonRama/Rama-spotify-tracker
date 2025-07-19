# app.py
import os
import streamlit as st
import pandas as pd
from playlist_utils import analyze_playlist
from spotify_auth import get_spotify_client

st.set_page_config(page_title="Spotify Playlist Analyzer", layout="wide")
st.title("🎧 Spotify Playlist Analyzer")

# ----------------- AUTH -----------------
st.sidebar.header("🔐 Connect to Spotify")

if "sp" not in st.session_state:
    if st.sidebar.button("Connect to Spotify"):
        with st.spinner("Connecting to Spotify..."):
            sp = get_spotify_client()
            if sp:
                st.session_state["sp"] = sp
                st.success("✅ Connected to Spotify!")
            else:
                st.error("❌ Failed to connect. Check your credentials.")
                st.stop()
    else:
        st.warning("🔌 Not connected to Spotify. Please click 'Connect to Spotify'.")
        st.stop()
else:
    sp = st.session_state["sp"]
    st.success("✅ Already connected to Spotify!")

# ----------------- GET PLAYLISTS -----------------
try:
    playlists_raw = sp.current_user_playlists()
    playlists = playlists_raw['items']
    if not playlists:
        st.warning("No playlists found in your account.")
        st.stop()
    playlist_options = {pl['name']: pl['id'] for pl in playlists}
except Exception as e:
    st.error(f"❌ Could not fetch playlists: {e}")
    st.stop()
    
selected_name = st.selectbox("Choose a playlist to analyze:", playlist_options.keys())

# ----------------- ANALYSIS -----------------
if selected_name:
    playlist_id = playlist_options[selected_name]
    with st.spinner("Analyzing playlist..."):
        try:
            df_summary, chart = analyze_playlist(sp, playlist_id)
            st.write("### Playlist Summary")
            st.dataframe(df_summary)
            st.altair_chart(chart, use_container_width=True)

            st.write("Rate this playlist:")
            rating = st.slider("Your Rating", 1, 5, 3)
            notes = st.text_area("Your Notes")
            st.success("Rating saved (in memory only).")
        except Exception as e:
            st.error(f"Analysis error: {e}")
