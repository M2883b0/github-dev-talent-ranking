import math
from functools import reduce


class CalculateSystem:
    def __init__(self):
        self.__alpha1 = None,
        self.__alpha2 = None,
        self.__alpha3 = None,
        self.__alpha4 = None,
        self.__lambda1 = 1.1

    def calculate_repos_importance(self, fork_num, star_num, subscribers_num, issue_num):
        repos_importance = (self.__alpha1 * fork_num + self.__alpha2 * star_num +
                            self.__alpha3 * subscribers_num + self.__alpha4 * issue_num)
        return repos_importance

    def calculate_personal_repos_ability(self, repos_importance, personal_contribution, is_owner):
        if is_owner == 1:
            personal_repos_ability = self.__lambda1 * (repos_importance * personal_contribution)
        elif is_owner == 0:
            personal_repos_ability = repos_importance * personal_contribution
        return personal_repos_ability

    def calculate_topic_ability(self, followers, all_topic_repos_ability, blog = 0, **kargs):
        if all_topic_repos_ability:
            topic_ability = followers / 100 + all_topic_repos_ability + blog
            topic_ability = int(topic_ability)
        else:
            return 0
        return topic_ability

    def calculate_ability(self, followers, ability, blog = 0, **kargs):
        if ability:
            pass
        else:
            ability = 0
        ability = followers / 100 + ability + blog
        ability = int(ability)
        return ability

    def calculate_coefficient(self, mean_fork, mean_star, mean_sub, mean_issue):
        mean_fork = round(mean_fork)
        mean_star = round(mean_star)
        mean_sub = round(mean_sub)
        mean_issue = round(mean_issue)
        numbers = [mean_fork, mean_star, mean_sub, mean_issue]
        lcm = self.__lcm_multiple(numbers)
        self.__alpha1 = lcm / mean_fork
        self.__alpha2 = lcm / mean_star
        self.__alpha3 = lcm / mean_sub
        self.__alpha4 = lcm / mean_issue

    # 计算两个数的 LCM
    def __lcm(self, a, b):
        return abs(a * b) // math.gcd(a, b)

    # 计算多个数的 LCM
    def __lcm_multiple(self, numbers):
        return reduce(self.__lcm, numbers)
