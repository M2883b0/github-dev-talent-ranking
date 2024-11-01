# 数据库相关信息
host = '8.134.144.185'
database = 'data'
user = 'root'
passwd = 'www.gzhu.edu.cn'

# 数据库相关连接信息
INIT_DATABASE_INFO = {
    'host': '8.134.144.185',
    'port': 3307,
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
# 已爬取的URL表
CRAWLED_URL_TABLE_NAME = 'crawled_url'
# users部分
# 用户信息表
USER_TABLE_NAME = 'users'
# 能力表
TALENT_TABLE_NAME = 'talent'
# 个人博客网页内容表
USER_BLOG_TABLE_NAME = 'blogs'
# 个人仓库关联表
USER_REPOS_TABLE_NAME = 'user_repos'
# 用户login名表
USER_LOGIN_NAME_TABLE_NAME = 'login_names'
# 组织表
ORGANIZATIONS_TABLE_NAME = 'organizations'
# 用户组织关联表
USER_ORGANIZATION_TABLE_NAME = 'user_organization'
# 用户关系网表
USER_RELATIONSHIPS_TABLE_NAME = 'relationships'

# repos部分
# 基本信息表
REPOS_INFO_TABLE_NAME = 'repos_info'
# 项目URL表
REPOS_URL_TABLE_NAME = 'repos_url'
# 项目语言占比表
REPOS_LANGUAGE_PROPORTION_TABLE_NAME = 'repos_lg_proportion'
# 项目参与者贡献表
REPOS_PARTICIPANTS_CONTRIBUTIONS_TABLE_NAME = 'repos_parti_contrib'
# 项目领域表
REPOS_FIELDS_TABLE_NAME = 'repos_fields'
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
    'columns_types': [MEDIUM_STRING_TYPES + PRIMARY_KEY, INT, MEDIUM_STRING_TYPES, MEDIUM_STRING_TYPES]
}

# 已爬取的URL表结构
CRAWLED_URL_TABLE_FIELD = {
    'columns': ['url'],
    'columns_types': [MEDIUM_STRING_TYPES + PRIMARY_KEY]
}

# 用户信息表结构
USER_TABLE_FIELD = {
    'columns': ['id', 'name', 'email_address', 'followers', 'bio', 'repos_count',
                'company', 'location', 'nation'],
    'columns_types': [INT + PRIMARY_KEY, MEDIUM_STRING_TYPES, MEDIUM_STRING_TYPES, INT, LONG_STRING_TYPES, INT,
                      MEDIUM_STRING_TYPES, MEDIUM_STRING_TYPES, MEDIUM_STRING_TYPES]
}

# 能力表结构
TALENT_TABLE_FIELD = {
    'columns': ['uid', 'topic', 'ability'],
    'columns_types': [INT + PRIMARY_KEY, MEDIUM_STRING_TYPES, INT]
}

# 用户仓库关联表结构
USER_REPOS_TABLE_FIELD = {
    'columns': ['uid', 'repos_url'],
    'columns_types': [INT + PRIMARY_KEY, MEDIUM_STRING_TYPES]
}

# 个人博客表结构
USER_BLOG_TABLE_FIELD = {
    'columns': ['uid', 'blog_html'],
    'columns_types': [INT + PRIMARY_KEY, LONG_STRING_TYPES]
}

# 用户login名表
USER_LOGIN_NAME_TABLE_FIELD = {
    'columns': ['uid', 'login_name'],
    'columns_types': [INT + PRIMARY_KEY, MEDIUM_STRING_TYPES]

}

# 组织表
ORGANIZATIONS_TABLE_FIELD = {
    'columns': ['organization_id', 'name', 'descript', 'location', 'organization_blog_html'],
    'columns_types': [MEDIUM_STRING_TYPES + PRIMARY_KEY, MEDIUM_STRING_TYPES, LONG_STRING_TYPES, MEDIUM_STRING_TYPES,
                      LONG_STRING_TYPES]
}

# 用户组织关联表结构
USER_ORGANIZATION_TABLE_FIELD = {
    'columns': ['uid', 'organization_id'],
    'columns_types': [INT + PRIMARY_KEY, INT]
}

