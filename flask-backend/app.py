import json

from flask import request
from flask import Flask
from flask import render_template
from utility.DatabaseManagerBackend import DatabaseManager
from utility.models import Topic
from sqlalchemy import and_, or_

app = Flask(__name__)


@app.route("/")
def hello():  # 主页
    # return render_template("index.html", name='123')
    return "Hello word"


@app.route("/get_topics_page")
def get_topics_page():   #一次性返回26个：A【9个】，B【9个】
    """
  列出所有的topic列表详细信息，获得一个topic的详细
  :return:
  """
    order = request.args.get("order")   # 按仓库数的排序方式【正序和逆序,不填的话，默认是正序】
    page = request.args.get("page")    # 分页
    limit = request.args.get("limit")  # 每页的限制,建议9个



    #要分多个情况，示例
    # if name=='':          #name为空，不指定name，返回topic list的情况
    #     if is_feature:  # is_feature = True #返回精选的
    #         print('')
    #     else:            # is_feature = False,表示不按feature筛选，返回所有的
    #         print('')
    # else:                #传了name，按照name，返回一个topic【'C'】或者list【'C%'】
    #     print('')


    # 例如得到：
    test = {
        "len":26,
        "A":[
            {
                "tpoic_name": "a1",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "a2",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "a3",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "a4",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "a5",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "a6",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "a7",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "a8",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "a9",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            }
        ],
        "B":[
            {
                "tpoic_name": "b1",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "b2",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "b3",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "b4",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "b5",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "b6",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": "3411"
            },
            {
                "tpoic_name": "b7",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "b8",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "b9",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            }
        ],
        "C":[
            {
                "tpoic_name": "c1",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "c2",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "c3",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "c4",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "c5",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "c6",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "c7",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "c8",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "c9",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            }
        ],

        "D": [
            {
                "tpoic_name": "d1",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "d2",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "d3",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "d4",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "d5",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "d6",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "d7",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "d8",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "d9",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            }
        ]
    }
    return json.dumps(test)

@app.route("/get_topic")
def get_topic():
    """
  1、搜索框，搜索topic跳转过来，2、所有topic页面的点击某个topic跳转过来
  :return:这个topic的开发者的榜单
  """
    order = request.args.get("order")  # 按仓库数的排序方式【正序和逆序,不填的话，默认是正序】
    topic = request.args.get("topic")    # topic名字，name
    is_first_letter = request.args.get('is_first_letter')
    is_feature = request.args.get("is_feature")
    page = request.args.get("page")      # 分页
    limit = request.args.get("limit")    # 每页的限制，可以20个等

    #示例
    test = {
        "total_count": 80,
        "size": 6,
        "total_pages": 16,
        "current_page": 1,
        "rank_list": [
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1,
            }
        ]
    }
    return json.dumps(test)



