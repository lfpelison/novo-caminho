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
    #url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^password_reset/$', views.password_reset, {'post_reset_redirect' : 'password_reset_done'},name="password_reset"),
    url(r'^confirmation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activationview, name='activation'),
    ]
