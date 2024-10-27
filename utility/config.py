# 数据库相关信息
host = '172.22.229.6'
database = 'data'
user = 'root'
passwd = '123456'

# 数据库相关信息
INIT_DATABASE_INFO = {
    'host': '172.22.229.6',
    'database': 'data',
    'user': 'root',
    'passwd': '123456'
}


# 表名
# users部分
# 用户信息表
USER_TABLE_NAME = 'users'
# 国家表
NATIONS_TABLE_NAME = 'nations'
# 能力表
TALENT_TABLE_NAME = 'talent'

# repos部分
# 基本信息表
REPOS_INFO_TABLE_NAME = 'repos_info'
# 项目重要程度表
REPOS_IMPORTANT_TABLE_NAME = 'repos_importance'
# topic表
TOPICS_TABLE_NAME = 'topics'

# URL类字段类和大小
LONG_STRING_TYPES = 'VARCHAR(255)'
# 名字类字段类和大小
SHORT_STRING_TYPES = 'VARCHAR(50)'
# 整数类
INT = 'INT'
# 小数类
DECIMAL = 'DECIMAL(5,2)'
# 类boolean
BOOLEAN = 'TINYINT(1)'
# 指定为主键
PRIMARY_KEY = ' PRIMARY KEY'
# 用户信息表结构
USER_TABLE_FIELD = {
    'columns': ['id', 'avatar_url', 'html_url', 'name',
                'followers', 'nation', 'ability'],
    'columns_types': [INT+PRIMARY_KEY, LONG_STRING_TYPES, LONG_STRING_TYPES, SHORT_STRING_TYPES,
                      INT, SHORT_STRING_TYPES, LONG_STRING_TYPES]
}
# 国家表结构
NATIONS_TABLE_FIELD = {
    'columns': ['id', 'followers_url', 'following_url', 'organizations_url',
                'company', 'location', 'nation'],
    'columns_types': [INT+PRIMARY_KEY, LONG_STRING_TYPES, LONG_STRING_TYPES, LONG_STRING_TYPES,
                      SHORT_STRING_TYPES, SHORT_STRING_TYPES, SHORT_STRING_TYPES]
}
# 能力表结构
TALENT_TABLE_FIELD = {
    'columns': ['id', 'repos_id_list', 'blog', 'ability', 'repos_url'],
    'columns_types': [INT+PRIMARY_KEY, LONG_STRING_TYPES, LONG_STRING_TYPES, LONG_STRING_TYPES, LONG_STRING_TYPES]
}
# repos表结构
REPOS_INFO_TABLE_FIELD = {
    'columns': ['rid', 'owner_url', 'languages_url', 'contributors_url',
                'forks_count', 'stargazers_count', 'importance', 'commit'],
    'columns_types': [INT+PRIMARY_KEY, LONG_STRING_TYPES, LONG_STRING_TYPES, LONG_STRING_TYPES,
                      INT, INT, DECIMAL, INT]
}
# repos重要性表结构
REPOS_IMPORTANT_TABLE_FIELD = {
    'columns': ['rid', 'forks_count', 'stargazers_count', 'topics', 'subscribers_count', 'importance'],
    'columns_types': [INT+PRIMARY_KEY, INT, INT, SHORT_STRING_TYPES, INT, DECIMAL]

}

# topic表结构
TOPICS_TABLE_FIELD = {
    'columns': ['name', 'descript', 'avi',
                'url', 'is_featured'],
    'columns_types': [SHORT_STRING_TYPES+PRIMARY_KEY, LONG_STRING_TYPES, LONG_STRING_TYPES,
                      LONG_STRING_TYPES, BOOLEAN]
}


ALL_TABLE_FIELD = {
    USER_TABLE_NAME: USER_TABLE_FIELD,
    NATIONS_TABLE_NAME: NATIONS_TABLE_FIELD,
    TALENT_TABLE_NAME: TALENT_TABLE_FIELD,
    REPOS_INFO_TABLE_NAME: REPOS_IMPORTANT_TABLE_FIELD,
    REPOS_IMPORTANT_TABLE_NAME: REPOS_IMPORTANT_TABLE_FIELD,
    TOPICS_TABLE_NAME: TOPICS_TABLE_FIELD
}
