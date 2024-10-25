# -*- encoding: utf-8 -*-
"""
@File    :   startSpider.py    
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/25 23:10    1.0         None
"""
from scrapy import cmdline

# cmdline.execute("scrapy crawl UserSpider".split())
cmdline.execute("scrapy crawl GetTopic".split())
