# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CourseItem(scrapy.Item):
    cls_name = scrapy.Field()
    cls_full_name = scrapy.Field() #check
    cls_dscr = scrapy.Field() #check
    cls_nbr = scrapy.Field() #check
    cls_daytime = scrapy.Field() #check
    cls_sec = scrapy.Field() #check
    cls_ins1 = scrapy.Field() #check
    cls_ins2 = scrapy.Field() #check
    cls_room = scrapy.Field() #check
    cls_units = scrapy.Field() #check
    cls_capacity = scrapy.Field() #check
    cls_waitlist_capacity = scrapy.Field() #check

    cls_capacity_number = scrapy.Field() #check
    cls_waitlist_number = scrapy.Field() #check
    cls_status = scrapy.Field() #check
