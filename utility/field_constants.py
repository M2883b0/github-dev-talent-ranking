class UserFields:
    ID = "id"
    NAME = "name"
    EMAIL_ADDRESS = "email_address"
    FOLLOWERS = "followers"
    BIO = "bio"
    REPOS_COUNT = "repos_count"
    COMPANY = "company"
    LOCATION = "location"
    NATION = "nation"


class TalentFields:
    UID = "uid"
    TOPIC = "topic"
    ABILITY = "ability"


class UserBlogFields:
    UID = "uid"
    BLOG_HTML = "blog_html"


class UserLoginNameFields:
    UID = "uid"
    LOGIN_NAME = "login_name"


class UserReposFields:
    UID = "uid"
    REPOS_URL = "repos_url"


class OrganizationFields:
    ORGANIZATION_ID = "organization_id"
    NAME = "name"
    DESCRIPT = "descript"
    LOCATION = "location"
    ORGANIZATION_BLOG_HTML = "organization_blog_html"


class UserOrganizationFields:
    UID = "uid"
    ORGANIZATION_ID = "organization_id"


class UserRelationshipFields:
    UID = "uid"
    RELATED_UID = "related_uid"
    IS_FAN = "is_fan"
    IS_FOLLOWER = "is_follower"
    IS_COLLABORATOR = "is_collaborator"


class ReposParticipantFields:
    UID = "uid"
    RID = "rid"


class ReposInfoFields:
    ID = "id"
    MAIN_LANGUAGE = "main_language"
    DESCRIPT = "descript"
    FORKS_COUNT = "forks_count"
    STARGAZERS_COUNT = "stargazers_count"
    SUBSCRIBERS_COUNT = "subscribers_count"
    IMPORTANCE = "importance"
    TOTAL_CONTRIBUTION_VALUE = "total_contribution_value"
    ISSUE_COUNT = "issue_count"


class ReposUrlFields:
    RID = "rid"
    REPOS_URL = "repos_url"


class ReposLanguageProportionFields:
    RID = "rid"
    LANGUAGE = "language"
    PROPORTION = "proportion"


class ReposParticipantContributionFields:
    RID = "rid"
    UID = "uid"
    IS_OWNER = "is_owner"
    PERSONAL_CONTRIBUTION_VALUE = "personal_contribution_value"


class ReposFieldFields:
    RID = "rid"
    TOPICS = "topics"


class TopicFields:
    NAME = "name"
    DESCRIPT = "descript"
    AVI = "avi"
    REPOS_COUNT = "repos_count"
    IS_FEATURED = "is_featured"


class TopicUrlFields:
    NAME = "name"
    TOPIC_URL = "topic_url"


class SpiderErrorFields:
    URL = "url"
    CODE = "code"
    SPIDER = "spider"
    DETAIL = "detail"


class CrawledUrlFields:
    URL = "url"
