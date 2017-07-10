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
<<<<<<< HEAD
    surl('download/', views.download, name='download'),

=======
    surl('config/', views.configuration, name='config'),
    surl('create_keyword/', views.create_keyword, name='create_keyword'),
    surl('create_ignored/', views.create_ignored, name='create_ignored'),
    surl('delete_keyword/', views.delete_keyword, name='delete_keyword'),
    surl('delete_ignored/', views.delete_ignored, name='delete_ignored'),
>>>>>>> 21aad1cedc77eb5c602ac26e0ff10ca4e981c757
]
