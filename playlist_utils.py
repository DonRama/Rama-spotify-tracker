# playlist_utils.py
import pandas as pd
import altair as alt
import streamlit as st

def analyze_playlist(sp, playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    tracks.extend(results["items"])

    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])

    track_data = []
    for item in tracks:
        track = item["track"]
        if track:
            audio_features = sp.audio_features(track["id"])[0]
            if audio_features:
                track_data.append({
                    "name": track["name"],
                    "artist": ', '.join([artist["name"] for artist in track["artists"]]),
                    "danceability": audio_features["danceability"],
                    "energy": audio_features["energy"],
                    "tempo": audio_features["tempo"],
                    "valence": audio_features["valence"],
                    "acousticness": audio_features["acousticness"],
                    "instrumentalness": audio_features["instrumentalness"],
                    "popularity": track["popularity"]
                })

    df = pd.DataFrame(track_data)

    # Summary statistics
    summary = df[["danceability", "energy", "tempo", "valence"]].describe().loc[["mean", "std"]]

    # Interactive chart
    chart = alt.Chart(df).mark_circle(size=80).encode(
        x=alt.X("tempo", title="Tempo"),
        y=alt.Y("danceability", title="Danceability"),
        color=alt.Color("energy", scale=alt.Scale(scheme="turbo")),
        tooltip=["name", "artist", "energy", "tempo", "danceability"]
    ).interactive()

    return df, summary, chart

@st.cache_data(show_spinner=False)
def get_playlist_data(sp, playlist_url):
    return sp.playlist_items(playlist_url)
