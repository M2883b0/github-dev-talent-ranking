# -*- encoding: utf-8 -*-
"""
@File    :   SpiderManager.py
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/29 0:18    1.0         None
"""
import logging
import time

from scrapy import signals
from scrapy.crawler import Crawler
from scrapy.signalmanager import SignalManager

from dataCrawler import database, SpiderIdleSignal, AllSpiderIdle, CrawlTopicDetailSignal, SendToManagerSignal
from dataCrawler.config import SPIDER_NUM

total_close_spider = 0
wait_to_close_spider = dict()


class SpiderManager:
    def __init__(self, crawler):
        self.crawler = crawler
        self.flag = True

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler)
        crawler.signals.connect(o.count_close_spider, signal=SpiderIdleSignal)
        crawler.signals.connect(o.handle_message, signal=SendToManagerSignal)

        return o

    def handle_message(self, sender, **kwargs):
        # print("fuckyou bro")
        print(sender.spider.name, kwargs)
        target = kwargs["target"]
        self.crawler.signals.send_catch_log(signal=CrawlTopicDetailSignal, url="http://www.baidu.com", op="crawl_list",
                                            meta={"1": "2"})
        if target == "TopicSpider":
            print(target)
            self.crawler.signals.send_catch_log(signal=CrawlTopicDetailSignal, url=kwargs["url"], op=kwargs["op"],
                                                meta=kwargs["meta"])
        elif target:
            pass
        else:
            print("fuckyou")

    def count_close_spider(self, sender, **meta):
        global total_close_spider
        wait_to_close_spider[meta["name"]] = meta["is_idle"]

        total_close_spider = sum(wait_to_close_spider.values())
        logging.info(f"有 {total_close_spider}个爬虫闲置，state: {wait_to_close_spider}")
        self.is_all_idle()

    def is_all_idle(self):
        if total_close_spider >= SPIDER_NUM:
            self.crawler.signals.send_catch_log(signal=AllSpiderIdle)

            assert isinstance(self.crawler, Crawler)
