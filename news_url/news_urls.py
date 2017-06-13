# -*- coding: utf-8 -*-

import requests
from scrapy.selector import Selector
search_keys = ('jose dirceu', 'pt')

def get_body(url):
    return requests.get(url).text.encode('utf-8')

def google_format(s_keys, pages):
    for i in range(pages):
        yield "http://www.google.com.br/search?q={0}&tbm=nws&start={1}".format(s_keys, i*10)

def google_parse(body):
    for url in Selector(text=body).xpath("//h3[@class='r']/a/@href").extract():
        yield url.strip('/url?q=')

def bing_format(s_keys):    # o search do bing so tem uma pagina
    return "http://www.bing.com/news/search?q={0}".format(s_keys)

def bing_parse(body):
    return Selector(text=body).xpath("//*[@id='algocore']/div/@url").extract()


def yahoo_format(s_keys, pages):
    for i in range(pages):
        yield "https://br.search.yahoo.com/search?p={0}&b={1}".format(s_keys, i*10-9)
def yahoo_parse(body):
    return Selector(text=body).xpath("//ol/li/div/div/h3/a/@href").extract()



def get_urls(s_keys,s_engines,pages):
    s_keys = "+".join((key.replace(' ','+') for key in s_keys))
    if 'google' in s_engines:
        for search_url in google_format(s_keys, pages):
            for news_url in google_parse(get_body(search_url)):
                yield news_url
    if 'bing' in s_engines:
        search_url = bing_format(s_keys)
        for news_url in bing_parse(get_body(search_url)):
            yield news_url
    if 'yahoo' in s_engines:
        for search_url in yahoo_format(s_keys, pages):
            for news_url in yahoo_parse(get_body(search_url)):
                yield news_url

if __name__ == "__main__":
    for url in get_urls(search_keys, ['google'], 10):
        print url
