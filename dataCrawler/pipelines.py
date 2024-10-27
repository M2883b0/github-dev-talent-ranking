# -*- encoding: utf-8 -*-
"""
@File    :   pipelines.py
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/25 23:31    1.0         None
"""
from utility.DataBaseManager import DatabaseManager
from utility.config import repos_topic
from dataCrawler.item import TopicItem, UserItem


class UserInfoPipeline:
    def __init__(self):
        database = DatabaseManager()
        database.connect()
        self.topics = database.query_data(repos_topic)
        pass

    def process_item(self, item, spider):
        if isinstance(item, TopicItem):
            if item["topic_name"] in self.topics:
                return
            item.insert_to_database()
            return item
        elif isinstance(item, UserItem):
            item.insert_to_database()
