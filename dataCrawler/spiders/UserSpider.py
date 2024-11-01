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
from dataCrawler.spiders.SpiderTemplate import SpiderTemplate
from utility.config import ERROR_TABLE_NAME




class UserSpider(SpiderTemplate):
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
        for lower_num in range(begin, end, config["user_followers_step"]):
            yield self.request(url=self.user_list_url.format(lower_num, lower_num + config["user_followers_step"], 1, 1),
                               callback=self.init_parse, meta={"begin": lower_num, "end": lower_num + config["user_followers_step"]})

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
        self.logger.info("parse function begin")
        result = json.loads(response.text)
        if not result:
            return
        if response.meta.get("is_follower"):
            li = result
        else:
            li = result["items"]
        for user in li:
            if user['id'] in crawled_users.keys() and crawled_users[user['id']] < config["user_followers_begin"]:
                continue
            # self.logger.info (f"解析用户{user['id']}详细信息字段")
            yield self.request(url=self.user_detail_template + user["login"], callback=self.parse_detail,
                               meta=response.meta)

    def parse_detail(self, response: Response, **kwargs: Any) -> Any:
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
        field = self.filter_dict(data, required_key)
        if response.meta.get("is_follower"):
            field["following_id"] = response.meta["follower_id"]
            yield UserInfo(**field)
        else:
            # "followers_url" 国籍判断

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
            yield self.request(url=org["url"] + "?per_page=100&page=1", callback=self._parse_organiztion, meta=response.meta)

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
        if data.get("blog"):
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
        if field.get("blog_html"):
            need_proxy_url = ["twitter", "github.com"]
            is_proxy = False
            for i in need_proxy_url:
                if i in field.get("blog_html"):
                    is_proxy = True
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


