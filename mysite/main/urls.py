from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('spotify/', views.spotify_view, name='spotify_view'),
    path('spotify_login/', views.spotify_login, name='spotify_login'),
    path('spotify_logout/', views.spotify_logout, name='spotify_logout'),
    path('spotify_temp_redirect/', views.spotify_temp_redirect, name='spotify_temp_redirect'),
    path('ajax_spotify_track_info/', views.ajax_spotify_track_info, name='ajax_spotify_track_info'),
    path('ajax_pause_play/', views.ajax_pause_play, name='ajax_pause_play'),
    path('ajax_next_song/', views.ajax_next_song, name='ajax_next_song'),
]

urlpatterns += staticfiles_urlpatterns()