import scrapy

"""
# 爬取所有的topic
"""

class NewsSpider(scrapy.Spider):
    name = "news_spider"
    start_urls = ['https://example.com/news']  # 替换为实际的新闻列表页面 URL

    def parse(self, response):
        # 使用 XPath 或 CSS 选择器定位新闻标题
        for article in response.css('div.article'):  # 根据网站结构调整选择器
            yield {
                'title': article.css('h2.title::text').get(),
            }