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
    i = 0
    print 'downloading', url
    myPage = requests.get(url).content.decode('gbk')
    myPageResults = Nav_Info(myPage)
    save_path = 'news'
    filename = str(i) + '_' + u'NewRank'
    StringListSave(save_path, filename, myPageResults)  # 保存导航的标题、网址
    i += 1
    for item, url in myPageResults:
        newPage = requests.get(url).content.decode('gbk')
        newPageResults = News_Info(newPage)
        filename = str(i) + '_' + item
        StringListSave(save_path, filename, newPageResults)  # 保存每一类别下各新闻的标题、网址
        i += 1


def Nav_Info(myPage):
    # 二级导航的标题和页面
    pageInfo = re.findall(r'<div class="subNav">.*?<div class="area areabg1">', myPage, re.S)[
        0].replace('<div class="subNav">', '').replace('<div class="area areabg1">', '')
    soup = BeautifulSoup(pageInfo, "lxml")
    tags = soup('a')
    topics = []
    for tag in tags:
        # 只要 科技、财经、体育 的新闻
        # if (tag.string=='科技' or tag.string=='财经' or tag.string=='体育'):
        topics.append((tag.string, tag.get('href', None)))
    return topics


def News_Info(newPage):
    # xpath 使用路径表达式来选取文档中的节点或节点集
    dom = etree.HTML(newPage)
    news_titles = dom.xpath('//tr/td/a/text()')
    news_urls = dom.xpath('//tr/td/a/@href')
    return zip(news_titles, news_urls)


def StringListSave(save_path, filename, slist):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path + '/' + filename + '.txt'
    with open(path, 'w+') as fp:
        for s in slist:
            fp.write('%s\t\t%s\n' % (s[0].encode('utf8'), s[1].encode('utf8')))

if __name__ == '__main__':
    start_url = 'http://news.163.com/rank/'
    Crawler(start_url)
