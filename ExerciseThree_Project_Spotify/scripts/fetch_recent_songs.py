import spotipy
from spotipy.oauth2 import SpotifyOAuth

import argparse
import json


parser = argparse.ArgumentParser(description='Process user input.')
parser.add_argument('--user', type=str, choices=['L', 'C'], help='User choice')

args = parser.parse_args()

print('User choice:', args.user)

if args.user == 'C':
    # Claras Credential
    CLIENT_ID = "b8db48d0784f4e2b9ab719adc118e918"
    CLIENT_SECRET = "0a7feca73df44f1c829f125dbe8a6b91"
else:
    # Lukas Credentials
    CLIENT_ID = "207e1c72689d4a0a88e0e721cb9bb254"
    CLIENT_SECRET = "2b98d70fb10b4ca1b0008405a353d35c"


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri="http://localhost:3000",
                                               scope="user-read-recently-played"))

results = sp.current_user_recently_played(limit=50)
# print(json.dumps(results['items'][-1], indent=2))

pop = 0
for item in results['items']:
    track = item['track']
    # print(track)
    print(
        str(item['played_at']) +
        str(track['popularity']) +
        ' ' + track['name'] +
        ' - ' + track['artists'][0]['name']
    )
    pop += int(track['popularity'])


print('corcy different kinda girl score: ' + str(pop/50))
