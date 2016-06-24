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
    global keywords, base_url
    keywords = ['滴滴', '打车']
    base_url = "http://zhidao.baidu.com"
    start_urls = ['http://zhidao.baidu.com/search?lm=0&rn=10&pn=0&fr=search&ie=gbk&word=' +
                  kw for kw in keywords]
    name = "Zhidao"

    @staticmethod
    def clean_data(page):
        removeImg = re.compile('<img.*?>')
        replaceLine = re.compile('<tr>|<div>|</div>|<p>|</p>|\r|\n')
        replaceBR = re.compile('<br>|<br >|<br />')
        removeExtraTag = re.compile('<em>|</em>|<strong>|</strong>')
        page = re.sub(removeImg,"",page)
        page = re.sub(replaceLine,"",page)
        page = re.sub(replaceBR,"",page)
        page = re.sub(removeExtraTag,"",page)
        return page

    def parse(self, response):
        '''
        Get all page urls
        '''
        html = HtmlXPathSelector(response)
        pageUrls = html.xpath('//div[@class="pager"]/a/@href').extract()
        #print pageUrls
        #print len(str(pageUrls[-1]).split('&pn='))
        pageBaseUrl = str(pageUrls[-1]).split('&pn=')[0]
        pageCount = int(str(pageUrls[-1]).split('&pn=')[1])
        print pageCount
        for i in range(0,20,10):#(0,pageCount+1,10)
            item = dict()
            item['pageUrl'] = base_url + pageBaseUrl + "&pn=" + str(i)
            yield Request(url=item['pageUrl'], meta={'item_1': item}, callback=self.first_parse)

    def first_parse(self, response):
        response = response.body.decode('gbk','ignore')
        response = self.clean_data(response)
        html = Selector(text=response)
        page = html.xpath('//div[@class="list"]/dl/dt/a')
        for i in page:
            item = dict()
            item['title'] = i.xpath('text()').extract_first()
            item['url'] = i.xpath('@href').extract_first()
            #print item['title'], item['url']
            yield Request(url=item['url'], meta={'item_1': item}, callback=self.second_parse)

    def second_parse(self, response):
        item_1 = response.meta['item_1']
        # print 'response ',response
        response = response.body.decode('gbk','ignore')
        ## remove image
        response = self.clean_data(response)
        html = Selector(text=response)
        ques = html.xpath('//pre[@accuse="qContent"]/span').extract_first()
        # 普通回答
        ans = html.xpath('//div[@accuse="aContent"]/span/text()').extract()
        # 专业回答
        ans_quality = html.xpath('//div[@class="quality-content-detail content"]/text()').extract()
        # 提问者采纳
        ans_best = html.xpath('//pre[@accuse="aContent"]/text()').extract()
        #print "Q", ques
        #print ans
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
