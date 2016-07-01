# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import scrapy
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from blogCrawler.items import BlogcrawlerItem
from scrapy.http import Request
from scrapy.selector import Selector
import re


class BlogSpider(BaseSpider):
    global keywords, base_url,count
    #keywords = ['滴滴', '打车']
    keywords = ['国美']
    base_url = "http://www.shuang0420.com"
    start_urls = ["http://www.shuang0420.com","http://www.shuang0420.com/page/2/","http://www.shuang0420.com/page/3/"]
    name = "Myblog"
    count = 0


    def parse(self, response):
        global count
        html = HtmlXPathSelector(response)
        pageUrls = html.xpath('//div[@class="post-more-link text-center"]/a/@href').extract()
        for i in pageUrls:
            item = dict()
            item['url'] = base_url + i
            for i in range(0,50):
                yield Request(url=item['url'], meta={'item_1': item}, callback=self.parse)
                print item['url']
                count +=1
        print count
