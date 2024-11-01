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
from dataCrawler.item import TopicItem, UserItem, OrgItem, ReposItem
from dataCrawler import crawled_users, crawled_orgs, crawled_topics, crawled_repos


class UserInfoPipeline:
    def __init__(self):
        self.topics = crawled_topics
        self.users = list(crawled_users.keys())
        self.orgs = crawled_orgs
        self.repos = list(crawled_repos.keys())

    def process_item(self, item, spider):
        # print("recvied item", item)
        if isinstance(item, TopicItem):
            if item["name"] not in self.topics:
                item.insert_to_database()
                self.topics.append(item["name"])
        elif isinstance(item, UserItem):
            if item["id"] not in self.users:
                # print(f"recved user id {item['id']} name {item['name']}")
                item.insert_to_database()
                self.users.append(item["id"])
        elif isinstance(item, OrgItem):
            if item["id"] not in self.users:
                item.insert_to_database()
                self.topics.append(item["id"])
        elif isinstance(item, ReposItem):
            if item["id"] not in self.repos:
                item.insert_to_database()
                self.topics.append(item["id"])

        return item
