# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import scrapy
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from tieba.items import TiebaItem
from scrapy.http import Request
import re


class TiebaSpider(BaseSpider):
    global keywords, base_url
    keywords = ['国美']
    base_url = "http://tieba.baidu.com"
    start_urls = ['http://tieba.baidu.com/f?ie=utf-8&kw=' +
                  kw for kw in keywords]
    name = "Tieba"

    def parse(self, response):
        '''
        Get all page urls
        '''
        html = HtmlXPathSelector(response)
        pageUrls = html.xpath(
            '//div[@class="pagination-default clearfix"]/a[@class="last pagination-item "]/@href').extract()
        pageBaseUrl = str(pageUrls[-1]).split('&pn=')[0]
        pageCount = int(str(pageUrls[-1]).split('&pn=')[1])
        #for i in range(0, 1):
        for i in range(0, pageCount + 1, 50):
            item = dict()
            item['pageUrl'] = pageBaseUrl + "&pn=" + str(i)
            yield Request(url=item['pageUrl'], meta={'item_1': item}, callback=self.first_parse)

    def first_parse(self, response):
        '''
        Get post urls
        '''
        html = HtmlXPathSelector(response)
        page = html.xpath(
            '//div[@class="threadlist_title pull_left j_th_tit "]/a')
        for i in page:
            item = dict()
            item['title'] = i.xpath('text()').extract_first()
            item['url'] = base_url + i.xpath('@href').extract_first()
            #print item['title'], item['url']
            yield Request(url=item['url'], meta={'item_1': item}, callback=self.second_parse)

    def second_parse(self, response):
        '''
        Get pages for every post
        '''
        html = HtmlXPathSelector(response)
        item_1 = response.meta['item_1']
        pageUrls = html.xpath(
            '//li[@class="l_pager pager_theme_5 pb_list_pager"]/a/@href')
        if (len(pageUrls) == 0):
            x = 1
            item = dict()
            item['title'] = item_1['title']
            item['url'] = item_1['url']
            yield Request(url=item['url'], meta={'item_1': item}, callback=self.third_parse)
        else:
            data = str(pageUrls[-1]).split("data=u'")[-1]
            pageBaseUrl = data.split('?pn=')[0]
            pageCount = int(data.split('?pn=')[1].split("'>")[0])
            #print pageBaseUrl
            #print pageCount
            #for i in range(1, 2):
            for i in range(1, pageCount + 1):
                item = dict()
                item['title'] = item_1['title']
                item['url'] = item_1['url']
                item['pageUrl'] = base_url + pageBaseUrl + "?pn=" + str(i)
                yield Request(url=item['pageUrl'], meta={'item_1': item}, callback=self.third_parse)

    def third_parse(self, response):
        '''
        Get every post content
        '''
        item_1 = response.meta['item_1']
        html = HtmlXPathSelector(response)
        print 'response ',response
        page = html.xpath(
            '//div[@class="d_post_content j_d_post_content  clearfix"]/text()').extract()
        #print 'page ',page
        items = []
        item = TiebaItem()
        item['title'] = item_1['title'].encode('utf8')
        item['url'] = item_1['url'].encode('utf8')
        item['pageUrl'] = item_1['pageUrl'].encode('utf8')
        page = [p.strip() for p in page]
        item['text'] = "##".join(page)
        print "saved", item['title'], item['text']
        items.append(item)
        '''
        for i in page:
            item = TiebaItem()
            item['title'] = item_1['title'].encode('utf8')
            item['url'] = item_1['url'].encode('utf8')
            item['pageUrl'] = item_1['pageUrl'].encode('utf8')
            item['text'] = i.xpath('text()').extract_first().strip()
            # print item['title'], item['url'], item['text']
            #rule = "|".join(keywords)
            #if re.search(rule, str(item['text'])):
            print "saved", item['title'], item['text']
            items.append(item)
            '''
        return items
