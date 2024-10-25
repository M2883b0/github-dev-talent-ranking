import scrapy

"""
# 爬取所有的topic
"""

class NewsSpider(scrapy.Spider):
    name = "topic_spider"
    start_urls = ['https://github.com/topics']  # 替换为实际的新闻列表页面 URL

    def parse(self, response):
        titles = []
        # 使用 XPath 或 CSS 选择器定位新闻标题
        for article in response.css('div.d-lg-flex container-lg p-responsive '):  # 根据网站结构调整选择器
            yield {
                'title': article.css('p.f3.lh-condensed.mb-0.mt-1.Link--primary::text').get(),
            }