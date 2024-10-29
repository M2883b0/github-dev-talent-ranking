#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :DatabaseManager.py
# @Time      :2024/10/25 下午9:30
# @Author    :C-Yu010124
import mysql.connector
from mysql.connector import Error
import utility.config as config
import logging


class DatabaseConnectionPool:
    # 初始化连接池
    def __init__(
            self, pool_name="database_pool", pool_size=20, host=config.INIT_DATABASE_INFO['host'],
            user=config.INIT_DATABASE_INFO['user'], passwd=config.INIT_DATABASE_INFO['passwd'],
            database=config.INIT_DATABASE_INFO['database']
    ):
        self.pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name=pool_name,
            pool_size=pool_size,
            host=host,
            user=user,
            passwd=passwd,
            database=database
        )

    # 获取连接
    def get_connection(self):
        return self.pool.get_connection()


class DatabaseManager:
    def __init__(self, connection_pool):
        """
        初始化数据库管理器
        :param connection_pool: 数据库连接池实例
        """
        self.connection_pool = connection_pool
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        从连接池获取连接
        :return: 无返回值
        """
        try:
            # 从连接池获取连接
            self.connection = self.connection_pool.get_connection()
            if self.connection.is_connected():
                db_info = self.connection.get_server_info()
                logging.info("已连接到 MySQL Server 版本：%s", db_info)
                self.cursor = self.connection.cursor()
                logging.info("已从连接池获取连接")
        except Error as e:
            logging.error("从连接池获取连接时发生错误: %s", e)

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


if __name__ == "__main__":
    db_connection_pool = DatabaseConnectionPool()
    db_manager = DatabaseManager(db_connection_pool)
    db_manager.connect()
    db_manager.close()

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
