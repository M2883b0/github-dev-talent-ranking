# -*- encoding: utf-8 -*-
"""
@File    :   ReposInfo.py    
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/31 14:35    1.0         None
"""
import scrapy


class ReposItem(scrapy.Item):
    url = scrapy.Field()

