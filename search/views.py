# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from news_urls import news_urls

def index(request):
    url_list = news_urls.get_urls( ("jose dirceu"), ('google'), 2)
    template = loader.get_template('search/index.html')
    context = {
        'url_list': url_list,
    }
    return HttpResponse(template.render(context, request))
