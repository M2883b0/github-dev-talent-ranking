# -*- encoding: utf-8 -*-
"""
@File    :   UserSpider.py
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/25 22:41    1.0         None
"""
import json
from typing import Any

import scrapy
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
    allowed_domains = ["github.com"]
    page = 1
    step = config["user_list_step"]
    start_urls = [config["user_info_api_template"].format(step, page)]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def parse(self, response: Response, **kwargs: Any) -> Any:
        result = json.loads(response.text)
        print(result)
        assert isinstance(result, dict)
        # 判断是否为用户基本信息列表
        if result.get("total_count"):
            logging.info(f"爬取第{self.page}页用户详细信息接口列表")
            total_count = result["total_count"]
            for user in result["items"]:
                assert isinstance(user, dict)
                yield scrapy.Request(url=user["url"])

            # 基本信息页面 Url 请求生成
            while True:
                self.page += 1
                if total_count // self.step < self.page:
                    if total_count % self.step:
                        yield scrapy.Request(url=config["user_info_api_template"].format(self.step, self.page))
                    break
                yield scrapy.Request(url=config["user_info_api_template"].format(self.step, self.page))
        # 如果不是那只能是详细用户信息接口
        else:
            logging.info(f"解析用户{result['id']}详细信息字段")
            # 提取项目所需要的字段
            required_key = (
                "id", "avatar_url", "html_url", "name", "followers", "followers_url", "following_url",
                "organizations_url",
                "company", "location", "blog", "repos_url")

            item = UserInfo(
                **{key: value for key, value in result.items() if key in required_key}
            )
            yield item
