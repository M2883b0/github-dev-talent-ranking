# -*- encoding: utf-8 -*-
"""
@File    :   InitDatabase.py    
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/26 11:00    1.0         None
"""

from DataBaseManager import DatabaseManager
import utility.config as config
from utility.config import *
from DataBaseManager import DatabaseConnection


# 将表结构生成SQL字符串的函数
def generate_table_sql(table_field):
    columns = table_field['columns']
    columns_types = table_field['columns_types']
    column_definitions = [f"{col} {col_type}" for col, col_type in zip(columns, columns_types)]
    return ', '.join(column_definitions)


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
    # 遍历所有表并创建
    try:
        for table_name, table_field in config.ALL_TABLE_FIELD.items():
            columns_sql = generate_table_sql(table_field)
            db_manager.create_table(table_name, columns_sql)
        print("所有表初始化完成")
    except Exception as e:
        print("表初始化过程中发生错误：", e)


def initialize_foreign_key(db_manager):
    """
    初始化表的外键
    :param db_manager:
    :return:
    """
    db_manager.add_foreign_key_constraint(TOPICS_URL_TABLE_NAME, 'name', TOPICS_TABLE_NAME, 'name', 'CASCADE', 'CASCADE')

if __name__ == "__main__":
    # 创建DatabaseManager对象并连接数据库
    # db_manager = DatabaseConnection(config.host, config.database_name, config.user_name, config.passwd)
    db_manager = DatabaseManager(**config.INIT_DATABASE_INFO)

    # 初始化数据库
    initialize_database(db_manager)

    db_manager.connect()

    # 初始化数据表
    initialize_table(db_manager)
    # 设置外键
    initialize_foreign_key(db_manager)
    db_manager.commit()
    db_manager.close()
