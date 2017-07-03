import newspaper
from newspaper import Config, Article
from lxml import etree

def configs():
    config = Config()
    config.language = 'pt'
    config.MAX_SUMMARY = 500  #number max of characters
    config.fetch_images = False  #we don't want images

    return config


##Function that requires a list of urls and return a json with Title, Text,
#Summary, URL, Date and Keywords
def url2features(list_url):

    for url in list_url:
        news_article = Article(url=url, config=configs()) #Create a article
        try:
            news_article.download()
            news_article.parse()
            news_article.nlp()
            yield news_article.summary
        except etree.XMLSyntaxError:
            print "\n\nBad XML\n\n"
        except newspaper.article.ArticleException:
            print "\n\nARTICLE ERROR\n\n"
