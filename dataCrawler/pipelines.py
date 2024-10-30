# -*- encoding: utf-8 -*-
"""
@File    :   pipelines.py
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/25 23:31    1.0         None
"""
from utility.DatabaseManager import DatabaseManager
from utility.config import TOPICS_TABLE_NAME
from dataCrawler.item import TopicItem, UserItem


class UserInfoPipeline:
    def __init__(self):
        self.topics = []
        self.users = []

    def process_item(self, item, spider):
        print("recvied item", item)
        if isinstance(item, TopicItem):
            if item["name"] not in self.topics:
                item.insert_to_database()
                self.topics.append(item["name"])
        elif isinstance(item, UserItem):
            if item["id"] not in self.users:
                item.insert_to_database()
                self.users.append(item["id"])

        return item
