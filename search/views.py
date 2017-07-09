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
from sklearn.externals import joblib
import time
import pandas as pd
from sklearn.linear_model import LogisticRegression
import numpy as np

def category_map(cat):
    art = {'category':'Nothing'}
    cat_template = {1:'Manifestacao', 2:'Crime', 3:'Economia', 4:'Politica', 5:'Dano-Ambiental', 6:'Positiva'}
    art['category'] = cat_template[int(cat)]
    return art['category']

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
            #Load predictions models
            risk_classifier = joblib.load('datascience/risk_classifier.cls')
            category_classifier = joblib.load('datascience/category_classifier.cls')
            risk_voc = joblib.load("datascience/risk_voc.cls")
            cat_voc = joblib.load("datascience/cat_voc.cls")

            #Get articl es
            articles_from_search = get_articles(urls_not_in_db)
            for art in articles_from_search:
                risk_summary_dtm = risk_voc.transform([art.summary])
                cat_summary_dtm = cat_voc.transform([art.summary])
                art_risk = risk_classifier.predict(risk_summary_dtm)
                art_category = category_classifier.predict(cat_summary_dtm)
                art_category = category_map(art_category)
                saved_article = Article().fill_and_create(art, entities, art_risk, art_category)
                if saved_article is not None:
                    print "SAVED AN ARTICLE: {0}".format(saved_article)
                    articles_to_display.append(saved_article)

            # filter(positives)
            print articles_to_display
            context['articles'] = articles_to_display
            loadingpagetime = time.time() - start
            print "LOADING PAGE TIME: {0}".format(loadingpagetime)
    return render(request, 'search/index.html', context)
