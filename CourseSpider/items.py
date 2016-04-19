# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CourseItem(scrapy.Item):
    # define the fields for your item here like:
    class_name = scrapy.Field()
    class_number = scrapy.Field()
    class_time = scrapy.Field()
    class_section = scrapy.Field()
    class_prof = scrapy.Field()
    class_location = scrapy.Field()
    class_capacity = scrapy.Field()
    class_enrollment_number = scrapy.Field()
    class_waitlist_capacity = scrapy.Field()
    class_waitlist_number = scrapy.Field()
    class_status = scrapy.Field() #Open / Wait / Closed
