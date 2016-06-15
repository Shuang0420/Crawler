#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib2
import requests
import re
from lxml import etree
import os
from bs4 import BeautifulSoup


def Crawler(url):
    global newPageResults
    i = 0
    print 'downloading', url
    myPage = requests.get(url).content
    myPageResults = Nav_Info(myPage)
    save_path = 'news'
    filename = str(i) + '_' + u'NewRank'
    # Save_As_Txt(save_path, filename, myPageResults)  # 保存导航的标题、网址
    Save_As_Txt(save_path, filename, myPageResults,0)
    for item, url in myPageResults:
        newPage = requests.get(url).content
        newPageResults.append(News_Info(newPage,item))
    print len(newPageResults)
    Save_As_Txt(save_path, 'didi', newPageResults,1)

def Nav_Info(myPage):
    # 二级导航的标题和页面
    dom = etree.HTML(myPage)
    news_titles = dom.xpath('//h3/a/text()')
    news_urls = dom.xpath('//h3/a/@href')
    return zip(news_titles, news_urls)

def News_Info(newPage,item):
    # xpath 使用路径表达式来选取文档中的节点或节点集
    #soup = BeautifulSoup(newPage, "lxml")
    dom = etree.HTML(newPage)
    content = dom.xpath('//p/text()')
    text = " ".join(content)
    text = item + text
    return "".join(text.split()).encode('utf8')


def Save_As_Txt(save_path, filename, slist,mode):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path + '/' + filename + '.txt'
    with open(path, 'w+') as fp:
        for s in slist:
            if mode == 0:
                fp.write('%s\t\t%s\n' % (s[0].encode('utf8'), s[1].encode('utf8')))
            else:
                fp.write(s+'\n')

if __name__ == '__main__':
    newPageResults = []
    for i in range(0,101,20):
        start_url = 'http://news.yodao.com/search?q=%E6%BB%B4%E6%BB%B4&start='+str(i)+'&length=10&s=rank&tr=no_range&keyfrom=search.page&suser=user163&site=163.com'
        Crawler(start_url)
