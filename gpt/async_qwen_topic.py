import os
from openai import OpenAI
import re
import ast
import json
import requests
from config import QWEN_API_KEY, QWEN_TOPIC_MODEL, TOPIC_THRESHOLDS
import logging
import os
import asyncio
from openai import AsyncOpenAI
import platform
from utility.DatabaseManagerBackend import DatabaseManager



seen = set()
all_topic_lists = []
with open("../topicList.txt", "r") as f:
    for line in f.read().strip().split("\n"):
        if line not in seen:
            seen.add(line)
            all_topic_lists.append(line)
# print(all_topic_lists)
# print(len(all_topic_lists))


with open("../feature_topicList.txt", "r") as f:
    t = f.read().strip().split("\n")
feature_topic_lists = list(t)
# print(feature_topic_lists)
# print(len(feature_topic_lists))

# 项目的描述，从数据库里拿（对所有没有topic的项目，都需要爬取）
description1 = 'huggingface\Transformers: State-of-the-art Machine Learning for Pytorch, TensorFlow, and JAX.'
description2 = 'Linux kernel source tree'
description3 = 'Visual Instruction Tuning (LLaVA) built towards GPT-4V level capabilities and beyond.'


# 创建异步客户端实例
client = AsyncOpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=QWEN_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 异步的具体任务
async def task(topic_list, project_description, all_topic_list):
    response = await client.chat.completions.create(
        model=QWEN_TOPIC_MODEL,
        messages=[
            {
                'role': 'system',
                'content': '你是一位计算机领域的技术顾问和大学教授，能够准确且简洁的回答用户的问题.'
            },
            {
                'role': 'user',
                'content': "技术列表:{}。项目描述:{}。请你根据项目描述，参考技术列表和计算机学术领域的研究方向，输出一些与项目最相关的技术名称和计算机领域名称。用英文回答，使用list格式输出结果：".format(
                    topic_list, project_description)
            }
        ],
        stream=False,
        temperature=0.6,
        top_p=0.8,
        max_tokens=512,
        presence_penalty=1,
        extra_body={
            "enable_search": False  # topic不需要联网
        }
    )
    output = response.choices[0].message.content
    # print(output)
    output_list = ast.literal_eval(output)  # 输出转为list
    predict_topic = [element for element in output_list if element in all_topic_list]
    threshold = TOPIC_THRESHOLDS  # 设置给项目最多打max个标签
    if len(predict_topic) > threshold:
        predict_topic = predict_topic[:threshold]  # 给项目上topic，保守一点，最多预测threshold个topic
    # print(predict_topic)
    return predict_topic


# 主异步函数
async def main():
    """
    异步预测项目的topic
    传入3个参数：feature_topic_lists(200那个), description, all_topic_lists（2000那个）
    """
    db_manager = DatabaseManager()

    question = [description1, description2, description3]
    tasks = [task(feature_topic_lists, q, all_topic_lists) for q in question]
    await asyncio.gather(*tasks)



if __name__ == '__main__':
    """
    异步预测项目的topic
    传入3个参数：feature_topic_lists(200那个), description, all_topic_lists（2000那个）
    """
    # 设置事件循环策略
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # 运行主协程
    asyncio.run(main())
