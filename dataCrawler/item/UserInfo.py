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

from utility.DatabaseManager import DatabaseManager
from dataCrawler import database, crawled_users
from utility.config import USER_TABLE_NAME, TALENT_TABLE_NAME, USER_BLOG_TABLE_NAME, USER_LOGIN_NAME_TABLE_NAME, \
    USER_RELATIONSHIPS_TABLE_NAME, USER_REPOS_TABLE_NAME

row_count = 0


# GitHub 提供了访问开发者的接口 https://api.github.com/users?since=0&per_page=1000
class UserInfo(scrapy.Item):
    # 接口获取信息
    id = scrapy.Field()
    login = scrapy.Field()
    name = scrapy.Field()
    followers = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    email = scrapy.Field()
    bio = scrapy.Field()
    public_repos = scrapy.Field()

    # 中间量
    repos_url = scrapy.Field()

    # 个人主页获取信息
    blog_html = scrapy.Field(default="")

    following_id = scrapy.Field(default=0)

    def insert_to_database(self):
        global row_count
        # print("begin insert ", crawled_users)
        # print("the item is ", self)
        if self['id'] not in crawled_users.keys():

            database.insert_data(
                USER_TABLE_NAME,
                [
                    self["id"], self["name"], self["email"],
                    self["followers"], self["bio"], self["public_repos"], self["company"], self["location"], ""]
            )
            database.insert_data(
                USER_LOGIN_NAME_TABLE_NAME,
                [
                    self["id"], self["login"]
                ]
            )
            if self.get("blog_html"):
                database.insert_data(
                    USER_BLOG_TABLE_NAME,
                    [
                        self["id"], self["blog_html"]
                    ]
                )
            if isinstance(self["repos_url"], list):
                for url in self["repos_url"]:
                    print(self["id"], url)
                    database.insert_data(
                        USER_REPOS_TABLE_NAME,
                        [
                            self["id"], url
                        ]
                    )
        if self.get("following_id"):
            # print("关系 item ", self["following_id"], self["id"], 1, 0, 0)
            database.insert_data(
                USER_RELATIONSHIPS_TABLE_NAME,
                [
                    self["id"], self["following_id"], 0, 1, 0
                ]
            )

        crawled_users[self['id']] = self['followers']
        row_count += 1
        if row_count >= 100:
            row_count = 0
            database.commit()
            print("committed ")
