# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CourseItem(scrapy.Item):
    name = scrapy.Field() #check
    fullName = scrapy.Field() #check
    description = scrapy.Field() #check
    number = scrapy.Field() #check
    time = scrapy.Field() #check
    section = scrapy.Field() #check
    instructor1 = scrapy.Field() #check
    instructor2 = scrapy.Field() #check
    room = scrapy.Field() #check
    unit = scrapy.Field() #check
    capacity = scrapy.Field() #check
    waitlist = scrapy.Field() #check
    enrolled = scrapy.Field() #check
    waitlistEnrolled = scrapy.Field() #check
    status = scrapy.Field() #check
    major = scrapy.Field() #check
    classType = scrapy.Field() 
    notes = scrapy.Field()
