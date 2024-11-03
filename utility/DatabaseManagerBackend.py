import logging
from enum import Enum
from sqlalchemy import join, select, update, Insert
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import joinedload, aliased, scoped_session, sessionmaker, Session

from utility.InitDatabase2 import UserProfileView
from utility.models import User, Talent, UserBlog, UserLoginName, UserRepos, UserOrganization, UserRelationship, \
    ReposParticipant, ReposInfo, ReposUrl, ReposLanguageProportion, ReposParticipantContribution, \
    ReposField, Topic, TopicUrl, Organization, SpiderError, CrawledUrl
import utility.config as config
from utility.Testconfig import INIT_DATABASE_INFO as INIT_DATABASE_INFO

from typing import Optional, List, Dict, Any
from sqlalchemy import and_, or_
import pymysql
from utility.field_constants import UserFields, UserOrganizationFields, UserRelationshipFields, UserReposFields, \
    UserBlogFields, UserLoginNameFields, ReposFieldFields, ReposInfoFields, ReposParticipantFields, ReposUrlFields, \
    ReposLanguageProportionFields, ReposParticipantContributionFields, OrganizationFields, TopicFields, \
    CrawledUrlFields, TopicUrlFields, TalentFields, SpiderErrorFields


class TableName(Enum):
    USER = "User"
    TALENT = "Talent"
    USER_BLOG = "UserBlog"
    USER_LOGIN_NAME = "UserLoginName"
    USER_REPOS = "UserRepos"
    ORGANIZATION = "Organization"
    USER_ORGANIZATION = "UserOrganization"
    USER_RELATIONSHIP = "UserRelationship"
    REPOS_PARTICIPANT = "ReposParticipant"
    REPOS_INFO = "ReposInfo"
    REPOS_URL = "ReposUrl"
    REPOS_LANGUAGE_PROPORTION = "ReposLanguageProportion"
    REPOS_PARTICIPANT_CONTRIBUTION = "ReposParticipantContribution"
    REPOS_FIELD = "ReposField"
    TOPIC = "Topic"
    TOPIC_URL = "TopicUrl"
    SPIDER_ERROR = "SpiderError"
    CRAWLED_URL = "CrawledUrl"


