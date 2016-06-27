# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class WynewsPipeline(object):
    def __init__(self):
        self.file = open('items.json', 'w')
    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False) + "\n"
        #line = line.encode(line,'utf8')
        self.file.write(line)
        return item
