import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from utility.models import User, Talent, UserBlog, UserLoginName, UserRepos, UserOrganization, UserRelationship, \
    ReposParticipant, ReposInfo, ReposUrl, ReposLanguageProportion, ReposParticipantContribution, \
    ReposField, Topic, TopicUrl, Organization, SpiderError, CrawledUrl

from utility.config import INIT_DATABASE_INFO


class DatabaseManager:
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

    def get_repos_calculate_info(self):
        """

        """
        session = self.get_session()
        query = session.query(ReposInfo)
        repos_calculate_info = query.all()
        # 解析为字典
        repos_calculate_info_list = []
        # for repos_info in repos_calculate_info:
        #     parse_info = {
        #         "rid": repos_info.id,
        #         "forks_count": repos_info.forks_count,
        #         "stargazers_count": repos_info.stargazers_count,
        #         "subscribers_count": repos_info.subscribers_count,
        #         "issue_count": repos_info.issue_count
        #     }
        #     repos_calculate_info_list.append(parse_info)
        for repos_info in repos_calculate_info:
            parse_info = ReposInfo.as_dict(repos_info)
            repos_calculate_info_list.append(parse_info)
        session.close()
        return repos_calculate_info_list

    def get_personal_repos_calculate_info(self):
        session = self.get_session()
        query = (session.query(
            ReposParticipantContribution.rid,
            ReposParticipantContribution.uid,
            ReposInfo.importance,
            ReposParticipantContribution.is_owner,
            ReposParticipantContribution.personal_contribution_value)
                 .join(ReposInfo, ReposInfo.id == ReposParticipantContribution.rid).filter(
            ReposParticipantContribution.uid == 404))
        personal_repos_calculate_info = query.all()
        personal_repos_calc_info_list = []
        for personal_repos_calc_info in personal_repos_calculate_info:
            parse_info = {
                "rid": personal_repos_calc_info.rid,
                "uid": personal_repos_calc_info.uid,
                "importance": personal_repos_calc_info.importance,
                "is_owner": personal_repos_calc_info.is_owner,
                "personal_contribution_value": personal_repos_calc_info.personal_contribution_value
            }
            personal_repos_calc_info_list.append(parse_info)
        return personal_repos_calc_info_list

    def get_calc_topic_ability(self):
        session = self.get_session()
        query = (session.query(User.id,
                               User.followers,
                               ReposParticipantContribution.repos_ability,
                               ReposField.topics)
                 .outerjoin(ReposParticipantContribution.uid == User.id)
                 .outerjoin(ReposField.rid == ReposParticipantContribution.rid)
                 )

    def update_repos_importance(self, new_values):
        """
        更新数据
        :param new_values: 新值，字典形式
        """
        session = self.get_session()
        try:
            # 批量更新
            session.bulk_update_mappings(ReposInfo, new_values)
            session.commit()
            print("gengxinchong")
        except Exception as e:
            session.rollback()
            logging.error("更新记录失败：%s", e)
        finally:
            session.close()

    def update_personal_repos_ability(self, new_values):
        """
        更新数据
        :param new_values: 新值，字典形式
        """
        session = self.get_session()
        try:
            # 批量更新
            session.bulk_update_mappings(ReposParticipantContribution, new_values)
            session.commit()
        except Exception as e:
            session.rollback()
            logging.error("更新记录失败：%s", e)
        finally:
            session.close()

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
