# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse


class UrlgoogleSpider(scrapy.Spider):
  name = "urlgoogle"

  #__init__ method receives *args and **kwargs
  def __init__(self, *args, **kwargs):
    #get all args in a list format
    self.searchKeys = list(args)
    #init allowed_domains
    self.allowed_domains = "www.google.com.br"
    self.start_urls = []
    #call a function to make the start_urls
    self.make_urls()

  def make_urls(self):
    #Format the first part of the url
    requestString = "http://" + self.allowed_domains + "/search?q="
    #Include all search words in the url following the google sintax
    for key in self.searchKeys:
      requestString = requestString + key + "+"
    #remove the last '+' character and set to news search mode
    requestString = requestString[:-1] + "&tbm=nws&start=0"
    self.start_urls.append(requestString)

  def parse(self, response):
    sel = Selector(response)
    for link in (sel.xpath("//h3[@class='r']/a/@href").extract()):
      item = GooglescrapItem()
      item['link'] = link
      yield item

class GooglescrapItem(scrapy.Item):
    link = scrapy.Field()
