# 数据库相关信息
host = '172.22.229.6'
database = 'data'
user = 'root'
passwd = '123456'

init_info = {
    'host': '172.22.229.6',
    'database': 'data',
    'user': 'root',
    'passwd': '123456'
}
# 表名
# users部分
# 用户信息表
users_info = 'users_info'


# 国家表
nations = 'nations'
# 能力表
talent = 'talent'

# repos部分
# 基本信息表
repos_info = 'repos_info'
# 项目重要程度表
repos_importance = 'repos_importance'
# topic表
repos_topic = 'repos_topic'
# topic表结构
topic_field = {
    'name': 'name',
    'descript': 'descript',
    'avi': 'avi',
    'url': 'url',
    'is_featured': 'is_featured'
}


all_table_field = {
    'repos_topic': topic_field

}