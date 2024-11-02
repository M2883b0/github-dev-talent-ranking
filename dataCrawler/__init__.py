# -*- encoding: utf-8 -*-
"""
@File    :   __init__.py.py    
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/25 21:01    1.0         None
"""
from utility.DatabaseManager import DatabaseManager, DatabaseConnectionPool
from utility.config import TOPICS_TABLE_NAME, TOPICS_URL_TABLE_NAME, USER_LOGIN_NAME_TABLE_NAME, \
    USER_TABLE_NAME, ORGANIZATIONS_TABLE_NAME, REPOS_INFO_TABLE_NAME, REPOS_URL_TABLE_NAME
from scrapy.signalmanager import SignalManager

database = DatabaseManager(DatabaseConnectionPool())
database.connect()
row_count = 0

SpiderIdleSignal = SignalManager()
AllSpiderIdle = SignalManager()
SendToManagerSignal = SignalManager()
message_list = []
# 设置个信号量，用于错误重爬和其他爬虫调用
CrawlTopicListSignal = SignalManager()
CrawlTopicDetailSignal = SignalManager()

crawled_topics = [key["name"] for key in database.query_data(TOPICS_URL_TABLE_NAME)]
_users = database.query_data(USER_TABLE_NAME)

if _users:
    crawled_users = {key["id"]: key['followers'] for key in _users}
else:
    crawled_users = dict()

_orgs = database.query_data(ORGANIZATIONS_TABLE_NAME)
if _orgs:
    crawled_orgs = [key["organization_id"] for key in _orgs]
else:
    crawled_orgs = dict()

_repos = database.query_data(REPOS_URL_TABLE_NAME)
if _repos:
    crawled_repos = [key['repos_url'] for key in _repos]
else:
    crawled_repos = []

