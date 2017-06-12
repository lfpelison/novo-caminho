# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

def google_format(s_keys, pages):
    search_keys = "+".join(s_keys)
    for i in range(pages):
        yield "http://www.google.com.br/search?q={0}&tbm=nws&start={1}".format(search_keys, i*10)


class NewsSpider(scrapy.Spider):
  name = "newsspider"
  def __init__(self, *args, **kwargs):
    print kwargs
    self.pages = kwargs['pages']
    self.search_keys = kwargs['search_keys']
    self.allowed_domains = "www.google.com.br" # allowed_domains vai ser uma lista depois?
    self.start_urls = []
    self.make_urls()

  def make_urls(self):
      for url in google_format(self.search_keys, self.pages):
          self.start_urls.append(url)

  def parse(self, response):
    sel = Selector(response)
    for link in (sel.xpath("//h3[@class='r']/a/@href").extract()):
      item = NewsSpiderItem()
      item['link'] = link
      yield item

class NewsSpiderItem(scrapy.Item):
    link = scrapy.Field()
