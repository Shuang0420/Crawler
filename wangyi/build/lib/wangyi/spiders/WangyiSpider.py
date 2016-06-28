# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import scrapy
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from wangyi.items import WangyiItem
from scrapy.http import Request
from scrapy.selector import Selector
import re


class WangyiSpider(BaseSpider):
    name = "Wangyi"

    def __init__(self, category=None, *args, **kwargs):
        super(WangyiSpider, self).__init__(*args, **kwargs)
        self.base_url = 'http://news.yodao.com/'
        self.start_urls = ['http://news.yodao.com/search?q=' +
                           category]

    @staticmethod
    def clean_data(page):
        removeImg = re.compile('<img.*?>')
        replaceLine = re.compile('<tr>|<div>|</div>|<p>|</p>|\r|\n|\t')
        replaceBR = re.compile('<br>|<br >|<br />')
        removeExtraTag = re.compile('<em>|</em>|<strong>|</strong>')
        page = re.sub(removeImg, "", page)
        page = re.sub(replaceLine, " ", page)
        page = re.sub(replaceBR, "", page)
        page = re.sub(removeExtraTag, "", page)
        return page

    def parse(self, response):
        response = response  # .body.decode('gbk','ignore')
        #response = self.clean_data(response)
        html = Selector(response)
        page = html.xpath('//h3/a')
        nextPage = html.xpath(
            '//div[@class="c-pages"]/a[@class="next-page"]/@href').extract_first()
        for i in page:
            item = dict()
            #item['title'] = i.xpath('text()').extract_first()
            item['url'] = i.xpath('@href').extract_first()
            # print item['title'], item['url']
            #if item['url'].startswith('http://news.163.com') or item['url'].startswith('http://news.yodao.com'):
            yield Request(url=item['url'], meta={'item_1': item}, callback=self.second_parse)
        if nextPage:
            # count+=1
            nextPage = self.base_url + nextPage
            yield Request(url=nextPage, callback=self.parse)

    def second_parse(self, response):
        item_1 = response.meta['item_1']
        # print 'response ',response
        #response = response.body.decode('gbk','ignore')
        # remove image
        #response = self.clean_data(response)
        html = Selector(response)
        title = html.xpath('//title/text()')
        text = html.xpath('//p/text()').extract()
        text2 = html.xpath('//div[@class="post_text"]/text()').extract()
        text.extend(text2)
        text = " ".join(text).encode('utf8')
        items = []
        item = WangyiItem()
        item['title'] = title.extract_first()
        item['url'] = item_1['url'].encode('utf8')
        item['text'] = "".join(text.split()).strip()
        # print item
        items.append(item)
        return items
