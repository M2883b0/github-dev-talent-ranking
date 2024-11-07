import math
import time
from calculateSystem.CalculateSystem import CalculateSystem
from utility.DatabaseManagerCalculate import DatabaseManager
from utility.field_constants import ReposInfoFields
from utility.models import User, ReposInfo, ReposParticipantContribution, Talent
from utility.InitDatabase2 import UserProfileView
from utility.models import User, Talent, UserBlog, UserLoginName, UserRepos, UserOrganization, UserRelationship, \
    ReposParticipant, ReposInfo, ReposUrl, ReposLanguageProportion, ReposParticipantContribution, \
    ReposField, Topic, TopicUrl, Organization, SpiderError, CrawledUrl, BlogScore

def calc_coefficient(calc_system, all_repos_info):
    """
    计算公式中的系数值
    """
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
    """
    计算某个项目本身的重要程度
    """
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
    """
    计算某个用户在某个项目中的能力体现
    """
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
    """
    计算用户在某个领域下的能力  只计算前200名
    """
    calc_topic_ability_info = db_manager.get_calc_topic_ability()
    topic_ability_list = []
    count = 0
    for info in calc_topic_ability_info:
        topic_ability = calc_system.calculate_topic_ability(**info)
        if info['topic']:
            pass
        else:
            info['topic'] = ' '
            continue
        topic_ability_dict = {
            "uid": info['uid'],
            "topic": info['topic'],
            "ability": topic_ability
        }
        topic_ability_list.append(topic_ability_dict)
        count += 1
        if count % 1000 == 0 or count == len(calc_topic_ability_info):
            db_manager.insert_talent(topic_ability_list)
            topic_ability_list = []
            print("topic_ability 插入")


def calculate_ability(calc_system, db_manager):
    """
    计算总能力值
    """
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


# def scale_repos_importance(db_manager):
#     """
#     将repos重要性放缩到w级
#     """
#     repos_importance, min_value, max_value = db_manager.get_repos_importance()
#     # 查询原始数据的最小值和最大值
#     count = 0
#     repos_importance_list = []
#     for rep_importance in repos_importance:
#         importance = rep_importance.importance
#         scale_factor = 10000 / (max_value - min_value)
#         scale_importance = (importance - min_value) * scale_factor
#         repos_ability_dict = {
#             "id": rep_importance.id,
#             "importance": int(scale_importance)
#         }
#         repos_importance_list.append(repos_ability_dict)
#         count += 1
#         if count % 100 == 0 or count == len(repos_importance):
#             db_manager.update_repos_importance(repos_importance_list)
#             repos_importance_list = []
#     if repos_importance_list:
#         db_manager.update_personal_repos_ability(repos_importance_list)


# def scale_repos_ability(db_manager):
#     """
#     将repos重要性缩放到10w级
#     """
#     repos_ability, min_value, max_value = db_manager.get_repos_ability()
#     # 查询原始数据的最小值和最大值
#     count = 0
#     repos_ability_list = []
#     for rep_ability in repos_ability:
#         ability = rep_ability.repos_ability
#         scale_factor = 100000 / (max_value - min_value)
#         scale_ability = (ability - min_value) * scale_factor
#         repos_ability_dict = {
#             "rid": rep_ability.rid,
#             "uid": rep_ability.uid,
#             "repos_ability": int(scale_ability)
#         }
#         repos_ability_list.append(repos_ability_dict)
#         count += 1
#         if count % 100 == 0 or count == len(repos_ability):
#             db_manager.update_personal_repos_ability(repos_ability_list)
#             repos_ability_list = []
#     if repos_ability_list:
#         db_manager.update_personal_repos_ability(repos_ability_list)


def scale_repos_importance(db_manager):
    """
    将repos重要性使用对数缩放到万级
    """
    # 获取原始数据的最小值和最大值
    repos_importance, min_value, max_value = db_manager.get_repos_importance()

    # 计算对数后的最小值和最大值
    log_min_value = math.log(min_value + 1)
    log_max_value = math.log(max_value + 1)

    count = 0
    repos_importance_list = []
    for rep_importance in repos_importance:
        importance = rep_importance.importance

        # 对数缩放公式
        log_importance = math.log(importance + 1)
        scale_factor = 10000 / (log_max_value - log_min_value)
        scale_importance = (log_importance - log_min_value) * scale_factor

        # 构造字典数据
        repos_importance_dict = {
            "id": rep_importance.id,
            "importance": int(scale_importance)
        }
        repos_importance_list.append(repos_importance_dict)

        # 批量更新数据库
        count += 1
        if count % 100 == 0 or count == len(repos_importance):
            db_manager.update_repos_importance(repos_importance_list)
            repos_importance_list = []

    # 确保最后一批数据也被更新
    if repos_importance_list:
        db_manager.update_repos_importance(repos_importance_list)

def scale_repos_ability(db_manager):
    """
    将repos重要性使用对数缩放到10万级
    """
    # 获取原始数据的最小值和最大值
    repos_ability, min_value, max_value = db_manager.get_repos_ability()

    # 计算对数后的最小值和最大值
    log_min_value = math.log(min_value + 1)
    log_max_value = math.log(max_value + 1)

    count = 0
    repos_ability_list = []
    for rep_ability in repos_ability:
        ability = rep_ability.repos_ability

        # 对数缩放公式
        log_ability = math.log(ability + 1)
        scale_factor = 100000 / (log_max_value - log_min_value)
        scale_ability = (log_ability - log_min_value) * scale_factor

        # 构造字典数据
        repos_ability_dict = {
            "rid": rep_ability.rid,
            "uid": rep_ability.uid,
            "repos_ability": int(scale_ability)
        }
        repos_ability_list.append(repos_ability_dict)

        # 批量更新数据库
        count += 1
        if count % 100 == 0 or count == len(repos_ability):
            db_manager.update_personal_repos_ability(repos_ability_list)
            repos_ability_list = []

    # 确保最后一批数据也被更新
    if repos_ability_list:
        db_manager.update_personal_repos_ability(repos_ability_list)

