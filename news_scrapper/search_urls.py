# -*- coding: utf-8 -*-

import requests
from scrapy.selector import Selector
import multiprocessing

def get_body(url):  # downloads the HTML as text
    try:
        return requests.get(url).text.encode('utf-8')
    except Exception as e:
        print e

def format(s_keys, s_engine, pages):    # format the search query into a URL
    if 'google' == s_engine:
        for page_num in pages:
            yield "http://www.google.com.br/search?q={0}&tbm=nws&start={1}".format(s_keys, page_num*10)
    if 'yahoo' == s_engine:
        for page_num in pages:
           yield "https://br.search.yahoo.com/search?p={0}&b={1}".format(s_keys, (page_num*10)+1)
    if 'bing' == s_engine:
        yield "http://www.bing.com/news/search?q={0}".format(s_keys)

def parse(body, s_engine):      # returns the list of URLs from a HTML body
    if 'google' == s_engine:
        urls = []
        for url in Selector(text=body).xpath("//h3[@class='r']/a/@href").extract():
            urls.append(url.strip('/url?q=').split('&sa=U&ved=')[0])
        return urls
    if 'yahoo' == s_engine:
        return Selector(text=body).xpath("//ol/li/div/div/h3/a/@href").extract()
    if 'bing' == s_engine:
        return Selector(text=body).xpath("//*[@id='algocore']/div/@url").extract()

def get_urls_from_engine((s_keys, s_engine, pages)):    # gets the URLs from the results on a single engine
    urls = []
    for search_url in format(s_keys, s_engine, pages):
        for news_url in parse(get_body(search_url), s_engine):
            urls.append(news_url)
    return urls

def get_urls(s_keys,s_engines,pages):
   s_keys = "+".join((key.replace(' ','+') for key in s_keys))
   args = [(s_keys,engine,pages) for engine in s_engines]
   pool = multiprocessing.Pool(multiprocessing.cpu_count()-1 or 1) # gets maximum number of CPU cores minus 1
   urls_list = pool.map(get_urls_from_engine, args)                # returns a list of (URL lists from each engine)
   return [url for urls in urls_list for url in urls]              # "flatten" list

if __name__ == "__main__":
   search_keys = ['neoway']
   print get_urls((search_keys), ['google'], range(1))
