# -*- encoding: utf-8 -*-
"""
@File    :   __init__.py.py    
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/25 21:01    1.0         None
"""
import logging

from utility.DatabaseManager import DatabaseManager, DatabaseConnectionPool
from utility.config import TOPICS_TABLE_NAME, TOPICS_URL_TABLE_NAME, USER_LOGIN_NAME_TABLE_NAME
from scrapy.signalmanager import SignalManager

database = DatabaseManager(DatabaseConnectionPool())
database.connect()

SpiderIdleSignal = SignalManager()
AllSpiderIdle = SignalManager()
SendToManagerSignal = SignalManager()
message_list = []
# 设置个信号量，用于错误重爬和其他爬虫调用
CrawlTopicListSignal = SignalManager()
CrawlTopicDetailSignal = SignalManager()

crawled_topics = [key["name"] for key in database.query_data(TOPICS_URL_TABLE_NAME)]
_users = database.query_data(USER_LOGIN_NAME_TABLE_NAME)
if _users:
    crawled_users = [key["id"] for key in database.query_data(USER_LOGIN_NAME_TABLE_NAME)]
else:
    crawled_users = []
    print(_users)
# crawled_users = database.query_data()
# crawled_repos = database.query_data()
# crawled_orgs = database.query_data()


