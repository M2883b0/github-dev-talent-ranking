# pip install --upgrade spark_ai_python
import ast

from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
import re
import json
import requests
from config import SPARKAI_URL, SPARKAI_APP_ID, SPARKAI_API_SECRET, SPARKAI_API_KEY, SPARKAI_DOMAIN, \
    SPARKAI_Authorization, SPARKAI_HTTP_URL, TOPIC_THRESHOLDS
import logging
from tqdm import tqdm
from utility.DatabaseManagerBackend import DatabaseManager

# seen = set()
# all_topic_lists = []
# with open("../topicList.txt", "r") as f:
#     for line in f.read().strip().split("\n"):
#         if line not in seen:
#             seen.add(line)
#             all_topic_lists.append(line)
# # print(all_topic_lists)
# # print(len(all_topic_lists))
#
#
# with open("../feature_topicList.txt", "r") as f:
#     t = f.read().strip().split("\n")
# feature_topic_lists = list(t)
# # print(feature_topic_lists)
# # print(len(feature_topic_lists))
#
# # 项目的描述，从数据库里拿（对所有没有topic的项目，都需要爬取）
# # description = 'huggingface\Transformers: State-of-the-art Machine Learning for Pytorch, TensorFlow, and JAX.'
# description = 'Linux kernel source tree'
# # description = 'Visual Instruction Tuning (LLaVA) built towards GPT-4V level capabilities and beyond.'

def output_to_topic(output, topic_list):
    """

    :param output:大模型的输出文本
    :param topic_list:
    :return:
    """
    # 通过正则匹配，提取大模型输出文本的feature tpoic
    pattern = r'\b(' + '|'.join(re.escape(tech) for tech in topic_list) + r')\b'
    # 查找大模型输出文本中，提到的技术
    matches = re.findall(pattern, output, flags=re.IGNORECASE)
    # 去重并排序
    unique_matches = []
    seen = set()
    for match in matches:
        match_lower = match.lower()
        if match_lower not in seen:
            seen.add(match_lower)
            unique_matches.append(match)
    return unique_matches


def websocket_no_stream(topic_list, project_description, all_topic_list):
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
            content='技术名称列表:{}。项目文本描述:"{}"。请你根据项目文本描述，从技术列表中列出10个最相关的技术。用列表格式输出：'.format(topic_list, project_description)
        )
    ]
    handler = ChunkPrintHandler()
    a = spark.generate([messages], callbacks=[handler])
    output = a.generations[0][0].text
    # print(output)
    predict_topic = output_to_topic(output, all_topic_list)
    threshold = TOPIC_THRESHOLDS  # 设置给项目最多打4个标签
    if len(predict_topic) > threshold:
        return predict_topic[:threshold]  # 给项目上topic，保守一点，最多预测threshold个topic
    else:
        return predict_topic


def http_no_stream(topic_list, project_description, all_topic_list):
    try:
        url = SPARKAI_HTTP_URL
        data = {
            "max_tokens": 512,
            "top_p": 0.8,
            "top_k": 2,
            "temperature": 0.3,
            "presence_penalty": 2,
            "messages": [
                {
                    "role": "system",
                    "content": "你现在是一名计算机领域的技术顾问，能够准确且简洁的回答用户的问题。"
                },
                {
                    "role": "user",
                    "content": "技术名称列表:{}。项目文本描述:{}。请你根据项目描述，参考技术列表和计算机学术领域的研究方向，输出一些与项目最相关的技术名称和计算机领域名称(技术名词使用英文表示)。使用list格式输出结果,例如['C','python'],只需返回一个列表：".format(topic_list, project_description)
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

        if 'code' in output_json and output_json['code'] != 0:      #错误
            code = output_json['code']
            logging.error(f'请求错误: {code},{output_json}')
            return []                              # 大模型非正常输出，返回空     #====
        elif 'code' in output_json and output_json['code'] == 0:
            output = output_json['choices'][0]['message']['content']
            print(output)
            output = ast.literal_eval(output)  # 输出转为list
            predict_topic = [element for element in output if element in all_topic_list]
            # predict_topic = output_to_topic(output, all_topic_list)  # 提取大模型的回答内容，提取出符合feature topic list
            threshold = TOPIC_THRESHOLDS  # 设置给项目最多打4个标签
            if len(predict_topic) > threshold:
                return predict_topic[:threshold]  # 给项目上topic，保守一点，最多预测threshold个topic
            else:
                return predict_topic
        elif 'error' in output_json:
            logging.error(output_json)
            return []
    except Exception as e:
        logging.error(f"错误信息：{e}")
        return ""



if __name__ == '__main__':
    """
    
    传入3个参数：feature_topic_lists(200那个), description, all_topic_lists（2000那个）
    """
    # # Websocket的方式
    # predict_topics = websocket_no_stream(feature_topic_lists, description, all_topic_lists)

    # # http的方式
    db_manager = DatabaseManager()
    feature_topic_lists, description_list, all_topic_lists = db_manager.get_qwen_topic_relevant_info()
    total_records = len(description_list)
    data = []
    count = 0
    for description in tqdm(description_list, total=total_records):
        rid = description["id"]
        print(rid)
        predict_topics = http_no_stream(feature_topic_lists, description["descript"], all_topic_lists)
        count = count + 1
        if predict_topics and len(predict_topics) != 0:
            for topic in predict_topics:
                temp_dict = {
                    "rid": rid,
                    "topics": topic
                }
                data.append(temp_dict)
        if count % 10 == 0 or count == total_records:
            print('插入数据')
            print(data)
            db_manager.insert_topic(data)
            data = []

    # 输出结果
    print(predict_topics)


    # predict_topics = http_no_stream(feature_topic_lists, description, all_topic_lists)


    # 输出结果
    print(predict_topics)
