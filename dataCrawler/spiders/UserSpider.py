# -*- encoding: utf-8 -*-
"""
@File    :   UserSpider.py
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/25 22:41    1.0         None
"""
import json
from typing import Any, Iterable

import scrapy
from scrapy import Request
from scrapy.http import Response
from twisted.python.failure import Failure
from twisted.internet.error import TCPTimedOutError

import logging

from dataCrawler import database, crawled_users
from dataCrawler.config import user_info_config as config
from dataCrawler.item.OrgInfo import OrgInfo
from dataCrawler.item.UserInfo import UserInfo
from utility.config import ERROR_TABLE_NAME


def url_list(user_number):
    """
    迭代器 生成要爬取的 url
    :return:
    """
    for i in range(2, user_number, config["user_list_step"]):
        yield config["user_info_api_template"].format(config["user_list_step"], 1)


class UserSpider(scrapy.Spider):
    name = "UserSpider"
    # allowed_domains = ["github.com"]
    step = config["user_list_step"]
    top1000url = config["user_info_api_top1000_template"]
    user_list_url = config["user_info_api_template"]
    user_detail_template = config["user_detail_template"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start_requests(self) -> Iterable[Request]:

        yield self.request(url=self.top1000url.format(1, 1), callback=self.init_parse)
        begin = config["user_followers_begin"]
        end = config["user_followers_end"]
        for lower_num in range(begin, end, 100):
            yield self.request(url=self.user_list_url.format(lower_num, lower_num + 100, 1, 1),
                               callback=self.init_parse, meta={"begin": lower_num, "end": lower_num + 100})

    def request(self, url, callback, meta=None):
        return scrapy.Request(url=url, callback=callback, errback=self.err_back, meta=meta)

    def err_back(self, failure: Failure):
        # TODO: 错误处理
        print("type of failure", type(failure))
        print("request url ", failure.request.url)

        print(failure.check(TCPTimedOutError))
        # if failure
        # response = failure.value.response
        # assert isinstance(response, Response)
        # code = response.status
        # url = response.url
        # meta = json.dumps(response.meta)
        # spider_name = self.name
        #
        # print(url, code, meta, spider_name)
        # database.insert_data(
        #     ERROR_TABLE_NAME,
        #     (
        #         url, code, spider_name, meta
        #     )
        # )
        #
        # database.commit()

    def init_parse(self, response: Response, **kwargs: Any) -> Any:
        result = json.loads(response.text)
        total_count = int(result["total_count"])
        page = 0
        for page in range(1, total_count // self.step + 1):
            if ".." in response.request.url:
                request = self.request(
                    url=self.user_list_url.format(response.meta["begin"], response.meta["end"], self.step, page),
                    callback=self.parse)
            else:
                request = self.request(url=self.top1000url.format(self.step, page), callback=self.parse)
            yield request

        if total_count % self.step:
            page += 1
            if ".." in response.request.url:
                request = self.request(
                    url=self.user_list_url.format(response.meta["begin"], response.meta["end"], self.step, page),
                    callback=self.parse)
            else:
                request = self.request(url=self.top1000url.format(self.step, page), callback=self.parse)
            yield request

    def parse(self, response: Response, **kwargs: Any) -> Any:
        logging.info("parse function begin")
        result = json.loads(response.text)
        if not result:
            return
        if response.meta.get("is_follower"):
            li = result
            # print("follower list ", len(li))
        else:
            li = result["items"]
        for user in li:
            if user['id'] in crawled_users.keys() and crawled_users[user['id']] < 500:
                continue
            # logging.info(f"解析用户{user['id']}详细信息字段")
            yield self.request(url=self.user_detail_template + user["login"], callback=self.parse_detail,
                               meta=response.meta)

    def parse_detail(self, response: Response, **kwargs: Any) -> Any:
        # print("begin parse Detail the meta is ", response.meta)
        data = json.loads(response.text)
        assert isinstance(data, dict)
        # 提取项目所需要的字段
        required_key = (
            "id",
            "login",
            "name",
            "followers",
            "company",
            "location",
            "email",
            "location",
            "bio",
            "repos_url",
            "public_repos"
        )
        field = {
            key: value for key, value in data.items() if key in required_key
        }
        # print(meta)
        if response.meta.get("is_follower"):
            field["following_id"] = response.meta["follower_id"]
            yield UserInfo(**field)
        else:
            # "followers_url" 国籍判断
            # TODO: 需要更改常量
            for page in range(1, 2):
                url = data["followers_url"] + f"?per_page=30&page={page}"
                yield self.request(url=url, callback=self.parse,
                                   meta={"is_follower": True, "follower_id": data["id"]})

            # "organizations_url"

            yield self.request(url=data["organizations_url"], callback=self.parse_organization,
                               meta={"partner_id": data["id"]})
            # "blog", personal page crawl
            if data["blog"]:
                field["blog_html"] = data["blog"]
            # yield self.request(url=data["html_url"], callback=self.personal_page_parse, meta={"field": field})
            yield self.request(url=data["repos_url"] + "?per_page=100&page=1", callback=self.personal_page_parse,
                               meta={"field": field})

    def parse_organization(self, response: Response, **kwargs: Any) -> Any:
        data = json.loads(response.text)
        if not data:
            return
        for org in data:
            self.request(url=org["url"], callback=self._parse_organiztion, meta=response.meta)

    def _parse_organiztion(self, response: Response, **kwargs: Any) -> Any:
        data = json.loads(response.text)

        required_key = (
            "id",
            "description",
            "login",
            "location"
        )

        field = self.filter_dict(data, required_key)
        field["partner_id"] = response.meta["partner_id"]
        if data["blog"]:
            self.request(url=self.url_check(data["blog"]), callback=self._downlaod_org_blog, meta={"field": field})
        else:
            yield OrgInfo(**field)

    def _downlaod_org_blog(self, response: Response, **kwargs: Any):
        main_lable = response.xpath("/html/body").extract()[0]
        blog = main_lable[:10000000]
        field = response.meta["field"]
        field["organization_blog_html"] = blog
        yield OrgInfo(**field)

    def _download_personal_blog(self, response: Response, **kwargs: Any):
        main_lable = response.xpath("/html/body").extract()[0]
        blog = main_lable[:10000000]
        field = response.meta["field"]
        field["blog_html"] = blog
        yield UserInfo(**field)

    def personal_page_parse(self, response: Response, **kwargs: Any) -> Any:
        field = response.meta["field"]

        # TODO: personal page

        if field.get("blog_html"):
            need_proxy_url = ["twitter", "github.com"]
            is_proxy = False
            for i in need_proxy_url:
                if i in field.get("blog_html"):
                    is_proxy=True
            yield self.request(url=self.url_check(field["blog_html"]), callback=self._download_personal_blog,
                               meta={"field": field, "is_proxy": is_proxy, "download_timeout": 5})
        else:
            data = json.loads(response.text)
            field["repos_url"] = [field["repos_url"]]
            for repo in data:
                field["repos_url"].append(repo["url"])
                if repo["name"].endswith("github.io"):
                    yield self.request(url=self.url_check(repo["name"]), callback=self._download_personal_blog,
                                       meta={"field": field})

            yield UserInfo(**field)

    def filter_dict(self, target, keys):
        return {
            key: value for key, value in target if key in keys
        }

    def url_check(self, url: str):
        if url.startswith("www."):
            url = "http://" + url
        elif url.startswith("http"):
            pass
        elif '.' in url:
            url = "http://" + url
        return url
