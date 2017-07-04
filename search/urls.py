from django.conf.urls import url
from smarturls import surl


from . import views

urlpatterns = [
    surl('/', views.IndexView.as_view(), name='index'),
]
