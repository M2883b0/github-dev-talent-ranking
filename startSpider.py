# -*- encoding: utf-8 -*-
"""
@File    :   startSpider.py    
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/25 23:10    1.0         None
"""
from scrapy.crawler import CrawlerProcess
from dataCrawler.spiders.TopicSpider import TopicSpider
from dataCrawler.spiders.UserSpider import UserSpider


if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            "LOG_LEVEL": "WARNING"
                                       }
    )

    process.crawl(TopicSpider)
    process.start()

