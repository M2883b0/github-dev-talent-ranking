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
from utility.DataBaseManager import DatabaseManager
from utility.config import TOPICS_TABLE_NAME


class TopicInfo(scrapy.Item):
    name = scrapy.Field()
    descript = scrapy.Field()
    image_url = scrapy.Field()
    url = scrapy.Field()
    repos_count = scrapy.Field()
    is_featured = scrapy.Field()

    # database = DatabaseManager()
    # database.connect()

    def insert_to_database(self):
        logging.info(f"insert topic {self['name']} to database")
        # self.database.insert_data(
        #     TOPICS_TABLE_NAME,
        #     [self["topic_name"], self["topic_descript"], self["topic_image"], self["topic_url"], self["is_featured"]]
        # )
        #
        # if self.cursor.rowcount >= 100:
        #     self.conn.commit()
        with open("topicList.txt", "a+", encoding="utf-8") as f:
            f.write(self["name"] + '\n')

    def close_spider(self, spider):
        # self.database.close()
        pass