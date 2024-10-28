# -*- encoding: utf-8 -*-
"""
@File    :   TopicSpider.py    
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/27 22:08    1.0         None
"""
import json
from typing import Any, Iterable

import scrapy
from scrapy import Request
from scrapy.http import Response
import logging
from dataCrawler.config import topic_config as config
from dataCrawler.item.TopicInfo import TopicInfo


class TopicSpider(scrapy.Spider):
    name = "TopicSpider"
    allowed_domains = ["github.com"]
    start_urls = [config["topic_list_api_template"].format(1, 1)]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start_requests(self) -> Iterable[Request]:

        yield scrapy.Request(url=self.start_urls[0], callback=self.init_parse)

    def init_parse(self, response: Response, **kwargs: Any) -> Any:
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
        主分析函数
        :param response: 网页返回信息
        :param kwargs: meta
        :return:
        """
        result = json.loads(response.text)
        logging.info(f"爬取第{response.meta['page']}页 topic 详细信息接口列表")

        for topic in result["items"]:
            assert isinstance(topic, dict)
            # 需要api 结合网页爬, 网页需要挂梯子
            meta = {
                "name": topic["display_name"] if topic["display_name"] else topic["name"],
                "description": topic["description"] if topic["description"] else topic["short_description"],
                "featured": topic["featured"],
                "is_proxy": True
            }

            yield scrapy.Request(url=config["base_url"] + topic["name"], callback=self.url_parse, meta=meta,
                                 errback=self.err_back)

            # 基本信息页面 Url 请求生成

        # 如果不是那只能是详细用户信息接口

    def url_parse(self, response: Response, **kwargs: Any) -> Any:
        """
        用于爬取 Topic Repos 数量和 Topic 图标
        :param response:
        :param kwargs:
        :return:
        """
        logging.info(f"解析Topic {response.meta['name']} 详细信息字段")
        # 提取项目所需要的字段

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
            logging.info(f"topic {response.meta['name'] } is useless")
            logging.info(f"信息异常 meta: {response.meta}")

    def err_back(self, failure):
        url = failure.request.url
        print("failed url ", url)
        with open("Failed Url.txt", "a+") as f:
            f.write(url + "\n")
