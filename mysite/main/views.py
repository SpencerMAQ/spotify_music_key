from collections import OrderedDict

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from .models import ToDoList, Item

from . import spotify
import spotipy

def index(response):
    return render(response, 'main/base.html', {})


def home(response):
    return render(response, 'main/home.html', {})


def spotify_view(response):
    sp_oauth = spotify.create_spotify_oauth()
    # TODO: session.clear() equiv of session.clear() of flask
    # for key in response.session.keys():
    #     del response.session[key]

    # https://stackoverflow.com/questions/12166368/django-request-session-getname-false-what-does-this-code-mean
    code = response.session.get('code')
    token_info = sp_oauth.get_access_token(code)
    response.session['spotify_token'] = token_info

    return HttpResponse('idk lol')

    # return render(response, 'main/spotify.html')

    # if response and current_track_info:
    #     artist = current_track_info.get('artists')
    #     track = current_track_info.get('track_name')
    #     key = current_track_info.get('key')
    #     mode = current_track_info.get('mode')
    #     key_confidence = current_track_info.get('key_confidence')
    #
    #     spotify_info = OrderedDict({
    #         'artist': artist,
    #         'track': track,
    #         'key': key,
    #         'key_confidence': round(key_confidence, 2),
    #         'mode': mode,
    #     })
    #
    #     print(spotify_info)

        # TODO: auto refresh site when track changes
        # https://stackoverflow.com/questions/19094720/how-to-automatically-reload-django-when-files-change

    # else:
    #     spotify_info = {'artist': 'Spotify currently not playing or auth code expired'}

    # return render(response, 'main/spotify.html', context=spotify_info)


def spotify_authorize(response):
    sp_oauth = spotify.create_spotify_oauth()
    # reset session first
    try:
        del response.session['spotify_token']
    except KeyError:
        pass

def spotify_login(response):
    # cache_handler = spotipy.cache_handler.DjangoSessionCacheHandler(response)
    # # creates a spotipy.oauth2.SpotifyOAuth object
    # auth_manager = spotify.create_spotify_oauth(cache_handler=cache_handler)
    #
    # if response.session.get('code'):
    #     auth_manager.get_access_token(response.session.get('code'))
    #     return redirect('/spotify')
    #
    # if not auth_manager.validate_token(cache_handler.get_cached_token()):
    #     auth_url = auth_manager.get_authorize_url()
    #     return HttpResponse(f'<h2><a href="{auth_url}">Sign in</a></h2>')


    # creates a spotipy.oauth2.SpotifyOAuth object
    sp_oauth = spotify.create_spotify_oauth()
    # the pop up page form spotify to authorize???
    auth_url = sp_oauth.get_authorize_url()
    # django takes you to auth_url then
    return redirect(auth_url)

def spotify_logout(response):
    # TODO
    # https://github.com/plamere/spotipy/blob/master/examples/app.py#L67
    pass


def create_todo(response):
    """
    Create a to-do list
    Then redirects to the list you just created
    """
    from .forms import CreateNewList

    if response.method == 'POST':
        # response.POST contains all of the inputted info into the form
        form = CreateNewList(response.POST)

        if form.is_valid():
            n = form.cleaned_data['name']
            t = ToDoList(name=n)
            t.save()

        # view the list you just created
        return HttpResponseRedirect(f'/{t.id}')

    else:
        form = CreateNewList()

    return render(response, 'main/create_todo.html', {'form': form})
