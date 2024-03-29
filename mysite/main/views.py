from collections import OrderedDict

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse


import spotipy
from .sp_token_utils import (update_or_create_user_tokens,
                             is_spotify_token_still_valid,
                             refresh_spotify_token, get_user_tokens,
                             create_spotify_oauth,
                             logout_and_delete_spotify_tokens)
from .spotify import get_current_track_info, get_theory_info

import time

def index(response):
    return render(response, 'main/base.html', {})


def home(response):
    return render(response, 'main/home.html', {})


def spotify_login(response):
    sp_oauth = create_spotify_oauth()
    external_auth_url = sp_oauth.get_authorize_url()

    return redirect(external_auth_url)


def spotify_temp_redirect(response):
    """
    Temp page where we get the auth code then exchange it for
    an OAuth Token
    """
    # TODO: redirect this to the main spotify page
    sp_oauth = create_spotify_oauth()
    # https://youtu.be/rYDDWVuv-kI?t=1193
    code = response.GET.get('code')
    error = response.GET.get('error') # TODO

    # DeprecationWarning: You're using 'as_dict = True'.get_access_token will return the token string directly in future versions.
    # Please adjust your code accordingly, or use get_cached_token instead.
    #   spotify_token = sp_oauth.get_access_token(code=code)
    sp_access_token_dict: dict = sp_oauth.get_access_token(code=code)

    if not response.session.exists(response.session.session_key):
        response.session.create()
    print('dasdsa', sp_access_token_dict)
    update_or_create_user_tokens(
        session_id=response.session.session_key,
        access_token=sp_access_token_dict.get('access_token'),
        expires_in=sp_access_token_dict.get('expires_in'),
        expires_at=sp_access_token_dict.get('expires_at'),
        refresh_token=sp_access_token_dict.get('refresh_token')
    )

    return redirect('spotify_view')


def spotify_logout(response):
    # session_id = response.session.session_key
    logout_and_delete_spotify_tokens()

    return render(response, 'main/spotify_logout.html', context={})


def spotify_view(response):
    session_id = response.session.session_key

    sp_token_django_obj = get_user_tokens(session_id=session_id)
    if not sp_token_django_obj:
        spotify_info = {'artist': 'You are not logged into Spotify'}
        return render(response, 'main/spotify.html', context=spotify_info)

    # print(f'valid or not: {is_spotify_token_still_valid(session_id=session_id)}')
    if not is_spotify_token_still_valid(session_id=session_id):
        refresh_spotify_token(session_id=session_id)
        sp_token_django_obj = get_user_tokens(session_id=session_id)

    # print(sp_token_django_obj.expires_at - time.time()) # TODO: delete this, just debugging stuff
    # print(sp_token_django_obj)
    sp = spotipy.Spotify(auth=sp_token_django_obj.access_token,
                         requests_timeout=10)
    current_track_info = get_current_track_info(sp.current_user_playing_track())
    if current_track_info:
        id = sp.current_user_playing_track().get('item').get('id')

    # and id because i get and error if the song is a local track (i.e. no ID)
    if current_track_info and id:

        current_track_theory_info = sp.audio_analysis(track_id=id)
        current_track_theory_info = get_theory_info(current_track_theory_info)

    # if response and current_track_info: # TODO: error handling if response contains and error or smthn
        artist = current_track_info.get('artists')
        first_artist = current_track_info.get('first_artist')
        track = current_track_info.get('track_name')
        track_name_for_searching = current_track_info.get('track_name_for_searching')
        key = current_track_theory_info.get('key')
        mode = current_track_theory_info.get('mode')
        key_confidence = current_track_theory_info.get('key_confidence')
        if key_confidence: key_confidence = round(key_confidence, 2)

        album_art = current_track_info.get('album_art')

        spotify_info = OrderedDict({
            'artist': artist,
            'track': track,
            'key': key,
            'key_confidence': key_confidence,
            'mode': mode,
            'first_artist': first_artist,
            'track_name_for_searching': track_name_for_searching,
            'album_art': album_art
        })

    else:
        spotify_info = {'artist': 'No song currently playing'}

    return render(response, 'main/spotify.html', context=spotify_info)

