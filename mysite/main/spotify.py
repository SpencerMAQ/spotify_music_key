import time
import re

from pprint import pprint
from collections import OrderedDict


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

# TODO: check to see if you can actually embed a mini player (with pause, play, next, back) and maybe a few queues
# ^if none, start doing your own manually-coded player
# https://stackoverflow.com/questions/71979852/how-to-play-and-pause-spotify-embed-with-javascript
# you might have to look into this: https://developer.spotify.com/documentation/web-playback-sdk/quick-start/
# WEB PLAYBACK SDK


def get_current_track_info(json_info: dict) -> dict or None:
    """
    Args:
        the raw unparsed current track info from spotify
    Returns:
        Current track info in a more human-readable dict
        Includes Track ID, Name, Artist, Album art, etc.
    """
    if not json_info:
        return None

    json_resp: dict = json_info

    track_id = json_resp.get('item').get('id')
    track_name = json_resp.get('item').get('name')
    track_name_for_searching = re.sub(r'\(.*?\)', r'', track_name)

    album_art = json_resp.get('item').get('album').get('images')
    if album_art: album_art = album_art[1].get('url')

    artists = [artist for artist in json_resp.get('item').get('artists')]
    first_artist = artists[0].get('name')

    link = json_resp.get('item').get('external_urls').get('spotify')

    artist_names = ', '.join([artist.get('name') for artist in artists])

    current_track_info = OrderedDict({
        "id": track_id,
        "track_name": track_name,
        "artists": artist_names,
        "link": link,
        'first_artist': first_artist,
        'track_name_for_searching': track_name_for_searching,
        'album_art': album_art
    })

    return current_track_info


def get_theory_info(json_info: dict) -> dict or None:
    """
    Args:
        The raw unparsed current track Music theory info
    Returns:
        Human-readable music theory info on the current track
    """
    json_resp = json_info

    # https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-analysis
    key = KEY_MAP.get(json_resp.get('track').get('key'))
    mode = MODE_MAP.get(json_resp.get('track').get('mode'))
    info = {
        'key': key,
        'key_confidence': (json_resp.get('track').get('key_confidence'))*100,
        'mode': mode
    }

    return info


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
