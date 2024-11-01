# -*- encoding: utf-8 -*-
"""
@File    :   OrgInfo.py    
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/30 15:45    1.0         None
"""
import scrapy

from dataCrawler import database
from utility.DatabaseManager import DatabaseManager
from utility.config import USER_TABLE_NAME, TALENT_TABLE_NAME, ORGANIZATIONS_TABLE_NAME, USER_RELATIONSHIPS_TABLE_NAME, \
    USER_ORGANIZATION_TABLE_NAME

row_count = 0


class OrgInfo(scrapy.Item):
    organizations_id = scrapy.Field()
    descript = scrapy.Field()
    login = scrapy.Field()
    location = scrapy.Field()
    organization_blog_html = scrapy.Field(default="")
    partner_id = scrapy.Field(default=0)

    def insert_to_database(self):
        global row_count
        if not self.get("organization_blog_html"):
            self["organization_blog_html"] = ""
        if not self.get("partner_id"):
            self["partner_id"] = 0
        database.insert_data(
            ORGANIZATIONS_TABLE_NAME,
            [
                self["organization_id"], self["descript"], self["location"],
                self["organization_blog_html"]]
        )

        database.insert_data(
            USER_ORGANIZATION_TABLE_NAME,
            [
                self["user_id"], self["organizations_id"]
            ]
        )

        row_count += 1
        if self.row_count >= 100:
            row_count = 0
            database.commit()
