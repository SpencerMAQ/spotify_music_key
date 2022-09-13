import requests
import spotipy
import time
import re

from pprint import pprint
from collections import OrderedDict
from spotipy.oauth2 import SpotifyOAuth

from ._secret_info import CLIENT_ID, CLIENT_SECRET


SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
ACCESS_TOKEN = 'BQCrwuEMO9htK36eV7trWP9o3iwjpCI5IjA3Nu3cCvgvdaRMyj02Akmwt_XoxVHr5So0c5rGN_QvQGl-Oqa7pYTC67kqxncu2Ym0dRBfE-tlX3C48gGo5vGYZnFXXjO-f5K7DtUrYoCuTqznQzN2kZMzhdZzXKVcdwTZoDypBSx8YFZYpjl5BLZevvx8kwh_csr1xWwj'
KEY_MAP = {
    -1: 'No Key Detected',
    0: 'C',
    1: 'C♯/D♭',
    2: 'D',
    3: 'D♯/E♭',
    4: 'E',
    5: 'F',
    6: 'F♯/G♭',
    7: 'G',
    8: 'G♯/A♭',
    9: 'A',
    10: 'A♯/B♭',
    11: 'B'
}

MODE_MAP = {
    0: 'minor',
    1: 'Major'
}

# TODO: better spotify API token, expires less, also try logging in to get auth
# TODO: check to see if you can actually embed a mini player (with pause, play, next, back) and maybe a few queues
# ^if none, start doing your own manually-coded player
# https://stackoverflow.com/questions/71979852/how-to-play-and-pause-spotify-embed-with-javascript
# you might have to look into this: https://developer.spotify.com/documentation/web-playback-sdk/quick-start/
# WEB PLAYBACK SDK

# TODO: might want to check out spotipy's cache handler
# https://spotipy.readthedocs.io/en/master/?highlight=cache#customized-token-caching
# https://github.com/plamere/spotipy/blob/master/examples/app.py#L43

def get_current_track_info() -> dict or None:
    # TODO: implement a retry strategy

    response = requests.get(
        SPOTIFY_GET_CURRENT_TRACK_URL,
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        }
    )

    if response:
        json_resp: dict = response.json()
    else:
        json_resp = None
        return json_resp
    #
    track_id = json_resp['item']['id']
    track_name = json_resp['item']['name']
    track_name_for_searching = re.sub(r'\(.*?\)', r'', track_name)

    album_art = json_resp.get('item').get('album').get('images')
    if album_art: album_art = album_art[1].get('url')

    artists = [artist for artist in json_resp['item']['artists']]
    first_artist = artists[0]['name']

    link = json_resp.get('item').get('external_urls').get('spotify')

    artist_names = ', '.join([artist['name'] for artist in artists])

    theory_info = get_theory_info(track_id=track_id)
    current_track_info = OrderedDict({
        "id": track_id,
        "track_name": track_name,
        "artists": artist_names,
        "link": link,
        'key': theory_info.get('key'),
        'key_confidence': theory_info.get('key_confidence'),
        'mode': theory_info.get('mode'),
        'first_artist': first_artist,
        'track_name_for_searching': track_name_for_searching,
        'album_art': album_art
    })

    return current_track_info

def get_theory_info(track_id: int) -> dict or None:
    response = requests.get(
        f'https://api.spotify.com/v1/audio-analysis/{track_id}',
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        }
    )

    if response:
        json_resp: dict = response.json()
    else:
        json_resp = {}
        return json_resp

    # https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-analysis
    key = KEY_MAP.get(json_resp.get('track').get('key'))
    mode = MODE_MAP.get(json_resp.get('track').get('mode'))
    info = {
        'key': key,
        'key_confidence': (json_resp.get('track').get('key_confidence'))*100,
        'mode': mode
    }

    return info


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri='http://127.0.0.1:8000/spotify_temp_redirect', # TODO: don't hardcode
        scope=['user-read-currently-playing', 'user-modify-playback-state'],
    )


def main():
    current_track_id = None
    while True:
        current_track_info = get_current_track_info()

        if current_track_info.get('id') != current_track_id:
            pprint(
		    	current_track_info,
		    	indent=4,
		    )
            current_track_id = current_track_info['id']

        # TODO (not urgent)
        # https://stackoverflow.com/questions/61366214/getting-a-request-or-notification-when-changing-a-track-in-spotify
        time.sleep(2)


if __name__ == '__main__':
    main()
