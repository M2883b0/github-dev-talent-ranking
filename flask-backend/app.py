import json
import random
import string

from flask import Flask
from flask import request
from flask_redis import FlaskRedis

# from utility.DatabaseManagerBackend import DatabaseManager, TableName

app = Flask(__name__)
# 配置redis
app.config['REDIS_URL'] = "redis://localhost:6379/0"
# 初始化 Redis 客户端
redis_client = FlaskRedis(app)

user_image_url_template = "https://avatars.githubusercontent.com/u/{}?v=4"
user_github_url_template = "https://avatars.githubusercontent.com/u/{}?v=4"


def get_topic_list(topic="", is_feature=False,
                   is_curated=False):  #模糊查询所有的topic，返回以"xx"开头的所有topic，按照仓库数量从大到小排序；同时支持is_feature,is_curated筛选
    classify = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                'V', 'W', 'X', 'Y', 'Z', '2', "3", "0", "."]
    name_li = [random.choice(classify) + random.choice(classify) + random.choice(classify) for _ in range(2000)]
    ret = []
    for name in name_li:
        topic = {
            "topic_name": name,
            "topic_url": f"https://github.com/topic/{name}",
            "topic_img_url": "https://raw.githubusercontent.com/github/explore/54ab64c16bdf4604d4fbb36326be6909d8088dcb/topics/abap2ui5/abap2ui5.png",
            "descrip": "abap2UI5 is a framework for developing UI5 apps purely in ABAP — no need for JavaScript, OData, or RAP! It is designed for both cloud and on-premise environments, offering a lightweight and easy-to-install solution that works across all ABAP systems, from NetWeaver 7.02 to ABAP Cloud.",
            "repos_num": 26,
            "is_feature": 0
        }
        ret.append(topic)
    return ret

def get_specific_topic_rank(topic, nation):  #对有这个topic领域的用户，按照这个topic分，排序，

    return get_total_talent(nation)


def get_related_rank(name, is_follower=True, is_following=True, is_collaborator=True):  # 返回这个用户的所有【粉丝、合作者....】个人信息，按照total_talent综合分分排序。
    return get_total_talent(name)


def get_user_info(login_name):  #返回一个用户的详细信息

    return {
        "id": random.randint(1, 237892349823),
        "login_name": "".join(
            random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(random.randint(4, 8))),
        "name": "".join(
            random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(random.randint(4, 8))),
        "email": "xxxxx@xx.com",
        "bio": "I am a dog xxxx.",
        "company": "Google Inc",
        "organize": "dasdadea",
        "nation": "China",
        "repos_num": 7,
        "stars_num": 41341,
        "followers_num": 394,
        "fork_num": 32131,
        "have_topic": ["Linux", "C", "C++"],
        "have_topic_talent": [100, 110, 120],
        "total_talent": 330,
    }


def get_total_talent(nation):  #对所有用户，按照"topic_talent"综合能力，排序。

    return [
        {
            "id": random.randint(1, 23093209),
            "login_name": "".join(
                random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(random.randint(4, 8))),
            "name": "".join(
                random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(random.randint(4, 8))),
            "email": "xxxxx@xx.com",
            "bio": "I am a dog xxxx.",
            "company": "Google Inc",
            "nation": "China",
            "repos_num": random.randint(1, 34),
            "stars_num": random.randint(2342, 23093209),
            "followers_num": random.randint(432, 293209),
            "fork_num": random.randint(234, 23093209),
            "topic": "",
            "topic_talent": random.randint(1, 23093209),
        }

        for _ in range(100)
    ]





@app.route("/")
def hello():  # 主页
    # return render_template("index.html", name='123')
    return "server is ready"


@app.route("/get_topics_page")
def get_topics_page():
    """
    #所有的page页面：一次性返回26个：A【9个】，B【9个】
  :return:
  """
    if request.args.get("num"):
        num = int(request.args["num"])  # 建议9个,就是每个topic首字母，只返回9个
    else:
        num = 9

    # Redis 代码[KEY ,VALUE]
    # 定义一个key
    cache_key = f"get_topics_page:num={num}"
    # 尝试从 Redis 缓存中获取数据
    cached_data = redis_client.get(cache_key)
    # 如果拿得到数据，就直接return了
    if cached_data:
        return cached_data
    # 如果拿不到，就执行下面的访问mysql的语句

    # 操作数据库:多表【topic、topic_url表】
    classify = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                'V', 'W', 'X', 'Y', 'Z', 'others']
    all_topic_classify = {
        key: [] for key in classify
    }
    topic_li = get_topic_list('', False,False)  #不要精选，全部topic给我
    for topic in topic_li:
        first_letter = topic["topic_name"][0].upper()
        if first_letter in classify:
            all_topic_classify[first_letter].append(topic)
        else:
            all_topic_classify["others"].append(topic)
    assert isinstance(all_topic_classify, dict)
    all_topic_classify = {
        key: value[:num] for key, value in all_topic_classify.items()
    }
    ret = all_topic_classify
    ret["len"] = len(all_topic_classify)  #只要前9个

    # Redis 代码
    # 把自定义的key，和对应的值，存入redis里面
    redis_client.set(cache_key, json.dumps(ret), ex=600)  # 设置过期时间为10分钟

    return json.dumps(ret)


