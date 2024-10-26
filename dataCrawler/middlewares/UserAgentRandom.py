# -*- encoding: utf-8 -*-
"""
@File    :   UserAgentRandom.py
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/26 20:36    1.0         None
"""
import random

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class UserAgentRandom(UserAgentMiddleware):

    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent=crawler.settings.get("USER_AGENT_LIST")
        )

    def process_request(self, request, spider):
        agent = random.choice(self.user_agent)
        request.headers["User-Agent"] = agent
