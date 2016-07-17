#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from ..items import CourseItem

from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class CourseSpider(BaseSpider):
    name = "course_spider"
    start_urls = ['https://www.example.com']

    def __init__(self):
        chromedriver = "/Users/SteveLeeLX/CodeRepository/CourseMaster Project/chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)

    def parse(self, response):
        driver = self.driver
        driver.get('https://public.lionpath.psu.edu/psc/CSPRD_2/EMPLOYEE/HRMS/c/PE_TE031.CLASS_SEARCH.GBL')
        # choose location
        for location in driver.find_element_by_xpath("//*[@id=\"SSR_CLSRCH_WRK_LOCATION$1\"]").find_elements_by_tag_name("option"):
            if location.get_attribute("value") == "UNIVPARK":
                location.click()
                time.sleep(2)
                break

        major_count = 1
        major_total = 300
        # major_total = len(driver.find_element_by_xpath("//*[@id=\"SSR_CLSRCH_WRK_SUBJECT_SRCH$2\"]").find_elements_by_tag_name("option"))

        while (major_count <= major_total):
            file = open('courses_data.json', 'r')
            driver.find_element_by_xpath("//*[@id=\"SSR_CLSRCH_WRK_SUBJECT_SRCH$2\"]").find_elements_by_tag_name("option")[major_count].click()
            # uncheck open class only
            driver.find_element_by_xpath("//*[@id=\"SSR_CLSRCH_WRK_SSR_OPEN_ONLY$6\"]").click()
            # search button
            driver.find_element_by_xpath("//*[@id=\"CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH\"]").click()
            # wait load
            t_end = time.time() + 15
            while (time.time() < t_end and driver.find_elements_by_xpath('//*[@id="MTG_CLASS_NBR$0"]') == []):
                time.sleep(0.2)
                pass
            time.sleep(0.1)

            if driver.find_elements_by_xpath('//*[@id="MTG_CLASS_NBR$0"]') != []:
                # init variables
                item = CourseItem()
                course_count = 0

                hxs = Selector(text=driver.page_source)

                nbr = hxs.xpath('//*[@id="MTG_CLASS_NBR$'+ str(course_count) +'"]')
                sec = hxs.xpath('//*[@id="MTG_CLASSNAME$'+ str(course_count) +'"]')
                daytime = hxs.xpath('//*[@id="MTG_DAYTIME$'+ str(course_count) +'"]')
                room = hxs.xpath('//*[@id="MTG_ROOM$'+ str(course_count) +'"]')
                ins = hxs.xpath('//*[@id="MTG_INSTR$'+ str(course_count) +'"]')

                # iterate classes
                while nbr != []:
                    # get basic info
                    item['number'] = nbr.css('::text').extract()[0]
                    item['time'] = daytime.css('::text').extract()[0]
                    item['room'] = room.css('::text').extract()[0]
                    item['instructor1'] = ins.css('::text').extract()[0]
                    try:
                        item['instructor2'] = ins.css('::text').extract()[1]
                    except IndexError:
                        pass

                    if (item['room'] == 'APPT' or item['room'] == 'TBA') and item['time'] == 'TBA':
                        pass
                    else:
                        # get the detail info
                        driver.find_element_by_xpath('//*[@id="MTG_CLASSNAME$'+ str(course_count) +'"]').click()
                        while (driver.find_elements_by_xpath('//*[@id="SSR_CLS_DTL_WRK_SSR_DESCRSHORT"]') == []):
                            time.sleep(0.2)
                            pass

                        detail_hxc = Selector(text=driver.page_source)

                        item['status'] = detail_hxc.xpath('//*[@id="SSR_CLS_DTL_WRK_SSR_DESCRSHORT"]').css('::text').extract()[0]
                        item['fullName'] = detail_hxc.xpath('//*[@id="DERIVED_CLSRCH_DESCR200"]').css('::text').extract()[0]
                        item['unit'] = detail_hxc.xpath('//*[@id="SSR_CLS_DTL_WRK_UNITS_RANGE"]').css('::text').extract()[0]
                        item['description'] = detail_hxc.xpath('//*[@id="DERIVED_CLSRCH_DESCRLONG"]').css('::text').extract()[0]
                        item['capacity'] = detail_hxc.xpath('//*[@id="SSR_CLS_DTL_WRK_ENRL_CAP"]').css('::text').extract()[0]
                        item['waitlist'] = detail_hxc.xpath('//*[@id="SSR_CLS_DTL_WRK_WAIT_CAP"]').css('::text').extract()[0]
                        item['enrolled'] = detail_hxc.xpath('//*[@id="SSR_CLS_DTL_WRK_ENRL_TOT"]').css('::text').extract()[0]
                        item['waitlistEnrolled'] = detail_hxc.xpath('//*[@id="SSR_CLS_DTL_WRK_WAIT_TOT"]').css('::text').extract()[0]

                        try:
                            item['classType'] = detail_hxc.xpath('//*[@id="SSR_CLS_DTL_WRK_SSR_CRSE_ATTR_LONG"]').css('::text').extract()[0]
                            item['notes'] = detail_hxc.xpath('//*[@id="DERIVED_CLSRCH_SSR_CLASSNOTE_LONG"]').css('::text').extract()[0]
                        except:
                            pass

                        yield item
                        # Return to basic info page
                        driver.find_element_by_xpath('//*[@id="CLASS_SRCH_WRK2_SSR_PB_BACK"]').click()


                    # increase
                    course_count = course_count + 1

                    # wait for load
                    while(driver.find_elements_by_xpath('//*[@id="MTG_CLASS_NBR$0"]')  == []):
                        pass

                    hxs = Selector(text=driver.page_source)

                    nbr = hxs.xpath('//*[@id="MTG_CLASS_NBR$'+ str(course_count) +'"]')
                    sec = hxs.xpath('//*[@id="MTG_CLASSNAME$'+ str(course_count) +'"]')
                    daytime = hxs.xpath('//*[@id="MTG_DAYTIME$'+ str(course_count) +'"]')
                    room = hxs.xpath('//*[@id="MTG_ROOM$'+ str(course_count) +'"]')
                    ins = hxs.xpath('//*[@id="MTG_INSTR$'+ str(course_count) +'"]')

                # back to main page
                driver.find_element_by_xpath('//*[@id="CLASS_SRCH_WRK2_SSR_PB_MODIFY$5$"]').click()
                major_count = major_count + 1
                while(driver.find_elements_by_xpath("//*[@id=\"SSR_CLSRCH_WRK_SUBJECT_SRCH$2\"]") == []):
                    time.sleep(0.2)
                    pass

        driver.close()
