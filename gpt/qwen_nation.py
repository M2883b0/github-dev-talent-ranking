import ast
import time

# from sqlalchemy.testing.plugin.plugin_base import logging

from config import QWEN_API_KEY, QWEN_NATION_MODEL, TOPIC_THRESHOLDS
import asyncio
from tqdm import tqdm
import logging
from openai import OpenAI
import platform
from utility.InitDatabase2 import UserProfileView

from utility.DatabaseManagerBackend import DatabaseManager

# from https://studycli.org/zh-CN/
Nation_list = ['阿尔巴尼亚', '阿尔及利亚', '美属萨摩亚', '安道尔', '安哥拉', '安圭拉岛', '南极洲', '安提瓜和巴布达',
               '阿根廷', '亚美尼亚', '阿鲁巴岛', '澳大利亚', '奥地利', '阿塞拜疆', '巴哈马', '巴林', '孟加拉国',
               '巴巴多斯', '白俄罗斯', '比利时', '伯利兹', '贝宁', '百慕大', '不丹', '玻利维亚', '波斯尼亚和黑塞哥维那',
               '博茨瓦纳',
               '巴西', '英属印度洋领地', '英属维尔京群岛', '文莱', '保加利亚', '布基纳法索', '缅甸', '布隆迪', '柬埔寨',
               '喀麦隆', '加拿大', '佛得角', '开曼群岛', '中非共和国', '乍得', '智利', '中国', '圣诞岛', '克利珀顿岛',
               '科科斯（基林）群岛', '哥伦比亚', '科摩罗', '刚果民主共和国', '刚果共和国', '库克群岛', '珊瑚海群岛',
               '哥斯达黎加',
               '科特迪瓦', '克罗地亚', '古巴', '塞浦路斯', '捷克共和国', '丹麦', '吉布地', '多米尼克', '多明尼加共和国',
               '厄瓜多尔', '埃及', '萨尔瓦多', '赤道几内亚', '厄立特里亚', '爱沙尼亚', '埃塞俄比亚', '欧罗巴岛',
               '福克兰群岛', '法罗群岛', '斐济', '芬兰', '法国', '法属圭亚那', '法属波利尼西亚', '加蓬', '冈比亚',
               '乔治亚', '德国',
               '加纳', '直布罗陀', '格洛里厄斯群岛', '希腊', '格陵兰', '格林纳达', '瓜德罗普岛', '关岛', '危地马拉',
               '根西岛', '几内亚', '几内亚比绍', '圭亚那', '海地', '罗马教廷（梵蒂冈城）', '洪都拉斯', '匈牙利', '冰岛',
               '印度', '印度尼西亚', '伊朗', '伊拉克', '爱尔兰', '马恩岛', '以色列', '意大利', '牙买加', '扬马延岛',
               '日本',
               '泽西岛', '约旦', '新胡安岛', '哈萨克斯坦', '肯尼亚', '基里巴斯', '科威特', '吉尔吉斯斯坦', '老挝',
               '拉脱维亚', '黎巴嫩', '莱索托', '利比里亚', '利比亚', '列支敦士登', '立陶宛', '卢森堡', '马其顿',
               '马达加斯加', '马拉维', '马来西亚', '马尔代夫', '马里', '马耳他', '马绍尔群岛', '马提尼克岛',
               '毛里塔尼亚', '毛里求斯',
               '马约特岛', '墨西哥', '密克罗尼西亚联邦', '摩尔多瓦', '摩纳哥', '蒙古', '蒙特塞拉特', '摩洛哥',
               '莫桑比克', '纳米比亚', '瑙鲁', '纳瓦萨岛', '尼泊尔', '荷兰', '荷属安的列斯', '新喀里多尼亚', '新西兰',
               '尼加拉瓜', '尼日尔', '尼日利亚', '纽埃', '诺福克岛', '朝鲜', '北马里亚纳群岛', '挪威', '阿曼',
               '巴基斯坦', '帕劳', '巴拿马',
               '巴布亚新几内亚', '西沙群岛', '巴拉圭', '秘鲁', '菲律宾', '皮特凯恩群岛', '波兰', '葡萄牙', '波多黎各',
               '卡塔尔', '留尼汪', '罗马尼亚', '俄罗斯', '卢旺达', '圣赫勒拿岛', '圣基茨和尼维斯', '圣卢西亚岛',
               '圣皮埃尔和密克隆群岛', '圣文森特和格林纳丁斯', '萨摩亚', '圣马力诺', '圣多美和普林西比', '沙特阿拉伯',
               '塞内加尔', '塞尔维亚和黑山',
               '塞舌尔群岛', '塞拉利昂', '新加坡', '斯洛伐克', '斯洛文尼亚', '所罗门群岛', '索马里', '南非', '韩国',
               '西班牙', '南沙群岛', '斯里兰卡', '苏丹', '苏里南', '斯瓦尔巴群岛', '斯威士兰', '瑞典', '瑞士', '叙利亚',
               '塔吉克斯坦', '坦桑尼亚', '泰国', '东帝汶', '多哥', '托克劳', '汤加', '特立尼达和多巴哥', '特罗姆兰岛',
               '突尼斯', '土耳其',
               '土库曼斯坦', '特克斯和凯科斯群岛', '图瓦卢', '乌干达', '乌克兰', '阿拉伯联合酋长国', '英国', '美国',
               '乌拉圭', '乌兹别克斯坦', '瓦努阿图', '委内瑞拉', '越南', '维尔京群岛', '威克岛', '瓦利斯和富图纳群岛',
               '西撒哈拉', '也门', '赞比亚', '津巴布韦']

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=QWEN_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