@app.route("/topic_rank")
def topic_rank():
    """
  1、搜索框，搜索topic跳转过来，2、所有topic页面的点击某个topic跳转过来
  :return:这个topic的开发者的榜单
  """
    topic = request.args.get("topic")    #  topic名字
    nation = request.args.get("nation")  # 筛选项：国籍
    page = request.args.get("page")      # 分页
    limit = request.args.get("limit")    # 每页的限制

    if topic:              #如果指定了topic，就返回这个topic的榜单talent排序的，开发者信息榜单
        print('')
    else:                  #如果没指定topic，就返回按开发者综合talent的排行版。
        print('')


    # 操作数据库拿到数据
    # 例如：
    test = {
        "total_count": 45,
        "size": 5,
        "total_pages": 9,
        "current_page": 1,
        "rank_list": [
            {
                "login_name": "zhangsan",
                "name": "zhang",
                "github_url": "github_url",
                "image_url": "xxx/png",
                "email": "xxxxx@xx.com",
                "bio": "I am a dog xxxx.",
                "company": "Google Inc",
                "nation": "China",
                "repos_num": 7,
                "stars_num": 41341,
                "followers_num": 394,
                "fork_num": 32131,
                "have_topic": ["Linux", "C", "C++"],
                "have_topic_talent": [100, 110, 120],
                "total_talent": 330,
            },
            {
                "login_name": "zhangsan",
                "name": "zhang",
                "github_url": "github_url",
                "image_url": "xxx/png",
                "email": "xxxxx@xx.com",
                "bio": "I am a dog xxxx.",
                "company": "Google Inc",
                "nation": "China",
                "repos_num": 7,
                "stars_num": 41341,
                "followers_num": 394,
                "fork_num": 32131,
                "have_topic": ["Linux", "C", "C++"],
                "have_topic_talent": [100, 110, 120],
                "total_talent": 330,
            },
            {
                "login_name": "zhangsan",
                "name": "zhang",
                "github_url": "github_url",
                "image_url": "xxx/png",
                "email": "xxxxx@xx.com",
                "bio": "I am a dog xxxx.",
                "company": "Google Inc",
                "nation": "China",
                "repos_num": 7,
                "stars_num": 41341,
                "followers_num": 394,
                "fork_num": 32131,
                "have_topic": ["Linux", "C", "C++"],
                "have_topic_talent": [100, 110, 120],
                "total_talent": 330,
            },
            {
                "login_name": "zhangsan",
                "name": "zhang",
                "github_url": "github_url",
                "image_url": "xxx/png",
                "email": "xxxxx@xx.com",
                "bio": "I am a dog xxxx.",
                "company": "Google Inc",
                "nation": "China",
                "repos_num": 7,
                "stars_num": 41341,
                "followers_num": 394,
                "fork_num": 32131,
                "have_topic": ["Linux", "C", "C++"],
                "have_topic_talent": [100, 110, 120],
                "total_talent": 330,
            },
            {
                "login_name": "zhangsan",
                "name": "zhang",
                "github_url": "github_url",
                "image_url": "xxx/png",
                "email": "xxxxx@xx.com",
                "bio": "I am a dog xxxx.",
                "company": "Google Inc",
                "nation": "China",
                "repos_num": 7,
                "stars_num": 41341,
                "followers_num": 394,
                "fork_num": 32131,
                "have_topic": ["Linux", "C", "C++"],
                "have_topic_talent": [100, 110, 120],
                "total_talent": 330,
            },
        ]
    }
    return json.dumps(test)


@app.route("/random_topic")
def random_topic():
    """
  :return:随机返回几个topic
  """
    num = request.args.get("num")   #随机返回几个topic，得有介绍和url的。【被人修改过的topic中随机选】

    # 操作数据库，还是哪里。拿到这个统计的数据
    # 例如：
    test = {
        "total_count": 6,
        "relate_topic_list": [
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1
            }
        ]
    }
    return json.dumps(test)




@app.route("/relate_topic")
def relate_topic():
    """
  :return:这个topic的，相似的几个topic
  """
    topic = request.args.get("topic")  # topic名字
    num = request.args.get("num")   #返回推荐的前几个，例如返回6个

    # 操作数据库，还是哪里。拿到这个统计的数据
    # 例如：
    test = {
        "total_count": 6,
        "relate_topic_list": [
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature":1
            }
        ]
    }
    return json.dumps(test)