class DatabaseManager:
    # 定义模型名称和模型类的映射关系
    TABLE_MAPPING = {
        "User": User,
        "Talent": Talent,
        "UserBlog": UserBlog,
        "UserLoginName": UserLoginName,
        "UserRepos": UserRepos,
        "Organization": Organization,
        "UserOrganization": UserOrganization,
        "UserRelationship": UserRelationship,
        "ReposParticipant": ReposParticipant,
        "ReposInfo": ReposInfo,
        "ReposUrl": ReposUrl,
        "ReposLanguageProportion": ReposLanguageProportion,
        "ReposParticipantContribution": ReposParticipantContribution,
        "ReposField": ReposField,
        "Topic": Topic,
        "TopicUrl": TopicUrl,
        "SpiderError": SpiderError,
        "CrawledUrl": CrawledUrl,
    }

    def __init__(self):
        """
        初始化数据库管理器，包括连接池和会话工厂
        """
        # 连接信息从配置文件读取
        database_url = f"mysql+pymysql://{INIT_DATABASE_INFO['user']}:{INIT_DATABASE_INFO['passwd']}@" \
                       f"{INIT_DATABASE_INFO['host']}:{INIT_DATABASE_INFO['port']}/{INIT_DATABASE_INFO['database']}"

        # 创建SQLAlchemy引擎和连接池
        self.engine = create_engine(database_url, pool_size=20, max_overflow=0)

        # 初始化会话工厂并配置为线程安全
        self.SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))
        logging.info("数据库连接池和会话工厂已初始化")

    def get_session(self):
        """
        获取数据库会话
        :return: 会话实例
        """
        return self.SessionLocal()

    def insert_data(self, base_model, data):
        """
        插入数据
        :param base_model:
        :param data: 插入的数据，字典形式
        """
        session = self.get_session()
        try:
            new_record = base_model(**data)
            session.add(new_record)
            session.commit()
            logging.info("记录插入成功")
        except Exception as e:
            session.rollback()
            logging.error("插入记录失败：%s", e)
        finally:
            session.close()

    def update_nation(self, new_values):
        """
        :param new_values: 传入的列表,每个元素是字典 [{"uid": uid, "nation": "中国"}, ]
        """
        session = self.get_session()
        for dic in new_values:
            uid = dic.get("uid")
            nation = dic.get("nation")

            stmt = (
                update(User).
                where(User.id == uid).
                values(nation=nation)
            )
            session.execute(stmt)

        session.commit()
        session.close()

    def get_topic(self, is_feature=False, is_curated=False):
        session = self.get_session()
        session.query(Topic.name, TopicUrl.topic_url, Topic.avi, Topic.descript, )


    def insert_topic(self, new_values):
        """
        :param new_values : 传入的列表,每个元素是字典 [{"rid": rid, "topic": "java"}, ]
        return: 无返回值
        """
        session = self.get_session()
        for dic in new_values:
            rid = dic.get("rid")
            topic_value = dic.get("topic")
            stmt = (
                Insert(ReposField).
                values(rid=rid, topics=topic_value)
            )
            session.execute(stmt)

        session.commit()
        session.close()

    def update_data(self, record_id, new_values):
        """
        更新数据
        :param record_id: 要更新的记录ID
        :param new_values: 新值，字典形式
        """
        session = self.get_session()
        try:
            session.query(User).filter(User.id == record_id).update(new_values)
            session.commit()
            logging.info("记录更新成功")
        except Exception as e:
            session.rollback()
            logging.error("更新记录失败：%s", e)
        finally:
            session.close()

    def delete_data(self, record_id):
        """
        删除数据
        :param record_id: 要删除的记录ID
        """
        session = self.get_session()
        try:
            session.query(User).filter(User.id == record_id).delete()
            session.commit()
            logging.info("记录删除成功")
        except Exception as e:
            session.rollback()
            logging.error("删除记录失败：%s", e)
        finally:
            session.close()

    # def get_topics_page(self, order, page, limit):
    #     session = self.get_session()
    #     session.query(Topic, Order).join(Order, User.id == Order.user_id))
    #
    # def query_with_filters(self, table_name, filters=None, logic=None, order_by=None, joins=None,
    #                        load_related=None, limit=None, offset=None,
    #                        ):
    #     """
    #     支持多表复杂查询和过滤的方法
    #     :param table_name: 查询的基础表类，例如 User 表  TableName.USER
    #     :param filters: 字典形式的过滤条件，如 {"nation": "中国"}
    #     :param order_by: 排序条件，包含字段名称和排序方向 ("asc" 或 "desc")  如 {"repos_count", "asc"}
    #     :param joins: 表之间的关系关联列表，使用模型中的关系属性名称
    #     :param load_related: 需要预加载的关联表列表，避免 N+1 查询
    #     :param limit: 返回结果的数量限制
    #     :param offset: 偏移量，用于分页
    #     :return: 查询结果的字典列表
    #     """
    #     session = self.get_session()
    #     table = self.TABLE_MAPPING.get(table_name.value)
    #     query = session.query(table)
    #
    #     # 动态加载关联表
    #     if joins:
    #         for join_model in joins:
    #             query = query.join(join_model)
    #
    #     # 动态加载预先指定的关联表关系
    #     if load_related:
    #         for relation in load_related:
    #             query = query.options(joinedload(relation))
    #
    #     # 根据过滤条件进行查询
    #     if filters:
    #         expressions = []
    #         for condition in filters:
    #             field = getattr(table, condition["field"])
    #             op = condition["op"]
    #             value = condition["value"]
    #             if op == "==":
    #                 expressions.append(field == value)
    #             elif op == "!=":
    #                 expressions.append(field != value)
    #             elif op == ">":
    #                 expressions.append(field > value)
    #             elif op == "<":
    #                 expressions.append(field < value)
    #             elif op == ">=":
    #                 expressions.append(field >= value)
    #             elif op == "<=":
    #                 expressions.append(field <= value)
    #
    #         # 根据逻辑操作组合条件
    #         if logic == "and":
    #             query = query.filter(and_(*expressions))
    #         elif logic == "or":
    #             query = query.filter(or_(*expressions))
    #
    #     # 设置排序
    #     if order_by:
    #         field = order_by['field']
    #         direction = order_by['direction']
    #         if direction == "asc":
    #             query = query.order_by(asc(getattr(table, field)))
    #         elif direction == "desc":
    #             query = query.order_by(desc(getattr(table, field)))
    #
    #     # 限制查询数量和偏移量（分页）
    #     if limit:
    #         query = query.limit(limit)
    #     if offset:
    #         query = query.offset(offset)
    #
    #     # 获取查询结果并转换为字典
    #     results = query.all()
    #     dict_results = [result.__dict__ for result in results]
    #     for r in dict_results:
    #         r.pop('_sa_instance_state', None)
    #     return dict_results

    # def get_user_profile(self,
    #         session: Session,
    #         log_name: str,
    #         name: Optional[str] = None,
    #         bio: Optional[str] = None,
    #         location: Optional[str] = None,
    #         email: Optional[str] = None,
    #         company: Optional[str] = None,
    #         organization_name: Optional[str] = None,
    #         organization_location: Optional[str] = None,
    #         blog_html: Optional[bool] = False,
    #         followers_list: Optional[bool] = False,
    #         following_list: Optional[bool] = False
    # ) -> List[Dict[str, Any]]:
    #     """
    #     获取用户的详细信息。
    #     :param session: 数据库会话
    #     :param log_name: 登录名（必填）
    #     :param name: 用户名（可选）
    #     :param bio: 简介（可选）
    #     :param location: 位置（可选）
    #     :param email: 邮箱（可选）
    #     :param company: 公司（可选）
    #     :param organization_name: 组织名（可选）
    #     :param organization_location: 组织地址（可选）
    #     :param blog_html: 是否包含博客内容（可选）
    #     :param followers_list: 是否包含粉丝列表（可选）
    #     :param following_list: 是否包含关注列表（可选）
    #     :return: 用户详细信息列表
    #     """
    #
    #     # 基础查询
    #     query = select(
    #         UserLoginName.login_name.label("log_name"),
    #         User.name.label("name") if name else None,
    #         User.bio if bio else None,
    #         User.location if location else None,
    #         User.email_address if email else None,
    #         User.company if company else None,
    #         Organization.name.label("organization_name") if organization_name else None,
    #         Organization.location.label("organization_location") if organization_location else None,
    #     ).join(User, User.id == UserLoginName.uid, isouter=True)
    #
    #     # 添加博客内容
    #     if blog_html:
    #         query = query.outerjoin(UserBlog, UserBlog.uid == User.id).add_columns(UserBlog.blog_html)
    #
    #     # 添加组织信息
    #     if organization_name or organization_location:
    #         query = query.outerjoin(UserOrganization, UserOrganization.uid == User.id) \
    #             .outerjoin(Organization, Organization.organization_id == UserOrganization.organization_id)
    #
    #     # 粉丝列表
    #     if followers_list:
    #         query = query.outerjoin(UserRelationship,
    #                                 (User.id == UserRelationship.related_uid) & (UserRelationship.is_follower == True)) \
    #             .add_columns(UserRelationship.uid.label("follower_id"))
    #
    #     # 关注列表
    #     if following_list:
    #         query = query.outerjoin(UserRelationship,
    #                                 (User.id == UserRelationship.uid) & (UserRelationship.is_follower == True)) \
    #             .add_columns(UserRelationship.related_uid.label("following_id"))
    #
    #     # 过滤条件
    #     query = query.filter(UserLoginName.login_name == log_name)
    #
    #     # 执行查询
    #     results = session.execute(query).all()
    #
    #     # 将结果转换为字典
    #     return [dict(row) for row in results]

    def get_qwen_nation_relevant_info(self):
        """
        返回用于推测用户国籍的相关信息
        return results_dict (list of dict) [{},{}]每个字典包含大模型推理所有所需的键
        """
        session = self.get_session()
        results_dict = session.query(UserProfileView).all()
        return_res = []
        # 处理结果并添加有意义的地理位置列表
        for result in results_dict:
            processed_result = {
                'uid': result.uid,
                'login_name': result.login_name,
                'name': result.name,
                'bio': result.bio,
                'location': result.location,
                'email_address': result.email_address,
                'company': result.company,
                'nation': result.nation,
                'organization_name': result.organization_name,
                "organizations_location": result.organization_location,
                'following_locations': result.following_locations,
                'follower_locations': result.follower_locations
            }
            # 获取 following_locations 字符串
            following_locations = result.following_locations
            follower_locations = result.follower_locations
            if following_locations is not None:
                # 处理字符串，按|分隔并去除空值
                following_locations = [loc.strip() for loc in following_locations.split('|') if loc.strip()]

                # 取前 10 个有意义的地理位置
                meaningful_following_locations = following_locations[:10]
                # 将列表转换为字符串，用逗号分隔
                processed_result['following_locations'] = ', '.join(meaningful_following_locations)
            if follower_locations is not None:
                # 处理字符串，按|分隔并去除空值
                follower_locations = [loc.strip() for loc in follower_locations.split('|') if loc.strip()]
                # 取前 10 个有意义的地理位置
                meaningful_follower_locations = follower_locations[:10]
                # 将列表转换为字符串，用逗号分隔
                processed_result['follower_locations'] = ', '.join(meaningful_follower_locations)
            if processed_result.get('nation') is "":
                return_res.append(processed_result)
        # 返回处理后的结果
        return results_dict

    def get_qwen_topic_relevant_info(self):
        """
        返回 热门topic列表,没有topic的repos描述列表,全部topic列表
        return:
            tuple: 包含三个元素的元组。
                - feat_topic_str (str): 热门topic列表，以逗号分隔的字符串。
                - topic_des_dict (list of dict): 没有topic的repos描述列表，每个元素是一个包含'id'和'descript'键的字典。
                - all_topic_str (str): 全部topic列表，以逗号分隔的字符串。
        """
        session = self.get_session()
        feat_topic_list = session.query(Topic.name).filter(Topic.is_featured == 1).all()
        feat_topic_str_list = [str(topic_name).strip("(),'") for topic_name in feat_topic_list]
        feat_topic_str = ','.join(feat_topic_str_list)
        all_topic_list = session.query(Topic.name).all()
        all_topic_str_list = [str(topic_name).strip("(),'") for topic_name in all_topic_list]
        all_topic_str = ','.join(all_topic_str_list)
        topic_des = session.query(ReposInfo.id, ReposInfo.descript).join(ReposField, ReposField.rid != ReposInfo.id).all()
        topic_des_dict = [{"id": uid, "descript": descript} for uid, descript in topic_des]
        return feat_topic_str, topic_des_dict, all_topic_str


