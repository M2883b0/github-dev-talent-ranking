mysql_host = "8..xxx.xxx"
mysql_port = 3360
mysql_user = "xxx"
mysql_ps = "xxx"
mysql_database = "xxx"


class Config():
    """工程配置信息"""
    # 数据库的配置信息
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}".format(mysql_user, mysql_ps, mysql_host, mysql_port, mysql_database)
    SQLALCHEMY_TRACK_MODIFICATIONS = False