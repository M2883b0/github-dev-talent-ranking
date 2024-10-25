# -*- encoding: utf-8 -*-
"""
@File    :   developerInfo.py
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/25 21:06    1.0         None
"""



# GitHub 提供了访问开发者的接口 https://api.github.com/users?since=0&per_page=1000
class DeveloperInfo():

    def __init__(self):
        id = 0


    def get_user(self):
        for i in range(100):
            url = user_info_api_template.format(i, 1000)
            response = requests.get(url)
            print(response.text)


if __name__ == "__main__":
    myspider = MySpider()
    myspider.get_user()