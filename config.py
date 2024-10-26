# -*- encoding: utf-8 -*-
"""
@File    :   config.py    
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/26 11:03    1.0         None
"""
# GitHub 官方提供的接口

# 用户信息接口
user_info_api_template = "https://api.github.com/users?since={}&per_page={}"
user_list_step = 1000
user_number = 5000

# All featured topics 接口 https://github.com/topics?page=6
base_url = "https://github.com"
topic_list_url = 'https://github.com/topics?page={}'
topic_name_xpath = '/html/body/div[1]/div//div[1]/div/div/a[2]/p[1]/text()'
topic_descript_xpath = "/html/body/div[1]/div//div[1]/div/div/a[2]/p[2]/text()"
topic_image_xpath_template = '/html/body/div[1]/div[4]/main/div[4]/div[1]/div/div[{}]/a[1]/img/@src'
topic_url_xpath = "/html/body/div[1]/div[4]/main/div[4]/div[1]/div/div/a[2]/@href"

topic_page_count = 5


# useragent list


