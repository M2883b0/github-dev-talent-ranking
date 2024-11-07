import json
import pandas as pd
import random
import pickle
import string

from flask import Flask,send_from_directory
from flask import request,render_template
from flask_redis import FlaskRedis
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


from utility.DatabaseManagerBackend import DatabaseManager

# app = Flask(__name__, static_folder='/static/dist', static_url_path='/')
app = Flask(__name__)
# 配置redis的信息
app.config['REDIS_URL'] = "redis://localhost:6379/0"
# 初始化 Redis 客户端
redis_client = FlaskRedis(app)
# redis中数据的保留时间(秒)
redis_time = 60   # 20分钟

user_image_url_template = "https://avatars.githubusercontent.com/u/{}?v=4"
user_github_url_template = "https://avatars.githubusercontent.com/u/{}?v=4"


@app.route("/")
def hello():  # 主页
    return render_template("index.html")
    # return "hello lyx"
    # return send_from_directory(app.static_folder, 'index.html')


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
    topic_li = database_manager.get_topic_list('')  #全部topic给我
    print(len(topic_li))
    for topic in topic_li:
        first_letter = topic["name"][0].upper()
        if first_letter in classify:
            all_topic_classify[first_letter].append(topic)
        else:
            all_topic_classify["others"].append(topic)
    assert isinstance(all_topic_classify, dict)
    all_topic_classify = {
        key: value[:num] for key, value in all_topic_classify.items()
    }
    ret = all_topic_classify
    # ret["len"] = len(all_topic_classify)  #只要前num个

    # Redis 代码
    # 把自定义的key，和对应的值，存入redis里面
    redis_client.set(cache_key, json.dumps(ret), ex=redis_time)  # 设置过期时间为1分钟

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
    if topic == 'C  ':
        topic = 'C++'
    if request.args.get("is_feature"):
        is_feature = (True if request.args.get("is_feature").lower() == 'true' else False)
    else:
        is_feature = False
    data_temp=database_manager.get_topic_list(topic, is_feature, False)
    if data_temp is None or len(data_temp)==0:
        return {
                    "code": 1,
                    "msg": "name no in topic list"
                }
    if len(topic)==1:  #字母
        topic_li = filter_first_topic(data_temp, topic)
        ret = {"total_count": len(topic_li), "topic_list": topic_li, "is_letter":True}
    else:
        topic_li = filter_topic(data_temp, topic)
        ret = {"total_count": len(topic_li), "topic_list": topic_li, "is_letter":False}
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
    nation = request.args.get("nation", "")  # 筛选项：国籍
    if nation == "\"\"" or nation == "''":
        nation = ""

    if topic == 'C  ':
        topic = 'C++'

    print(topic)
    print(nation)
    # Redis 代码[KEY ,VALUE]
    # 定义把哪些数据放入redis，定义一个key
    redis_rank_name = ['', 'C', 'Python', 'C++']  # 前端首页放固定的几个热门topic榜单。【''表示综合榜单】
    cache_key = f"topics_rank:topic={topic}:nation={nation}"
    if topic in redis_rank_name and nation == "":
        # 尝试从 Redis 缓存中获取数据
        cached_data = redis_client.get(cache_key)
        # 如果拿得到数据，就直接return了
        if cached_data:
            return cached_data
        # 如果拿不到，就执行下面的访问mysql的语句

    if topic:  # 如果指定了topic，就返回这个topic的榜单talent排序的，开发者信息榜单
        data = database_manager.get_specific_topic_rank(topic, nation)
    else:  # 如果没指定topic，就返回按开发者综合talent的榜单。
        data = database_manager.get_total_talent(nation)
    if data is None or len(data)==0:
        return {
            "code": 1,
            "msg": "no people"
        }
    if len(data) > 100:     # 只返回top100榜单
        data = data[:100]
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
    if topic in redis_rank_name and nation == "":
        redis_client.set(cache_key, json.dumps(ret), ex=redis_time)  # 设置过期时间为1分钟

    return json.dumps(ret)


