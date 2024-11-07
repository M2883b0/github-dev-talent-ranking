# pip install --upgrade spark_ai_python

from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
import re
import json
import requests
from config import SPARKAI_URL, SPARKAI_APP_ID, SPARKAI_API_SECRET, SPARKAI_API_KEY, SPARKAI_DOMAIN, \
    SPARKAI_Authorization, SPARKAI_HTTP_URL, TOPIC_THRESHOLDS
import logging
from tqdm import tqdm
from bs4 import BeautifulSoup

from utility.DatabaseManagerBackend import DatabaseManager


def websocket_no_stream(bio, blog_html):
    """

    :return:
    """
    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )
    messages = [
        ChatMessage(
            role="system",
            content='你现在是一名计算机领域的技术顾问，能够准确且简洁的回答用户的问题。'
        ),
        ChatMessage(
            role="user",
            content='用户简介:{}。用户博客网页爬取的内容:{}。请你根据上述信息，给这个用户的开发能力打分，满分5分。不要看html内容的长度，要根据内容的技术程度。如果是全是生活博客，开发者能力分数就很低，如果是是技术分享博客，则根据内容的图文丰富性和技术研究的深入程度，进行评分。结果用数字输出，例如输出:2分。'.format(
                bio, blog_html)
        )
    ]
    handler = ChunkPrintHandler()
    a = spark.generate([messages], callbacks=[handler])
    output = a.generations[0][0].text
    number = re.findall(r'\d+', output)
    if number:
        blog_score = int(number[0])
    else:
        blog_score = 0
    return blog_score






def http_no_stream(blog_html):
    url = SPARKAI_HTTP_URL
    data = {
        "max_tokens": 30,
        "top_p": 0.8,
        "top_k": 1,
        "temperature": 0.5,
        "presence_penalty": 1,
        "messages": [
            {
                "role": "system",
                "content": "你现在是一名计算机领域的技术顾问，能够准确且简洁的回答用户的问题。"
            },
            {
                "role": "user",
                "content": "用户博客网页爬取的内容:{}。请你根据上述信息，给这个用户的开发能力打分，满分5分，最低0分。根据内容的技术程度。如果是生活记录博客，开发者能力分数就很低，如果是是技术分享博客，则根据内容的图文丰富性和技术研究的深入程度，进行评分。结果用数字输出，例如输出:2分。然后给出理由，为什么得到这个分数，是由哪些信息相加得到的".format(
                    blog_html)
            }
        ],
        "model": "lite"
    }
    data["stream"] = False
    # 我的鉴权信息
    header = {
        "Authorization": SPARKAI_Authorization
    }
    response = requests.post(url, headers=header, json=data)

    # 大模型流式响应解析示例，data["stream"] = True
    # response.encoding = "utf-8"
    # for line in response.iter_lines(decode_unicode="utf-8"):
    #     print(line)

    # 非流式:大模型生成完，再一次性返回
    output_json = json.loads(response.text)

    if 'code' in output_json and output_json['code'] != 0:  # 错误
        code = output_json['code']
        logging.error(f'请求错误: {code},{output_json}')
        return ""  # 大模型非正常输出，返回空     #====
    elif 'code' in output_json and output_json['code'] == 0:  # 正确
        output = output_json['choices'][0]['message']['content']
        print(output)
        number = re.findall(r'\d+', output)
        if number:
            blog_score = int(number[0])
        else:
            blog_score = 0
        return blog_score

    elif 'error' in output_json:
        logging.error(output_json)
        return []


if __name__ == '__main__':


    # # Websocket的方式
    # predict_topics = websocket_no_stream(feature_topic_lists, description, all_topic_lists)

    db_manager = DatabaseManager()
    results = db_manager.get_spark_blog_relevant_info()
    total_records = len(results)
    print(total_records)
    data=[]
    count=0
    for q in tqdm(results, total=total_records):
        uid = q["uid"]
        blog_html = q["blog_html"]
        # 清空html格式
        soup = BeautifulSoup(blog_html, 'html.parser')
        blog_html = soup.get_text(separator=' ', strip=True)
        count = count + 1
        if len(blog_html) > 20000:
            blog_html = blog_html[:20000]
        # # http的方式
        predict_score = http_no_stream(blog_html)
        temp_dict = {
            "uid":uid,
            "blog_score":predict_score
        }
        data.append(temp_dict)
        if count%10 ==0 or count == total_records:
            print("插入数据")
            print(data)
            db_manager.insert_blog_score(data)
            data=[]

        # 输出结果
        print(predict_score)
