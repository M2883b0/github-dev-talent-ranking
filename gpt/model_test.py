import os
from openai import OpenAI
import re
import ast
import json
import requests
from twisted.web.html import output
from config import QWEN_API_KEY, QWEN_MODEL, TOPIC_THRESHOLDS
import logging
import os
import asyncio
from openai import AsyncOpenAI
import platform



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
# description = 'huggingface\Transformers: State-of-the-art Machine Learning for Pytorch, TensorFlow, and JAX.'
description = 'Linux kernel source tree'
# description = 'Visual Instruction Tuning (LLaVA) built towards GPT-4V level capabilities and beyond.'



# 创建异步客户端实例
client = AsyncOpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=QWEN_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 定义异步任务列表
async def task(question):
    print(f"Sending question: {question}")
    response = await client.chat.completions.create(
        messages=[
            {"role": "user", "content": question}
        ],
        model="qwen-plus",
    )
    print(f"Received answer: {response.choices[0].message.content}")

# 主异步函数
async def main():
    questions = ["你是谁？", "你会什么？", "天气怎么样？"]
    tasks = [task(q) for q in questions]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    # 设置事件循环策略
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # 运行主协程
    asyncio.run(main(), debug=False)
