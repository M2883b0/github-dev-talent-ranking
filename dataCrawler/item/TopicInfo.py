# -*- encoding: utf-8 -*-
"""
@File    :   TopicInfo.py    
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/26 22:28    1.0         None
"""
import logging

import scrapy
from dataCrawler import database
from utility.config import TOPICS_TABLE_NAME, TOPICS_URL_TABLE_NAME

row_count = 0


class TopicInfo(scrapy.Item):
    name = scrapy.Field()
    descript = scrapy.Field()
    is_featured = scrapy.Field()
    curated = scrapy.Field()

    image_url = scrapy.Field()
    url = scrapy.Field()
    repos_count = scrapy.Field()


    def insert_to_database(self):
        global row_count
        database.insert_data(
            TOPICS_TABLE_NAME,
            [self["name"], self["descript"], self["image_url"], self["repos_count"], self["is_featured"], self["curated"]]
        )

        database.insert_data(
            TOPICS_URL_TABLE_NAME,
            [self["name"], self["url"]]
        )
        logging.info(f"insert topic {self['name']} to database")
        row_count += 1
        if row_count >= 100:
            row_count = 0
            database.commit()

    def close_spider(self, spider):
        print("item closed")
        database.commit()
