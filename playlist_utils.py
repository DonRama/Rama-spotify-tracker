# playlist_utils.py
import pandas as pd
import altair as alt

def analyze_playlist(sp, playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    tracks.extend(results['items'])
    
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    audio_features = []
    track_names = []

    for item in tracks:
        track = item['track']
        if track:  # Avoid NoneType
            track_id = track['id']
            features = sp.audio_features(track_id)[0]
            if features:
                audio_features.append(features)
                track_names.append(track['name'])

    df = pd.DataFrame(audio_features)
    df['name'] = track_names
    summary = df[['tempo', 'energy', 'danceability', 'valence']].mean().to_frame(name='average').round(2)
    
    chart = alt.Chart(df).mark_circle(size=80).encode(
        x='energy',
        y='valence',
        color=alt.value('orange'),
        tooltip=['name', 'energy', 'valence']
    ).interactive().properties(title='Valence vs Energy')

    return summary, chart
