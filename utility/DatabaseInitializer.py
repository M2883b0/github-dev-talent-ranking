import logging
import mysql.connector
from mysql.connector import Error

import utility.config as config


class DatabaseInitializer:
    def __init__(
            self, host=config.INIT_DATABASE_INFO['host'], database=config.INIT_DATABASE_INFO['database'],
            user=config.INIT_DATABASE_INFO['user'], passwd=config.INIT_DATABASE_INFO['passwd'],
            charset=config.INIT_DATABASE_INFO['charset'], collations=config.INIT_DATABASE_INFO['collations'],
            all_table_field=config.ALL_TABLE_FIELD, master_slave_mapping_rule=config.MASTER_SLAVE_MAPPING_RULE
    ):
        """
        初始化数据库管理器
        :param host: 数据库主机地址
        :param database: 数据库名称
        :param user: 数据库用户名
        :param passwd: 数据库密码
        :param charset: 数据库字符集
        :param collations: 数据库排序
        :param all_table_field: 数据库所有表结构
        """
        self.host = host
        self.database = database
        self.user = user
        self.passwd = passwd
        self.charset = charset
        self.collations = collations
        self.all_table_field = all_table_field
        self.master_slave_mapping_rule = master_slave_mapping_rule
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        建立数据库连接并选择指定的数据库
        """
        try:
            # 连接到MySQL服务器
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.passwd,
                database=self.database  # 默认连接到指定的数据库
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                logging.info("数据库连接成功，已选择数据库 %s", self.database)
        except Error as e:
            logging.error("数据库连接失败：%s", e)

    def close(self):
        try:
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
            logging.info("初始化数据库连接关闭成功")
        except Error as e:
            logging.error("初始化数据库连接关闭失败: %s", e)

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
                    self.cursor.execute(f"CREATE DATABASE {self.database} CHARACTER SET {self.charset} COLLATE {self.collations}")
                    logging.info("数据库 %s 创建成功", self.database)
        except Error as e:
            logging.error("创建数据库时发生错误：%s", e)
        finally:
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
    def create_all_tables(self):
        try:
            for table_name, table_fields in self.all_table_field.items():
                column_definitions = self.__generate_table_sql(table_fields)
                self.__create_table(table_name, column_definitions)
            logging.info("所有表创建成功")
        except Error as e:
            logging.info("创建表过程发生错误: %s", e)

    def __create_table(self, table_name, columns):
        """
        创建表结构
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

    def add_foreign_key_for_all_tables(self):
        # 获取各个列的值
        master_table_values = self.master_slave_mapping_rule['master_table']
        slave_table_values = self.master_slave_mapping_rule['slave_table']
        foreign_key_column_values = self.master_slave_mapping_rule['foreign_key_column']
        referenced_column_values = self.master_slave_mapping_rule['referenced_column']
        on_delete_action_values = self.master_slave_mapping_rule['on_delete_action']
        on_update_action_values = self.master_slave_mapping_rule['on_update_action']
        for table_name, foreign_key_column, referenced_table, referenced_column, on_delete_action, on_update_action in zip(
                master_table_values, slave_table_values, foreign_key_column_values, referenced_column_values,
                on_delete_action_values, on_update_action_values
        ):
            self.__add_foreign_key_constraint(table_name, foreign_key_column, referenced_table, referenced_column,
                                              on_delete_action, on_update_action)

    def __add_foreign_key_constraint(self, table_name, foreign_key_column, referenced_table, referenced_column,
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

    def __generate_table_sql(self, table_field):
        """
        将表结构生成SQL字符串的函数
        :param table_field:
        :return:
        """
        columns = table_field['columns']
        columns_types = table_field['columns_types']
        column_definitions = [f"{col} {col_type}" for col, col_type in zip(columns, columns_types)]
        return ', '.join(column_definitions)
