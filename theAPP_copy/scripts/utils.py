import spotipy
from spotipy.oauth2 import SpotifyOAuth

import pandas as pd
import json


def keep_keys(dictionary, keys):
    return {key: dictionary[key] for key in keys if key in dictionary}


CLIENT_ID = "b8db48d0784f4e2b9ab719adc118e918"
CLIENT_SECRET = "0a7feca73df44f1c829f125dbe8a6b91"


def get_df(userID, userSecret, debug=False):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=userID,
                                                   client_secret=userSecret,
                                                   redirect_uri="http://localhost:3000",
                                                   scope="user-read-recently-played"))

    results = sp.current_user_recently_played(limit=50)

    def get_track_info(row):
        track_ID = row['song_ID']
        res = sp.audio_features(track_ID)
        keys = [
            'danceability',
            'energy',
            'loudness',
            'speechiness',
            'acousticness',
            'instrumentalness',
            'liveness',
            'valence',
            'tempo',
        ]
        fetures = keep_keys(res[0], keys=keys)
        # print(json.dumps(fetures, indent=2))
        return fetures

    fetched_songs = []
    for item in results['items']:
        item_data = {
            "TIME_STAMP": item['played_at'],
            "song_ID": item['track']['id'],
            "song_Name": item['track']['name'],
            # TODO for all artists
            "artist": item['track']['artists'][0]['name'],
            "album": item['track']['album']['id'],
            "album_name": item['track']['album']['name'],
            "popularity": item['track']['popularity'],
            "explicit": item['track']['explicit'],
        }
        fetched_songs.append(item_data)
    df = pd.DataFrame(fetched_songs)

    sample_df = df.copy()
    sample_df[[
        'danceability',
        'energy',
        'loudness',
        'speechiness',
        'acousticness',
        'instrumentalness',
        'liveness',
        'valence',
        'tempo',
    ]] = sample_df.apply(get_track_info, axis=1, result_type='expand')

    return sample_df


if __name__ == "__main__":
    print(get_df(CLIENT_ID, CLIENT_SECRET, debug=True))
