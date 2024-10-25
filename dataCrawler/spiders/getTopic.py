import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from scrapy.selector import Selector
import time

"""
# 爬取所有的topic
"""

class NewsSpider(scrapy.Spider):
    name = "topic_spider"
    start_urls = ['https://github.com/topics']  # topic URL

    def __init__(self, *args, **kwargs):
        super(NewsSpider, self).__init__(*args, **kwargs)
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    def parse(self, response):
        """

        :param response:
        :return:
        """
        self.driver.get(response.url)
        # 循环点击“加载更多”按钮
        while True:
            time.sleep(2)  # 等待时间
            sel = Selector(text=self.driver.page_source)
            titles = sel.css('p.f3.lh-condensed.mb-0.mt-1.Link--primary::text').getall()  # 替换为实际的选择器

            for title in titles:
                yield {'title': title}

            try:
                load_more_button = self.driver.find_element("xpath", "/html/body/div[1]/div[5]/main/div[4]/div[1]/form/button']")  # 替换为实际的按钮文本
                load_more_button.click()
            except Exception as e:
                self.logger.info("没有更多内容了，停止爬取。")
                break

    def closed(self, reason):
        self.driver.quit()  #当爬虫运行结束时，调用 self.driver.quit() 可以关闭 Selenium 的 WebDriver 实例。这有助于释放系统资源，如内存和进程