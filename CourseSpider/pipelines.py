# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.exceptions import DropItem

class CleanUpPipeline(object):
    def process_item(self, item, spider):
        # name
        full_name = item['cls_full_name']
        full_name = full_name.replace('\u00a0','')

        dash_index = full_name.index('-')
        space_index = full_name.index(' ', dash_index+2)

        item['cls_name'] = full_name[0:dash_index-1]
        item['cls_sec'] = full_name[dash_index+2:space_index]
        item['cls_full_name'] = full_name[space_index+1:]

        # units
        item['cls_units'] = item['cls_units'].replace(' units', '')
        return item

class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('major201-250.jl', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
