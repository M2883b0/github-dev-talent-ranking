# -*- encoding: utf-8 -*-
"""
@File    :   HeaderRandom.py
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/26 20:36    1.0         None
"""
import random
from itertools import cycle

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class HeaderRandom(UserAgentMiddleware):
    tokens = []

    def __init__(self, agents, token_list):
        super().__init__()
        self.agents = agents
        self.tokens = cycle(token_list)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            agents=crawler.settings.get("USER_AGENT_LIST"),
            token_list=crawler.settings.get("TOKEN")
        )

    def process_request(self, request, spider):
        print(f"request url {request.url}")
        agent = random.choice(self.agents)
        token = next(self.tokens)
        request.headers["User-Agent"] = agent
        request.headers["Authorization"] = "Bearer " + token
