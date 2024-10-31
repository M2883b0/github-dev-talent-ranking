import json

from flask import request
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():   #主页
    return "Hello World!111"

@app.route("/get_topics")
def get_topics():
  """
  列出所有的topic列表详细信息，获得一个topic的详细
  :return:
  """
  order = request.args.get("order")  #按某种的排序方式【正序和逆序,不填的话，默认是正序】
  is_feature = request.args.get("is_feature")  #筛选项：可以只返回精选的topic，默认开启。为False，就是都返回
  repos_count = request.args.get("repos_count")  #筛选仓库数大于xxx数的topic，默认为0（例如只看仓库数大于500的topic列表）
  name = request.args.get("name")         # 指定topic_name,就只返回一个topic详细信息

  # ===操作数据库，拿数据

  # ===

  # 例如得到：
  test={
  "total_count": 1600,
  "topic_list": [
    {
      "tpoic_nam": "python",
      "topic_url": "xxx",
      "topic_img_url": "",
      "descrip": "sasdfadfsa",
      "repos_num": "3411"
    },
    {
      "tpoic_nam": "python",
      "topic_url": "xxx",
      "topic_img_url": "",
      "descrip": "sasdfadfsa",
      "repos_num": "3411"
    },
    {
      "tpoic_nam": "python",
      "topic_url": "xxx",
      "topic_img_url": "",
      "descrip": "sasdfadfsa",
      "repos_num": "3411"
    },
    {
      "tpoic_nam": "python",
      "topic_url": "xxx",
      "topic_img_url": "",
      "descrip": "sasdfadfsa",
      "repos_num": "3411"
    },
    {
      "tpoic_nam": "python",
      "topic_url": "xxx",
      "topic_img_url": "",
      "descrip": "sasdfadfsa",
      "repos_num": "3411"
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
  topic = request.args.get("topic")  #topic名字
  nation = request.args.get("nation")  #筛选项：国籍
  page = request.args.get("page")   #分页
  limit = request.args.get("limit")  #每页的限制


  #操作数据库拿到数据
  #例如：
  test={
    "topic": "Linux",
    "total_count": 45,
    "size": 5,
    "total_pages": 9,
    "current_page": 1,
    "rank_list": [
        {
            "name": "xiaomiu",
            "image_url": "xxx/png",
            "forks_num": 10,
            "stars_num": 10,
            "repos_num": 10,
            "talent": 2000
        },
        {
            "name": "xiaomiu",
            "image_url": "xxx/png",
            "forks_num": 10,
            "stars_num": 10,
            "repos_num": 10,
            "talent": 2000
        },
        {
            "name": "xiaomiu",
            "image_url": "xxx/png",
            "forks_num": 10,
            "stars_num": 10,
            "repos_num": 10,
            "talent": 2000
        },
        {
            "name": "xiaomiu",
            "image_url": "xxx/png",
            "forks_num": 10,
            "stars_num": 10,
            "repos_num": 10,
            "talent": 2000
        },
        {
            "name": "xiaomiu",
            "image_url": "xxx/png",
            "forks_num": 10,
            "stars_num": 10,
            "repos_num": 10,
            "talent": 2000
        }
    ]
}
  return json.dumps(test)


@app.route("/relate_topic")
def relate_topic():
  """
  :return:这个topic的，相似的几个topic
  """
  topic = request.args.get("topic")  #topic名字


  #操作数据库，还是哪里。拿到这个统计的数据
  #例如：
  test={
    "total_count": 6,
    "relate_topic_list": [
        {
            "tpoic_nam": "python",
            "topic_url": "xxx",
            "topic_img_url": "",
            "descrip": "sasdfadfsa",
            "repos_num": "3411"
        },
        {
            "tpoic_nam": "python",
            "topic_url": "xxx",
            "topic_img_url": "",
            "descrip": "sasdfadfsa",
            "repos_num": "3411"
        },
        {
            "tpoic_nam": "python",
            "topic_url": "xxx",
            "topic_img_url": "",
            "descrip": "sasdfadfsa",
            "repos_num": "3411"
        },
        {
            "tpoic_nam": "python",
            "topic_url": "xxx",
            "topic_img_url": "",
            "descrip": "sasdfadfsa",
            "repos_num": "3411"
        },
        {
            "tpoic_nam": "python",
            "topic_url": "xxx",
            "topic_img_url": "",
            "descrip": "sasdfadfsa",
            "repos_num": "3411"
        },
        {
            "tpoic_nam": "python",
            "topic_url": "xxx",
            "topic_img_url": "",
            "descrip": "sasdfadfsa",
            "repos_num": "3411"
        }
    ]
}
  return json.dumps(test)




@app.route("/search_users")
def relate_topic():
  """
  :return:返回这个用户的页面信息【个人详细信息、】
  """
  login_name = request.args.get("name")    # login名
  page = request.args.get("page")    # 分页
  limit = request.args.get("limit")  # 每页的限制


  #操作数据库，还是哪里。拿到这个统计的数据
  #例如：
  test={
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
                }
            ]
        }
    ]
}
  return json.dumps(test)





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5780, debug=True)