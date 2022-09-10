from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('spotify/', views.spotify_view, name='create_todo'),
    # path('/spotify', views.spotify_view, name='create_todo'),
    path('spotify_login/', views.spotify_login, name='spotify_login'),
]