def scale_topic_ability(db_manager):
    """
    将topic_ability缩放到0-100
    """
    topic_ability_list, min_value, max_value = db_manager.get_topic_ability()
    # 查询原始数据的最小值和最大值
    count = 0
    topic_ability_scale_list = []
    for topic_ability in topic_ability_list:
        ability = topic_ability.ability
        scale_factor = 100 / (max_value - min_value)
        scale_ability = (ability - min_value) * scale_factor
        topic_ability_scale_dict = {
            "uid": topic_ability.uid,
            "topic": topic_ability.topic,
            "ability": round(scale_ability, 2),
        }
        topic_ability_scale_list.append(topic_ability_scale_dict)
        count += 1
        if count % 100 == 0 or count == len(topic_ability_list):
            db_manager.update_topic_ability(topic_ability_scale_list)
            topic_ability_scale_list = []
    if topic_ability_scale_list:
        db_manager.update_topic_ability(topic_ability_scale_list)


# def scale_ability(db_manager):
#     """
#     将总能力值缩放到0-100
#     """
#     total_ability_list, min_value, max_value = db_manager.get_total_ability()
#     # 查询原始数据的最小值和最大值
#     count = 0
#     total_ability_scale_list = []
#     for total_ability in total_ability_list:
#         ability = total_ability.total_ability
#         scale_factor = 100 / (max_value - min_value)
#         scale_ability = (ability - min_value) * scale_factor
#         total_ability_dict = {
#             "id": total_ability.id,
#             "total_ability": round(scale_ability, 2)
#         }
#         total_ability_scale_list.append(total_ability_dict)
#         count += 1
#         if count % 100 == 0 or count == len(total_ability):
#             db_manager.update_ability(total_ability_scale_list)
#             total_ability_scale_list = []
#     # 确保最后一批数据也被更新
#     if total_ability_scale_list:
#         db_manager.update_ability(total_ability_scale_list)

def scale_ability(db_manager):
    """
    将总能力值使用对数缩放到0-100
    """
    # 获取原始数据的最小值和最大值
    total_ability_list, min_value, max_value = db_manager.get_total_ability()

    # 计算对数后的最小值和最大值
    log_min_value = math.log(min_value + 1)
    log_max_value = math.log(max_value + 1)

    # 遍历总能力值列表并进行对数缩放
    count = 0
    total_ability_scale_list = []
    for total_ability in total_ability_list:
        ability = total_ability.total_ability

        # 对数缩放公式
        log_ability = math.log(ability + 1)
        scale_factor = 100 / (log_max_value - log_min_value)
        scale_ability = (log_ability - log_min_value) * scale_factor

        # 生成新的字典数据
        total_ability_dict = {
            "id": total_ability.id,
            "total_ability": round(scale_ability, 2)
        }
        total_ability_scale_list.append(total_ability_dict)

        # 批量更新数据库
        count += 1
        if count % 100 == 0 or count == len(total_ability_list):
            print(total_ability_scale_list)
            db_manager.update_ability(total_ability_scale_list)
            total_ability_scale_list = []

    # 确保最后一批数据也被更新
    if total_ability_scale_list:
        db_manager.update_ability(total_ability_scale_list)


if __name__ == "__main__":
    calc_system = CalculateSystem()
    db_manager = DatabaseManager()
    all_repos_info = db_manager.get_repos_calculate_info()

    # session = db_manager.get_session()
    # session.query(ReposInfo).update({ReposInfo.importance: 0})
    # session.query(ReposParticipantContribution).update({ReposParticipantContribution.repos_ability: 0})
    # session.query(User).update({User.total_ability: 0})
    # session.commit()

    #
    #
    # 计算系数
    print("---------计算系数-----------------")
    calc_coefficient(calc_system, all_repos_info)
    # # 只拿没有importance值的项目
    #
    print("----------计算项目重要性---------------")
    # # 计算项目重要性并插入
    filter_repos_info = db_manager.get_repos_importance_calculate_info()
    # print(len(filter_repos_info))
    calc_repos_importance_list(calc_system, db_manager, filter_repos_info)

    # 项目重要性缩放
    print("---------项目重要程度缩放---------------")
    scale_repos_importance(db_manager)
    # 计算个人项目能力值并插入
    print("----------计算个人在某个项目中的能力值---------------")
    calc_personal_repos_ability(calc_system, db_manager)

    # 对repos_ability放缩到10w级
    print("-----------缩放repos_ability-----------------")
    scale_repos_ability(db_manager)

    #
    # 计算topic能力值并插入
    print("---------计算个人topic能力值并插入----------")
    calculate_topic_ability(calc_system, db_manager)

    print("---------缩放topic_ability--------------")
    # 将topic_ability值进行缩放
    scale_topic_ability(db_manager)

    # 计算总能力值并插入
    print('--------计算总能力并更新------------')
    calculate_ability(calc_system, db_manager)

    # 总能力清零
    # session = db_manager.get_session()
    # session.query(User).update({User.total_ability: 0})
    # session.commit()
    # 对总能力进行缩放
    print("-----------总能力缩放--------------")
    scale_ability(db_manager)
