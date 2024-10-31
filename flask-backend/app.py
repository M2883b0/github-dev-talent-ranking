import json

from flask import request
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():   #主页
    return "Hello World!111"

@app.route("/all_topics")
def all_topics():
  """
  PPT3,所有topic页面:返回所有的topic，列出来，让用户去选
  怎么列出来，按什么规律列，按首字母排？
  :return:
  """
  order = request.args.get("order")  #按某种的排序方式【正序和逆序,不填的话，默认是正序】
  is_feature = request.args.get("is_feature")  #筛选项：可以只返回精选的topic，默认开启
  repos_count = request.args.get("repos_count")  #筛选仓库数大于xxx数的topic，默认为0（例如只看仓库数大于500的topic列表）

  # ===操作数据库拿到数据

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


@app.route("/search_topic")
def all_topics():
  """
  #返回所有的topic，列出来，让用户去选
  怎么列出来，按首字母排？
  :return:
  """
  order = request.args.get("order")  #按某种的排序方式【正序和逆序,不填的话，默认是正序】
  is_feature = request.args.get("is_feature")  #筛选项：可以只返回精选的topic，默认开启
  repos_count = request.args.get("repos_count")  #筛选仓库数大于xxx数的topic，默认为0（例如只看仓库数大于500的topic列表）


  #操作数据库拿到数据
  #例如：
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



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5780, debug=True)