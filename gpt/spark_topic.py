# pip install --upgrade spark_ai_python

from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
import re

#星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看

# Spark4.0 Ultra 请求地址，对应的domain参数为4.0Ultra：
# wss://spark-api.xf-yun.com/v4.0/chat

# Spark Max-32K请求地址，对应的domain参数为max-32k
# wss://spark-api.xf-yun.com/chat/max-32k

# Spark Max请求地址，对应的domain参数为generalv3.5
# wss://spark-api.xf-yun.com/v3.5/chat

# Spark Pro-128K请求地址，对应的domain参数为pro-128k：
#  wss://spark-api.xf-yun.com/chat/pro-128k

# Spark Pro请求地址，对应的domain参数为generalv3：
# wss://spark-api.xf-yun.com/v3.1/chat

# Spark Lite请求地址，对应的domain参数为lite：（免费）
# wss://spark-api.xf-yun.com/v1.1/chat


# 账户api key
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v1.1/chat'
#星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
SPARKAI_APP_ID = '97c319c8'
SPARKAI_API_SECRET = 'MmM4MWQyNmE4Yjc5OTQ3N2Y1YjgyN2Mx'
SPARKAI_API_KEY = 'cd82673c0fa28173962de388b84146c9'
#星火认知大模型Spark Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = 'lite'

#从数据库拿

topic_list = []
with open("../topicList.txt", "r") as f:
    t = f.read().strip().split("\n")
topic_list = list(t)
print(topic_list)
project_description = 'huggingface\Transformers: State-of-the-art Machine Learning for Pytorch, TensorFlow, and JAX.'


def output_to_topic(output):
    """

    :param output:
    :return:
    """
    pattern = r'\b(' + '|'.join(re.escape(tech) for tech in topic_list) + r')\b'
    # 查找文本中提到的技术
    matches = re.findall(pattern, output, flags=re.IGNORECASE)
    # 去重并排序
    unique_matches = []
    seen = set()

    for match in matches:
        match_lower = match.lower()
        if match_lower not in seen:
            seen.add(match_lower)
            unique_matches.append(match)
    print(unique_matches)




def test_non_stream():
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
            content='你现在是一名计算机领域的技术顾问，能够准确且简洁的回答用户的问题。请你根据项目文本描述，从技术列表中选出5个最相关的技术元素。'
        ),
        ChatMessage(
            role="user",
            content='技术名称列表:{}。项目文本描述:"{}"。用列表格式输出：'.format(topic_list, project_description)
        )
    ]
    handler = ChunkPrintHandler()
    a = spark.generate([messages], callbacks=[handler])
    output = a.generations[0][0].text
    print(output)
    output_to_topic(output)


# def test_stream():
#     """
#     还没修好
#     :return:
#     """
#     from sparkai.core.callbacks import StdOutCallbackHandler
#     spark = ChatSparkLLM(
#         spark_api_url=SPARKAI_URL,
#         spark_app_id=SPARKAI_APP_ID,
#         spark_api_key=SPARKAI_API_KEY,
#         spark_api_secret=SPARKAI_API_SECRET,
#         spark_llm_domain=SPARKAI_DOMAIN,
#         request_timeout=30, #
#         streaming=True,
#
#     )
#     messages = [ChatMessage(
#         role="user",
#         content='编写一个贪吃蛇游戏的开发流程',
#         )]
#     handler = ChunkPrintHandler()
#     a = spark.generate([messages], callbacks=[handler])
#     print(a)



if __name__ == '__main__':
    test_non_stream()