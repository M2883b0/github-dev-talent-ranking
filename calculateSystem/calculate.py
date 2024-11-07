import time

import utility.models
from calculateSystem.CalculateSystem import CalculateSystem
from utility.DatabaseManagerCalculate import DatabaseManager
from utility.field_constants import UserFields, UserOrganizationFields, UserRelationshipFields, UserReposFields, \
    UserBlogFields, UserLoginNameFields, ReposFieldFields, ReposInfoFields, ReposParticipantFields, ReposUrlFields, \
    ReposLanguageProportionFields, ReposParticipantContributionFields, OrganizationFields, TopicFields, \
    CrawledUrlFields, TopicUrlFields, TalentFields, SpiderErrorFields


def calc_coefficient(calc_system, db_manager, all_repos_info):
    mean_fork = 0
    mean_star = 0
    mean_subscribe = 0
    mean_issue = 0
    repos_total_num = len(all_repos_info)
    for repos_info in all_repos_info:
        # 使用提前定义好的键值常量
        mean_fork += (repos_info[ReposInfoFields.FORKS_COUNT] / repos_total_num)
        mean_star += (repos_info[ReposInfoFields.STARGAZERS_COUNT] / repos_total_num)
        mean_subscribe += (repos_info[ReposInfoFields.SUBSCRIBERS_COUNT] / repos_total_num)
        mean_issue += (repos_info[ReposInfoFields.ISSUE_COUNT] / repos_total_num)
    # 计算系数
    calc_system.calculate_coefficient(
        mean_fork=mean_fork,
        mean_star=mean_star,
        mean_sub=mean_subscribe,
        mean_issue=mean_issue
    )


def calc_repos_importance_list(calc_system, db_manager, all_repos_info):
    # 计算项目importance
    repos_total_num = len(all_repos_info)
    count = 0
    repos_importance_list = []
    for repos_info in all_repos_info:
        rid = repos_info[ReposInfoFields.ID]
        fork_num = repos_info[ReposInfoFields.FORKS_COUNT]
        star_num = repos_info[ReposInfoFields.STARGAZERS_COUNT]
        subscribe_num = repos_info[ReposInfoFields.SUBSCRIBERS_COUNT]
        issue_num = repos_info[ReposInfoFields.ISSUE_COUNT]
        repos_importance = calc_system.calculate_repos_importance(
            fork_num=fork_num,
            star_num=star_num,
            subscribers_num=subscribe_num,
            issue_num=issue_num
        )
        repos_importance_dict = {
            ReposInfoFields.ID: rid,
            ReposInfoFields.IMPORTANCE: int(repos_importance)
        }
        repos_importance_list.append(repos_importance_dict)
        count += 1
        if count % 100 == 0 or count == repos_total_num:
            db_manager.update_repos_importance(repos_importance_list)
            time.sleep(0.5)
            repos_importance_list = []


def calc_personal_repos_ability(calc_system, db_manager):
    personal_repos_calculate_info = db_manager.get_personal_repos_calculate_info()
    personal_repos_ability_list = []
    count = 0
    for personal_repos_cal_info in personal_repos_calculate_info:
        # 获取计算所需字段值
        parse_info_to_calc = {
            "repos_importance": personal_repos_cal_info['importance'],
            "personal_contribution": personal_repos_cal_info['personal_contribution_value'],
            "is_owner": personal_repos_cal_info['is_owner']
        }
        # 计算
        repos_ability = calc_system.calculate_personal_repos_ability(**parse_info_to_calc)
        # 构建更新所需信息字典
        parse_info = {
            "rid": personal_repos_cal_info['rid'],
            "uid": personal_repos_cal_info['uid'],
            "repos_ability": repos_ability
        }
        personal_repos_ability_list.append(parse_info)
        count += 1
        if count % 100 == 0 or count == len(personal_repos_calculate_info):
            db_manager.update_personal_repos_ability(personal_repos_ability_list)
            print('gengxin')
            personal_repos_ability_list = []


def calculate_topic_ability(calc_system, db_manager):
    calc_topic_ability_info = db_manager.get_calc_topic_ability()
    topic_ability_list = []
    count = 0
    for info in calc_topic_ability_info:
        topic_ability = calc_system.calculate_topic_ability(**info)
        if info['topic']:
            pass
        else:
            info['topic'] = ' '
        topic_ability_dict = {
            "uid": info['uid'],
            "topic": info['topic'],
            "ability": topic_ability
        }
        topic_ability_list.append(topic_ability_dict)
        count += 1
        if count % 100 == 0 or count == len(calc_topic_ability_info):
            db_manager.insert_talent(topic_ability_list)
            topic_ability_list = []
            print("topic_ability 插入")


def calculate_ability(calc_system, db_manager):
    calc_ability_info = db_manager.get_calc_ability()
    ability_list = []
    count = 0
    for info in calc_ability_info:
        ability = calc_system.calculate_ability(**info)
        ability_dict = {
            "id": info['uid'],
            "total_ability": ability
        }
        ability_list.append(ability_dict)
        count += 1
        if count % 100 == 0 or count == len(calc_ability_info):
            db_manager.update_ability(ability_list)

            ability_list = []

if __name__ == "__main__":
    calc_system = CalculateSystem()
    db_manager = DatabaseManager()
    # all_repos_info = db_manager.get_repos_calculate_info()
    # 计算系数
    # print("---------计算系数-----------------")
    # calc_coefficient(calc_system, db_manager, all_repos_info)
    # # 只拿没有importance值的项目
    #
    # print("----------计算项目重要性---------------")
    # # 计算项目重要性并插入
    # filter_repos_info = db_manager.get_repos_importance_calculate_info()
    # print(len(filter_repos_info))
    # calc_repos_importance_list(calc_system, db_manager, filter_repos_info)

    # 项目重要性缩放
    # 计算个人项目能力值并插入
    # print("----------计算个人在某个项目中的能力值---------------")
    # calc_personal_repos_ability(calc_system, db_manager)

    # 对repos_ability做


    #
    # 计算topic能力值并插入
    # print("---------计算个人topic能力值并插入")



    # calculate_topic_ability(calc_system, db_manager)
    # 计算总能力值并插入
    print('--------计算总能力并更新------------')
    calculate_ability(calc_system, db_manager)
    # session.query(User).update({User.followers_count: 0})
    # 计算topic能力值
    # 计算total能力值
