# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from news_urls.news_urls import get_urls
from news_urls.parsing_news import url2features
from django.views import generic, View
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from forms import SearchForm

@login_required
def index(request):
    form = SearchForm()
    context = {'form': form}
    if request.method == 'GET':
        form = SearchForm(request.GET)
        print form.is_valid()
        if form.is_valid():
            print form.cleaned_data
            entities = [e.strip(' ') for e in form.cleaned_data['query'].split(',')] # Split and clean query
            search_engines = form.cleaned_data['engines']
            # page = self.request.GET.get('page', 1)
            url_list = get_urls(entities, search_engines, 1) ## TODO: remove forbidden URLs from list
                                                             ## TODO: when scrapper is fixed, change how many pages to get in get_urls
            articles = ["Titulo:{0}\nSumario:\n{1}\n".format(a.title,a.summary) for a in url2features(url_list)]
            context['articles'] = list(articles)
    return render(request, 'search/index.html', context)
