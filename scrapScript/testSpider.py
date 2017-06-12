from scrapy.crawler import CrawlerProcess
from GoogleUrls import UrlgoogleSpider
searchWords = ('jose', 'maria')
MySpider = UrlgoogleSpider(1)
print MySpider.start_urls
process = CrawlerProcess({
  'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(MySpider, 10, *searchWords)
process.start() # the script will block here until all crawling jobs are finishe
