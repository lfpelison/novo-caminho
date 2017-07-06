from django.conf.urls import url
from smarturls import surl


from django.contrib.auth import views as auth_views
from . import views

app_name = 'dashboard'
urlpatterns = [
    surl('/', views.index, name='index'),
    surl('login/', auth_views.login, name='login'),
    surl('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    surl('signup/', views.signup, name='signup'),
    surl('about/', views.about, name='about'),
    surl('services/', views.services, name='services'),
    surl('contact/', views.contact, name='contact'),
]
