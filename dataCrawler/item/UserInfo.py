# -*- encoding: utf-8 -*-
"""
@File    :   UserInfo.py
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/25 21:06    1.0         None
"""
import scrapy


# GitHub 提供了访问开发者的接口 https://api.github.com/users?since=0&per_page=1000
class UserInfo(scrapy.Item):
    ID = scrapy.Field()
    user_name = scrapy.Field()
    avatar_url = scrapy.Field()
    url = scrapy.Field()

