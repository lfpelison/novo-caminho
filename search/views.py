# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from news_scrapper.search_urls import get_urls
from news_scrapper.url_parser import get_articles
from django.views import generic, View
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from forms import SearchForm
from models import Article, Query, Keyword
import time, sys, json
from reportlab.pdfgen import canvas
from io import BytesIO
from time import gmtime, strftime


from django.core.files.storage import FileSystemStorage

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from urlparse import urlparse


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
    form = SearchForm(user=request.user)
    context = {'form': form}
    if request.method == 'GET':
        start = time.time()
        form = SearchForm(request.GET,user=request.user)
        if form.is_valid():
            entities = [e.strip(' ') for e in form.cleaned_data['query'].split(',')] # Split and clean query
            search_engines = form.cleaned_data['engines']
            keywords = form.cleaned_data['keywords']
            search_keys = entities + keywords
            # page = self.request.GET.get('page', 1)
            urls = get_urls(search_keys, search_engines, range(1)) ## TODO: remove forbidden URLs from list
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
            print search_keys
            print articles_to_display
            context['articles'] = articles_to_display
            context['urls'] = urls
            loadingpagetime = time.time() - start
            print "LOADING PAGE TIME: {0}".format(loadingpagetime)
        else:
            print "-----FORMULARIO INVALIDO------"
    return render(request, 'search/index.html', context)



@login_required
def history(request):
    context = {'queries':request.user.query_set.all()}
    return render(request, 'search/history.html', context)

def get_domain(url):
    return urlparse(url).netloc


@login_required
def download(request):
    #form = ReportForm()
    #context = {'form': form}
    if request.method == 'GET':
        urls = request.GET.getlist("article_url")
        #form = ReportForm(request.GET.getlist("article_url[]"))
        time = strftime("%Y-%m-%d-%H_%M_%S", gmtime())
        doc = SimpleDocTemplate("/tmp/relatorioNOTICIAS%s.pdf" %time)
        styles = getSampleStyleSheet()
        Story = [Spacer(1,0*inch)]
        style = styles["Normal"]
        bogustext = ("Relatório de notícias:")
        p = Paragraph(bogustext, style)
        Story.append(p)
        Story.append(Spacer(1,0.2*inch))
        for i, url in enumerate(urls):
            article_in_db = Article.objects.filter(url=url).first()
            bogustext = ("%d. Título da notícia: %s." % (i+1, article_in_db.title))
            p = Paragraph(bogustext, style)
            Story.append(p)
            bogustext = ("Resumo da notícia: %s." % article_in_db.long_summary)
            p = Paragraph(bogustext, style)
            Story.append(p)
            if article_in_db.publish_date != None:
                bogustext = ("Data de publicação: %s." % article_in_db.publish_date)
                p = Paragraph(bogustext, style)
                Story.append(p)
            bogustext = ("Risco dessa notícia: %s." % article_in_db.risk)
            p = Paragraph(bogustext, style)
            Story.append(p)
            bogustext = "Entidades envolvidas na notícia: "
            for entity in article_in_db.entities:
                bogustext += ("%s " %entity)
            p = Paragraph(bogustext, style)
            Story.append(p)
            bogustext = ("Categoria da notícia: %s." % article_in_db.category)
            p = Paragraph(bogustext, style)
            Story.append(p)
            bogustext = ("Fonte da notícia: %s" % get_domain(url))
            p = Paragraph(bogustext, style)
            Story.append(p)
            bogustext = ("Url da notícia: %s" % url)
            p = Paragraph(bogustext, style)
            Story.append(p)
            Story.append(Spacer(1,0.2*inch))
        doc.build(Story)

        fs = FileSystemStorage("/tmp")
        with fs.open("relatorioNOTICIAS%s.pdf" %time) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = ('attachment; filename="relatorioNOTICIAS%s.pdf"' %time)
            return response

    return response
