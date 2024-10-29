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

    def process_item(self, item, spider):
        if isinstance(item, TopicItem):
            item.insert_to_database()
            return item
        elif isinstance(item, UserItem):
            item.insert_to_database()
            return item
