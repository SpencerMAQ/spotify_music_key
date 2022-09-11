from collections import OrderedDict

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from .models import ToDoList, Item

from . import spotify

def index(response):
    return render(response, 'main/base.html', {})


def home(response):
    return render(response, 'main/home.html', {})


def spotify_view(response):
    import json
    try:
        current_track_info = spotify.get_current_track_info()
    except json.JSONDecodeError:
        current_track_info = None

    if response and current_track_info:
        artist = current_track_info.get('artists')
        first_artist = current_track_info.get('first_artist')
        track = current_track_info.get('track_name')
        track_name_for_searching = current_track_info.get('track_name_for_searching')
        key = current_track_info.get('key')
        mode = current_track_info.get('mode')
        key_confidence = current_track_info.get('key_confidence')

        spotify_info = OrderedDict({
            'artist': artist,
            'track': track,
            'key': key,
            'key_confidence': round(key_confidence, 2),
            'mode': mode,
            'first_artist': first_artist,
            'track_name_for_searching': track_name_for_searching
        })

    else:
        spotify_info = {'artist': 'No song currently playing or Auth Key expired'}

    return render(response, 'main/spotify.html', context=spotify_info)


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
