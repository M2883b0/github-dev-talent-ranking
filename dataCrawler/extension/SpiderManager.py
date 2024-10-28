# -*- encoding: utf-8 -*-
"""
@File    :   SpiderManager.py
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/29 0:18    1.0         None
"""
import logging
from typing import Any, Self

from scrapy import signals
from scrapy.crawler import Crawler
from scrapy.signalmanager import SignalManager
from scrapy.extensions import corestats
from dataCrawler import database
from dataCrawler.spiders.TopicSpider import CrawlTopicListSignal, CrawlTopicDetailSignal


class TotalSpierCloseSignal(SignalManager):
    pass


def close_all():
    database.commit()
    database.close()


class SpiderManager(corestats):
    def __init__(self, stat):
        super().__init__(stat)
        self.num_of_close_spider = 0

    @classmethod
    def from_crawler(cls, crawler):
        super(SpiderManager, cls).from_crawler(crawler)
        o = cls(crawler.stats)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def spider_closed(self):
        self.num_of_close_spider += 1
        if self.num_of_close_spider == 1:
            close_all()
            logging.info(f"all spider closed")