def ajax_spotify_track_info(response):
    # https://koenwoortman.com/python-django-view-return-json-response/#:~:text=The%20JsonResponse%20transforms%20the%20data,to%20be%20transformed%20to%20JSON.
    session_id = response.session.session_key

    sp_token_django_obj = get_user_tokens(session_id=session_id)
    if not sp_token_django_obj:
        return JsonResponse({})

    if not is_spotify_token_still_valid(session_id=session_id):
        refresh_spotify_token(session_id=session_id)
        sp_token_django_obj = get_user_tokens(session_id=session_id)

    sp = spotipy.Spotify(auth=sp_token_django_obj.access_token,
                         requests_timeout=10)
    current_track_info = get_current_track_info(sp.current_user_playing_track())
    if current_track_info:
        id = sp.current_user_playing_track().get('item').get('id')

    # and id because i get and error if the song is a local track (i.e. no ID)
    if current_track_info and id:

        current_track_theory_info = sp.audio_analysis(track_id=id)
        current_track_theory_info = get_theory_info(current_track_theory_info)

        # if response and current_track_info: # TODO: error handling if response contains and error or smthn
        artist = current_track_info.get('artists')
        first_artist = current_track_info.get('first_artist')
        track = current_track_info.get('track_name')
        track_name_for_searching = current_track_info.get('track_name_for_searching')
        key = current_track_theory_info.get('key')
        mode = current_track_theory_info.get('mode')
        key_confidence = current_track_theory_info.get('key_confidence')
        if key_confidence: key_confidence = round(key_confidence, 2)

        album_art = current_track_info.get('album_art')

        spotify_info = OrderedDict({
            'artist': artist,
            'track': track,
            'key': key,
            'key_confidence': key_confidence,
            'mode': mode,
            'first_artist': first_artist,
            'track_name_for_searching': track_name_for_searching,
            'album_art': album_art,
            'is_playing': current_track_info.get('is_playing')
        })

    else:
        spotify_info = {'artist': 'No song currently playing'}


    # TODO: test when no track is playing
    # ajax_info = get_current_track_info(current_track_info)
    # print(current_track_info.get('progress_ms'))
    # print(type(current_track_info.get('progress_ms')))
    # x = sp.start_playback()
    print('playing or not: ', spotify_info.get('is_playing'))
    # print('track: ', spotify_info.get('artist'))
    # print(x)
    return JsonResponse(spotify_info)

def ajax_pause_play(response):
    """
    pauses or plays the current track from JS
    based on click events from JS
    """
    status_to_send_to_sp = response.GET.get('status_to_send_to_sp')
    # print(status_to_send_to_sp)
    session_id = response.session.session_key

    sp_token_django_obj = get_user_tokens(session_id=session_id)
    if not sp_token_django_obj:
        return

    if not is_spotify_token_still_valid(session_id=session_id):
        refresh_spotify_token(session_id=session_id)
        sp_token_django_obj = get_user_tokens(session_id=session_id)

    sp = spotipy.Spotify(auth=sp_token_django_obj.access_token,
                         requests_timeout=10)
    x = None
    if status_to_send_to_sp == 'play':
        x = sp.start_playback()
    elif status_to_send_to_sp == 'pause':
        x = sp.pause_playback()


    return JsonResponse({'a': x})


def ajax_next_song(response):
    session_id = response.session.session_key

    sp_token_django_obj = get_user_tokens(session_id=session_id)
    if not sp_token_django_obj:
        return

    if not is_spotify_token_still_valid(session_id=session_id):
        refresh_spotify_token(session_id=session_id)
        sp_token_django_obj = get_user_tokens(session_id=session_id)

    sp = spotipy.Spotify(auth=sp_token_django_obj.access_token,
                         requests_timeout=10)

    sp.next_track()

    # shit expects a json idk bruh
    return JsonResponse({})
