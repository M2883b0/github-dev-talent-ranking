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
from dataCrawler.config import user_info_api_template


class UserSpider(scrapy.Spider):
    name = "UserSpider"
    allowed_domains = ["github.com"]
    start_urls = [user_info_api_template.format(0, 1000)]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def parse(self, response: Response, **kwargs: Any) -> Any:
        userLi = json.loads(response.text)
        print(len(userLi))
        yield scrapy.Request(user_info_api_template)
