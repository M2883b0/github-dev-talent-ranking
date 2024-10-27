# -*- encoding: utf-8 -*-
"""
@File    :   TopicInfo.py    
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/26 22:28    1.0         None
"""
import scrapy
from utility.DataBaseManager import DatabaseManager
from utility.config import repos_topic


class TopicInfo(scrapy.Item):
    topic_name = scrapy.Field()
    topic_descript = scrapy.Field()
    topic_image = scrapy.Field()
    topic_url = scrapy.Field()
    is_featured = scrapy.Field()
    database = DatabaseManager()
    database.connect()

    def insert_to_database(self):
        self.database.insert_data(repos_topic, [self["topic_name"], self["topic_descript"],
                                           self["topic_image"], self["topic_url"], self["is_featured"]])
        # with open("./topicList.txt", "a+") as f:
        #     f.write(self["topic_name"] + "\n")

    def close_spider(self, spider):
        self.database.close()
