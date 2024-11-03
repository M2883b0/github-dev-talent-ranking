import json
import random

from flask import request
from flask import Flask
from flask import render_template
from utility.DatabaseManagerBackend import DatabaseManager, TableName
from utility.models import Topic, TopicUrl
from sqlalchemy import and_, or_, func, desc, asc

from utility.field_constants import UserFields, UserOrganizationFields, UserRelationshipFields, UserReposFields, \
    UserBlogFields, UserLoginNameFields, ReposFieldFields, ReposInfoFields, ReposParticipantFields, ReposUrlFields, \
    ReposLanguageProportionFields, ReposParticipantContributionFields, OrganizationFields, TopicFields, \
    CrawledUrlFields, TopicUrlFields, TalentFields, SpiderErrorFields

app = Flask(__name__)

user_image_url_template = "https://avatars.githubusercontent.com/u/{}?v=4"
user_github_url_template = "https://avatars.githubusercontent.com/u/{}?v=4"


@app.route("/")
def hello():  # 主页
    # return render_template("index.html", name='123')
    return "Hello word"


@app.route("/get_topics_page")
def get_topics_page():
    """
    #所有的page页面：一次性返回26个：A【9个】，B【9个】
  :return:
  """
    order = request.args.get("order")  # 按topic仓库数的排序方式【正序和逆序,不填的话，默认是正序】
    page = request.args.get("page")  # 分页
    limit = request.args.get("limit")  # 每页的限制,建议9个,就是每个topic首字母，只返回9个

    # 操作数据库:多表【topic、topic_url表】

    # 例如得到：
    test = {
        "len": 26,
        "A": [
            {
                "tpoic_name": "a1",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "a2",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "a3",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "a4",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "a5",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "a6",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "a7",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "a8",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "a9",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            }
        ],
        "B": [
            {
                "tpoic_name": "b1",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "b2",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "b3",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "b4",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "b5",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
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
                "is_feature": 1,
            },
            {
                "tpoic_name": "b8",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "b9",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            }
        ],
        "C": [
            {
                "tpoic_name": "c1",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "c2",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
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
                "is_feature": 1,
            },
            {
                "tpoic_name": "c5",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "c6",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "c7",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "c8",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "c9",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            }
        ],

        "D": [
            {
                "tpoic_name": "d1",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "d2",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "d3",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "d4",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "d5",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "d6",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "d7",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "d8",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "d9",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            }
        ]
    }
    return json.dumps(test)


@app.route("/get_topic")
def get_topic():
    """
  1、精确查询：【搜索框搜索，跳到topic榜单】；【点击某个topic跳转，跳到topic榜单】，这个榜单的第一个，就是返回单个topic的信息。
  2、模糊查询，所有topic的列表，A只展示9个，点击A的所有topic。就需要模糊查询所有以A开头的topic，按仓库排序。
  :return:这个topic的开发者的榜单
  """
    order = request.args.get("order")  # 按仓库数的排序方式【正序和逆序,不填的话，默认是正序】
    topic = request.args.get("topic")  # topic名字，name
    is_first_letter = request.args.get('is_first_letter')
    is_feature = request.args.get("is_feature")
    page = request.args.get("page")  # 分页
    limit = request.args.get("limit")  # 每页的限制，可以20个等

    db_manager = DatabaseManager()
    # session = self.get_session()
    filters = []
    filters.append(Topic.name.like(f'{topic}%'))
    if is_feature:
        filters.append(Topic.is_featured == bool(int(is_feature)))
    # query = session.query(Topic, TopicUrl.url) \
    #     .join(TopicUrl, Topic.name == TopicUrl.name, isouter=True) \
    #     .filter(and_(*filters))
    # if order:      #True
    #     query = query.order_by(desc(Topic.repos_count))
    # else:
    #     query = query.order_by(asc(Topic.repos_count))
    # 添加分页
    # offset = (int(page) - 1) * int(limit)
    # query = query.offset(offset).limit(int(limit))
    # results = query.all()

    # 查询数据库，多表【topic表和topic_url表】

    if is_first_letter:  # 首字母模糊查询name，例如返回C开头的topic
        print('')
    else:
        print('')  # 精确查询name，例如只返回C这一个topic

    # 示例
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
                "is_feature": 1,
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1,
            }
        ]
    }
    return json.dumps(test)


