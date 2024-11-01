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
    id = scrapy.Field()
    description = scrapy.Field()
    login = scrapy.Field()
    location = scrapy.Field()

    ##
    organization_blog_html = scrapy.Field()
    partner_id = scrapy.Field()

    def insert_to_database(self):
        global row_count
        for field in ["organization_blog_html", "partner_id", "organization_blog_html", "location", "description"]:
            if not self.get(field):
                if field == "partner_id":
                    self[field] = 0
                self[field] = ""
        try:
            database.insert_data(
                ORGANIZATIONS_TABLE_NAME,
                [
                    self["id"], self["login"], self["description"], self["location"],
                    self["organization_blog_html"]]
            )
        except:
            pass
        try:

            database.insert_data(
                USER_ORGANIZATION_TABLE_NAME,
                [
                    self["partner_id"], self["id"]
                ]
            )
        except:
            pass
        row_count += 1
        if row_count >= 100:
            row_count = 0
            database.commit()
