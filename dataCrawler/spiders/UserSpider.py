# -*- encoding: utf-8 -*-
"""
@File    :   UserSpider.py
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/25 22:41    1.0         None
"""
import json
from typing import Any, Iterable

import scrapy
from scrapy import Request
from scrapy.http import Response

import logging
from dataCrawler.config import user_info_config as config
from dataCrawler.item.UserInfo import UserInfo


def url_list(user_number):
    """
    迭代器 生成要爬取的 url
    :return:
    """
    for i in range(2, user_number, config["user_list_step"]):
        yield config["user_info_api_template"].format(config["user_list_step"], 1)


class UserSpider(scrapy.Spider):
    name = "UserSpider"
    # allowed_domains = ["github.com"]
    step = config["user_list_step"]
    top1000url = config["user_info_api_top1000_template"]
    user_list_url = config["user_info_api_template"]
    user_detail_template = config["user_detail_template"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start_requests(self) -> Iterable[Request]:

        yield self.request(url=self.top1000url.format(1, 1), callback=self.init_parse)
        begin = config["user_followers_begin"]
        end = config["user_followers_end"]
        for lower_num in range(begin, end, 100):
            yield self.request(url=self.user_list_url.format(lower_num, lower_num + 100, 1, 1),
                               callback=self.init_parse, meta={"begin": lower_num, "end": lower_num + 100})

    def request(self, url, callback, meta=None):
        return scrapy.Request(url=url, callback=callback, errback=self.err_back, meta=meta)

    def err_back(self, failture):
        print("type of failure", type(failture))
        print(failture.value)
        # print(failture)
        pass

    def init_parse(self, response: Response, **kwargs: Any) -> Any:
        result = json.loads(response.text)
        total_count = int(result["total_count"])
        page = 0
        for page in range(1, total_count // self.step + 1):
            if ".." in response.request.url:
                request = self.request(
                    url=self.user_list_url.format(response.meta["begin"], response.meta["end"], self.step, page),
                    callback=self.parse)
            else:
                request = self.request(url=self.top1000url.format(self.step, page), callback=self.parse)
            yield request

        if total_count % self.step:
            page += 1
            if ".." in response.request.url:
                request = self.request(
                    url=self.user_list_url.format(response.meta["begin"], response.meta["end"], self.step, page),
                    callback=self.parse)
            else:
                request = self.request(url=self.top1000url.format(self.step, page), callback=self.parse)
            yield request


    def parse(self, response: Response, **kwargs: Any) -> Any:
        logging.info("parse function begin")
        # print(response.text)
        result = json.loads(response.text)
        if not result:
            if response.meta.get("is_follower"):
                li = result
            else:
                li = result["items"]
            for user in li:
                logging.info(f"解析用户{user['id']}详细信息字段")
                yield self.request(url=self.user_detail_template + user["login"], callback=self.parse_detail,
                                   meta=response.meta)
        else:
            print("result is None")

    def parse_detail(self, response: Response, **kwargs: Any) -> Any:
        print("begin parse Detail")
        data = json.loads(response.text)
        assert isinstance(data, dict)
        # 提取项目所需要的字段
        required_key = (
            "id",
            "login",
            "name",
            "followers",
            "company",
            "location",
            "email",
            "location",
            "bio"
        )
        meta = {
            key: value for key, value in data.items() if key in required_key
        }
        print(meta)
        if response.meta.get("is_follower"):
            meta["following_id"] = response.meta["follower_id"]
            yield UserInfo(**meta)
        else:
            # "followers_url" 国籍判断
            # TODO: 需要更改常量
            for page in range(1, 2):
                url = data["followers_url"] + f"?per_page=1&page={page}"
                yield self.request(url=data["followers_url"], callback=self.parse,
                                   meta={"is_follower": True, "follower_id": data["id"]})

            # "organizations_url"
            yield self.request(url=data["organizations_url"], callback=self.parse_organization,
                               meta={"partner_id": data["id"]})
            # "blog", personal page crawl

            yield self.request(url=data["html_url"], callback=self.personal_page_parse, meta=meta)

    def parse_organization(self, response: Response, **kwargs: Any) -> Any:
        pass

    def personal_page_parse(self, response: Response, **kwargs: Any) -> Any:
        pass
