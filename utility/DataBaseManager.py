#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :DataBaseManager.py
# @Time      :2024/10/25 下午9:30
# @Author    :C-Yu010124
import mysql.connector
from mysql.connector import Error
import pandas as pd



class DatabaseManager:
    def __init__(self, host, database, user, passwd):
        """

        :param host: 数据库主机地址
        :param database: 数据库名称
        :param user: 数据库用户名
        :param passwd: 数据库密码
        """
        self.host = host
        self.database = database
        self.user = user
        self.passwd = passwd
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
                print("已连接到 MySQL Server 版本：", db_info)

                # 创建游标
                self.cursor = self.connection.cursor()

                # 检查数据库是否存在，不存在则创建
                self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
                print(f"数据库 {self.database} 创建成功")

                # 关闭当前连接，重新连接到创建好的数据库
                self.connection.close()
                self.connection = mysql.connector.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.passwd
                )
                if self.connection.is_connected():
                    print("已连接到数据库:", self.database)
                    self.cursor = self.connection.cursor()
        except Error as e:
            print("连接过程中发生错误：", e)

    def close(self):
        """
        关闭数据库
        :return: 无返回值
        """
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("MySQL 连接已关闭")

    def create_table(self, table_name, columns):
        """

        :param table_name: 创建表的名称
        :param columns: 列名
        :return:
        """
        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
            print(f"表 {table_name} 创建成功")
        except Error as e:
            print(e)

    def insert_data(self, table_name, columns, values):
        try:
            placeholders = ', '.join(['%s'] * len(values))
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            self.cursor.execute(sql, values)
            self.connection.commit()
            print(self.cursor.rowcount, "记录插入成功")
        except Error as e:
            print(e)

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
            self.connection.commit()
            print(self.cursor.rowcount, "记录删除成功")
        except Error as e:
            print(e)


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
            self.connection.commit()
            print(self.cursor.rowcount, "记录更新成功")
        except Error as e:
            print(e)

    def query_data(self, table_name):
        """
        查询数据，并返回JSON格式的结果
        :param table_name: 表名
        :return: JSON格式的字符串
        """
        try:
            self.cursor.execute(f"SELECT * FROM {table_name}")
            result = self.cursor.fetchall()

            # 获取列名
            column_names = [desc[0] for desc in self.cursor.description]

            # 将查询结果转换为DataFrame
            df = pd.DataFrame(result, columns=column_names)

            # 将DataFrame转换为JSON格式的字符串
            json_result = df.to_json(orient='records', force_ascii=False)
            return json_result
        except Error as e:
            print(e)


if __name__ == "__main__":

    db_manager = DatabaseManager('localhost', 'testdb123', 'root', 'Sql147369')
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
    db_manager.update_data('users',"name='王五'",'id=2')
    json_result = db_manager.query_data('users')
    print(json_result)
    db_manager.close()