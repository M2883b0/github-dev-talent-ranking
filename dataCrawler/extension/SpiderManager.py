# -*- encoding: utf-8 -*-
"""
@File    :   SpiderManager.py
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/29 0:18    1.0         None
"""
import logging

from scrapy.crawler import Crawler
from scrapy.signalmanager import SignalManager

from dataCrawler import database, SPIDER_NUM

total_close_spider = 0

SpiderIdleSignal = SignalManager()
AllSpiderIdle = SignalManager()
# 设置个信号量，用于错误重爬和其他爬虫调用
CrawlTopicListSignal = SignalManager()
CrawlTopicDetailSignal = SignalManager()


class SpiderManager():
    def __init__(self, crawler):
        self.crawler = crawler
        self.wait_to_close_spider = {}
        self.flag = True

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler)
        crawler.signals.connect(o.count_close_spider, signal=SpiderIdleSignal)
        return o

    def count_close_spider(self, sender, **meta):
        global total_close_spider
        self.wait_to_close_spider[meta["name"]] = meta["is_closed"]
        total_close_spider = sum(self.wait_to_close_spider.values())
        logging.info(f"有 {total_close_spider}个爬虫闲置，state: {self.wait_to_close_spider}")
        self.is_all_closed()

    def is_all_closed(self):
        if total_close_spider == SPIDER_NUM:
            database.commit()
            database.close()
            assert isinstance(self.crawler, Crawler)
            self.crawler.signals.send_catch_log(signal=AllSpiderIdle)
