import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import joinedload, aliased, scoped_session, sessionmaker
from models import User, Talent, UserBlog, UserLoginName, UserRepos, UserOrganization, UserRelationship, \
    ReposParticipant, ReposInfo, ReposUrl, ReposLanguageProportion, ReposParticipantContribution, \
    ReposField, Topic, TopicUrl, Organization, SpiderError, CrawledUrl
import utility.config as config
from sqlalchemy import and_, or_
import pymysql

class DatabaseManager:
    def __init__(self):
        """
        初始化数据库管理器，包括连接池和会话工厂
        """
        # 连接信息从配置文件读取
        database_url = f"mysql+pymysql://{config.INIT_DATABASE_INFO['user']}:{config.INIT_DATABASE_INFO['passwd']}@" \
                       f"{config.INIT_DATABASE_INFO['host']}/{config.INIT_DATABASE_INFO['database']}"

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

    def query_with_filters(self, base_model, filters=None, joins=None, load_related=None, limit=None, offset=None):
        """
        支持多表复杂查询和过滤的方法
        :param base_model: 查询的基础模型类，例如 User 表
        :param filters: 字典形式的过滤条件，如 {"nation": "中国"}
        :param joins: 表之间的关系关联列表，使用模型中的关系属性名称
        :param load_related: 需要预加载的关联表列表，避免 N+1 查询
        :param limit: 返回结果的数量限制
        :param offset: 偏移量，用于分页
        :return: 查询结果的字典列表
        """
        session = self.get_session()
        query = session.query(base_model)

        # 动态加载关联表
        if joins:
            for join_model in joins:
                query = query.join(join_model)

        # 动态加载预先指定的关联表关系
        if load_related:
            for relation in load_related:
                query = query.options(joinedload(relation))

        # 根据过滤条件进行查询
        if filters:
            for attr, value in filters.items():
                query = query.filter(getattr(base_model, attr) == value)

        # 限制查询数量和偏移量（分页）
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        # 获取查询结果并转换为字典
        results = query.all()
        dict_results = [result.__dict__ for result in results]
        for r in dict_results:
            r.pop('_sa_instance_state', None)
        return dict_results


# 使用示例
if __name__ == "__main__":
    db_manager = DatabaseManager()

    # 插入数据示例
    # db_manager.insert_data(User, {"id": 1, "name": "张三", "nation": "中国"})
    # db_manager.insert_data(User, {"id": 2, "name": "李四", "nation": "美国"})
    # db_manager.insert_data(User, {"id": 3, "name": "王五", "nation": "英国"})

    # 插入几条数据
    users_data = [
        {
            'id': 1,
            'name': 'Alice Smith',
            'email_address': 'alice.smith@example.com',
            'followers': 500,
            'bio': 'A passionate developer and tech enthusiast.',
            'repos_count': 10,
            'company': 'Tech Innovations Inc.',
            'location': 'San Francisco, CA',
            'nation': 'United States'
        },
        {
            'id': 2,
            'name': 'Bob Johnson',
            'email_address': 'bob.johnson@example.com',
            'followers': 300,
            'bio': 'Full-stack developer with a focus on web technologies.',
            'repos_count': 15,
            'company': 'Web Solutions Corp.',
            'location': 'New York, NY',
            'nation': 'United States'
        },
        {
            'id': 3,
            'name': 'Charlie Lee',
            'email_address': 'charlie.lee@example.com',
            'followers': 800,
            'bio': 'Data scientist specializing in machine learning.',
            'repos_count': 10,
            'company': 'Data Insights Ltd.',
            'location': 'Los Angeles, CA',
            'nation': 'United States'
        }
    ]

    # 插入数据
    # for user_data in users_data:
    #     db_manager.insert_data(User, user_data)
    #
    #
    #
    #
    #
    # db_manager.insert_data(UserBlog, {"uid": 1, "blog_html": "张三中国jfslajfiwofnsadnsdfajfweijafasdfsajflwjieofjwaf"})
    # db_manager.insert_data(UserBlog, {"uid": 2, "blog_html": "李四美国fajfweijafasdfsajflwjieofjwaf"})
    # db_manager.insert_data(UserBlog, {"uid": 3, "blog_html": "王五美国ajfiwofnsadnsdfajfweijafasdfsajflwjieofjwaf"})
    #
    # db_manager.insert_data(UserLoginName, {"uid": 1, "login_name": "zhangsan"})
    # db_manager.insert_data(UserLoginName, {"uid": 2, "login_name": "lisi"})
    # db_manager.insert_data(UserLoginName, {"uid": 3, "login_name": "wangwu"})

    # 查询示例
    # 1.查询某用户及其博客信息和登录名
    # 过滤出 nation 为 "中国" 的用户，同时加载用户的博客信息和登录名
    # filters = {"nation": "中国"}
    # load_related = [User.blogs, User.login_name]  # 预加载博客和登录名，避免额外查询
    #
    # result = db_manager.query_with_filters(User, filters=filters, load_related=load_related)
    # result1 = [blog.__dict__ for blog in result[0]['blogs']]
    # result2 = [login.__dict__ for login in result[0]['login_name']]
    # print(result1)
    # print(result2)
    # 2.获取某项目的所有参与者及其贡献信息
    # 获取 repos_id 为 1 的项目的所有参与者，并预加载他们的贡献信息
    # filters = {"rid": 1}
    # joins = [ReposParticipant]
    # load_related = [ReposParticipantContribution]
    #
    # result = db_manager.query_with_filters(ReposInfo, filters=filters, joins=joins, load_related=load_related)
    # print(result)

    # 3.分页查询带条件的主题信息
    # 查询 is_featured 为 True 的主题，按分页返回，每页10条
    # filters = {"is_featured": True}
    # limit = 10
    # offset = 0  # 从第 0 条开始
    #
    # result = db_manager.query_with_filters(Topic, filters=filters, limit=limit, offset=offset)
    # print(result)

    # 4.获取某组织及其下所有用户的基本信息
    # 查询 organization_id 为 "org_001" 的组织，并加载所有用户信息
    # filters = {"organization_id": "org_001"}
    # load_related = [Organization.users]
    #
    # result = db_manager.query_with_filters(Organization, filters=filters, load_related=load_related)
    # print(result)

    # 5.使用 and_ 和 or_ 实现复杂条件查询
    # 设置查询条件
    filters = and_(
        User.nation == "中国",
        or_(
            User.followers > 1000,
            User.name.like("%张%")
        )
    )
    # 在这个查询中，and_确保用户在“中国”，or_则用于表示“关注人数多于1000人或名字包含‘张’”。
    # 执行查询

    filters = {
        'is_featured' : 1
    }
    filters = and_(

    )
    result = db_manager.query_with_filters(Topic, filters=filters)

    print(result[0])
