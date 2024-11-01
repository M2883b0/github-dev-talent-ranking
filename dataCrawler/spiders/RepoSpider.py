# -*- encoding: utf-8 -*-
"""
@File    :   RepoSpider.py    
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/27 0:13    1.0         None
"""
from typing import Any, Iterable

import scrapy
from scrapy import Request
from scrapy.http import Response

from dataCrawler import database
from dataCrawler.spiders.SpiderTemplate import SpiderTemplate
from dataCrawler import crawled_repos
from dataCrawler.item.TopicInfo import TopicInfo


class RepoSpider(SpiderTemplate):
    name = "RepoSpider"
    custom_settings = {
        "DOWNLOAD_TIMEOUT": 5
    }

    def start_requests(self) -> Iterable[Request]:
        # self.request(url=)
        pass

    def parse(self, response: Response, **kwargs: Any) -> Any:
        print(response.request.headers["Authorization"])
