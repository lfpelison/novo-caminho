import news_urls
import parsing_news
from newspaper import Article
#import numpy as np
#import pandas as pd
import csv

import sys
reload(sys)
sys.setdefaultencoding('utf8')

url_list = []
url_list = news_urls.get_urls(["Fischer Brusque"], ["google"], 5)

articles = parsing_news.url2features(url_list)
with open('Paulao.csv', 'a+') as csvfile:
    news_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    rows_num = len(list(news_reader))

    news_writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#    news_writer.writerow(['Linha'] + ['Resumo'] + ['Risco'] + ['Categoria'])

    for i, summary in enumerate(articles):
        news_writer.writerow([str(i+rows_num)] + [summary] + ['Alto'] + ['XXXXXXX'])
        print i+rows_num
