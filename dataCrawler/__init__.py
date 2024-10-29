# -*- encoding: utf-8 -*-
"""
@File    :   __init__.py.py    
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/25 21:01    1.0         None
"""
import logging

from utility.DataBaseManager import DatabaseManager
from utility.config import TOPICS_TABLE_NAME, TOPICS_URL_TABLE_NAME

database = DatabaseManager()
database.connect()

crawled_topics = [key["name"] for key in database.query_data(TOPICS_URL_TABLE_NAME)]

SPIDER_NUM = 1
# crawled_users = database.query_data()
# crawled_repos = database.query_data()
# crawled_orgs = database.query_data()