@app.route("/search_users")
def search_users():
    """
  :return:返回这个用户的页面信息【个人详细信息、】
  """
    login_name = request.args.get("name")  # login名
    page = request.args.get("page")  # 分页
    limit = request.args.get("limit")  # 每页的限制


    # TODO: 关系圈：先调用数据库，如果没有，就调用爬虫接口现场爬。


    # 操作数据库，还是哪里。拿到这个统计的数据
    # 例如：
    test = {
        "login_name": "zhangsan",
        "name": "zhang",
        "github_url": "github_url",
        "image_url": "xxx/png",
        "email": "xxxxx@xx.com",
        "bio": "I am a dog xxxx.",
        "company": "Google Inc",
        "organize": "dasdadea",
        "organize_image_url": "xxxx/png",
        "organize_url": "github/dasda",
        "nation": "China",
        "repos_num": 7,
        "stars_num": 41341,
        "followers_num": 394,
        "fork_num": 32131,
        "have_topic": ["Linux", "C", "C++"],
        "have_topic_talent": [100, 110, 120],
        "total_talent": 330,
        "relate_rank_list": [
            {
                "total_count": 45,
                "size": 5,
                "total_pages": 9,
                "current_page": 1,
                "rank_list": [
                    {
                        "login_name": "zhangsan",
                        "name": "zhang",
                        "github_url": "github_url",
                        "image_url": "xxx/png",
                        "email": "xxxxx@xx.com",
                        "bio": "I am a dog xxxx.",
                        "company": "Google Inc",
                        "organize": "dasdadea",
                        "organize_image_url": "xxxx/png",
                        "organize_url": "github/dasda",
                        "nation": "China",
                        "repos_num": 7,
                        "stars_num": 41341,
                        "followers_num": 394,
                        "fork_num": 32131,
                        "have_topic": ["Linux", "C", "C++"],
                        "have_topic_talent": [100, 110, 120],
                        "total_talent": 330,
                    },
                    {
                        "login_name": "zhangsan",
                        "name": "zhang",
                        "github_url": "github_url",
                        "image_url": "xxx/png",
                        "email": "xxxxx@xx.com",
                        "bio": "I am a dog xxxx.",
                        "company": "Google Inc",
                        "organize": "dasdadea",
                        "organize_image_url": "xxxx/png",
                        "organize_url": "github/dasda",
                        "nation": "China",
                        "repos_num": 7,
                        "stars_num": 41341,
                        "followers_num": 394,
                        "fork_num": 32131,
                        "have_topic": ["Linux", "C", "C++"],
                        "have_topic_talent": [100, 110, 120],
                        "total_talent": 330,
                    },
                    {
                        "login_name": "zhangsan",
                        "name": "zhang",
                        "github_url": "github_url",
                        "image_url": "xxx/png",
                        "email": "xxxxx@xx.com",
                        "bio": "I am a dog xxxx.",
                        "company": "Google Inc",
                        "organize": "dasdadea",
                        "organize_image_url": "xxxx/png",
                        "organize_url": "github/dasda",
                        "nation": "China",
                        "repos_num": 7,
                        "stars_num": 41341,
                        "followers_num": 394,
                        "fork_num": 32131,
                        "have_topic": ["Linux", "C", "C++"],
                        "have_topic_talent": [100, 110, 120],
                        "total_talent": 330,
                    },
                    {
                        "login_name": "zhangsan",
                        "name": "zhang",
                        "github_url": "github_url",
                        "image_url": "xxx/png",
                        "email": "xxxxx@xx.com",
                        "bio": "I am a dog xxxx.",
                        "company": "Google Inc",
                        "organize": "dasdadea",
                        "organize_image_url": "xxxx/png",
                        "organize_url": "github/dasda",
                        "nation": "China",
                        "repos_num": 7,
                        "stars_num": 41341,
                        "followers_num": 394,
                        "fork_num": 32131,
                        "have_topic": ["Linux", "C", "C++"],
                        "have_topic_talent": [100, 110, 120],
                        "total_talent": 330,
                    },
                    {
                        "login_name": "zhangsan",
                        "name": "zhang",
                        "github_url": "github_url",
                        "image_url": "xxx/png",
                        "email": "xxxxx@xx.com",
                        "bio": "I am a dog xxxx.",
                        "company": "Google Inc",
                        "organize": "dasdadea",
                        "organize_image_url": "xxxx/png",
                        "organize_url": "github/dasda",
                        "nation": "China",
                        "repos_num": 7,
                        "stars_num": 41341,
                        "followers_num": 394,
                        "fork_num": 32131,
                        "have_topic": ["Linux", "C", "C++"],
                        "have_topic_talent": [100, 110, 120],
                        "total_talent": 330,
                    }
                ]
            }
        ]
    }
    return json.dumps(test)


if __name__ == "__main__":
    database_manager = DatabaseManager()
    # database_manager.query_with_filters()
    app.run(host="0.0.0.0", port=5780, debug=True)
