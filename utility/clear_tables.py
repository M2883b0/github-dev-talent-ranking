import mysql.connector
from mysql.connector import Error
import utility.config as config


class Database:
    def __init__(
            self, host=config.INIT_DATABASE_INFO['host'], database=config.INIT_DATABASE_INFO['database'],
            user=config.INIT_DATABASE_INFO['user'], passwd=config.INIT_DATABASE_INFO['passwd'],
            port=config.INIT_DATABASE_INFO['port']
    ):
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
        self.port = port
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
                password=self.passwd,
                port=self.port
            )
            if self.connection.is_connected():
                db_info = self.connection.get_server_info()
                print("已连接到 MySQL Server 版本：", db_info)

                # 创建游标
                self.cursor = self.connection.cursor()

                # 关闭当前连接
                self.connection.close()

                # 重新连接到指定数据库
                self.connection = mysql.connector.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.passwd,
                    port=self.port
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

    def clear_table(self, table_name):
        """
        清空指定表的内容
        :param table_name: 要清空的表名
        """
        try:
            self.connect()  # 确保连接数据库

            # 清空表的SQL语句
            self.cursor.execute(f"DELETE FROM {table_name}")
            self.connection.commit()  # 提交事务
            print(f"Table '{table_name}' has been cleared.")

        except Error as e:
            print(f"Error occurred: {e}")
        finally:
            self.close()  # 确保关闭连接


# 示例调用
if __name__ == "__main__":
    db = Database()
    db.clear_table("login_names")  # 指定要清空的表名
    db.clear_table("relationships")
    db.clear_table("organizations")
    db.clear_table("user_repos")
    db.clear_table("users")
    db.clear_table("blogs")

