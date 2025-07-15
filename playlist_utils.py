# playlist_utils.py
import pandas as pd
import altair as alt

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
        if track:  # skip nulls
            audio_features = sp.audio_features(track["id"])[0]
            if audio_features:
                track_data.append({
                    "name": track["name"],
                    "artist": track["artists"][0]["name"],
                    "danceability": audio_features["danceability"],
                    "energy": audio_features["energy"],
                    "tempo": audio_features["tempo"]
                })

    df = pd.DataFrame(track_data)
    summary = df.describe().loc[["mean", "std"]]
    
    chart = alt.Chart(df).mark_circle(size=80).encode(
        x="tempo",
        y="danceability",
        color="energy",
        tooltip=["name", "artist"]
    ).interactive()

    return summary, chart

