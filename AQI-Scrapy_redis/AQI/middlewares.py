# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging
from selenium import webdriver
from scrapy.http import HtmlResponse
from retrying import retry


class AqiSeleniumMiddleware(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.num = 1
        # self.options = webdriver.ChromeOptions()
        # self.options.add_argument("--handless")
        # self.driver = webdriver.Chrome(chrome_options=self.options)

    @retry(stop_max_attempt_number=20, wait_fixed=200)
    def retry_load_page(self, request):
        try:
            self.driver.find_element_by_xpath("//td[@align='center'][1]")
        except:
            logging.debug("Retry %s (%d times)" % (request.url, self.num))
            self.num += 1
            raise Exception("%s page loading failed." % request.url)

    def process_request(self, request, spider):
        if "monthdata" in request.url or "daydata" in request.url:
            self.driver.get(request.url)
            self.num = 1

            try:
                self.retry_load_page(request)
                html = self.driver.page_source
                logging.debug("Retry %s. (Successful)" % request.url)
                return HtmlResponse(url=self.driver.current_url, body=html.encode("utf-8"), encoding="utf-8",
                                    request=request)
            except Exception as e:
                logging.error(e)

    def __del__(self):
        self.driver.quit()


# options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# driver = webdriver.Chrome(chrome_options=options)
# driver.get("")
# driver.page_source()

