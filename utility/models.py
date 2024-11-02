# models.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint, \
    PrimaryKeyConstraint, Table, MetaData, create_engine
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from utility.config import INIT_DATABASE_INFO_DATABASE3306 as INIT_DATABASE_INFO

Base = declarative_base()
metadata = MetaData()

# 用户信息表
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email_address = Column(String(255))
    followers = Column(Integer, default=0)
    bio = Column(MEDIUMTEXT)
    repos_count = Column(Integer)
    company = Column(String(255))
    location = Column(String(255))
    nation = Column(String(255))
    blogs = relationship("UserBlog", backref="user", cascade="all, delete-orphan")


    # 关联关系
    blogs = relationship("UserBlog", backref="user", cascade="all, delete-orphan")
    talents = relationship("Talent", backref="user", cascade="all, delete-orphan")
    login_name = relationship("UserLoginName", backref="user", cascade="all, delete-orphan")
    repos = relationship("UserRepos", backref="user", cascade="all, delete-orphan")
    organizations = relationship("UserOrganization", backref="user", cascade="all, delete-orphan")
    # 指定外键以避免多个路径冲突
    relationships = relationship("UserRelationship",
                                 primaryjoin="User.id == UserRelationship.uid",
                                 backref="user",
                                 cascade="all, delete-orphan")



    repos_participation = relationship("ReposParticipant", backref="user", cascade="all, delete-orphan")


