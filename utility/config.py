# 数据库相关信息
host = '8.134.144.185'
database = 'data'
user = 'root'
passwd = 'www.gzhu.edu.cn'

# 数据库相关连接信息
INIT_DATABASE_INFO = {
    'host': '8.134.144.185',
    'database': 'data',
    'user': 'root',
    'passwd': 'www.gzhu.edu.cn',
    'charset': 'utf8mb4',
    'collations': 'utf8mb4_unicode_ci'
}

# 数据库创建配置
DATABASE_INFO = {


}

#
# 表名

# 测试表存储请求失败的url
ERROR_TABLE_NAME = 'spider_error'

# users部分
# 用户信息表
USER_TABLE_NAME = 'users'
# 个人博客网页内容表
USER_BLOG_TABLE_NAME = 'blogs'
# 用户login名表
USER_LOGIN_NAME_TABLE_NAME = 'login_names'
# 组织表
ORGANIZATIONS_TABLE_NAME = 'organizations'
# 用户关系网表
USER_RELATIONSHIPS_TABLE_NAME = 'relationships'
# 能力表
TALENT_TABLE_NAME = 'talent'

# repos部分
# 基本信息表
REPOS_INFO_TABLE_NAME = 'repos_info'
# 项目重要程度表
REPOS_IMPORTANT_TABLE_NAME = 'repos_importance'
# 项目成员表
REPOS_PARTICIPANTS_TABLE_NAME = 'repos_participants'
# topic表
TOPICS_TABLE_NAME = 'topics'
# topic url表
TOPICS_URL_TABLE_NAME = 'topics_url'

# 基础数据库数据常量设置

# 超长文本字段类
LONG_STRING_TYPES = 'MEDIUMTEXT'
# URL类字段类和大小
MEDIUM_STRING_TYPES = 'VARCHAR(255)'
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

# 数据库字段名常量设置


# 爬虫错误日志表结构
ERROR_TABLE_FIELD = {
    'columns': ['url', 'code', 'spider', 'detail'],
    'columns_types': [MEDIUM_STRING_TYPES + PRIMARY_KEY, INT, SHORT_STRING_TYPES, SHORT_STRING_TYPES]
}

# 用户信息表结构
USER_TABLE_FIELD = {
    'columns': ['id', 'name', 'followers', 'bio',
                'organizations_id', 'company', 'location', 'nation'],
    'columns_types': [INT + PRIMARY_KEY, SHORT_STRING_TYPES, INT, LONG_STRING_TYPES,
                      SHORT_STRING_TYPES, SHORT_STRING_TYPES, SHORT_STRING_TYPES, SHORT_STRING_TYPES]
}

# 能力表结构
TALENT_TABLE_FIELD = {
    'columns': ['id', 'repos_id_list', 'blog', 'ability', 'repos_url'],
    'columns_types': [INT + PRIMARY_KEY, MEDIUM_STRING_TYPES, MEDIUM_STRING_TYPES, MEDIUM_STRING_TYPES,
                      MEDIUM_STRING_TYPES]
}


# 个人博客表结构
USER_BLOG_TABLE_FIELD = {
    'columns': ['id', 'blog_html'],
    'columns_types': [INT + PRIMARY_KEY, LONG_STRING_TYPES]
}

# 用户login名表
USER_LOGIN_NAME_TABLE_FIELD = {
    'columns': ['id', 'login_name'],
    'columns_types': [INT + PRIMARY_KEY, SHORT_STRING_TYPES]

}

# 组织表
ORGANIZATIONS_TABLE_FIELD = {
    'columns': ['organization_id', 'descript', 'location', 'organization_blog_html'],
    'columns_types': [SHORT_STRING_TYPES + PRIMARY_KEY, MEDIUM_STRING_TYPES, SHORT_STRING_TYPES, LONG_STRING_TYPES]
}

# 用户关系网表
USER_RELATIONSHIPS_TABLE_FIELD = {
    'columns': ['user_id', 'related_user_id',
                'is_fan', 'is_follower', 'is_collaborator'],
    'columns_types': [INT + PRIMARY_KEY, INT, BOOLEAN, BOOLEAN, BOOLEAN]
}

# 项目成员表
REPOS_PARTICIPANTS_TABLE_FIELD = {
    'columns': ['id', 'rid'],
    'columns_types': [INT + PRIMARY_KEY, INT]
}


# repos基本信息表结构
REPOS_INFO_TABLE_FIELD = {
    'columns': ['rid', 'language', 'forks_count', 'stargazers_count',
                'importance', 'total_contribution_value', 'commit'],
    'columns_types': [INT + PRIMARY_KEY, SHORT_STRING_TYPES, MEDIUM_STRING_TYPES, MEDIUM_STRING_TYPES,
                      INT, INT, DECIMAL, INT]
}

# repos重要性表结构
REPOS_IMPORTANT_TABLE_FIELD = {
    'columns': ['rid', 'forks_count', 'stargazers_count', 'topics', 'subscribers_count', 'importance'],
    'columns_types': [INT + PRIMARY_KEY, INT, INT, SHORT_STRING_TYPES, INT, DECIMAL]

}

# topic表结构
TOPICS_TABLE_FIELD = {
    'columns': ['name', 'descript', 'avi',
                'repos_count', 'is_featured'],
    'columns_types': [SHORT_STRING_TYPES + PRIMARY_KEY, MEDIUM_STRING_TYPES, MEDIUM_STRING_TYPES,
                      INT, BOOLEAN]
}

# topic url表结构
TOPICS_URL_TABLE_FIELD = {
    'columns': ['name', 'topic_url'],
    'columns_types': [SHORT_STRING_TYPES + PRIMARY_KEY, MEDIUM_STRING_TYPES]

}


# ALL_TABLE_FIELD = {
#     USER_TABLE_NAME: USER_TABLE_FIELD,
#     TALENT_TABLE_NAME: TALENT_TABLE_FIELD,
#     REPOS_INFO_TABLE_NAME: REPOS_IMPORTANT_TABLE_FIELD,
#     REPOS_IMPORTANT_TABLE_NAME: REPOS_IMPORTANT_TABLE_FIELD,
#     TOPICS_TABLE_NAME: TOPICS_TABLE_FIELD
# }

ALL_TABLE_FIELD = {
    ERROR_TABLE_NAME: ERROR_TABLE_FIELD,
    TOPICS_TABLE_NAME: TOPICS_TABLE_FIELD,
    TOPICS_URL_TABLE_NAME: TOPICS_URL_TABLE_FIELD

}