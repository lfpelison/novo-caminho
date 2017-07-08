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
from models import Article, Query
import time, sys, json


def save_articles(articles, entities):
    saved_articles = []
    for art in articles:
        saved_article = Article().fill_and_create(art, entities)
        if saved_article is not None:
            print "SAVED AN ARTICLE: {0}".format(saved_article).encode('utf-8')
            sys.stdout.flush()
            saved_articles.append(saved_article)
    return saved_articles

def check_articles_db(urls, entities):
    urls_not_in_db = []
    articles_to_display = []
    for url in urls:
        article_in_db = Article.objects.filter(url=url).first()
        if article_in_db is None:
            urls_not_in_db.append(url)
        else:
            article_in_db.entities = list(set(article_in_db.entities).union(set(entities))) # update the Article's entities
            article_in_db.save()
            articles_to_display.append(article_in_db)
    return [articles_to_display, urls_not_in_db]


@login_required
def index(request):
    form = SearchForm()
    context = {'form': form}
    if request.method == 'GET':
        start = time.time()

        form = SearchForm(request.GET)
        if form.is_valid():
            entities = [e.strip(' ') for e in form.cleaned_data['query'].split(',')] # Split and clean query
            search_engines = form.cleaned_data['engines']

            # page = self.request.GET.get('page', 1)
            urls = get_urls(entities, search_engines, range(1)) ## TODO: remove forbidden URLs from list
                                                                ## TODO: pagination
                                                                ## TODO: categories and risk
            urls_not_in_db = []
            articles_to_display = []

            [articles_to_display, urls_not_in_db] = check_articles_db(urls, entities)   # checks the URLs from the search, and returns the Articles
                                                                                        # already stored, as well as the URLs th(at are not stored

            articles_from_search = get_articles(urls_not_in_db)             # downloads "Newspaper Articles" from the URLs given
            saved_articles = save_articles(articles_from_search, entities)  # saves the "Newspaper Articles" into "Django Articles" and returns them
            articles_to_display.append(saved_articles)                      # show the just saved Articles

            query = Query.objects.create(name="Pesquisa sobre {0}".format(entities), user=request.user, entities=json.dumps(entities), engines=json.dumps(search_engines))
            print query
            print articles_to_display
            context['articles'] = articles_to_display
            loadingpagetime = time.time() - start
            print "LOADING PAGE TIME: {0}".format(loadingpagetime)
    return render(request, 'search/index2.html', context)

@login_required
def history(request):
    context = {'queries':request.user.query_set.all()}
    return render(request, 'search/history.html', context)
