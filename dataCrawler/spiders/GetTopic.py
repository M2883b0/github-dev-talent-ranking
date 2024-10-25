from typing import Any

import scrapy
from scrapy.http import Response
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from scrapy.selector import Selector
import time

"""
# 爬取所有的topic
"""


class GetTopic(scrapy.Spider):
    name = "GetTopic"
    start_urls = ['https://github.com/topics']  # 填 topic URL

    def __init__(self, *args, **kwargs):
        super(GetTopic, self).__init__(*args, **kwargs)

        # 设置无头模式
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 启用无头模式
        chrome_options.add_argument('--no-sandbox')  # 适用于某些云环境
        chrome_options.add_argument('--disable-dev-shm-usage')  # 解决某些系统的共享内存问题
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        self.titles_set = set()

    def parse(self, response: Response, **kwargs: Any) -> Any:
        """

        :param response:
        :return:
        """
        self.driver.get(response.url)
        # 循环点击“加载更多”按钮
        while True:
            time.sleep(3)  # 等待时间
            sel = Selector(text=self.driver.page_source)
            titles = sel.css('p.f3.lh-condensed.mb-0.mt-1.Link--primary::text').getall()  # 替换为topic文本，所在的class的名字，作为选择器
            for title in titles:
                # 清理换行符和多余空白
                title_cleaned = title.strip().replace('\n', '').replace('  ', ' ')
                title_cleaned = ' '.join(title_cleaned.split())  # 去掉多余空格
                if title_cleaned not in self.titles_set:
                    self.titles_set.add(title_cleaned)
                    yield {'title': title_cleaned}  # 仅输出新数据

            try:
                # 找到load more按钮
                load_more_button = self.driver.find_element("xpath",
                                                            "/html/body/div[1]/div[4]/main/div[4]/div[1]/form/button")  # 替换为实际的按钮文本的xpath
                load_more_button.click()
            except Exception as e:
                self.logger.info("没有更多内容了，停止爬取。")
                break

    def closed(self, reason):
        self.driver.quit()  # 当爬虫运行结束时，调用 self.driver.quit() 可以关闭 Selenium 的 WebDriver 实例。这有助于释放系统资源，如内存和进程
