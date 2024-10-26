# -*- encoding: utf-8 -*-
"""
@File    :   TopicInfo.py    
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/26 22:28    1.0         None
"""
import scrapy


class TopicInfo(scrapy.Item):
    topic_name = scrapy.Field()
    topic_descript = scrapy.Field()
    topic_image = scrapy.Field()
    topic_url = scrapy.Field()

    def insert_to_database(self):
        pass