# app.py
import streamlit as st
import pandas as pd
from playlist_utils import analyze_playlist
from spotify_auth import get_spotify_client

st.set_page_config(page_title="Spotify Playlist Analyzer", layout="wide")
st.title("🎧 Spotify Playlist Analyzer")

# Sidebar: Spotify Authentication
st.sidebar.header("🔐 Connect to Spotify")

if "sp" not in st.session_state:
    if st.sidebar.button("Connect to Spotify"):
        with st.spinner("Connecting to Spotify..."):
            sp = get_spotify_client(st.secrets)
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

# Fetch playlists safely
# Try fetching playlists safely
playlists = []
playlist_options = {}

try:
    playlists_raw = sp.current_user_playlists()
    playlists = playlists_raw.get('items', [])
except Exception as e:
    st.error(f"❌ Could not fetch playlists: {e}")
    st.stop()

if not playlists:
    st.warning("⚠️ You don't have any playlists in your account.")
    st.stop()

# Now build the dictionary outside the try-block to guarantee it's available
playlist_options = {pl['name']: pl['id'] for pl in playlists}


# Select playlist to analyze
selected_name = st.selectbox("Choose a playlist to analyze:", playlist_options.keys())

if selected_name:
    playlist_id = playlist_options[selected_name]
    with st.spinner("Analyzing playlist..."):
        try:
            df_tracks, df_summary, chart = analyze_playlist(sp, playlist_id)

            # Display analysis results
            st.subheader("📊 Playlist Summary")
            st.dataframe(df_summary)

            st.subheader("🎼 Vibe Visualization")
            st.altair_chart(chart, use_container_width=True)

            st.subheader("🎵 Track Details")
            st.dataframe(df_tracks)

            # User rating
            st.subheader("📝 Rate this Playlist")
            rating = st.slider("Your Rating (1 = 😐, 5 = 🔥)", 1, 5, 3)
            notes = st.text_area("Your Notes (optional)")

            if st.button("Submit Rating"):
                st.success("✅ Rating saved (not yet stored — feature coming soon!)")
                st.write(f"⭐ Your Rating: {rating}/5")
                if notes:
                    st.markdown("🗒️ Your Notes:")
                    st.markdown(f"> {notes}")

        except Exception as e:
            st.error(f"❌ Failed to analyze playlist: {e}")
