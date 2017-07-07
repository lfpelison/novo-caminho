# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from news_scrapper.search_urls import get_urls
from news_scrapper.url_parser import get_articles
from django.views import generic, View
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from forms import SearchForm
from models import Article
import time, sys

@login_required
def index(request):
    form = SearchForm()
    context = {'form': form}
    if request.method == 'GET':
        start = time.time()

        form = SearchForm(request.GET)
        print form.is_valid()
        if form.is_valid():
            print form.cleaned_data
            entities = [e.strip(' ') for e in form.cleaned_data['query'].split(',')] # Split and clean query
            search_engines = form.cleaned_data['engines']
            # page = self.request.GET.get('page', 1)
            urls = get_urls(entities, search_engines, range(1)) ## TODO: remove forbidden URLs from list
                                                                ## TODO: when scrapper is fixed, change how many pages to get in get_urls
                                                                ## TODO: new entity same url---DONE
            urls_not_in_db = []
            articles_to_display = []
            for url in urls:
                article_in_db = Article.objects.filter(url=url).first()
                if article_in_db is None:
                    urls_not_in_db.append(url)
                else:
                    article_in_db.entities = list(set(article_in_db.entities).union(set(entities))) # gets the union between the entities
                    article_in_db.save()
                    articles_to_display.append(article_in_db)

            articles_from_search = get_articles(urls_not_in_db)
            for art in articles_from_search:
                saved_article = Article().fill_and_create(art, entities)
                if saved_article is not None:
                    print "SAVED AN ARTICLE: {0}".format(saved_article).encode('utf-8')
                    sys.stdout.flush()
                    articles_to_display.append(saved_article)

            # predict(articles)
            # filter(positives)
            print articles_to_display
            context['articles'] = articles_to_display
            loadingpagetime = time.time() - start
            print "LOADING PAGE TIME: {0}".format(loadingpagetime)
    return render(request, 'search/index2.html', context)
