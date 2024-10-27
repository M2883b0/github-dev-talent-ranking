# -*- encoding: utf-8 -*-
"""
@File    :   Proxy.py
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/26 20:24    1.0         None
"""
import random


class Proxy:
    def __init__(self, ip):
        self.ip = ip

    @classmethod
    def from_crawler(cls, crawler):
        return cls(ip=crawler.settings.get("PROXIES_LIST"))

    def process_request(self, request, spider):
        assert isinstance()
        spider
        ip = random.choice(self.ip)
        request.meta["proxy"] = ip
