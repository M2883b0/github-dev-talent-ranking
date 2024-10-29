# -*- encoding: utf-8 -*-
"""
@File    :   UserInfo.py
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/25 21:06    1.0         None
"""
import logging

import scrapy

from utility.DataBaseManager import DatabaseManager
from utility.config import USER_TABLE_NAME, TALENT_TABLE_NAME


# GitHub 提供了访问开发者的接口 https://api.github.com/users?since=0&per_page=1000
class UserInfo(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    avatar_url = scrapy.Field()
    html_url = scrapy.Field()
    followers = scrapy.Field()
    followers_url = scrapy.Field()
    following_url = scrapy.Field()
    organizations_url = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    blog = scrapy.Field()
    repos_url = scrapy.Field()

    # database = DatabaseManager()
    # database.connect()

    def insert_to_database(self):
        # self.database.insert_data(
        #     USER_TABLE_NAME,
        #     [
        #         self["id"], self["avatar_url"],self["html_url"],
        #         self["name"], "", ""]
        # )
        # self.database.insert_data(
        #     NATIONS_TABLE_NAME,
        #     [
        #         self["id"], self["followers_url"], self["following_url"],
        #         self["organizations_url"], self["company"]]
        # )
        # self.database.insert_data(
        #     TALENT_TABLE_NAME,
        #     [
        #         self["topic_name"], self["topic_descript"], self["topic_image"],
        #         self["topic_url"], self["is_featured"]]
        # )
        #
        # self.database.insert_data()
        # self.database.insert_data()
        pass

    def close_spider(self, spider):
        # self.database.close()
        pass
