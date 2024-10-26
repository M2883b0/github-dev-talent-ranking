import redis
import json

class RedisManager:
    def __init__(self, host='localhost', port=6379, db=0):
        """
        :param host: Redis主机地址
        :param port: Redis端口
        :param db: 使用的数据库索引
        """
        self.host = host
        self.port = port
        self.db = db
        self.connection = None

    def connect(self):
        """
        连接Redis
        :return: 无返回值
        """
        try:
            self.connection = redis.StrictRedis(host=self.host, port=self.port, db=self.db)
            # 测试连接
            self.connection.ping()
            print("已连接到 Redis")
        except redis.ConnectionError as e:
            print("连接Redis时发生错误：", e)

    def close(self):
        """
        关闭Redis连接
        :return: 无返回值
        """
        if self.connection:
            self.connection = None
            print("Redis连接已关闭")

    def set_cache(self, key, value, expiration=None):
        """
        设置缓存
        :param key: 缓存键
        :param value: 缓存值，可以是字符串、字典等
        :param expiration: 过期时间（秒）
        :return: 无返回值
        """
        if isinstance(value, dict):
            value = json.dumps(value)  # 将字典转换为JSON字符串
        self.connection.set(key, value, ex=expiration)
        print(f"缓存已设置: {key}")

    def get_cache(self, key):
        """
        获取缓存
        :param key: 缓存键
        :return: 缓存值，若不存在则返回None
        """
        value = self.connection.get(key)
        if value is not None:
            try:
                return json.loads(value)  # 将JSON字符串转换为字典
            except json.JSONDecodeError:
                return value.decode('utf-8')  # 返回字符串
        return None

    def delete_cache(self, key):
        """
        删除缓存
        :param key: 缓存键
        :return: 无返回值
        """
        self.connection.delete(key)
        print(f"缓存已删除: {key}")

    def clear_cache(self):
        """
        清除所有缓存
        :return: 无返回值
        """
        self.connection.flushdb()
        print("所有缓存已清除")
