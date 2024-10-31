import json
import logging
from typing import Any, Iterable, Union

import scrapy
from scrapy import Request, signals, Spider
from scrapy.http import Response
from twisted.internet.defer import Deferred

from dataCrawler import CrawlTopicDetailSignal, SendToManagerSignal, CrawlTopicListSignal
from dataCrawler import database
from dataCrawler.config import all_curated_topics_config as config
from dataCrawler.spiders.SpiderTemplate import SpiderTemplate


class FeaturedTopicSpider(SpiderTemplate):
    name = "FeaturedTopicSpider"

    start_urls = [config["curated_topic_list_url"].format(1, 1)]  # 填 topic URL

    # custom_settings = {
    #     "DOWNLOAD_TIMEOUT": 1
    # }

    def start_requests(self) -> Iterable[Request]:
        yield scrapy.Request(url=self.start_urls[0], callback=self.init_parse)

    def init_parse(self, response: Response, **kwargs: Any) -> Any:
        """
        用于获取Featured topic 数量，方便分配查询API参数，同时发出获取 ‘topic列表’请求
        """
        # self.crawler.signals.send_catch_log(signal=CrawlTopicDetailSignal, url="http://www.baidu.com", op="crawl_list",
        #                                     meta={"1": "2"})

        step = config["curated_topic_list_step"]
        total_count = json.loads(response.text)["total_count"]
        logging.info(f"curated target total_count is {total_count}")
        page = 0
        while True:
            page += 1
            meta = {"page": page}
            if total_count // step < page:
                if total_count % step:
                    self.send("crawl_list", config["curated_topic_list_url"].format(step, page), meta)
                break
            self.send("crawl_list", config["curated_topic_list_url"].format(step, page), meta)
        self.crawler.signals.send_catch_log(signal=signals.spider_idle)

        # while True:
        #     page += 1
        #     meta = {"page": page}
        #     if total_count // step < page:
        #         if total_count % step:
        #             yield scrapy.Request(url=config["topic_list_api_template"].format(step, page), meta=meta)
        #         break
        #     yield scrapy.Request(url=config["topic_list_api_template"].format(step, page),
        #                          errback=self.err_back, meta=meta)

    # def parse(self, response: Response, **kwargs: Any) -> Any:
    #     topic_names = response.xpath(config["topic_name_xpath"]).extract()
    #     topic_description = [i.strip() for i in response.xpath(config["topic_descript_xpath"]).extract()]
    #     topic_images = []
    #     topic_urls = [config["base_url"] + i for i in response.xpath(config["topic_url_xpath"]).extract()]
    #     for i in range(1, len(topic_names) + 1):
    #         tmp = response.xpath(config["topic_image_xpath_template"].format(i)).extract()
    #         if tmp:
    #             topic_images.append(tmp[0])
    #         else:
    #             topic_images.append("")
    #     for topic_name, topic_descript, topic_image, topic_url, is_featured \
    #             in zip(topic_names, topic_description, topic_images, topic_urls, [True for _ in topic_urls]):
    #         # print(topic_url, topic_image, topic_name, topic_descript, is_featured, " data in featured")
    #         if topic_url:
    #             meta = {
    #                 "name": topic_name,
    #                 "description": topic_description,
    #                 "featured": True,
    #                 "is_proxy": True
    #             }
    #             self.crawler.signals.send_catch_log(
    #                 signal=SendToManagerSignal,
    #                 target="TopicSpider",
    #                 op="crawl_detail",
    #                 url=f'{config["base_url"]}/topics/{topic_name}',
    #                 meta=meta
    #             )
    #     self.crawler.signals.send_catch_log(signal=signals.spider_idle)

    def send(self, op: str, url: str, meta: dict):
        self.crawler.signals.send_catch_log(
            signal=SendToManagerSignal,
            target="TopicSpider",
            op=op,
            url=url,
            meta=meta
        )