def task(uid, login_name, name=None, bio=None, location=None, email_address=None, company=None, organization_name=None,
         organizations_location=None, blog_html=None, follower_locations=None, following_locations=None, nation=None):
    """

    :param login_name:  登录名（必填）
    :param name:  用户名（可选）
    :param bio:  简介（可选）
    :param location:  定位（可选）
    :param email_address:  邮箱（可选）
    :param company:  公司（可选）
    :param organization_name:  组织名（可选）
    :param organizations_location:  组织地址（可选）
    :param blog_html:  博客链接的内容（可选）
    :param follower_locations:  粉丝的位置列表（可选）
    :param following_locations:  关注的位置列表（可选）
    :return:
    """

    if nation:  # 如果nation已经有了，就不处理这个数据
        return ""

    print(login_name)
    person_info = "用户名：'{}'".format(login_name)
    if name:
        person_info = person_info + "，姓名：'{}'".format(name)
    if bio:
        person_info = person_info + "，简介：'{}'".format(bio)
    if location:
        person_info = person_info + "，ip位置：'{}'".format(location)
    if email_address:
        person_info = person_info + "，邮箱：'{}'".format(email_address)
    if company:
        person_info = person_info + "，工作的公司：'{}'".format(company)
    if organization_name:
        person_info = person_info + "，加入的组织：'{}'".format(organization_name)
    if organizations_location:
        person_info = person_info + "，组织的位置：'{}'".format(organizations_location)
    if blog_html:
        person_info = person_info + "，个人博客信息：'{}'".format(blog_html)
    if follower_locations:
        person_info = person_info + "，粉丝的ip位置分布列表：'{}'".format(follower_locations)
    if following_locations:
        person_info = person_info + "，关注的ip位置分布列表：'{}'".format(following_locations)

    try:
        response = client.chat.completions.create(
            model=QWEN_NATION_MODEL,
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
                    'content': "{}。\n利用这个人的基本信息和社交关系网络,共同的提供的线索，猜测这个人的国籍是什么(只需要猜测一个国籍，国籍使用中文表示)，并且同时给出猜测的概率值。\n使用list列表返回结果，若提供用户的信息太少难以推测其国籍，则返回['',0]。只需返回一个list列表，例如['中国', 0.9]，不要其他的输出：".format(
                        person_info)
                }
            ],
            stream=False,
            temperature=0.6,
            top_p=0.8,
            max_tokens=32,
            presence_penalty=1,
            extra_body={
                "enable_search": True  # 联网搜索
            }
        )
    except Exception as e:
        logging.error("用户{}，国籍预测出错: {}".format(login_name, e))
        return ""
    output = response.choices[0].message.content
    print(output)
    try:
        output_list = ast.literal_eval(output)
        if (output_list[1] >= 0.4) and (output_list[0] in Nation_list):  # 猜测概率
            insert = {
                "id": uid,
                "nation": output_list[0]
            }
        else:
            insert = {
                "id": uid,
                "nation": "N/A"
            }
        return insert
    except (ValueError, SyntaxError) as e:
        logging.error("用户{}，国籍预测出错: {}，模型的输出是{}".format(login_name, e, output))
        return ""


def main():
    db_manager = DatabaseManager()
    results = db_manager.get_qwen_nation_relevant_info()

    total_records = len(results)
    print(total_records)
    data = []
    count = 0
    for q in tqdm(results, total=total_records):
        insert = task(**q)
        count = count + 1
        if insert:
            data.append(insert)
        if count % 30 == 0 or count == total_records:
            print('插入数据')
            db_manager.update_nation(data)
            data = []


if __name__ == '__main__':
    # log_name = "geenie97"
    # name = "유진"
    # bio = ""
    # location = ""
    # email = ""
    # company = ""
    # oraganization_name = ""
    # oraganization_loaction = ""
    # blog_html = ""
    # followers_list = "['Yonsei University  College of Artificial Intelligence','MICV Lab at Yonsei University',' Yonsei University - Computer Science  Seoul, South Korea','@kakao  Seoul, Korea','Korea','KFTC  Jeongja-dong, Korea']"
    # following_list = "['Yonsei University - Computer Science  Seoul, South Korea','Yonsei University  College of Artificial Intelligence','MICV Lab at Yonsei University','@bigdyl-yonsei  Daejeon,Korea','@kakao  Seoul, Korea','KFTC  Jeongja-dong, Korea','Seoul, Republic of Korea']"

    main()
