# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from news_scrapper.search_urls import get_urls
from news_scrapper.url_parser import get_articles
from django.views import generic, View
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from forms import *
from models import Article, Query, Keyword
import time, sys, json
from reportlab.pdfgen import canvas
from io import BytesIO
from time import gmtime, strftime


from datascience.news_classifier import NewsClassifier


from django.core.files.storage import FileSystemStorage

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from urlparse import urlparse




def save_articles(articles, entities):
    saved_articles = []
    for art in articles:
        predictions = NewsClassifier().news_predictions(art.summary)
        saved_article = Article().fill_and_create(art, entities, predictions['risk'], predictions['category'])
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


def get_domain(url):
    return urlparse(url).netloc

def calculate_risk(entities):
    risk = {}
    for entity in entities:
        articles = [art for art in Article.objects.all() if entity in art.entities]
        l=[art.risk for art in articles if art.risk != None]
        if len(l)>0:
            risk[entity] = float(sum(l))/len(l)
        else:
            risk[entity] = 1
    return risk


@login_required
def index(request):
    form = SearchForm(user=request.user)
    context = {'form': form}

    if request.method == 'GET':
        start = time.time()
        page = int(request.GET.get('page',1)) # Gets the page number or 1 if it does not exist in the GET dict
        context['page'] = page
        form = SearchForm(request.GET,user=request.user)
        if form.is_valid():
            entities = [e.strip(' ').lower() for e in form.cleaned_data['query'].split(',')] # Split and clean query
            search_engines = form.cleaned_data['engines']
            keywords = form.cleaned_data['keywords']
            search_keys = entities + keywords

            print page
            urls = get_urls(search_keys, search_engines, range(page-1,page))

            ignored_domains = [ign.name for ign in request.user.ignoreddomain_set.all()]                 # Gets all IgnoredDomains from User
            urls = [url for url in urls if get_domain(url) not in ignored_domains] # Gets the non-ignored URLs

            [articles_to_display, urls_not_in_db] = check_articles_db(urls, entities)   # checks the URLs from the search, and returns the Articles
                                                                                        # already stored, as well as the URLs th(at are not stored

            articles_from_search = get_articles(urls_not_in_db)             # downloads "Newspaper Articles" from the URLs given
            saved_articles = save_articles(articles_from_search, entities)  # saves the "Newspaper Articles" into "Django Articles" and returns them
            context['risks'] = calculate_risk(entities)
            for entity in entities:
                context['risks'][entity] = int(100*(context['risks'][entity]-1)/2) # Format to percent

            if saved_articles:
                articles_to_display += saved_articles                       # show the just saved Articles

            if 'dont_save_query' not in request.GET:
                query = Query.objects.create(name="Pesquisa sobre {0}".format(entities), user=request.user, entities=json.dumps(entities), engines=json.dumps(search_engines))
            articles_to_display = [art for art in articles_to_display if art.category != "Positiva"]
            context['articles'] = articles_to_display
            context['urls'] = urls
            categories_dict = {}
            for art in articles_to_display:
                if art.category not in categories_dict.keys():
                    categories_dict[art.category] = 1
                else:
                    categories_dict[art.category] += 1
            context['categories'] = categories_dict
            loadingpagetime = time.time() - start
            print "LOADING PAGE TIME: {0}".format(loadingpagetime)
        else:
            print "-----FORMULARIO INVALIDO------"

    return render(request, 'search/index.html', context)



@login_required
def history(request):
    context = {'queries':request.user.query_set.all()}
    return render(request, 'search/history.html', context)


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
            article_in_db = Article.objects.filter(url=str(url)).first()
            if article_in_db is not None:
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
                if article_in_db.risk == 1:
                    bogustext = "Risco dessa notícia: Baixo."
                    p = Paragraph(bogustext, style)
                    Story.append(p)
                elif article_in_db.risk == 2:
                    bogustext = "Risco dessa notícia: Médio."
                    p = Paragraph(bogustext, style)
                    Story.append(p)
                elif article_in_db.risk == 3:
                    bogustext = "Risco dessa notícia: Alto."
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


@login_required
def configuration(request):
    context = {
        'keyword_form':KeywordForm(),
        'ignored_form':IgnoredDomainForm(),
        'keywords':request.user.keyword_set.all(),
        'ignored_domains':request.user.ignoreddomain_set.all(),
        }
    return render(request, 'search/configuration.html', context)


@login_required
def create_keyword(request):
    if request.method == "POST":
        form = KeywordForm(request.POST)
        if form.is_valid():
            form.instance.name = form.instance.name.lower()
            form.instance.user = request.user
            print form.save()
    return redirect(reverse('search:config'))

@login_required
def create_ignored(request):
    if request.method == "POST":
        form = IgnoredDomainForm(request.POST)
        if form.is_valid():
            form.instance.name = form.instance.name.lower()
            form.instance.user = request.user
            print form.save()
    return redirect(reverse('search:config'))

@login_required
def delete_keyword(request):
    if request.method == "POST":
        keyword_id = request.POST['keyword_id']
        Keyword.objects.get(pk=keyword_id).delete()
    return redirect(reverse('search:config'))

@login_required
def delete_ignored(request):
    if request.method == "POST":
        ignored_id = request.POST['ignored_id']
        IgnoredDomain.objects.get(pk=ignored_id).delete()
    return redirect(reverse('search:config'))
