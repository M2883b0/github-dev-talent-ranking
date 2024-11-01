# -*- encoding: utf-8 -*-
"""
@File    :   ReposInfo.py    
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/31 14:35    1.0         None
"""
import scrapy

from dataCrawler import database
from utility.config import REPOS_INFO_TABLE_NAME, REPOS_URL_TABLE_NAME, REPOS_LANGUAGE_PROPORTION_TABLE_NAME, \
    REPOS_PARTICIPANTS_TABLE_NAME, REPOS_FIELDS_TABLE_NAME

row_count = 0


class ReposItem(scrapy.Item):
    # api.github.com/repos/xx
    id = scrapy.Field()
    url = scrapy.Field()  # api url
    language = scrapy.Field()
    description = scrapy.Field()
    forks_count = scrapy.Field()
    stargazers_count = scrapy.Field()
    subscribers_count = scrapy.Field()
    topics = scrapy.Field()
    owner = scrapy.Field()
    open_issues_count = scrapy.Field()
    # importance = scrapy.Field()

    languages_percent = scrapy.Field()
    contributor_id = scrapy.Field()
    personal_contribution_value = scrapy.Field()

    def insert_to_database(self):
        global row_count

        database.insert_data(
            REPOS_INFO_TABLE_NAME,
            [
                self["organization_id"], self["descript"], self["location"],
                self["organization_blog_html"]]
        )

        database.insert_data(
            REPOS_URL_TABLE_NAME,
            [
                self["id"], self["url"]]
        )

        database.insert_data(
            REPOS_LANGUAGE_PROPORTION_TABLE_NAME,
            [
                self["organization_id"], self["descript"], self["location"],
                self["organization_blog_html"]]
        )

        database.insert_data(
            REPOS_PARTICIPANTS_TABLE_NAME,
            [
                self["organization_id"], self["descript"], self["location"],
                self["organization_blog_html"]]
        )

        database.insert_data(
            REPOS_FIELDS_TABLE_NAME,
            [
                self["organization_id"], self["descript"], self["location"],
                self["organization_blog_html"]]
        )

        row_count += 1
        if self.row_count >= 100:
            row_count = 0
            database.commit()
