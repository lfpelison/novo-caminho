# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from googleScrap.items import GooglescrapItem

class UrlgoogleSpider(scrapy.Spider):
    name = "urlgoogle"
    #def __init__(self):
    allowed_domains = ["www.google.com.br"]
    start_urls = ['http://www.google.com.br/search?q=jose+dirceu&tbm=nws&start=0']

    def parse(self, response):
        sel = Selector(response)
        for link in (sel.xpath('//h3[@class="r _gJs"]/a[@class="l _PMs"]/@href').extract()):
        #for link in sel.xpath('//h2[@class="esc-lead-article-title"]/a/@url').extract():
            item = GooglescrapItem()
            item['link'] = link
            print link
            yield item

#'http://news.google.com/news/section?q=dirceu'


#http://www.google.com.br/search?q=jose+dirceu&tbm=nws&start=10',
#'http://www.google.com.br/search?q=jose+dirceu&tbm=nws&start=20',
#'http://www.google.com.br/search?q=jose+dirceu&tbm=nws&start=30',
#'http://www.google.com.br/search?q=jose+dirceu&tbm=nws&start=40',
#'http://www.google.com.br/search?q=jose+dirceu&tbm=nws&start=50',
#'http://www.google.com.br/search?q=jose+dirceu&tbm=nws&start=60',
#'http://www.google.com.br/search?q=jose+dirceu&tbm=nws&start=70',
#'http://www.google.com.br/search?q=jose+dirceu&tbm=nws&start=80',
#'http://www.google.com.br/search?q=jose+dirceu&tbm=nws&start=90',
#'http://www.google.com.br/search?q=jose+dirceu&tbm=nws&start=100']
