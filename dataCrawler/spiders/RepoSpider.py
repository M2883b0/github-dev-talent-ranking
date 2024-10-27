# -*- encoding: utf-8 -*-
"""
@File    :   RepoSpider.py    
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/27 0:13    1.0         None
"""
from typing import Any

import scrapy
from scrapy.http import Response


from dataCrawler.item.TopicInfo import TopicInfo


def url_list():
    """
    迭代器 生成要爬取的 url
    :return:
    """
    for i in range(1, 25):
        # yield topic_list_url.format(i)
        yield "https://api.52vmy.cn/api/query/itad"


urls = url_list()


class RepoSpider(scrapy.Spider):
    name = "RepoSpider"
    start_urls = [next(urls)]  # 填 topic URL
    custom_settings = {
        "DOWNLOAD_TIMEOUT": 5
    }

    def parse(self, response: Response, **kwargs: Any) -> Any:

        print(response.request.headers["Authorization"])

        for url in urls:
            # print(url)
            yield scrapy.Request(url, dont_filter=True)

