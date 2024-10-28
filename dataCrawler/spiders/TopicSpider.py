# -*- encoding: utf-8 -*-
"""
@File    :   TopicSpider.py    
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/27 22:08    1.0         None
"""
import json
from typing import Any, Iterable, Union

from twisted.internet.defer import Deferred
from typing_extensions import Self

import scrapy
from scrapy import Request, Spider
from scrapy.crawler import Crawler
from scrapy.http import Response
from scrapy.signalmanager import SignalManager
import logging

from dataCrawler import database, crawled_topics
from dataCrawler.config import topic_config as config
from dataCrawler.item.TopicInfo import TopicInfo
from utility.config import ERROR_TABLE_NAME


# 设置两个信号量，用于错误重爬和其他爬虫调用
class CrawlTopicListSignal(SignalManager):
    pass


class CrawlTopicDetailSignal(SignalManager):
    pass


class TopicSpider(scrapy.Spider):
    name = "TopicSpider"
    allowed_domains = ["github.com"]
    handle_httpstatus_list = [403, 429]
    start_urls = [config["topic_list_api_template"].format(1, 1)]

    @classmethod
    def from_crawler(cls, crawler: Crawler, *args: Any, **kwargs: Any) -> Self:
        spider = super(TopicSpider, cls).from_crawler(crawler, *args, **kwargs)
        assert isinstance(spider, TopicSpider)
        crawler.signals.connect(spider.crawl_topic_list_handle, signal=CrawlTopicListSignal)
        crawler.signals.connect(spider.crawl_topic_detail_handle, signal=CrawlTopicDetailSignal)
        # crawler.signals.connect(spider.crawl_topic_detail_handle, signal=)
        return spider

    def start_requests(self) -> Iterable[Request]:

        yield scrapy.Request(url=self.start_urls[0], callback=self.init_parse)

    def init_parse(self, response: Response, **kwargs: Any) -> Any:
        """
        用于获取topic 数量，方便分配查询API参数，同时发出获取 ‘topic列表’请求
        """
        page = 0
        step = config["topic_list_step"]
        total_count = json.loads(response.text)["total_count"]
        logging.info(f"target total_count is {total_count}")
        while True:
            page += 1
            meta = {"page": page}
            if total_count // step < page:
                if total_count % step:
                    yield scrapy.Request(url=config["topic_list_api_template"].format(step, page), meta=meta)
                break
            yield scrapy.Request(url=config["topic_list_api_template"].format(step, page),
                                 errback=self.err_back, meta=meta)

    def parse(self, response: Response, **kwargs: Any) -> Any:
        """
        主分析函数，分析有哪些topic 再精爬，使用url_parse分析精爬数据
        :param response: 网页返回信息
        :param kwargs: meta
        :return:
        """
        result = json.loads(response.text)
        logging.info(f"爬取第{response.meta['page']}页 topic 详细信息接口列表")

        for topic in result["items"]:
            assert isinstance(topic, dict)
            # 判断是否在爬过的列表中
            # TODO: set crawled topics name field
            if topic["name"] in crawled_topics or topic["display_name"] in crawled_topics:
                logging.info(f"topic {topic['name']} 已经爬过了")
                continue
            # 需要api 结合网页爬, 网页需要挂梯子 所以设置is_proxy
            meta = {
                "name": topic["display_name"] if topic["display_name"] else topic["name"],
                "description": topic["description"] if topic["description"] else topic["short_description"],
                "featured": topic["featured"],
                "is_proxy": True
            }

            yield scrapy.Request(url=config["base_url"] + topic["name"], callback=self.url_parse, meta=meta,
                                 errback=self.err_back)

    def url_parse(self, response: Response, **kwargs: Any) -> Any:
        """
        用于爬取 Topic Repos 数量和 Topic 图标
        :param response:
        :param kwargs:
        :return:
        """
        logging.info(f"解析Topic {response.meta['name']} 详细信息字段")
        # 提取项目所需要的字段
        if not response.meta:
            logging.info(f"信息异常 meta: {response.meta}")
            return

        if response.xpath(config["img_url_xpath"]).extract():
            image_url = response.xpath(config["img_url_xpath"]).extract()[0]
        else:
            image_url = ""

        repos_count = response.xpath(config["repos_count_xpath"]).extract()
        if repos_count:
            repos_count = repos_count[0]
            assert isinstance(repos_count, str)
            repos_count = int(repos_count.replace(',', ''))

            item = TopicInfo(
                {
                    "name": response.meta["name"],
                    "descript": response.meta["description"],
                    "url": response.request.url,
                    "image_url": image_url,
                    "repos_count": repos_count,
                    "is_featured": response.meta["featured"]
                }
            )
            yield item
        else:
            logging.info(f"topic {response.meta['name']} is dropped")

    def err_back(self, failure_response: Response):
        url = failure_response.request.url
        code = failure_response.status
        meta = json.dumps(failure_response.meta)
        spider_name = self.name

        database.insert_data(
            ERROR_TABLE_NAME,
            (
                url, code, spider_name, meta
            )
        )

    def close(spider: Spider, reason: str) -> Union[Deferred, None]:
        database.commit()

    def crawl_topic_list_handle(self, sender, **kwargs):
        url = kwargs.get("url")
        meta = kwargs.get("meta")
        yield scrapy.Request(url=url, errback=self.err_back, meta=meta)

    def crawl_topic_detail_handle(self, sender, **kwargs):
        url = kwargs.get("url")
        meta = kwargs.get("meta")
        yield scrapy.Request(url=url, errback=self.err_back, callback=self.url_parse, meta=meta)
