# -*- encoding: utf-8 -*-
"""
@File    :   SpiderTemplate.py    
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/29 20:09    1.0         None
"""
import json
import logging
from typing import Any, Union

import scrapy
from scrapy import signals, Spider
from scrapy.exceptions import DontCloseSpider
from scrapy.crawler import Crawler
from scrapy.http import Response
from twisted.internet.defer import Deferred
from twisted.python.failure import Failure
from typing_extensions import Self

from dataCrawler import database, CrawlTopicDetailSignal
from dataCrawler import SpiderIdleSignal, AllSpiderIdle
from utility.config import ERROR_TABLE_NAME


class SpiderTemplate(scrapy.Spider):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.is_all_idle = False

    @classmethod
    def from_crawler(cls, crawler: Crawler, *args: Any, **kwargs: Any) -> Self:
        """
        连接信号量
        :param crawler:
        :param args:
        :param kwargs:
        :return:
        """
        spider = super(SpiderTemplate, cls).from_crawler(crawler, *args, **kwargs)
        assert isinstance(spider, SpiderTemplate)
        crawler.signals.connect(spider.all_spider_idle_handle, signal=AllSpiderIdle)
        crawler.signals.connect(spider.on_idle, signal=signals.spider_idle)

        return spider

    def request(self, url, callback, meta=None):
        return scrapy.Request(url=url, callback=callback, errback=self.err_back, meta=meta)

    def err_back(self, failure_response: Response):
        def err_back(self, failure: Failure):
            # TODO: 错误处理
            print("type of failure", type(failure))
            print("response ", failure.response)
            print("request url ", failure.request.url)

            # if failure
            # response = failure.value.response
            # assert isinstance(response, Response)
            # code = response.status
            # url = response.url
            # meta = json.dumps(response.meta)
            # spider_name = self.name
            #
            # print(url, code, meta, spider_name)
            # database.insert_data(
            #     ERROR_TABLE_NAME,
            #     (
            #         url, code, spider_name, meta
            #     )
            # )
            #
            # database.commit()

    def on_idle(self):
        database.commit()
        self.crawler.signals.send_catch_log(SpiderIdleSignal, name=self.name, is_idle=True)
        logging.info(f"spider name {self.name} is blocked in idle")
        # scrapy.Request("http://baidu.com", errback=lambda **x:x, callback=self._drop_parse, dont_filter=True)

    def all_spider_idle_handle(self):
        self.is_all_idle = True

    def close(spider: Spider, reason: str) -> Union[Deferred, None]:
        logging.info(f"spider {spider.name} is closed")
        return super().close(spider, reason=reason)

    def _drop_parse(self):
        pass

    def filter_dict(self, target:dict, keys):
        return {
            key: value for key, value in target.items() if key in keys
        }

    def url_check(self, url: str):
        if url.startswith("www."):
            url = "http://" + url
        elif url.startswith("http"):
            pass
        elif '.' in url:
            url = "http://" + url
        return url


