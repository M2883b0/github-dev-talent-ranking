# -*- encoding: utf-8 -*-
"""
@File    :   InitDatabase.py
@Author  :   m2883b0
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/10/26 11:00    1.0         None
"""
import mysql.connector
from mysql.connector import Error
import utility.config as config
from utility.config import *
from DatabaseManager import DatabaseConnectionPool, DatabaseManager
from utility.DatabaseInitializer import DatabaseInitializer
import logging

def generate_table_sql(table_field):
    """
    将表结构生成SQL字符串的函数
    :param table_field:
    :return:
    """
    columns = table_field['columns']
    columns_types = table_field['columns_types']
    column_definitions = [f"{col} {col_type}" for col, col_type in zip(columns, columns_types)]
    return ', '.join(column_definitions)


def initialize_database(database_initializer):
    try:
        database_initializer.create_database()
    except Exception as e:
        print("数据库初始化过程中发生错误：", e)


def initialize_table(database_initializer):
    """
    自动初始化数据库的表结构
    :param database_initializer: DatabaseManager对象
    """
    # 遍历所有表并创建
    try:
        for table_name, table_field in config.ALL_TABLE_FIELD.items():
            columns_sql = generate_table_sql(table_field)
            database_initializer.create_table(table_name, columns_sql)
        print("所有表初始化完成")
    except Exception as e:
        print("表初始化过程中发生错误：", e)


def initialize_foreign_key(database_initializer):
    """
    初始化表的外键
    :param db_manager:
    :return:
    """
    database_initializer.add_foreign_key_constraint(TOPICS_URL_TABLE_NAME, 'name', TOPICS_TABLE_NAME, 'name', 'CASCADE', 'CASCADE')

if __name__ == "__main__":
    db_initializer = DatabaseInitializer(**config.INIT_DATABASE_INFO)
    # 初始化数据库
    db_initializer.create_database()
    # 连接数据库
    db_initializer.connect()
    # 初始化数据表
    db_initializer.create_all_tables()
    # 设置外键
    # db_initializer.add_foreign_key_for_all_tables()
    # 关闭数据库连接
    db_initializer.close()