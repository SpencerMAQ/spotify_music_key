import requests
import time
import spotipy

from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
from collections import OrderedDict

# from . import views

from django.urls import path

SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
ACCESS_TOKEN = 'BQCK29suRvw-TlQRoSwjexcCQk1p0lhBLsVHH7_Ntx1iKOScpF7Mt8HxKVllpPl_EpqNIFCG1Du01STdDqAcEX0_TewwhlByvE-mDEQysarkzM69O9OibMg4USlmoYyPNvUfZ6KiX2gb-6X2XU5kRCJwg2-HrXmlqN8U7OIb-TPb08xvC1E1k5yOCU-rrXfY9BOUiAYf'
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
        json_resp = response.json()
    else:
        json_resp = None
        return json_resp

    track_id = json_resp['item']['id']
    track_name = json_resp['item']['name']
    artists = [artist for artist in json_resp['item']['artists']]

    link = json_resp['item']['external_urls']['spotify']

    artist_names = ', '.join([artist['name'] for artist in artists])

    theory_info = get_theory_info(track_id=track_id)
    current_track_info = OrderedDict({
        "id": track_id,
        "track_name": track_name,
        "artists": artist_names,
        "link": link,
        'key': theory_info.get('key'),
        'key_confidence': theory_info.get('key_confidence'),
        'mode': theory_info.get('mode')
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
        print(response)
        json_resp: dict = response.json()
    else:
        json_resp = None
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


# def create_spotify_oauth():
#     return SpotifyOAuth(
#         client_id='9f02cc6a5c9341b0be33ee481fcf77ce',
#         client_secret='62b96979822148ed833854e7cb74d079',
#         redirect_uri='http://127.0.0.1:8000/spotify', # TODO: don't hardcode
#         scope=['user-read-currently-playing', 'user-modify-playback-state'],
#     )


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
