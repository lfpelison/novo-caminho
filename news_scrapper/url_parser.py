import newspaper
from newspaper import Config, Article
from lxml import etree
import multiprocessing
import logging
import traceback

config = Config()
config.language = 'pt'
config.MAX_SUMMARY = 500  #number max of characters
config.fetch_images = False  #we don't want images



# Requires an URL and returns the Article object
def get_article(url):
    article = Article(url=url, config=config) #Create a article
    try:
        article.download()
        article.parse()
        article.nlp()
        return article
    except Exception as e:
        logging.error(traceback.format_exc())

# Gets the Articles using multiprocessing to raise performance
def get_articles(urls):
    pool = multiprocessing.Pool(multiprocessing.cpu_count()-1 or 1) # gets maximum number of CPU cores minus 1
    articles = [article for article in pool.map(get_article, urls) if article is not None]                              # returns the articles
    return articles

if __name__ == "__main__":
    urls = [u'http://www.em.com.br/app/noticia/politica/2017/07/06/interna_politica,881792/nova-legenda-pode-abrigar-bolsonaro-nas-eleicoes-presidenciais-de-2018.shtml']
    print urls
    art = get_articles(urls)
    print art
    for article in art:
        print article.summary.encode('utf-8')
        print article.publish_date
