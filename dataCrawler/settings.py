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

SPIDER_MODULES = [
    'dataCrawler.spiders.UserSpider',
    "dataCrawler.spiders.FeaturedTopicSpider",
    'dataCrawler.spiders.RepoSpider'
]

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 100  # 最大并发量 默认16

DOWNLOAD_DELAY = 0.09  # 下载延迟 0.3秒 15s/min

REFERER_ENABLED = False

RETRY_ENABLED = False  # 打开重试开关
# RETRY_TIMES = 10  # 重试次数
# RETRY_HTTP_CODES = [429, 403]  # 重试的HTTP状态码
# FEED_EXPORT_ENCODING = "utf-8"  # 导出编码

# Override the default request headers: # 请求报头,我们打开
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

ITEM_PIPELINES = {
    "dataCrawler.pipelines.UserInfoPipeline": 300
}

# LOG_LEVEL = 'DEBUG'
# LOG_LEVEL = 'WARNING'
# LOG_LEVEL = 'ERROR'
# settings.py
LOG_ENABLED = False

# 爬虫中间件
# SPIDER_MIDDLEWARES = {
# 'dataCrawler.middlewares.SpiderManager.SpiderManager': 553,
# }

# 下载中间件
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'dataCrawler.middlewares.HeaderRandom.HeaderRandom': 400,
    'dataCrawler.middlewares.Proxy.Proxy': 543,
}

EXTENSIONS = {
    'dataCrawler.extension.SpiderManager.SpiderManager': 500
}

USER_AGENT_LIST = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR "
    "2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR "
    "3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; "
    ".NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR "
    "3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 ("
    "Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
]

PROXIES_LIST = ['http://127.0.0.1:7890']

TOKEN = [
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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"
]
