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
from dataCrawler.config import user_info_api_template, user_number, user_list_step
from dataCrawler.item.UserInfo import UserInfo


def url_list():
    """
    迭代器 生成要爬取的 url
    :return:
    """
    for i in range(0, user_number, user_list_step):
        yield user_info_api_template.format(i, user_list_step)


urls = url_list()


class UserSpider(scrapy.Spider):
    name = "UserSpider"
    allowed_domains = ["github.com"]
    start_urls = [next(urls)]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def parse(self, response: Response, **kwargs: Any) -> Any:
        userLi = json.loads(response.text)
        if isinstance(userLi, list):
            for user in userLi:
                assert isinstance(user, dict)
                print(user.get("id"), user.get("login"), user.get("avatar_url"), user.get("url"))
                item = UserInfo(ID=user.get("id"), user_name=user.get("login"), avatar_url=user.get("avatar_url"),
                                url=user.get("url"))
                yield item
        else:
            return None
        for url in urls:
            yield scrapy.Request(url)
