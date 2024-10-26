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




# Topic常量
Topic_url = 'https://github.com/topics'
Topic_css = 'p.f3.lh-condensed.mb-0.mt-1.Link--primary'
Topic_button_Xpath = '/html/body/div[1]/div[4]/main/div[4]/div[1]/form/button'