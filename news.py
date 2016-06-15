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
    # Save_As_Txt(save_path, filename, myPageResults)  # 保存导航的标题、网址
    Save_As_Html(save_path, filename, myPageResults)
    i += 1
    for item, url in myPageResults:
        newPage = requests.get(url).content.decode('gbk')
        newPageResults = News_Info(newPage)
        filename = str(i) + '_' + item
        # Save_As_Txt(save_path, filename, newPageResults)  #
        # 保存每一类别下各新闻的标题、网址
        Save_As_Html(save_path, filename, newPageResults)
        i += 1


def Nav_Info(myPage):
    # 二级导航的标题和页面
    dom = etree.HTML(myPage)
    news_titles = dom.xpath('//div[@class="subNav"]/a/text()')
    news_urls = dom.xpath('//div[@class="subNav"]/a/@href')
    return zip(news_titles, news_urls)


def News_Info(newPage):
    # xpath 使用路径表达式来选取文档中的节点或节点集
    dom = etree.HTML(newPage)
    news_titles = dom.xpath('//tr/td/a/text()')
    news_urls = dom.xpath('//tr/td/a/@href')
    return zip(news_titles, news_urls)


def Save_As_Txt(save_path, filename, slist):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path + '/' + filename + '.txt'
    with open(path, 'w+') as fp:
        for s in slist:
            fp.write('%s\t\t%s\n' % (s[0].encode('utf8'), s[1].encode('utf8')))


def Save_As_Html(save_path, filename, slist):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path + '/' + filename + '.html'
    with open(path, 'w+') as fp:
        fp.write(
            "<html><head> <meta charset='UTF-8'> </head><body><h1>Today's hot news</h1>")
        fp.write('<br/>')
        # 列表形式
        fp.write('<table>')
        for s in slist:
            fp.write('<tr>')
            fp.write('<td>')
            fp.write('<td>' + s[0].encode('utf8') + '</td>')
            fp.write('<td><a href>' + s[1].encode('utf8') + '</a > </td >')
            fp.write('</tr>')
        fp.write("</table>")
        # 超链接形式
        '''
        for s in slist:
            fp.write('<a href="' + s[1].encode('utf8') + '">'+s[0].encode('utf8') +'</a> <br/>')
        '''
        fp.write("</body></html>")

if __name__ == '__main__':
    start_url = 'http://news.163.com/rank/'
    Crawler(start_url)
