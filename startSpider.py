# -*- encoding: utf-8 -*-
"""
@File    :   startSpider.py    
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/25 23:10    1.0         None
"""
from scrapy.crawler import CrawlerProcess
from dataCrawler.spiders.FeaturedTopicSpider import FeaturedTopicSpider
from dataCrawler.spiders.UserSpider import UserSpider
from dataCrawler.spiders.RepoSpider import RepoSpider
from dataCrawler.spiders.TopicSpider import TopicSpider
from scrapy.utils.project import get_project_settings

if __name__ == "__main__":
    settings = get_project_settings()
    process = CrawlerProcess(
        settings=settings
    )

    process.crawl(TopicSpider)
    # process.crawl(RepoSpider)
    # process.crawl(UserSpider)
    process.start()
