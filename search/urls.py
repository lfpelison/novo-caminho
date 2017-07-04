from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from smarturls import surl
import api

from . import views
#app_name = 'search'

urlpatterns = [
    surl('/', views.index, name='index'),
]
