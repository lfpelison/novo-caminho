# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ArticlesView
from smarturls import surl

app_name = 'api'

urlpatterns = {
    surl('auth/', include('rest_framework.urls',
        namespace='rest_framework')),
    surl('articles/(?P<entities>.+)/$', ArticlesView.as_view()),
}

# Adiciona os sufixos de URL aceitos aos nossos urlpatterns.
# Por padrão adiciona html e json.
urlpatterns = format_suffix_patterns(urlpatterns)
