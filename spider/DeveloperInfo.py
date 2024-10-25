# -*- encoding: utf-8 -*-
"""
@File    :   DeveloperInfo.py    
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/25 21:06    1.0         None
"""
import scrapy

# GitHub 提供了访问开发者的接口 https://api.github.com/users?since=0&per_page=1000
class DeveloperInfo():

    def __init__(self):
        id = 0
