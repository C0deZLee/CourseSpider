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
        full_name = item['fullName']
        full_name = full_name.replace('\u00a0','')

        dash_index = full_name.index('-')
        space_index = full_name.index(' ', dash_index+2)

        item['name'] = full_name[0:dash_index-1]
        item['section'] = full_name[dash_index+2:space_index]
        item['fullName'] = full_name[space_index+1:]

        # units
        item['unit'] = item['unit'].replace(' units', '')

        # major
        item['major'] = item['name'].split(' ')[0]

        return item

class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('courses_data.json', 'a')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
