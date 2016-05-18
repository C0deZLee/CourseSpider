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
    start_urls = ['https://www.google.com']

    def __init__(self):
        chromedriver = "/Users/SteveLeeLX/CodeRepository/CourseMaster Project/chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)

    def login(self):
        self.driver.get('https://www.lionpath.psu.edu/psc/CSPRD/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.CLASS_SEARCH.GBL?Page=SSR_CLSRCH_ENTRY&Action=U&ExactKeys=Y&TargetFrameName=None')
        username_textbox = self.driver.find_element_by_name("login")
        username_textbox.send_keys("xpl5016")
        password_textbox = self.driver.find_element_by_name("password")
        password_textbox.send_keys("abcd1234")
        self.driver.find_element_by_xpath("//*[@id=\"main-content\"]/form/div[4]/input").click()

    def parse(self, response):
        driver = self.driver
        # Login
        self.login()
        # choose location
        for location in driver.find_element_by_xpath("//*[@id=\"SSR_CLSRCH_WRK_LOCATION$1\"]").find_elements_by_tag_name("option"):
            if location.get_attribute("value") == "UNIVPARK":
                location.click()
                time.sleep(2)
                break

        major_count = 201
        major_total = 250
        # major_total = len(driver.find_element_by_xpath("//*[@id=\"SSR_CLSRCH_WRK_SUBJECT_SRCH$2\"]").find_elements_by_tag_name("option"))

        while (major_count <= major_total):
            driver.find_element_by_xpath("//*[@id=\"SSR_CLSRCH_WRK_SUBJECT_SRCH$2\"]").find_elements_by_tag_name("option")[major_count].click()
            # uncheck open class only
            driver.find_element_by_xpath("//*[@id=\"SSR_CLSRCH_WRK_SSR_OPEN_ONLY$6\"]").click()
            # search button
            driver.find_element_by_xpath("//*[@id=\"CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH\"]").click()
            # wait load
            t_end = time.time() + 15
            while (time.time() < t_end and driver.find_elements_by_xpath('//*[@id="MTG_CLASS_NBR$0"]') == []):
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
                    item['cls_nbr'] = nbr.css('::text').extract()[0]
                    item['cls_daytime'] = daytime.css('::text').extract()[0]
                    item['cls_room'] = room.css('::text').extract()[0]
                    item['cls_ins1'] = ins.css('::text').extract()[0]
                    try:
                        item['cls_ins2'] = ins.css('::text').extract()[1]
                    except IndexError:
                        pass

                    if (item['cls_room'] == 'APPT' or item['cls_room'] == 'TBA') and item['cls_daytime'] == 'TBA':
                        pass
                    else:
                        # get the detail info
                        driver.find_element_by_xpath('//*[@id="MTG_CLASSNAME$'+ str(course_count) +'"]').click()
                        while (driver.find_elements_by_xpath('//*[@id="SSR_CLS_DTL_WRK_SSR_DESCRSHORT"]') == []):
                            pass

                        detail_hxc = Selector(text=driver.page_source)

                        item['cls_status'] = detail_hxc.xpath('//*[@id="SSR_CLS_DTL_WRK_SSR_DESCRSHORT"]').css('::text').extract()[0]
                        item['cls_full_name'] = detail_hxc.xpath('//*[@id="DERIVED_CLSRCH_DESCR200"]').css('::text').extract()[0]
                        item['cls_units'] = detail_hxc.xpath('//*[@id="SSR_CLS_DTL_WRK_UNITS_RANGE"]').css('::text').extract()[0]
                        item['cls_dscr'] = detail_hxc.xpath('//*[@id="DERIVED_CLSRCH_DESCRLONG"]').css('::text').extract()[0]
                        item['cls_capacity'] = detail_hxc.xpath('//*[@id="SSR_CLS_DTL_WRK_ENRL_CAP"]').css('::text').extract()[0]
                        item['cls_waitlist_capacity'] = detail_hxc.xpath('//*[@id="SSR_CLS_DTL_WRK_WAIT_CAP"]').css('::text').extract()[0]
                        item['cls_capacity_number'] = detail_hxc.xpath('//*[@id="SSR_CLS_DTL_WRK_ENRL_TOT"]').css('::text').extract()[0]
                        item['cls_waitlist_number'] = detail_hxc.xpath('//*[@id="SSR_CLS_DTL_WRK_WAIT_TOT"]').css('::text').extract()[0]
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
                    pass

        driver.close()
