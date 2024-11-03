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
    total_ability = Column(Integer)
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
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# 个人博客表
class UserBlog(Base):
    __tablename__ = 'blogs'
    uid = Column(Integer, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    blog_html = Column(MEDIUMTEXT)
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# 用户登录名表
class UserLoginName(Base):
    __tablename__ = 'login_names'
    uid = Column(Integer, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    login_name = Column(String(255), unique=True)
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# 用户仓库关联表
class UserRepos(Base):
    __tablename__ = 'user_repos'
    uid = Column(Integer, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'))
    repos_url = Column(String(255), unique=True)
    __table_args__ = (
        PrimaryKeyConstraint('uid', 'repos_url'),
    )
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Organization(Base):
    __tablename__ = 'organizations'
    organization_id = Column(Integer, primary_key=True)
    name = Column(String(255))
    descript = Column(MEDIUMTEXT)
    location = Column(String(255))
    organization_blog_html = Column(MEDIUMTEXT)
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

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
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

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
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# 项目成员表
class ReposParticipant(Base):
    __tablename__ = 'repos_participants'
    uid = Column(Integer, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'))
    rid = Column(Integer, ForeignKey('repos_info.id', onupdate='CASCADE', ondelete='CASCADE'))
    __table_args__ = (
        PrimaryKeyConstraint('uid', 'rid'),
    )
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

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
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# 项目URL表
class ReposUrl(Base):
    __tablename__ = 'repos_url'
    rid = Column(Integer, ForeignKey('repos_info.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    repos_url = Column(String(255))
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# 项目语言占比表
class ReposLanguageProportion(Base):
    __tablename__ = 'repos_lg_proportion'
    rid = Column(Integer, ForeignKey('repos_info.id', onupdate='CASCADE', ondelete='CASCADE'))
    language = Column(String(255))
    proportion = Column(Integer)
    __table_args__ = (
        PrimaryKeyConstraint('rid', 'language'),
    )
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

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
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# 项目领域表
class ReposField(Base):
    __tablename__ = 'repos_fields'
    rid = Column(Integer, ForeignKey('repos_info.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    topics = Column(String(255), ForeignKey('topics.name', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# topic表
class Topic(Base):
    __tablename__ = 'topics'
    name = Column(String(50), primary_key=True)
    descript = Column(MEDIUMTEXT)
    avi = Column(String(255))
    repos_count = Column(Integer)
    is_featured = Column(Boolean)
    is_curated = Column(Boolean)
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# topic url表
class TopicUrl(Base):
    __tablename__ = 'topics_url'
    name = Column(String(50), ForeignKey('topics.name', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    topic_url = Column(String(255))
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

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
user_relation_location_view_sql = """
CREATE VIEW user_relation_location_view AS
SELECT 
    u1.id AS uid,
    GROUP_CONCAT(u2.location ORDER BY u2.location SEPARATOR '| ') AS follower_locations,   -- 保留粉丝的地理位置，包括重复项
    GROUP_CONCAT(u3.location ORDER BY u3.location SEPARATOR '| ') AS following_locations    -- 保留关注者的地理位置，包括重复项
FROM 
    users u1
LEFT JOIN 
    relationships r1 ON u1.id = r1.uid AND r1.is_follower = 1               -- 获取粉丝关系
LEFT JOIN 
    users u2 ON r1.related_uid = u2.id                                       -- 粉丝的信息
LEFT JOIN 
    relationships r2 ON u1.id = r2.related_uid AND r2.is_follower = 1       -- 获取关注者关系
LEFT JOIN 
    users u3 ON r2.uid = u3.id                                             -- 关注者的信息
GROUP BY 
    u1.id;
"""




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
    users.nation AS nation,
    user_relation_location_view.follower_locations AS follower_locations,
    user_relation_location_view.following_locations AS following_locations
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
LEFT JOIN
    user_relation_location_view ON user_relation_location_view.uid = users.id
WHERE 
    users.followers > 500 AND users.nation = ""
"""






db_url = (
    f"mysql+mysqlconnector://{INIT_DATABASE_INFO['user']}:{INIT_DATABASE_INFO['passwd']}"
    f"@{INIT_DATABASE_INFO['host']}:{INIT_DATABASE_INFO['port']}/{INIT_DATABASE_INFO['database']}"
)
engine = create_engine(db_url, echo=True)


