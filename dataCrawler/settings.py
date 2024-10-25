# -*- encoding: utf-8 -*-
"""
@File    :   settings.py
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/25 23:13    1.0         None
"""
# Scrapy settings for mySpider project


BOT_NAME = 'github-dev-talent-ranking-spider'  # scrapy项目名

SPIDER_MODULES = ['mySpider.spiders']
NEWSPIDER_MODULE = 'mySpider.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32 # 最大并发量 默认16

# DOWNLOAD_DELAY = 3 # 下载延迟 3秒

# Override the default request headers: # 请求报头,我们打开
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}


ITEM_PIPELINES = {
    "dataCrawler.pipelines.UserInfoPipeline": 300
}
# 爬虫中间件
# SPIDER_MIDDLEWARES = {
#    'mySpider.middlewares.MyspiderSpiderMiddleware': 543,
# }

# 下载中间件
# DOWNLOADER_MIDDLEWARES = {
#    'mySpider.middlewares.MyspiderDownloaderMiddleware': 543,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'mySpider.pipelines.MyspiderPipeline': 300, # 管道
# }
