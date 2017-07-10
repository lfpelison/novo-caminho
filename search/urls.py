from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from smarturls import surl
import api

from . import views

app_name = 'search'

urlpatterns = [
    surl('/', views.index, name='index'),
    surl('history/', views.history, name='history'),
    surl('config/', views.configuration, name='config'),
    surl('keyword/', views.keyword, name='keyword'),
    surl('ignored/', views.ignored, name='ignored'),
]
