import os
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import time
from selenium import webdriver


from ..items import CourseItem

#chromedriver = "/usr/local/Cellar/chromedriver/2.16/bin/chromedriver"
chromedriver = "/Users/SteveLeeLX/Downloads/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)


class ProductSpider(BaseSpider):
    name = "course_spider"
    allowed_domains = ['psu.edu']
    start_urls = ['http://schedule.psu.edu']

    def __init__(self):
        self.driver = webdriver.Chrome(chromedriver)

    def parse(self, response):

        i = 1

        while i < 300:
            self.driver.get(response.url)
            semester_select = self.driver.find_element_by_name("Semester")
            allOptions1 = semester_select.find_elements_by_tag_name("option")
            for option1 in allOptions1:
                if option1.get_attribute("value") == "SUMMER 2016":
                    option1.click()
                    break

            campus_select = self.driver.find_element_by_name("CrseLoc")
            allOptions2 = campus_select.find_elements_by_tag_name("option")
            for option2 in allOptions2:
                if option2.get_attribute("value") == "UP::University Park":
                    option2.click()
                    break

            course_select = self.driver.find_element_by_name("course_abbrev")
            allOptions3 = course_select.find_elements_by_tag_name("option")
            allOptions3[i].click()

            #for option3 in allOptions3:
            #    if option3.get_attribute("value") == "A B E":
            #        option3.click()
            #        break

            submit = self.driver.find_element_by_name("search")
            submit.click()

            self.driver.get("http://schedule.psu.edu/act_search.cfm?viewAll=Y")

            hxs = HtmlXPathSelector(text=self.driver.page_source)
            tables = hxs.select("//table")
            item = CourseItem()
            for table in tables:
                classes = table.select("tbody/tr[@class='course_details']")
                for Aclass in classes:
                    item['class_name'] = table.select("thead/tr/th/p[@class='course_abbrev']/text()").extract()
                    item['class_number'] = Aclass.select("td[1]/p/text()").extract()
                    item['class_time'] = Aclass.select("td[4]/p/text()").extract()
                    item['class_section'] = Aclass.select("td[2]/p/text()").extract()
                    item['class_prof'] = Aclass.select("td[6]/p/a/text()").extract()
                    yield item
            i = i +1
        self.driver.close()
