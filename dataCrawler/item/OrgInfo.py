# -*- encoding: utf-8 -*-
"""
@File    :   OrgInfo.py    
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/30 15:45    1.0         None
"""
import scrapy

from utility.DatabaseManager import DatabaseManager
from utility.config import USER_TABLE_NAME, TALENT_TABLE_NAME

class OrgInfo(scrapy.Item):
    organizations_id
    descript
    location
    organization_blog_html