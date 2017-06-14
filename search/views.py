# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from news_urls import news_urls

def index(request):
    url_list = news_urls.get_urls( ("jose dirceu"), ('google'), 2)
    url_list = ["<a href={0}>{0}</a>".format(url) for url in url_list]
    return HttpResponse('<br><br>'.join(url_list))
