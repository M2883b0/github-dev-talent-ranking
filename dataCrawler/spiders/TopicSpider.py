from typing import Any

import scrapy
from scrapy.http import Response

from dataCrawler.config import topic_list_url, topic_descript_xpath, topic_image_xpath_template, topic_name_xpath, topic_page_count, \
    topic_url_xpath, base_url
from dataCrawler.item.TopicInfo import TopicInfo


def url_list():
    """
    迭代器 生成要爬取的 url
    :return:
    """
    for i in range(1, topic_page_count+1):
        yield topic_list_url.format(i)
        # yield "https://api.52vmy.cn/api/query/itad"


urls = url_list()


class TopicSpider(scrapy.Spider):
    name = "TopicSpider"
    start_urls = [next(urls)]  # 填 topic URL
    custom_settings = {
        "DOWNLOAD_TIMEOUT": 5
    }

    def parse(self, response: Response, **kwargs: Any) -> Any:
        topic_names = response.xpath(topic_name_xpath).extract()
        topic_descripts = [i.strip() for i in response.xpath(topic_descript_xpath).extract()]
        topic_images = []
        topic_urls = [base_url+i for i in response.xpath(topic_url_xpath).extract()]
        for i in range(1, len(topic_names)+1):
            tmp = response.xpath(topic_image_xpath_template.format(i)).extract()
            if tmp:
                topic_images.append(tmp[0])
            else:
                topic_images.append("")
        for topic_name, topic_descript, topic_image, topic_url in zip(topic_names, topic_descripts, topic_images, topic_urls):
            yield TopicInfo(topic_name=topic_name, topic_descript=topic_descript, topic_image=topic_image, topic_url=topic_url)

        for url in urls:
            yield scrapy.Request(url)
