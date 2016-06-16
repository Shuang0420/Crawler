# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsScrapyItem(scrapy.Item):
    category = scrapy.Field()
    url = scrapy.Field()
    secondary_title = scrapy.Field()
    secondary_url = scrapy.Field()
