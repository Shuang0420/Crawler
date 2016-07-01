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
    base_url = "http://www.shuang0420.com"
    start_urls = ["http://www.shuang0420.com"]
    name = "Myblog"


    def parse(self, response):
        html = HtmlXPathSelector(response)
        pageUrls = html.xpath('//div[@class="post-more-link text-center"]/a/@href').extract()
        content = html.xpath('//p/text()').extract()
        items = []
        if not pageUrls:
            yield Request(url=response.url, dont_filter=True)
        for i in pageUrls:
            item = dict()
            item['url'] = base_url + i
            items.append(item)
        print content
        yield items