def get_specific_topic_rank(topic, nation):
    return [
        {
            "id": 1,
            "login_name": "test",
            "name": "zhang",
            "email": "xxxxx@xx.com",
            "bio": "I am a dog xxxx.",
            "company": "Google Inc",
            "nation": "China",
            "repos_num": 7,
            "stars_num": 41341,
            "followers_num": 394,
            "fork_num": 32131,
            "topic": [100, 110, 120],
            "topic_talent": 330,
        },
    ]


def get_total_talent(nation):
    return [
        {
            "id": 1,
            "login_name": "test",
            "name": "zhang",
            "email": "xxxxx@xx.com",
            "bio": "I am a dog xxxx.",
            "company": "Google Inc",
            "nation": "China",
            "repos_num": 7,
            "stars_num": 41341,
            "followers_num": 394,
            "fork_num": 32131,
            "topic": [100, 110, 120],
            "topic_talent": 330,
        },
    ]


@app.route("/topic_rank")
def topic_rank():
    """
  1、搜索框，搜索topic跳转过来，2、所有topic页面的点击某个topic跳转过来
  :return:这个topic的开发者的榜单
  """
    topic = request.args.get("topic")  # topic名字
    nation = request.args.get("nation")  # 筛选项：国籍

    if topic:  # 如果指定了topic，就返回这个topic的榜单talent排序的，开发者信息榜单
        data = get_specific_topic_rank(topic,
                                       nation)  # login_name id email bio company nation repos_num stars_num followers_num followers_num fork_num topic have_topic_talent total_talent
    else:  # 如果没指定topic，就返回按开发者综合talent的排行版。
        data = get_total_talent(nation)
    ret = {}
    users_info = []
    ret["total_count"] = len(data)
    for user in data:
        if not user["name"]:
            user["name"] = user["login_name"]
        user["github_url"] = user_github_url_template.format(user["id"])
        user["image_url"] = user_image_url_template.format(user["login_name"])
        user.pop("login_name", None)
        user.pop("id", None)
        users_info.append(user)
    # login_name id email bio company nation repos_num stars_num followers_num followers_num fork_num topic talent
    ret["rank_list"] = users_info
    # 例如：
    return json.dumps(ret)


def get_all_curated_topic():
    return [
        {
            "tpoic_name": "abap2UI5",
            "topic_url": "https://github.com/topic/abap2UI5",
            "topic_img_url": "https://raw.githubusercontent.com/github/explore/54ab64c16bdf4604d4fbb36326be6909d8088dcb/topics/abap2ui5/abap2ui5.png",
            "descrip": "abap2UI5 is a framework for developing UI5 apps purely in ABAP — no need for JavaScript, OData, or RAP! It is designed for both cloud and on-premise environments, offering a lightweight and easy-to-install solution that works across all ABAP systems, from NetWeaver 7.02 to ABAP Cloud.",
            "repos_num": 26,
            "is_feature": 0
        },
    ]

@app.route("/random_topic")
def random_topic():
    """
  :return:随机返回几个topic
  """
    num = int(request.args.get("num"))  # 随机返回几个topic，得有介绍和url的。【从被人修改过的topic中随机选】
    curated_topics = get_all_curated_topic()
    topic_li = random.choices(curated_topics, k=num)
    ret = {}
    ret["total_count"] = len(topic_li)
    ret["topic_list"] = topic_li

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
                "is_feature": 1
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1
            }
        ]
    }
    return json.dumps(ret)


@app.route("/relate_topic")
def relate_topic():
    """
  :return:这个topic的，相似的几个topic
  """
    topic = request.args.get("topic")  # topic名字
    num = request.args.get("num")  # 返回推荐的前几个，例如返回6个

    # 读取，统计表单，excel表
    # 读取num个最相关的topic，组成list。例如用户查询C，返回【C++，C#，....】
    relate_list = ['C++', 'C#', ...]
    # 调用数据库接口，得到test最终数据

    # 操作数据库，单表
    # 例如：
    test = {
        "total_count": len(relate_list),
        "relate_topic_list": [
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1
            },
            {
                "tpoic_name": "python",
                "topic_url": "xxx",
                "topic_img_url": "",
                "descrip": "sasdfadfsa",
                "repos_num": 3411,
                "is_feature": 1
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

    # 操作数据库，多表

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