# 能力表
class Talent(Base):
    __tablename__ = 'talent'
    uid = Column(Integer, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'))
    topic = Column(String(255))
    ability = Column(Integer)
    __table_args__ = (
        PrimaryKeyConstraint('uid', 'topic'),
    )


# 个人博客表
class UserBlog(Base):
    __tablename__ = 'blogs'
    uid = Column(Integer, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    blog_html = Column(MEDIUMTEXT)


# 用户登录名表
class UserLoginName(Base):
    __tablename__ = 'login_names'
    uid = Column(Integer, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    login_name = Column(String(255), unique=True)


# 用户仓库关联表
class UserRepos(Base):
    __tablename__ = 'user_repos'
    uid = Column(Integer, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'))
    repos_url = Column(String(255), unique=True)
    __table_args__ = (
        PrimaryKeyConstraint('uid', 'repos_url'),
    )


class Organization(Base):
    __tablename__ = 'organizations'
    organization_id = Column(Integer, primary_key=True)
    name = Column(String(255))
    descript = Column(MEDIUMTEXT)
    location = Column(String(255))
    organization_blog_html = Column(MEDIUMTEXT)


# 用户组织关联表
class UserOrganization(Base):
    __tablename__ = 'user_organization'
    uid = Column(Integer, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'))
    # organization_id = Column(Integer,
    #                          ForeignKey('organizations.organization_id', onupdate='CASCADE', ondelete='CASCADE'),
    #                          )
    organization_id = Column(Integer)
    __table_args__ = (
        PrimaryKeyConstraint('uid', 'organization_id'),
    )


# 用户关系网表
class UserRelationship(Base):
    __tablename__ = 'relationships'
    uid = Column(Integer, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'))
    # related_uid = Column(Integer, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'))
    related_uid = Column(Integer)
    is_fan = Column(Boolean)
    is_follower = Column(Boolean)
    is_collaborator = Column(Boolean)
    __table_args__ = (
        PrimaryKeyConstraint('uid', 'related_uid'),
    )


# 项目成员表
class ReposParticipant(Base):
    __tablename__ = 'repos_participants'
    uid = Column(Integer, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'))
    rid = Column(Integer, ForeignKey('repos_info.id', onupdate='CASCADE', ondelete='CASCADE'))
    __table_args__ = (
        PrimaryKeyConstraint('uid', 'rid'),
    )


# 项目基本信息表
class ReposInfo(Base):
    __tablename__ = 'repos_info'
    id = Column(Integer, primary_key=True)
    main_language = Column(String(255))
    descript = Column(MEDIUMTEXT)
    forks_count = Column(Integer)
    stargazers_count = Column(Integer)
    subscribers_count = Column(Integer)
    importance = Column(Integer)
    total_contribution_value = Column(Integer)
    issue_count = Column(Integer)

    # 关联关系
    urls = relationship("ReposUrl", backref="repo", cascade="all, delete-orphan")
    languages = relationship("ReposLanguageProportion", backref="repo", cascade="all, delete-orphan")
    participants = relationship("ReposParticipantContribution", backref="repo", cascade="all, delete-orphan")
    fields = relationship("ReposField", backref="repo", cascade="all, delete-orphan")


# 项目URL表
class ReposUrl(Base):
    __tablename__ = 'repos_url'
    rid = Column(Integer, ForeignKey('repos_info.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    repos_url = Column(String(255))


# 项目语言占比表
class ReposLanguageProportion(Base):
    __tablename__ = 'repos_lg_proportion'
    rid = Column(Integer, ForeignKey('repos_info.id', onupdate='CASCADE', ondelete='CASCADE'))
    language = Column(String(255))
    proportion = Column(Integer)
    __table_args__ = (
        PrimaryKeyConstraint('rid', 'language'),
    )


# 项目参与者贡献表
class ReposParticipantContribution(Base):
    __tablename__ = 'repos_parti_contribution'
    rid = Column(Integer, ForeignKey('repos_info.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    uid = Column(Integer, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    is_owner = Column(Boolean)
    repos_ability = Column(Integer)
    personal_contribution_value = Column(Integer)
    __table_args__ = (
        PrimaryKeyConstraint('rid', 'uid'),
    )


# 项目领域表
class ReposField(Base):
    __tablename__ = 'repos_fields'
    rid = Column(Integer, ForeignKey('repos_info.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    topics = Column(String(255), ForeignKey('topics.name', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)


# topic表
class Topic(Base):
    __tablename__ = 'topics'
    name = Column(String(50), primary_key=True)
    descript = Column(MEDIUMTEXT)
    avi = Column(String(255))
    repos_count = Column(Integer)
    is_featured = Column(Boolean)


# topic url表
class TopicUrl(Base):
    __tablename__ = 'topics_url'
    name = Column(String(50), ForeignKey('topics.name', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    topic_url = Column(String(255))


# 组织表


# 爬虫错误日志表
class SpiderError(Base):
    __tablename__ = 'spider_error'
    url = Column(String(255), primary_key=True)
    code = Column(Integer)
    spider = Column(String(255))
    detail = Column(String(255))


# 已爬取的URL表
class CrawledUrl(Base):
    __tablename__ = 'crawled_url'
    url = Column(String(255), primary_key=True)


# 定义视图SQL查询
user_profile_view_sql = """
CREATE VIEW user_profile_view AS
SELECT 
    login_names.login_name AS login_name,
    users.id AS uid,
    users.name AS name,
    users.bio AS bio,
    users.location AS location,
    users.email_address AS email_address,
    users.company AS company,
    organizations.name AS organization_name,
    organizations.location AS organization_location,
    blogs.blog_html AS blog_html,
    users.nation AS nation
FROM 
    login_names
LEFT JOIN 
    users ON login_names.uid = users.id
LEFT JOIN 
    user_organization ON users.id = user_organization.uid
LEFT JOIN 
    organizations ON user_organization.organization_id = organizations.organization_id
LEFT JOIN 
    blogs ON users.id = blogs.uid
WHERE 
    users.followers > 500 and users.nation = "";
"""

# 定义视图SQL查询
user_relation_view_sql = """
CREATE VIEW user_relation_view AS
SELECT 
    relationships.uid AS uid,
    relationships.related_id AS related_id,
    relationships.is_follower AS is_follower,
    u2.location AS locatioin,
    followes_list,
    following_list
FROM 
    relationships
LEFT JOIN 
    users u1 ON relationships.uid = u1.id
LEFT JOIN 
    user u2 ON relationships.related_id = u2.uid;
WHERE 
    users.followers > 500 and users.nation = "";
"""


db_url = (
    f"mysql+mysqlconnector://{INIT_DATABASE_INFO['user']}:{INIT_DATABASE_INFO['passwd']}"
    f"@{INIT_DATABASE_INFO['host']}:{INIT_DATABASE_INFO['port']}/{INIT_DATABASE_INFO['database']}"
)
engine = create_engine(db_url, echo=True)

class UserProfileView(Base):
    # __table__ = Table("user_profile_view", metadata, autoload_with=engine)
    # __table__ = Table("user_profile_view", metadata)
    # __table_args__ = {'autoload_with': engine, 'extend_existing': True}
    # SQLAlchemy 不会强制要求主键
    # __mapper_args__ = {"primary_key": []}
    __tablename__ = "user_profile_view"
    __table_args__ = {'autoload_with': engine}

    # 将 login_name 设为伪主键
    login_name = Column(String, primary_key=True)


class UserProfileView(Base):

    __tablename__ = "user_relation_view"
    __table_args__ = {'autoload_with': engine}

    # 将 login_name 设为伪主键
    uid = Column(String)
    related_id = Column()
