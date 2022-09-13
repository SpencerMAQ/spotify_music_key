from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('spotify/', views.spotify_view, name='spotify_view'),
    path('spotify_login/', views.spotify_login, name='spotify_login'),
    path('spotify_logout/', views.spotify_logout, name='spotify_logout'),
]

urlpatterns += staticfiles_urlpatterns()