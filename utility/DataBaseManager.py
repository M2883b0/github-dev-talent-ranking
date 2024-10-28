#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :DataBaseManager.py
# @Time      :2024/10/25 下午9:30
# @Author    :C-Yu010124
import mysql.connector
from mysql.connector import Error
import pandas as pd
import utility.config as config
import logging


class DatabaseConnection:
    # 初始化连接池
    def __init__(self, host, user, password, database):
        self.pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=5,
            host=host,
            user=user,
            password=password,
            database=database
        )

    # 获取连接
    def get_connection(self):
        return self.pool.get_connection()



class DatabaseManager:
    def __init__(
            self, host=config.INIT_DATABASE_INFO['host'], database=config.INIT_DATABASE_INFO['database'],
            user=config.INIT_DATABASE_INFO['user'], passwd=config.INIT_DATABASE_INFO['passwd'],
            charset=config.INIT_DATABASE_INFO['charset'], collations=config.INIT_DATABASE_INFO['collations']
    ):
        """
        初始化数据库管理器
        :param host: 数据库主机地址
        :param database: 数据库名称
        :param user: 数据库用户名
        :param passwd: 数据库密码
        :param charset: 数据库字符集
        :param collations: 数据库排序
        """
        self.host = host
        self.database = database
        self.user = user
        self.passwd = passwd
        self.charset = charset
        self.collations = collations
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        连接数据库，并在数据库不存在的情况下创建它
        :return: 无返回值
        """
        try:
            # 先尝试连接到MySQL服务器，但不指定数据库
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.passwd
            )
            if self.connection.is_connected():
                db_info = self.connection.get_server_info()
                logging.info("已连接到 MySQL Server 版本：%s", db_info)

                # 创建游标
                self.cursor = self.connection.cursor()

                # 关闭当前连接
                self.connection.close()

                # 重新连接到指定数据库
                self.connection = mysql.connector.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.passwd
                )
                if self.connection.is_connected():
                    logging.info("已连接到数据库: %s", self.database)
                    self.cursor = self.connection.cursor()
        except Error as e:
            logging.error("连接过程中发生错误:%s ", e)

    def close(self):
        """
        关闭数据库
        :return: 无返回值
        """
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            logging.info("MySQL 连接已关闭")

    def commit(self):
        """
        提交事务
        :return: 无返回值
        """
        try:
            self.connection.commit()
            logging.info("事务提交成功")
        except Error as e:
            logging.error("提交事务时发生错误: %s", e)

    def get_rowcount(self):
        """
        返回游标rowcount
        :return: rowcount值
        """
        try:
            return self.cursor.rowcount
        except Error as e:
            logging.error("获取rowcount失败: %s", e)

    def create_database(self):
        """
        创建数据库并设置字符集和校对规则
        :return: 无返回值
        """
        try:
            # 连接到MySQL服务器
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.passwd
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()

                # 检查数据库是否已存在
                self.cursor.execute("SHOW DATABASES LIKE %s", (self.database,))
                result = self.cursor.fetchone()

                if result:
                    logging.info("数据库 %s 已存在", self.database)
                else:
                    # 创建数据库
                    charset = self.charset
                    collation = self.collations
                    self.cursor.execute(f"CREATE DATABASE {self.database} CHARACTER SET {charset} COLLATE {collation}")
                    logging.info("数据库 %s 创建成功", self.database)
        except Error as e:
            logging.error("创建数据库时发生错误：%s", e)
        finally:
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()

    def create_table(self, table_name, columns):
        """

        :param table_name: 创建表的名称
        :param columns: 列名
        :return:
        """
        try:
            # 检查表是否已存在
            self.cursor.execute("SHOW TABLES LIKE %s", (table_name,))
            result = self.cursor.fetchone()

            if result:
                logging.info("表 %s 已存在", table_name)
            else:
                # 创建表
                self.cursor.execute(f"CREATE TABLE {table_name} ({columns})")
                logging.info("表 %s 创建成功", table_name)
        except Error as e:
            logging.error("创建表时发生错误：%s", e)
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()

    def get_rowcount(self):

    def insert_data(self, table_name, values):
        """

        在数据库中插入数据
        :param table_name: 表名
        :param columns: 列的字典
        :param values: 插入的值 tuple
        :return:
        """
        try:
            # 取出表结构字典
            table_field = config.ALL_TABLE_FIELD[table_name]
            columns = ', '.join(table_field['columns'])
            # 插入新数据
            placeholders = ', '.join(['%s'] * len(values))
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            self.cursor.execute(sql, values)
            logging.info("%d 记录插入成功", self.cursor.rowcount)
        except Error as e:
            logging.error("错误: %s", e)

    def delete_data(self, table_name, condition):
        """
        删除数据
        :param table_name: 表名
        :param condition: 删除条件，例如 "id=1"
        :return:
        """
        try:
            sql = f"DELETE FROM {table_name} WHERE {condition}"
            self.cursor.execute(sql)
            logging.info("%d 记录删除成功", self.cursor.rowcount)
        except Error as e:
            logging.error("删除数据时发生错误: %s", e)

    def update_data(self, table_name, set_values, condition):
        """
        更新数据
        :param table_name: 表名
        :param set_values: 要设置的值，例如 "name='李四'
        :param condition: 更新条件，例如 "id=1"
        :return:
        """
        try:
            sql = f"UPDATE {table_name} SET {set_values} WHERE {condition}"
            self.cursor.execute(sql)
            logging.info("%d 记录更新成功", self.cursor.rowcount)
        except Error as e:
            logging.error("更新数据时发生错误: %s", e)

    import pandas as pd
    from sqlite3 import Error

    def query_data(self, table_name, primary_key=None, primary_key_value=None):
        """
        查询数据，并返回JSON格式的结果
        :param table_name: 表名
        :param primary_key: 主键字段名（可选）
        :param primary_key_value: 主键对应的值（可选）
        :return: 字典列表
        """
        try:
            if primary_key and primary_key_value is not None:
                # 根据主键查询
                query = f"SELECT * FROM {table_name} WHERE {primary_key} = %s"
                self.cursor.execute(query, (primary_key_value,))
            else:
                # 查询所有记录
                query = f"SELECT * FROM {table_name}"
                self.cursor.execute(query)

            result = self.cursor.fetchall()

            # 获取列名
            column_names = [desc[0] for desc in self.cursor.description]

            # 将查询结果转换为字典列表
            dict_results = [dict(zip(column_names, row)) for row in result]
            return dict_results

            # # 将查询结果转换为DataFrame
            # df = pd.DataFrame(result, columns=column_names)
            #
            # # 将DataFrame转换为JSON格式的字符串
            # json_result = df.to_json(orient='records', force_ascii=False)
            # return json_result
        except Error as e:
            logging.error("查询数据时发生错误: %s", e)
            return None

    def add_foreign_key_constraint(self, table_name, foreign_key_column, referenced_table, referenced_column,
                                   on_delete_action=None, on_update_action=None):
        """
        为指定的表添加外键约束
        :param table_name: 目标表名
        :param foreign_key_column: 外键所在的列名
        :param referenced_table: 引用的表名
        :param referenced_column: 引用的列名
        :param on_delete_action: 当引用表中的记录被删除时的行为（例如 'CASCADE', 'RESTRICT', 'NO ACTION', 'SET NULL', 'SET DEFAULT'）
        :param on_update_action: 当引用表中的记录被更新时的行为（例如 'CASCADE', 'RESTRICT', 'NO ACTION', 'SET NULL', 'SET DEFAULT'）
        :return: 无返回值
        """
        try:
            constraint_name = f"fk_{table_name}_{foreign_key_column}"

            # 检查外键约束是否存在
            self.cursor.execute(
                f"SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS "
                f"WHERE TABLE_NAME = %s AND CONSTRAINT_TYPE = 'FOREIGN KEY' AND CONSTRAINT_NAME = %s",
                (table_name, constraint_name)
            )
            result = self.cursor.fetchone()

            if result:
                logging.info("外键约束 %s 已经存在", constraint_name)
            else:
                # 构建外键约束的SQL语句
                sql = (
                    f"ALTER TABLE {table_name} "
                    f"ADD CONSTRAINT {constraint_name} "
                    f"FOREIGN KEY ({foreign_key_column}) REFERENCES {referenced_table}({referenced_column})"
                )

                if on_delete_action:
                    sql += f" ON DELETE {on_delete_action}"

                if on_update_action:
                    sql += f" ON UPDATE {on_update_action}"

                # 添加外键约束
                self.cursor.execute(sql)
                logging.info("外键约束 %s 添加成功", constraint_name)
        except Error as e:
            logging.error("添加外键约束时发生错误: %s", e)


if __name__ == "__main__":
    db_manager = DatabaseManager(**config.INIT_DATABASE_INFO)
    db_manager.connect()

    db_manager.create_table('users', 'id INT, name VARCHAR(255), score INT')
    db_manager.insert_data('users', 'id, name, score', (1, '张三', 100))
    json_result = db_manager.query_data('users')
    print(json_result)
    db_manager.insert_data('users', 'id, name, score', (2, '李四', 90))
    json_result = db_manager.query_data('users')
    print(json_result)
    db_manager.delete_data('users', 'id = 1')
    json_result = db_manager.query_data('users')
    print(json_result)
    db_manager.update_data('users', "name='王五'", 'id=2')
    json_result = db_manager.query_data('users')
    print(json_result)
    db_manager.close()
