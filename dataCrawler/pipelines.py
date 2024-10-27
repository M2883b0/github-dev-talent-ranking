# -*- encoding: utf-8 -*-
"""
@File    :   pipelines.py
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/25 23:31    1.0         None
"""


class UserInfoPipeline:
    def process_item(self, item, spider):

        item.insert_to_database()
        return item
