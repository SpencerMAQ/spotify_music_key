"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# defines things like 127.0.0.1:8080/home
# / signin, etc.
urlpatterns = [
    # 127.0.0.1:8080/admin
    path('admin/', admin.site.urls),
    # path '' means just the main page as IT IS (e.g. google.com) nothing follows (y8.com)
    # include('main.urls') means we'll simply be redirected to main/urls.py (not mysite/urls.py)

    # 127.0.0.1:8080
    # what the code below means:
    # if you don't type admin or anything after 127.0.0.1:8080
    # then whatever path is going to be passed over to main/urls.py
    path('', include('main.urls')),
]
