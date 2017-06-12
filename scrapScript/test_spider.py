from scrapy.crawler import CrawlerProcess
from news_urls import NewsSpider
search_words = ('jose', 'maria')
my_spider = NewsSpider(pages=2, search_keys=search_words)
process = CrawlerProcess({
 'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(my_spider, pages=2, search_keys=search_words)
process.start() # the script will block here until all crawling jobs are finished
