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
from dataCrawler.config import user_info_config as config
from dataCrawler.item.UserInfo import UserInfo


def url_list(user_number):
    """
    迭代器 生成要爬取的 url
    :return:
    """
    for i in range(2, user_number, config["user_list_step"]):
        yield config["user_info_api_template"].format(config["user_list_step"], 1)


urls = None


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
        total_count = result["total_count"]
        for user in result["items"]:
            assert isinstance(user, dict)
            print(user.get("id"), user.get("login"), user.get("avatar_url"), user.get("url"))
            item = UserInfo(ID=user.get("id"), user_name=user.get("login"), avatar_url=user.get("avatar_url"),
                            url=user.get("url"))
            yield item

        # 基本信息页面 Url 请求生成
        while True:
            self.page += 1
            if total_count // self.step < self.page:
                if total_count % self.step:
                    yield scrapy.Request(url=config["user_info_api_template"].format(self.step, self.page))
                break
            yield scrapy.Request(url=config["user_info_api_template"].format(self.step, self.page))

