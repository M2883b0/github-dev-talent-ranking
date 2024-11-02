from sqlalchemy import create_engine, text, Table, MetaData, Column, String
from sqlalchemy.orm import sessionmaker
from utility.models import Base  # 假设你的模型定义在这里
from utility.config import INIT_DATABASE_INFO_DATABASE3306 as INIT_DATABASE_INFO
from utility.models import user_profile_view_sql

db_url = (
    f"mysql+mysqlconnector://{INIT_DATABASE_INFO['user']}:{INIT_DATABASE_INFO['passwd']}"
    f"@{INIT_DATABASE_INFO['host']}:{INIT_DATABASE_INFO['port']}/{INIT_DATABASE_INFO['database']}"
)
engine = create_engine(db_url, echo=True)
metadata = MetaData()


class DatabaseInitializer:
    def __init__(self):
        db_url = (
            f"mysql+mysqlconnector://{INIT_DATABASE_INFO['user']}:{INIT_DATABASE_INFO['passwd']}"
            f"@{INIT_DATABASE_INFO['host']}:{INIT_DATABASE_INFO['port']}"
        )  # 注意这里没有指定数据库名
        self.engine = create_engine(db_url, echo=True)
        self.Session = sessionmaker(bind=self.engine)



    def create_database(self):
        """创建数据库和表结构"""
        database_name = INIT_DATABASE_INFO['database']

        # 从 Engine 获取 Connection 并执行 SQL 语句
        with self.engine.connect() as connection:
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS `{database_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            print(f"数据库 {database_name} 已创建")

        # 更新连接字符串以指向新创建的数据库
        charset = INIT_DATABASE_INFO.get('charset', 'utf8mb4')
        collation = INIT_DATABASE_INFO.get('collation', 'utf8mb4_unicode_ci')
        db_url = (
            f"mysql+mysqlconnector://{INIT_DATABASE_INFO['user']}:{INIT_DATABASE_INFO['passwd']}"
            f"@{INIT_DATABASE_INFO['host']}:{INIT_DATABASE_INFO['port']}/{database_name}?charset={charset}&collation={collation}"
        )
        self.engine = create_engine(db_url, echo=True)
        self.Session = sessionmaker(bind=self.engine)

        # 创建表结构
        Base.metadata.create_all(self.engine)
        print("表结构已创建")


    def drop_database(self):
        """删除数据库和表结构"""
        database_name = INIT_DATABASE_INFO['database']
        with self.engine.connect() as connection:
            connection.execute(text(f"DROP DATABASE IF EXISTS `{database_name}`"))
            print(f"数据库 {database_name} 已删除")

    def create_session(self):
        """创建并返回一个新会话"""
        db_url = (
            f"mysql+mysqlconnector://{INIT_DATABASE_INFO['user']}:{INIT_DATABASE_INFO['passwd']}"
            f"@{INIT_DATABASE_INFO['host']}:{INIT_DATABASE_INFO['port']}/{INIT_DATABASE_INFO['database']}"
        )
        engine = create_engine(db_url, echo=True)
        self.Session = sessionmaker(bind=engine)
        return self.Session()


def create_user_profile_view(session):
    # 如果视图已存在则删除旧视图
    session.execute(text("DROP VIEW IF EXISTS user_profile_view"))
    # 创建新的视图
    session.execute(text(user_profile_view_sql))
    session.commit()





if __name__ == "__main__":
    db_initializer = DatabaseInitializer()



    session = db_initializer.create_session()  # 获取新的会话
    # session = sessionmaker(bind=engine)
    create_user_profile_view(session)
    # db_initializer.create_database()
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



# class UserProfileView(Base):
#     # __table__ = Table("user_profile_view", metadata, autoload_with=engine)
#     # __table__ = Table("user_profile_view", metadata)
#     # __table_args__ = {'autoload_with': engine, 'extend_existing': True}
#     # SQLAlchemy 不会强制要求主键
#     # __mapper_args__ = {"primary_key": []}
#     __tablename__ = "user_profile_view"
#     __table_args__ = {'autoload_with': engine}
#
#     # 将 login_name 设为伪主键
#     login_name = Column(String, primary_key=True)