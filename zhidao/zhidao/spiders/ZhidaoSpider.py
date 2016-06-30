# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import scrapy
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from zhidao.items import ZhidaoItem
from scrapy.http import Request
from scrapy.selector import Selector
import re


class ZhidaoSpider(BaseSpider):
    name = "Zhidao"

    def __init__(self, category=None, file=None, *args, **kwargs):
        super(ZhidaoSpider, self).__init__(*args, **kwargs)
        self.base_url = "http://zhidao.baidu.com"
        if category and file:
            print 'please choose exactly one way of input'
        if category:
            category = category.split('，')
        if file:
            f = open(file, 'r')
            category = f.readlines()
        self.start_urls = ['http://zhidao.baidu.com/search?lm=0&rn=10&pn=0&fr=search&ie=gbk&word=' +
                           item for item in category]

    @staticmethod
    def clean_data(page):
        removeImg = re.compile('<img.*?>')
        replaceLine = re.compile('<tr>|<div>|</div>|<p>|</p>|\r|\n')
        replaceBR = re.compile('<br>|<br >|<br />')
        removeExtraTag = re.compile('<em>|</em>|<strong>|</strong>')
        page = re.sub(removeImg, "", page)
        page = re.sub(replaceLine, "", page)
        page = re.sub(replaceBR, "", page)
        page = re.sub(removeExtraTag, "", page)
        return page

    def parse(self, response):
        response = response.body.decode('gbk', 'ignore')
        response = self.clean_data(response)
        html = Selector(text=response)
        page = html.xpath('//div[@class="list"]/dl/dt/a')
        nextPage = html.xpath(
            '//div[@class="pager"]/a[@class="pager-next"]/@href').extract_first()
        for i in page:
            item = dict()
            item['title'] = i.xpath('text()').extract_first()
            item['url'] = i.xpath('@href').extract_first()
            yield Request(url=item['url'], meta={'item_1': item}, callback=self.second_parse)
        if nextPage:
            nextPage = self.base_url + nextPage
            yield Request(url=nextPage, callback=self.parse)

    def second_parse(self, response):
        item_1 = response.meta['item_1']
        # print 'response ',response
        response = response.body.decode('gbk', 'ignore')
        # remove image
        response = self.clean_data(response)
        html = Selector(text=response)
        ques = html.xpath('//pre[@accuse="qContent"]/span').extract_first()
        # 普通回答
        ans = html.xpath('//div[@accuse="aContent"]/span/text()').extract()
        # 专业回答
        ans_quality = html.xpath(
            '//div[@class="quality-content-detail content"]/text()').extract()
        # 提问者采纳
        ans_best = html.xpath('//pre[@accuse="aContent"]/text()').extract()
        # print "Q", ques
        # print ans
        items = []
        if ques == None:
            ques = item_1['title'].encode('utf8')
        item = ZhidaoItem()
        item['title'] = item_1['title'].encode('utf8')
        item['url'] = item_1['url'].encode('utf8')
        item['question'] = ques.encode('utf8').strip()
        ans.extend(ans_quality)
        ans.extend(ans_best)
        item['answer'] = "##".join(ans)
        # print i.xpath('text()').extract(),i.xpath('@href').extract()
        print item
        items.append(item)
        return items