# 用户关系网表
USER_RELATIONSHIPS_TABLE_FIELD = {
    'columns': ['uid', 'related_uid',
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
    'columns': ['id', 'main_language', 'descript', 'forks_count', 'stargazers_count',
                'subscribers_count', 'importance', 'total_contribution_value', 'issue_count'],
    'columns_types': [INT + PRIMARY_KEY, MEDIUM_STRING_TYPES, LONG_STRING_TYPES, INT, INT,
                      INT, INT, INT, INT]
}

# 项目URL表结构
REPOS_URL_TABLE_FIELD = {
    'columns': ['rid', 'repos_url'],
    'columns_types': [INT + PRIMARY_KEY, MEDIUM_STRING_TYPES]
}

# 项目语言占比表结构
REPOS_PROPORTION_TABLE_FIELD = {
    'columns': ['rid', 'language', 'proportion'],
    'columns_types': [INT + PRIMARY_KEY, MEDIUM_STRING_TYPES, INT]
}

# 项目参与者贡献表结构
REPOS_PARTICIPANTS_CONTRIBUTIONS_TABLE_FIELD = {
    'columns': ['rid', 'uid', 'is_owner', 'personal_contribution_value'],
    'columns_types': [INT + PRIMARY_KEY, INT, BOOLEAN, INT]
}

# 项目领域表
REPOS_FIELDS_TABLE_FIELD = {
    'columns': ['rid', 'topics'],
    'columns_types': [INT + PRIMARY_KEY, MEDIUM_STRING_TYPES]
}
# topic表结构
TOPICS_TABLE_FIELD = {
    'columns': ['name', 'descript', 'avi',
                'repos_count', 'is_featured'],
    'columns_types': [SHORT_STRING_TYPES + PRIMARY_KEY, LONG_STRING_TYPES, MEDIUM_STRING_TYPES,
                      INT, BOOLEAN]
}

# topic url表结构
TOPICS_URL_TABLE_FIELD = {
    'columns': ['name', 'topic_url'],
    'columns_types': [SHORT_STRING_TYPES + PRIMARY_KEY, MEDIUM_STRING_TYPES]

}

REPOS_LANGUAGE_PROPORTION_TABLE_FIELD = {
    'columns': ['rid', 'language', 'proportion'],
    'columns_types': [SHORT_STRING_TYPES + PRIMARY_KEY, MEDIUM_STRING_TYPES, INT]
}

# ALL_TABLE_FIELD = {
#     USER_TABLE_NAME: USER_TABLE_FIELD,
#     TALENT_TABLE_NAME: TALENT_TABLE_FIELD,
#     REPOS_INFO_TABLE_NAME: REPOS_IMPORTANT_TABLE_FIELD,
#     REPOS_IMPORTANT_TABLE_NAME: REPOS_IMPORTANT_TABLE_FIELD,
#     TOPICS_TABLE_NAME: TOPICS_TABLE_FIELD
# }

ALL_TABLE_FIELD = {
    USER_TABLE_NAME: USER_TABLE_FIELD,
    ERROR_TABLE_NAME: ERROR_TABLE_FIELD,
    TALENT_TABLE_NAME: TALENT_TABLE_FIELD,
    USER_BLOG_TABLE_NAME: USER_BLOG_TABLE_FIELD,
    USER_LOGIN_NAME_TABLE_NAME: USER_LOGIN_NAME_TABLE_FIELD,
    USER_REPOS_TABLE_NAME: USER_REPOS_TABLE_FIELD,
    USER_ORGANIZATION_TABLE_NAME: USER_ORGANIZATION_TABLE_FIELD,
    ORGANIZATIONS_TABLE_NAME: ORGANIZATIONS_TABLE_FIELD,
    CRAWLED_URL_TABLE_NAME: CRAWLED_URL_TABLE_FIELD,
    TOPICS_TABLE_NAME: TOPICS_TABLE_FIELD,
    TOPICS_URL_TABLE_NAME: TOPICS_URL_TABLE_FIELD,
    USER_RELATIONSHIPS_TABLE_NAME: USER_RELATIONSHIPS_TABLE_FIELD,
    REPOS_FIELDS_TABLE_NAME: REPOS_FIELDS_TABLE_FIELD,
    REPOS_INFO_TABLE_NAME: REPOS_INFO_TABLE_FIELD,
    REPOS_LANGUAGE_PROPORTION_TABLE_NAME: REPOS_LANGUAGE_PROPORTION_TABLE_FIELD,
    REPOS_PARTICIPANTS_CONTRIBUTIONS_TABLE_NAME: REPOS_PARTICIPANTS_CONTRIBUTIONS_TABLE_FIELD,
    REPOS_PARTICIPANTS_TABLE_NAME: REPOS_PARTICIPANTS_TABLE_FIELD,
    REPOS_URL_TABLE_NAME: REPOS_URL_TABLE_FIELD
}



# 级联行为常量
CASCADE = 'CASCADE'
RESTRICT = 'RESTRICT'
NO_ACTION = 'NO ACTION'
SET_NULL = 'SET NULL'
SET_DEFAULT = 'SET DEFAULT'
# 主表-从表映射字典 用于添加外键约束
MASTER_SLAVE_MAPPING_RULE = {
    'master_table': ['', ''],
    'slave_table': ['', ''],
    'foreign_key_column': ['', ''],
    'referenced_column': ['', ],
    'on_delete_action': [''],
    'on_update_action': ['']
}

# 获取各个列的值
master_table_values = MASTER_SLAVE_MAPPING_RULE['master_table']
slave_table_values = MASTER_SLAVE_MAPPING_RULE['slave_table']
foreign_key_column_values = MASTER_SLAVE_MAPPING_RULE['foreign_key_column']
referenced_column_values = MASTER_SLAVE_MAPPING_RULE['referenced_column']
