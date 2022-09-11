from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('spotify/', views.spotify_view, name='create_todo'),
]

urlpatterns += staticfiles_urlpatterns()