@app.route("/random_topic")
def random_topic():
    """
  :return:随机返回几个topic
  """
    num = int(request.args.get("num", 5))  # 随机返回几个topic，得有介绍和url的。【从被人修改过的topic中随机选】

    curated_topics = database_manager.get_topic_list("", is_curated=True)
    topic_li = random.choices(curated_topics, k=num)
    ret = {}
    ret["total_count"] = len(topic_li)
    ret["topic_list"] = topic_li

    # 例如：
    return json.dumps(ret)


def filter_first_topic(topic_li: list, letter):
    return [topic for topic in topic_li if topic["name"].startswith(letter.upper()) or topic["name"].startswith(letter.lower())]

def filter_topic(topic_li: list, letter):
    return [topic for topic in topic_li if topic["name"].lower() == letter.lower()]

def load_excel(file_path):
    df = pd.read_excel(file_path, index_col=0)
    return df

# 查找与指定属性最相关的属性
def find_most_related_attributes(df, target_attribute, num=5):
    if target_attribute not in df.index:
        return []

    target_row = df.loc[target_attribute]
    related_attributes = []

    for attr, prob in target_row.items():
        if prob > 0 and attr != target_attribute:
            related_attributes.append((attr, prob))

    # 按概率从大到小排序
    related_attributes.sort(key=lambda x: x[1], reverse=True)

    # 返回前num个属性
    if len(related_attributes) >= num:
        return related_attributes[:num]
    else:
        # 如果不足num个，随机找其他的属性凑够num个
        remaining_attributes = [attr for attr in df.index if
                                attr != target_attribute and attr not in [a[0] for a in related_attributes]]
        random.shuffle(remaining_attributes)
        additional_attributes = remaining_attributes[:num - len(related_attributes)]
        for attr in additional_attributes:
            related_attributes.append((attr, 0.0))

        return related_attributes

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

    file_name = './flask-backend/correlation_matrix.xlsx'

    # Redis,定义一个key
    cache_key = "correlation_matrix.xlsx"
    # 尝试从 Redis 缓存中拿数据
    cached_data = redis_client.get(cache_key)
    if cached_data:
        df = pickle.loads(cached_data)
    else:  # 现场加载数据
        df = load_excel(file_name)
        # 使用 pickle 序列化 DataFrame
        pickled_df = pickle.dumps(df)
        # 再写入 redis
        redis_client.set(cache_key, pickled_df, ex=redis_time*2)  # 设置过期时间

    if topic == 'C  ':
        topic = 'C++'
    related_attributes = find_most_related_attributes(df, topic, num*10)
    if related_attributes and len(related_attributes)!=0:
        specific_relate_list = [attr for attr, prob in related_attributes]
    else:
        return random_topic()

    # 调用数据库接口
    li = []
    for tp in specific_relate_list:
        relate_data_list = database_manager.get_topic_list(tp, False,False)
        if relate_data_list and len(relate_data_list)!=0:
            tmp = filter_topic(relate_data_list, tp)
            if tmp:
                li.append(tmp[0])
    if len(li)>num:
        li=li[:num]
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
            "code": 1,
            "msg": "please input name"
        }
    # TODO: 关系圈：3个勾选项，例如：只查看粉丝的榜单，不看其他关系的。
    is_follower = request.args.get("is_follower", True)
    is_following = request.args.get("is_following", True)
    is_collaborator = request.args.get("is_collaborator", True)

    # # 将字符串转换为布尔值
    # if is_follower is None:
    #     return False
    # elif is_follower.lower() == 'true':
    #     is_follower = True
    # elif is_follower.lower() == 'false':
    #     is_follower = False
    # else:


    # 操作数据库，多表
    # 查user表，得到这个用户的详细信息
    user = database_manager.get_user_info(name)

    # TODO: 先调用数据库，如果没有这个人，就调用爬虫接口现场爬。

    if user is None:
        return {
            "code": 1,
            "msg": "user does not exist"
        }


    # 处理这个用户的信息
    user = generate_user_info(user[0])

    # 关系榜单
    li = database_manager.get_related_rank(name, is_follower, is_following, is_collaborator)
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
    database_manager = DatabaseManager()
    app.run(host="0.0.0.0", port=80)
    # app.run(host="0.0.0.0", port=10072)
