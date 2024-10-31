# -*- encoding: utf-8 -*-
"""
@File    :   startSpider.py    
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/25 23:10    1.0         None
"""
import asyncio
import logging

from scrapy.crawler import CrawlerRunner, CrawlerProcess
from twisted.internet import reactor

from dataCrawler.spiders.FeaturedTopicSpider import FeaturedTopicSpider
from dataCrawler.spiders.UserSpider import UserSpider
from dataCrawler.spiders.RepoSpider import RepoSpider
from dataCrawler.spiders.TopicSpider import TopicSpider
from dataCrawler.spiders.UserSpider import UserSpider
from scrapy.utils.project import get_project_settings
from dataCrawler import database
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":

    settings = get_project_settings()
    process = CrawlerProcess(
        settings=settings
    )
    # logging.info("Starting spider1...")
    # process.crawl(TopicSpider)
    process.crawl("UserSpider")
    # logging.info("Starting spider2...")
    # process.crawl(FeaturedTopicSpider)
    # 启动爬虫引擎
    logging.info("Starting crawler process...")
    process.start()
    database.close()