@app.route("/get_topic")
def get_topic():
    """
  1、模糊查询，所有topic的列表，A只展示9个，点击A的所有topic。就需要模糊查询所有以A开头的topic，按仓库数量从大到小排序。
  :return:
  """
    if request.args.get("topic"):
        topic = request.args.get("topic")  # topic名字，name
    else:
        topic = ""
    if request.args.get("is_feature"):
        is_feature = bool(request.args["is_feature"])
    else:
        is_feature = False

    topic_li = get_topic_list(topic, is_feature,False)
    ret = {"total_count": len(topic_li), "topic_list": topic_li}
    return json.dumps(ret)


@app.route("/topic_rank")
def topic_rank():
    """
  1、搜索框，搜索topic跳转过来，2、所有topic页面的点击某个topic跳转过来
  :return:这个topic的开发者的榜单
  """
    if request.args.get("topic"):
        topic = request.args.get("topic")  # topic名字，name
    else:
        topic = ''
    nation = request.args.get("nation", "%%")  # 筛选项：国籍

    # Redis 代码[KEY ,VALUE]
    # 定义把哪些数据放入redis，定义一个key
    redis_rank_name = ['', 'C', 'Python', 'Linux']  # 前端首页放固定的几个热门topic榜单。【""表示综合榜单】
    if topic in redis_rank_name:
        cache_key = f"topics_rank:topic={topic}"
        # 尝试从 Redis 缓存中获取数据
        cached_data = redis_client.get(cache_key)
        # 如果拿得到数据，就直接return了
        if cached_data:
            return cached_data
        # 如果拿不到，就执行下面的访问mysql的语句

    if topic:  # 如果指定了topic，就返回这个topic的榜单talent排序的，开发者信息榜单
        data = get_specific_topic_rank(topic,
                                       nation)  # login_name id email bio company nation repos_num stars_num followers_num followers_num fork_num topic have_topic_talent total_talent
    else:  # 如果没指定topic，就返回按开发者综合talent的榜单。
        data = get_total_talent(nation)
    ret = {}
    users_info = []
    ret["total_count"] = len(data)
    for user in data:
        user = generate_user_info(user)
        users_info.append(user)
    # login_name id email bio company nation repos_num stars_num followers_num followers_num fork_num topic talent
    ret["rank_list"] = users_info

    # Redis 代码
    # 把自定义的key，和对应的值，存入redis里面
    if topic in redis_rank_name:
        redis_client.set(cache_key, json.dumps(ret), ex=600)  # 设置过期时间为10分钟

    return json.dumps(ret)


@app.route("/random_topic")
def random_topic():
    """
  :return:随机返回几个topic
  """
    num = int(request.args.get("num", 5))  # 随机返回几个topic，得有介绍和url的。【从被人修改过的topic中随机选】

    curated_topics = get_topic_list("", is_curated=True)
    topic_li = random.choices(curated_topics, k=num)
    ret = {}
    ret["total_count"] = len(topic_li)
    ret["topic_list"] = topic_li

    # 例如：
    return json.dumps(ret)


def filter_topic(topic_li: list, letter):
    return [topic for topic in topic_li if topic["topic_name"].startswith(letter)]


@app.route("/relate_topic")
def relate_topic():
    """
  :return:这个topic的，相似的几个topic
  """
    topic = request.args.get("topic")  # topic名字
    if not topic:
        return {
            "code": 1,
            "msg": "please input topic name"
        }
    num = int(request.args.get("num", 6))  # 返回推荐的前几个，例如返回6个

    # TODO: 先找统计信息，找出最相关的num个。
    # 1、读取，统计表，【excel表,NxN】
    # 读取num个最相关的topic，组成list。例如用户查询C，返回【C++，C#，....】
    specific_relate_list = ['d', 'B', 'C', "a"]
    # 调用数据库接口
    li = []
    for tp in specific_relate_list:
        tmp = filter_topic(get_topic_list(tp, False,False), tp.upper())
        if tmp:
            li.append(tmp[0])
    ret = {"total_count": len(li), "relate_topic_list": li}
    # 操作数据库，单表
    return json.dumps(ret)


def generate_user_info(user):
    if not user["name"]:
        user["name"] = user["login_name"]
    user["github_url"] = user_github_url_template.format(user["id"])
    user["image_url"] = user_image_url_template.format(user["login_name"])
    user.pop("login_name", None)
    user.pop("id", None)
    return user


@app.route("/search_users")
def search_users():
    """
  :return:返回这个用户的页面信息【个人详细信息】
  """
    name = request.args.get("name")  # login名
    if not name:
        return {
            "code": 400,
            "msg": "please input name"
        }
    # TODO: 关系圈：3个勾选项，例如：只查看粉丝的榜单，不看其他关系的。
    # is_follower = request.args.get("is_follower")
    # is_following = request.args.get("is_following")
    # is_collaborator = request.args.get("is_collaborator")

    # 操作数据库，多表
    # 查user表，得到这个用户的详细信息
    user = get_user_info(name)

    # TODO: 先调用数据库，如果没有这个人，就调用爬虫接口现场爬。

    # 处理这个用户的信息
    user = generate_user_info(user)

    # 关系榜单
    li = get_related_rank(name, True, True, True)
    related_user_list = []
    for ur in li:
        # 处理【粉丝、合作者的信息】
        ur = generate_user_info(ur)
        related_user_list.append(ur)

    user["relate_rank_list"] = {
        "total_count": len(related_user_list),
        "rank_list": related_user_list
    }

    return json.dumps(user)


if __name__ == "__main__":
    # database_manager = DatabaseManager()
    # database_manager.query_with_filters()
    app.run(host="0.0.0.0", port=80, debug=True, threaded=True)