# 使用示例
if __name__ == "__main__":
    db_manager = DatabaseManager()

    # 插入数据示例
    # db_manager.insert_data(User, {"id": 1, "name": "张三", "nation": "中国"})
    # db_manager.insert_data(User, {"id": 2, "name": "李四", "nation": "美国"})
    # db_manager.insert_data(User, {"id": 3, "name": "王五", "nation": "英国"})

    # 插入数据示例
    # db_manager.insert_data(User, {"id": 1, "name": "张三", "nation": "中国"})
    # db_manager.insert_data(User, {"id": 2, "name": "李四", "nation": "美国"})
    # db_manager.insert_data(User, {"id": 3, "name": "王五", "nation": "英国"})

    #
    # 插入数据示例
    data_to_insert = [
        {
            "name": "Python编程",
            "descript": "关于Python编程的各种教程和资源。",
            "avi": "https://example.com/avatars/python.jpg",
            "repos_count": 75,
            "is_featured": True,
            "is_curated": True
        },
        {
            "name": "机器学习",
            "descript": "关于机器学习的基础知识和最新进展。",
            "avi": "https://example.com/avatars/ml.jpg",
            "repos_count": 120,
            "is_featured": False,
            "is_curated": True

        },
        {
            "name": "前端开发",
            "descript": "关于前端开发的技术和最佳实践。",
            "avi": "https://example.com/avatars/frontend.jpg",
            "repos_count": 90,
            "is_featured": True,
            "is_curated": True

        },
        {
            "name": "数据科学",
            "descript": "关于数据科学的工具和技术。",
            "avi": "https://example.com/avatars/data_science.jpg",
            "repos_count": 50,
            "is_featured": False,
            "is_curated": True

        },
        {
            "name": "云计算",
            "descript": "关于云计算的服务和解决方案。",
            "avi": "https://example.com/avatars/cloud.jpg",
            "repos_count": 60,
            "is_featured": True,
            "is_curated": True

        }
    ]

    data_to_insert = [
        {
            "name": "Python编程",
            "descript": "关于Python编程的各种教程和资源。",
            "avi": "https://example.com/avatars/python.jpg",
            "repos_count": 75,
            "is_featured": True,
            "is_curated": True
        },
        {
            "name": "机器学习",
            "descript": "关于机器学习的基础知识和最新进展。",
            "avi": "https://example.com/avatars/ml.jpg",
            "repos_count": 120,
            "is_featured": False,
            "is_curated": True
        },
        {
            "name": "前端开发",
            "descript": "关于前端开发的技术和最佳实践。",
            "avi": "https://example.com/avatars/frontend.jpg",
            "repos_count": 90,
            "is_featured": True,
            "is_curated": True
        },
        {
            "name": "数据科学",
            "descript": "关于数据科学的工具和技术。",
            "avi": "https://example.com/avatars/data_science.jpg",
            "repos_count": 50,
            "is_featured": False,
            "is_curated": True
        },
        {
            "name": "云计算",
            "descript": "关于云计算的服务和解决方案。",
            "avi": "https://example.com/avatars/cloud.jpg",
            "repos_count": 60,
            "is_featured": True,
            "is_curated": True
        }
    ]

    # 使用你的插入方法插入数据
    db_manager.insert_data(Topic, data_to_insert[0])
    db_manager.insert_data(Topic, data_to_insert[1])
    db_manager.insert_data(Topic, data_to_insert[2])
    db_manager.insert_data(Topic, data_to_insert[3])
    db_manager.insert_data(Topic, data_to_insert[4])

    data_to_insert = [
        {
            "id": 1,
            "main_language": "Python",
            "descript": "A comprehensive library of Python scripts and tools.",
            "forks_count": 120,
            "stargazers_count": 85,
            "subscribers_count": 30,
            "importance": 5,
            "total_contribution_value": 100.00,
            "issue_count": 15
        },
        {
            "id": 2,
            "main_language": "Java",
            "descript": "Collection of Java frameworks and applications.",
            "forks_count": 90,
            "stargazers_count": 120,
            "subscribers_count": 45,
            "importance": 4,
            "total_contribution_value": 150.00,
            "issue_count": 20
        },
        {
            "id": 3,
            "main_language": "JavaScript",
            "descript": "Various JavaScript libraries and plugins.",
            "forks_count": 150,
            "stargazers_count": 200,
            "subscribers_count": 50,
            "importance": 6,
            "total_contribution_value": 200.00,
            "issue_count": 25
        },
        {
            "id": 4,
            "main_language": "C++",
            "descript": "Advanced C++ algorithms and data structures.",
            "forks_count": 75,
            "stargazers_count": 100,
            "subscribers_count": 25,
            "importance": 5,
            "total_contribution_value": 120.00,
            "issue_count": 10
        },
        {
            "id": 5,
            "main_language": "Ruby",
            "descript": "Ruby on Rails projects and gems.",
            "forks_count": 110,
            "stargazers_count": 150,
            "subscribers_count": 35,
            "importance": 4,
            "total_contribution_value": 180.00,
            "issue_count": 18
        }
    ]
    for i in range(len(data_to_insert)):
        db_manager.insert_data(ReposInfo, data_to_insert[i])

    # session = db_manager.get_session()
    # results = session.query(UserProfileView).all()
    # print(type(results[0]))
    results = db_manager.get_qwen_nation()
    for i in results:
        print(i.follower_locations)
        print(i.following_locations)
    value = [{"uid": 1, "nation": "美国"}, {"uid": 2, "nation": "中国"}]
    db_manager.update_nation(value)
    feature_topic_lists, topic_description, all_topic_lists = db_manager.get_qwen_topic()
    print(feature_topic_lists)
    print(topic_description)
    print(all_topic_lists)

    db_manager.update_topic([{"rid": 2, "topic": "vue"}, {"rid": 3, "topic": "云计算"}])
