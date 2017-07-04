from django.conf.urls import url
from smarturls import surl


from . import views

app_name = 'dashboard'
urlpatterns = [
    surl('/', views.index, name='index'),
]
