#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from scrapy.spiders import BaseSpider
from scrapy.http import Response,FormRequest,Request
from scrapy.selector import Selector
import time
from selenium import webdriver
from ..items import CourseItem

class ProductSpider(BaseSpider):
    name = "course_spider"
    start_urls = ['https://www.lionpath.psu.edu/psc/CSPRD/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.CLASS_SEARCH.GBL?Page=SSR_CLSRCH_ENTRY&Action=U&ExactKeys=Y&TargetFrameName=None']

    def __init__(self):
        chromedriver = "/Users/SteveLeeLX/CodeRepository/CourseMaster Project/chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)

    def parse(self, response):

        # Login
        self.driver.get('https://www.lionpath.psu.edu/psc/CSPRD/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.CLASS_SEARCH.GBL?Page=SSR_CLSRCH_ENTRY&Action=U&ExactKeys=Y&TargetFrameName=None')
        username_textbox = self.driver.find_element_by_name("login")
        username_textbox.send_keys("xpl5016")
        password_textbox = self.driver.find_element_by_name("password")
        password_textbox.send_keys("abcd1234")
        self.driver.find_element_by_xpath("//*[@id=\"main-content\"]/form/div[4]/input").click()
        # Select
        # for campus in self.driver.find_element_by_xpath("//*[@id=\"SSR_CLSRCH_WRK_CAMPUS$0\"]").find_elements_by_tag_name("option"):
        #     if campus.get_attribute("value") == "UP":
        #         campus.click()
        #         time.sleep(2)
        #         break
        for location in self.driver.find_element_by_xpath("//*[@id=\"SSR_CLSRCH_WRK_LOCATION$1\"]").find_elements_by_tag_name("option"):
            if location.get_attribute("value") == "UNIVPARK":
                location.click()
                time.sleep(1)
                break

        # there are 249 majors
        majors = self.driver.find_element_by_xpath("//*[@id=\"SSR_CLSRCH_WRK_SUBJECT_SRCH$2\"]").find_elements_by_tag_name("option")
        majors[6].click()

        # course_number_filter
        self.driver.find_element_by_xpath("//*[@id=\"SSR_CLSRCH_WRK_SSR_EXACT_MATCH1$3\"]").find_elements_by_tag_name("option")[0].click()
        # open_class_only_checkbox
        self.driver.find_element_by_xpath("//*[@id=\"SSR_CLSRCH_WRK_SSR_OPEN_ONLY$6\"]").click()
        # search button
        self.driver.find_element_by_xpath("//*[@id=\"CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH\"]").click()
        time.sleep(2)

        # with open("/Users/SteveLeeLX/Desktop/try2.html","w+") as f:
        #     f.write(self.driver.page_source.encode('utf-8'))
        #     # hxs = Selector(text=f.read())

        hxs = Selector(text=self.driver.page_source)

        course_count = 0   # init the count for courses
        course_nbr_path = '//*[@id="MTG_CLASS_NBR$'+ str(course_count) +'"]'
        course_name_path = '//*[@id="MTG_CLASSNAME$'+ str(course_count) +'"]'
        course_daytime_path = '//*[@id="MTG_DAYTIME$'+ str(course_count) +'"]'
        course_room_path = '//*[@id="MTG_ROOM$'+ str(course_count) +'"]'
        course_ins_path = '//*[@id="MTG_INSTR$'+ str(course_count) +'"]'

        nbr = hxs.xpath(course_nbr_path)
        sec = hxs.xpath(course_name_path)
        daytime = hxs.xpath(course_daytime_path)
        room = hxs.xpath(course_room_path)
        ins = hxs.xpath(course_ins_path)

        while nbr != []:
            # item = CourseItem()
            # item['cls_nbr'] = nbr.css('::text').extract()[0]
            # item['cls_sec'] = sec.css('::text').extract()[0]
            # item['cls_daytime'] = daytime.css('::text').extract()[0]
            # item['cls_room'] = room.css('::text').extract()[0]
            # item['cls_ins1'] = ins.css('::text').extract()[0]
            # item['cls_ins2'] = ins.css('::text').extract()[1]

            # yield item

            # This is basic info
            print nbr.css('::text').extract()
            print sec.css('::text').extract()
            print daytime.css('::text').extract()
            print room.css('::text').extract()
            print ins.css('::text').extract()

            # Go to the detail page
            self.driver.find_element_by_xpath(course_name_path).click()
            time.sleep(2)
            detail_hxc = Selector(text=self.driver.page_source)

            status = detail_hxc.xpath('//*[@id="SSR_CLS_DTL_WRK_SSR_DESCRSHORT"]').css('::text').extract()
            full_name = detail_hxc.xpath('//*[@id="DERIVED_CLSRCH_DESCR200"]').css('::text').extract()
            units = detail_hxc.xpath('//*[@id="SSR_CLS_DTL_WRK_UNITS_RANGE"]').css('::text').extract()
            dscr = detail_hxc.xpath('//*[@id="DERIVED_CLSRCH_DESCRLONG"]').css('::text').extract()
            erl_capacity = detail_hxc.xpath('//*[@id="SSR_CLS_DTL_WRK_ENRL_CAP"]').css('::text').extract()
            wait_capacity = detail_hxc.xpath('//*[@id="SSR_CLS_DTL_WRK_WAIT_CAP"]').css('::text').extract()

            erl_total = detail_hxc.xpath('//*[@id="SSR_CLS_DTL_WRK_ENRL_TOT"]').css('::text').extract()
            wait_total = detail_hxc.xpath('//*[@id="SSR_CLS_DTL_WRK_WAIT_TOT"]').css('::text').extract()

            # Return to basic info page
            self.driver.find_element_by_xpath('//*[@id="CLASS_SRCH_WRK2_SSR_PB_BACK"]').click()
            time.sleep(2)
            hxs = Selector(text=self.driver.page_source)

            # increasment
            course_count = course_count + 1
            course_nbr_path = '//*[@id="MTG_CLASS_NBR$'+ str(course_count) +'"]'
            course_sec_path = '//*[@id="MTG_CLASSNAME$'+ str(course_count) +'"]'
            course_daytime_path = '//*[@id="MTG_DAYTIME$'+ str(course_count) +'"]'
            course_room_path = '//*[@id="MTG_ROOM$'+ str(course_count) +'"]'
            course_ins_path = '//*[@id="MTG_INSTR$'+ str(course_count) +'"]'

            nbr = hxs.xpath(course_nbr_path)
            sec = hxs.xpath(course_name_path)
            daytime = hxs.xpath(course_daytime_path)
            room = hxs.xpath(course_room_path)
            ins = hxs.xpath(course_ins_path)

    #     #self.driver.close()
    #    self.driver.get(response.url)
    #         semester_select = self.driver.find_element_by_name("Semester")
    #         allOptions1 = semester_select.find_elements_by_tag_name("option")
    #         for option1 in allOptions1:
    #             if option1.get_attribute("value") == "SUMMER 2016":
    #                 option1.click()
    #                 break
       #
    #         campus_select = self.driver.find_element_by_name("CrseLoc")
    #         allOptions2 = campus_select.find_elements_by_tag_name("option")
    #         for option2 in allOptions2:
    #             if option2.get_attribute("value") == "UP::University Park":
    #                 option2.click()
    #                 break
       #
    #         course_select = self.driver.find_element_by_name("course_abbrev")
    #         allOptions3 = course_select.find_elements_by_tag_name("option")
    #         allOptions3[i].click()
       #
    #         #for option3 in allOptions3:
    #         #    if option3.get_attribute("value") == "A B E":
    #         #        option3.click()
    #         #        break
       #
    #         submit = self.driver.find_element_by_name("search")
    #         submit.click()
       #
    #         self.driver.get("http://schedule.psu.edu/act_search.cfm?viewAll=Y")
       #
    #         hxs = HtmlXPathSelector(text=self.driver.page_source)
    #         tables = hxs.select("//table")
    #         item = CourseItem()
    #         for table in tables:
    #             classes = table.select("tbody/tr[@class='course_details']")
    #             for Aclass in classes:
    #                 item['class_name'] = table.select("thead/tr/th/p[@class='course_abbrev']/text()").extract()
    #                 item['class_number'] = Aclass.select("td[1]/p/text()").extract()
    #                 item['class_time'] = Aclass.select("td[4]/p/text()").extract()
    #                 item['class_section'] = Aclass.select("td[2]/p/text()").extract()
    #                 item['class_prof'] = Aclass.select("td[6]/p/a/text()").extract()
    #                 yield item
    #         i = i +1
    #     self.driver.close()
