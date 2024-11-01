# -*- encoding: utf-8 -*-
"""
@File    :   RepoSpider.py    
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/27 0:13    1.0         None
"""
import json
from typing import Any, Iterable

import scrapy
from scrapy import Request
from scrapy.http import Response
from dataCrawler.config import repos_info_config as config

from dataCrawler import database
from dataCrawler.item.ReposInfo import ReposInfo
from dataCrawler.spiders.SpiderTemplate import SpiderTemplate
from dataCrawler import crawled_repos
from dataCrawler.item.TopicInfo import TopicInfo


class RepoSpider(SpiderTemplate):
    name = "RepoSpider"

    per_page = config["repos_list_step"]
    top1000url = config["repos_info_api_top1000_template"]
    repos_list_url = config["repos_info_api_template"]

    # user_detail_template = config["user_detail_template"]

    def start_requests(self) -> Iterable[Request]:
        yield self.request(url=self.top1000url.format(1, 1), callback=self.init_parse)
        begin = config["repos_stars_begin"]
        end = config["repos_stars_end"]
        step = config["repos_stars_step"]
        for lower_num in range(begin, end, step):
            yield self.request(
                url=self.repos_list_url.format(lower_num, lower_num + step, 1, 1),
                callback=self.init_parse, meta={"begin": lower_num, "end": lower_num + step})

    def init_parse(self, response: Response, **kwargs: Any) -> Any:
        result = json.loads(response.text)
        total_count = int(result["total_count"])
        page = 0
        for page in range(1, total_count // self.per_page + 1):
            if ".." in response.request.url:
                request = self.request(
                    url=self.repos_list_url.format(response.meta["begin"], response.meta["end"], self.per_page, page),
                    callback=self.parse)
            else:
                request = self.request(url=self.top1000url.format(self.per_page, page), callback=self.parse)
            yield request

        if total_count % self.per_page:
            page += 1
            if ".." in response.request.url:
                request = self.request(
                    url=self.repos_list_url.format(response.meta["begin"], response.meta["end"], self.per_page, page),
                    callback=self.parse)
            else:
                request = self.request(url=self.top1000url.format(self.per_page, page), callback=self.parse)
            yield request

    def parse(self, response: Response, **kwargs: Any) -> Any:
        self.logger.info("parse function begin")
        result = json.loads(response.text)
        if not result:
            return
        for repo in result["items"]:
            if repo['id'] in crawled_repos.keys() and crawled_repos[repo['id']] < config["user_followers_begin"]:
                continue
            # self.logger.info (f"解析用户{user['id']}详细信息字段")
            yield self.request(url=repo["url"], callback=self.parse_detail,
                               meta=response.meta)

    def parse_detail(self, response: Response, **kwargs: Any) -> Any:
        data = json.loads(response.text)
        assert isinstance(data, dict)
        # 提取项目所需要的字段
        required_key = (
            "id",
            "url",
            "language",
            "description",
            "forks_count",
            "stargazers_count",
            "subscribers_count",
            "topics",
            "owner",
            "open_issues_count",
        )
        field = self.filter_dict(data, required_key)
        # "languages_percent"
        url = data["languages_url"]
        yield self.request(url=url, callback=self.parse,
                           meta={"field": field, "contributors_url": data["contributors_url"]})

    def parse_language(self, response: Response, **kwargs: Any) -> Any:
        data = json.loads(response.text)
        field = response.meta["field"]
        field["languages_percent"] = data
        # "personal_contribution_value", personal page crawl
        url = response.meta["contributors_url"]
        yield self.request(url=url + "?page=1&per_page=100", callback=self.parse_contributors,
                           meta={"field": field, "page": 1, "contributors_url": url})

    def parse_contributors(self, response: Response, **kwargs: Any) -> Any:
        data = json.loads(response.text)
        field = response.meta["field"]
        url = response.meta["contributors_url"]
        page = response.meta["page"]
        assert isinstance(data, list)
        if response.meta.get("personal_contribution_value"):
            personal_contribution_value = response.meta.get("personal_contribution_value")
        else:
            personal_contribution_value = dict()
        for user in data:
            personal_contribution_value[user["id"]] = user["contributions"]
        if len(data) == 100:
            yield self.request(url=url + "?page={}&per_page=100".format(page), callback=self.parse_contributors,
                               meta={"field": field, "page": page+1, "contributors_url": url})
        else:
            yield ReposInfo(**field)
