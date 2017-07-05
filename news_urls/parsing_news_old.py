# -*- coding: utf-8 -*-
import newspaper
from newspaper import Config, Article

def configs():
    config = Config()
    config.language = 'pt'
    config.MAX_SUMMARY = 500  #number max of characters
    config.fetch_images = False  #we don't want images

    return config


##Function that requires a list of urls and return a generator with the articles
## as objects
def url2features(list_url):
    for url in list_url:
        news_article = Article(url=url, config=configs()) #Create a article
        news_article.download()
        news_article.parse()
        news_article.nlp()

        yield news_article



    ##parse
    #print "Title ----------------------------------------", news_article.title
    #print "Text ----------------------------------------", news_article.text
    #print "URL_News ----------------------------------------", news_article.url
    #print "URL_Source ----------------------------------------", news_article.source_url
    #print "Date ----------------------------------------", news_article.publish_date

    ##nlp
    #print "Summary ----------------------------------------", news_article.summary
    #print "Keywords ----------------------------------------", news_article.keywords
