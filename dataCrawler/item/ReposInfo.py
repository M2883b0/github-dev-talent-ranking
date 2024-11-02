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
    REPOS_PARTICIPANTS_TABLE_NAME, REPOS_FIELDS_TABLE_NAME, REPOS_PARTICIPANTS_CONTRIBUTIONS_TABLE_FIELD, \
    REPOS_PARTICIPANTS_CONTRIBUTIONS_TABLE_NAME

row_count = 0


class ReposInfo(scrapy.Item):
    # api.github.com/repos/xx
    id = scrapy.Field()
    url = scrapy.Field()  # api url
    language = scrapy.Field()
    description = scrapy.Field()
    forks_count = scrapy.Field()
    stargazers_count = scrapy.Field()
    subscribers_count = scrapy.Field()
    topics = scrapy.Field()  # list
    owner = scrapy.Field()
    open_issues_count = scrapy.Field()
    # importance = scrapy.Field()

    languages_percent = scrapy.Field()  # dict {"language": 1212}
    personal_contribution_value = scrapy.Field()  # dict {id: contribution}

    def insert_to_database(self):
        global row_count
        row_count += 1
        for field in ["url", "language", "description"]:
            if not self.get(field):
                self[field] = ""
        for field in ["forks_count", "stargazers_count", "subscribers_count", "open_issues_count"]:
            if not self.get(field):
                self[field] = 0
        for field in ["topics", "languages_percent"]:
            if not self.get(field):
                self[field] = []
        if not self.get("owner"):
            self["owner"] = {"id": 0}
        if not self.get("languages_percent"):
            self["languages_percent"] = {"id": 0}
        if not self.get("personal_contribution_value"):
            self["personal_contribution_value"] = {0: 0}
        total_value = sum(self["personal_contribution_value"].values())
        database.insert_data(
            REPOS_INFO_TABLE_NAME,
            [
                self["id"], self["language"], self["description"], self["subscribers_count"],
                self["forks_count"], self["stargazers_count"], 0,
                total_value, self["open_issues_count"]
            ]
        )
        database.insert_data(
            REPOS_URL_TABLE_NAME,
            [
                self["id"], self["url"]
            ]
        )
        for language, proportion in self["languages_percent"].items():
            database.insert_data(
                REPOS_LANGUAGE_PROPORTION_TABLE_NAME,
                [
                    self["id"], language, proportion
                ]
            )
        try:
            for topic in set(self["topics"] + [self["language"]]):
                database.insert_data(
                    REPOS_FIELDS_TABLE_NAME,
                    [
                        self["id"], topic
                    ]
                )
        except:
            pass
        for uid, contribute in self["personal_contribution_value"].items():
            if uid == self["owner"]["id"]:
                is_owner = 1
            else:
                is_owner = 0
            database.insert_data(
                REPOS_PARTICIPANTS_CONTRIBUTIONS_TABLE_NAME,
                [
                    self["id"], uid, is_owner, contribute
                ]
            )

        # if row_count >= 100:
        #     row_count = 0
        database.commit()
