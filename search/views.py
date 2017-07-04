# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from django.shortcuts import render, get_object_or_404
from news_urls import news_urls
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin


#class IndexView(LoginRequiredMixin, generic.ListView): para proibir usuarios nao logados de acessar essa pagina
class IndexView(generic.ListView):
    template_name = 'search/index.html'
    context_object_name = 'url_list'

    def get_queryset(self):
        return news_urls.get_urls( ("jose dirceu"), ('google'), 2)
