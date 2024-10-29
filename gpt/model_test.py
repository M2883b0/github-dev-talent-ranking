from config import QWEN_API_KEY, QWEN_MODEL, TOPIC_THRESHOLDS
import asyncio
from openai import AsyncOpenAI
import platform



blog="I am a Senior Applied Scientist in Amazon AGI. I closely collaborate with AWS AI Labs. Before this, I was an applied scientist in Amazon Halo where I worked on problems at the intersection of Computer Vision and Health. Prior to Amazon, I was a Principal Computer Vision Researcher at Magic Leap. I finished my Ph.D. from the School of Interactive Computing at Georgia Institute of Technology. I was advised by Professor Henrik I. Christensen and Professor Frank Dellaert. I completed my Bachelors and Masters in Computer Science from IIIT Hyderabad where I was advised by Prof. P J Narayanan."


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



client = AsyncOpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=QWEN_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
async def main(log_name,name=None,bio=None,location=None,email=None,company=None,oraganization_name=None,oraganization_loaction=None,blog_html=None,followers_list=None,following_list=None):
    """

    :param log_name:  登录名（必填）
    :param name:  用户名（可选）
    :param bio:  简介（可选）
    :param location:  定位（可选）
    :param email:  邮箱（可选）
    :param company:  公司（可选）
    :param oraganization_name:  组织名（可选）
    :param oraganization_loaction:  组织地址（可选）
    :param blog_html:  博客链接的内容（可选）
    :param followers_list:  粉丝的位置列表（可选）
    :param following_list:  关注的位置列表（可选）
    :return:
    """
    person_info = "用户名：'{}'".format(log_name)
    if name:
        person_info = person_info + "，姓名：'{}'".format(name)
    if bio:
        person_info = person_info + "，简介：'{}'".format(bio)
    if location:
        person_info = person_info + "，ip位置：'{}'".format(location)
    if email:
        person_info = person_info + "，邮箱：'{}'".format(email)
    if company:
        person_info = person_info + "，工作的公司：'{}'".format(company)
    if oraganization_name:
        person_info = person_info + "，加入的组织：'{}'".format(oraganization_name)
    if oraganization_loaction:
        person_info = person_info + "，组织的位置：'{}'".format(oraganization_loaction)
    if blog_html:
        person_info = person_info + "，个人博客信息：'{}'".format(blog_html)
    if followers_list:
        person_info = person_info + "，粉丝的ip位置分布列表：'{}'".format(followers_list)
    if following_list:
        person_info = person_info + "，关注的ip位置分布列表：'{}'".format(following_list)



    response = await client.chat.completions.create(
        model=QWEN_MODEL,
        messages=[
            {
                'role': 'system',
                # 'content': '你是一位有帮助的助手，能够准确且简洁的回答用户的问题。'
                'content': '你是一位有帮助的助手，你的任务是根据这个用户的某个社交网址主页的信息，推测这个用户的国籍，并给出推测的概率。'
            },
            {
                'role': 'user',
                # 'content': "这个一个人的博客主页内容：'{}'。\n利用这个人的基本信息和社交关系网络,共同的所提供的线索，猜测这个人最可能的原始国籍是什么(国籍使用英语表示)，并且同时给出猜测的概率值。使用list列表输出结果：".format(blog)
                # 'content': "GitHub账户名字是“torvalds”，用户名是“Linus Torvalds”，目前在Linux Foundation公司上班，GitHub显示目前的定位是在：“Portland, OR”，同时也是位于Spain的DROPCitizenShip组织的一员。\n利用这个人的基本信息和社交关系网络,共同的提供的线索，猜测这个人的国籍是什么(国籍使用英语表示)，并且同时给出猜测的概率值。\n使用list列表返回结果："
                'content': "{}。\n利用这个人的基本信息和社交关系网络,共同的提供的线索，猜测这个人的国籍是什么(国籍使用英语表示)，并且同时给出猜测的概率值。\n使用list列表返回结果，若提供用户的信息太少难以推测其国籍，则返回['','0']。只需返回list列表：".format(person_info)
            }
        ],
        stream=False,
        temperature=0.6,
        top_p=0.8,
        max_tokens=512,
        presence_penalty=1,
        extra_body={
            "enable_search": True  # 联网
        }
    )
    output = response.choices[0].message.content
    print(output)

if __name__ == '__main__':

    log_name = "geenie97"
    name = "유진"
    bio = ""
    location = ""
    email = ""
    company = ""
    oraganization_name = ""
    oraganization_loaction = ""
    blog_html = ""
    followers_list = "['Yonsei University  College of Artificial Intelligence','MICV Lab at Yonsei University',' Yonsei University - Computer Science  Seoul, South Korea','@kakao  Seoul, Korea','Korea','KFTC  Jeongja-dong, Korea']"
    following_list = "['Yonsei University - Computer Science  Seoul, South Korea','Yonsei University  College of Artificial Intelligence','MICV Lab at Yonsei University','@bigdyl-yonsei  Daejeon,Korea','@kakao  Seoul, Korea','KFTC  Jeongja-dong, Korea','Seoul, Republic of Korea']"

    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main(log_name=log_name, name=name))
