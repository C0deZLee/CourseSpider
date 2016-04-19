import os
from scrapy.spider import BaseSpider
from scrapy.http import Response,FormRequest,Request
from scrapy.selector import HtmlXPathSelector
import time
from selenium import webdriver
from ..items import CourseItem

class ProductSpider(BaseSpider):
    name = "course_spider"
    #allowed_domains = ['psu.edu']
    start_urls = ['https://webaccess.psu.edu/']

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
        password_textbox.send_keys("StateIamsteve18")
        self.driver.find_element_by_xpath("//*[@id=\"main-content\"]/form/div[4]/input").click()

        # Select
        for campus in self.driver.find_element_by_xpath("//*[@id=\"SSR_CLSRCH_WRK_CAMPUS$0\"]").find_elements_by_tag_name("option"):
            if campus.get_attribute("value") == "UP":
                campus.click()
                time.sleep(5)
                break

        for location in self.driver.find_element_by_xpath("//*[@id=\"SSR_CLSRCH_WRK_LOCATION$1\"]").find_elements_by_tag_name("option"):
            if location.get_attribute("value") == "UNIVPARK":
                location.click()
                time.sleep(5)
                break


        # there are 249 majors
        majors = self.driver.find_element_by_xpath("//*[@id=\"SSR_CLSRCH_WRK_SUBJECT_SRCH$2\"]").find_elements_by_tag_name("option")
        majors[1].click()

        # course_number_filter
        self.driver.find_element_by_xpath("//*[@id=\"SSR_CLSRCH_WRK_SSR_EXACT_MATCH1$3\"]").find_elements_by_tag_name("option")[0].click()
        # open_class_only_checkbox
        self.driver.find_element_by_xpath("//*[@id=\"SSR_CLSRCH_WRK_SSR_OPEN_ONLY$6\"]").click()
        # search button
        self.driver.find_element_by_xpath("//*[@id=\"CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH\"]").click()

        #
        # for major in majors:
        #     major.click()
        #     search_button.click()

        #time.sleep(5)

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
