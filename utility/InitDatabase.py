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


# class DatabaseInitializer:
#     def __init__(
#             self, host=config.INIT_DATABASE_INFO['host'], database=config.INIT_DATABASE_INFO['database'],
#             user=config.INIT_DATABASE_INFO['user'], passwd=config.INIT_DATABASE_INFO['passwd'],
#             charset=config.INIT_DATABASE_INFO['charset'], collations=config.INIT_DATABASE_INFO['collations']
#     ):
#         """
#         初始化数据库管理器
#         :param host: 数据库主机地址
#         :param database: 数据库名称
#         :param user: 数据库用户名
#         :param passwd: 数据库密码
#         :param charset: 数据库字符集
#         :param collations: 数据库排序
#         """
#         self.host = host
#         self.database = database
#         self.user = user
#         self.passwd = passwd
#         self.charset = charset
#         self.collations = collations
#         self.connection = None
#         self.cursor = None
#
#     def create_database(self):
#         """
#         创建数据库并设置字符集和校对规则
#         :return: 无返回值
#         """
#         try:
#             # 连接到MySQL服务器
#             self.connection = mysql.connector.connect(
#                 host=self.host,
#                 user=self.user,
#                 password=self.passwd
#             )
#             if self.connection.is_connected():
#                 self.cursor = self.connection.cursor()
#
#                 # 检查数据库是否已存在
#                 self.cursor.execute("SHOW DATABASES LIKE %s", (self.database,))
#                 result = self.cursor.fetchone()
#
#                 if result:
#                     logging.info("数据库 %s 已存在", self.database)
#                 else:
#                     # 创建数据库
#                     charset = self.charset
#                     collation = self.collations
#                     self.cursor.execute(f"CREATE DATABASE {self.database} CHARACTER SET {charset} COLLATE {collation}")
#                     logging.info("数据库 %s 创建成功", self.database)
#         except Error as e:
#             logging.error("创建数据库时发生错误：%s", e)
#         finally:
#             if self.connection.is_connected():
#                 self.cursor.close()
#                 self.connection.close()
#
#     def create_table(self, table_name, columns):
#         """
#         创建表结构
#         :param table_name: 创建表的名称
#         :param columns: 列名
#         :return:
#         """
#         try:
#             # 检查表是否已存在
#             self.cursor.execute("SHOW TABLES LIKE %s", (self.table_name,))
#             result = self.cursor.fetchone()
#
#             if result:
#                 logging.info("表 %s 已存在", self.table_name)
#             else:
#                 # 创建表
#                 self.cursor.execute(f"CREATE TABLE {self.table_name} ({self.columns})")
#                 logging.info("表 %s 创建成功", self.table_name)
#         except Error as e:
#             logging.error("创建表时发生错误：%s", e)
#             if self.connection.is_connected():
#                 self.cursor = self.connection.cursor()
#
#     def add_foreign_key_constraint(self, table_name, foreign_key_column, referenced_table, referenced_column,
#                                    on_delete_action=None, on_update_action=None):
#         """
#         为指定的表添加外键约束
#         :param table_name: 目标表名
#         :param foreign_key_column: 外键所在的列名
#         :param referenced_table: 引用的表名
#         :param referenced_column: 引用的列名
#         :param on_delete_action: 当引用表中的记录被删除时的行为（例如 'CASCADE', 'RESTRICT', 'NO ACTION', 'SET NULL', 'SET DEFAULT'）
#         :param on_update_action: 当引用表中的记录被更新时的行为（例如 'CASCADE', 'RESTRICT', 'NO ACTION', 'SET NULL', 'SET DEFAULT'）
#         :return: 无返回值
#         """
#         try:
#             constraint_name = f"fk_{table_name}_{foreign_key_column}"
#
#             # 检查外键约束是否存在
#             self.cursor.execute(
#                 f"SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS "
#                 f"WHERE TABLE_NAME = %s AND CONSTRAINT_TYPE = 'FOREIGN KEY' AND CONSTRAINT_NAME = %s",
#                 (table_name, constraint_name)
#             )
#             result = self.cursor.fetchone()
#
#             if result:
#                 logging.info("外键约束 %s 已经存在", constraint_name)
#             else:
#                 # 构建外键约束的SQL语句
#                 sql = (
#                     f"ALTER TABLE {table_name} "
#                     f"ADD CONSTRAINT {constraint_name} "
#                     f"FOREIGN KEY ({foreign_key_column}) REFERENCES {referenced_table}({referenced_column})"
#                 )
#
#                 if on_delete_action:
#                     sql += f" ON DELETE {on_delete_action}"
#
#                 if on_update_action:
#                     sql += f" ON UPDATE {on_update_action}"
#
#                 # 添加外键约束
#                 self.cursor.execute(sql)
#                 logging.info("外键约束 %s 添加成功", constraint_name)
#         except Error as e:
#             logging.error("添加外键约束时发生错误: %s", e)
#
#     def generate_table_sql(table_field):
#         """
#         将表结构生成SQL字符串的函数
#         :param table_field:
#         :return:
#         """
#         columns = table_field['columns']
#         columns_types = table_field['columns_types']
#         column_definitions = [f"{col} {col_type}" for col, col_type in zip(columns, columns_types)]
#         return ', '.join(column_definitions)

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
    db_initializer = DatabaseInitializer()
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