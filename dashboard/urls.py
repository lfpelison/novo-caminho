from django.conf.urls import url
from smarturls import surl


from django.contrib.auth import views as auth_views
from . import views

app_name = 'dashboard'
urlpatterns = [
    surl('/', views.index, name='index'),
    surl('login/', auth_views.login, name='login'),
    surl('signup/', views.signup, name='signup'),
]
