# -*- encoding: utf-8 -*-
"""
@File    :   InitDatabase.py    
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/26 11:00    1.0         None
"""

from DataBaseManager import DatabaseManager
import config
from DataBaseManager import DatabaseConnection


def initialize_database(db_manager):
    try:
        db_manager.create_database()
    except Exception as e:
        print("数据库初始化过程中发生错误：", e)


def initialize_table(db_manager):
    """
    自动初始化数据库的表结构
    :param db_manager: DatabaseManager对象
    """
    tables = {
        # users部分
        # 用户信息表
        'users_info': 'Uid INT PRIMARY KEY, avi VARCHAR(255), name VARCHAR(50), followers INT, nation VARCHAR(50), '
                      'ability VARCHAR(255)',
        # 国家表
        'nations': 'Uid INT PRIMARY KEY, followers_url VARCHAR(255), following_url VARCHAR(255), '
                   'organizations_url VARCHAR(255), company VARCHAR(50), location VARCHAR(50), nation VARCHAR(50)',
        # 能力表
        'talent': 'order_id INT PRIMARY KEY, user_id INT, product_id INT, quantity INT',

        # repos部分
        # 基本信息表
        'repos_info': 'rid INT PRIMARY KEY, owner_url VARCHAR(255), languages_url VARCHAR(100), '
                      'contributors_url VARCHAR(255),'
                      'forks_count INT, stargazers_count INT, importance DECIMAL(2,2), commit VARCHAR(255)',

        # 项目重要程度表
        'repos_importance': 'rid INT PRIMARY KEY PRIMARY KEY, forks_count INT,stargazers_count INT, '
                            'topics VARCHAR(255),'
                            'subscribers_count INT, importance DECIMAL(2,2)',

        # topic表
        'repos_topic': 'id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), descript VARCHAR(255), '
                       'avi VARCHAR(255), url VARCHAR(255)'

    }

    try:
        for table_name, columns in tables.items():
            db_manager.create_table(table_name, columns)
        print("所有表初始化完成")
    except Exception as e:
        print("表初始化过程中发生错误：", e)


if __name__ == "__main__":
    # 创建DatabaseManager对象并连接数据库
    # db_manager = DatabaseConnection(config.host, config.database_name, config.user_name, config.passwd)
    db_manager = DatabaseManager(config.host, config.database_name, config.user_name, config.passwd)

    # 初始化数据库
    initialize_database(db_manager)

    db_manager.connect()

    # 初始化数据表
    initialize_table(db_manager)