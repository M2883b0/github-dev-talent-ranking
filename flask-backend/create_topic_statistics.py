import csv
from collections import defaultdict
import pandas as pd


# 读取CSV文件
def read_csv(file_path):
    user_attributes = defaultdict(set)
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过表头
        for row in reader:
            user_id, attribute = row
            user_attributes[user_id].add(attribute)
    return user_attributes


# 获取所有属性
def get_all_attributes(user_attributes):
    all_attributes = set()
    for attributes in user_attributes.values():
        all_attributes.update(attributes)
    return sorted(all_attributes)


# 计算属性之间的相关性
def calculate_correlation(user_attributes, all_attributes):
    n = len(all_attributes)
    correlation_matrix = [[0] * n for _ in range(n)]

    attribute_index = {attr: i for i, attr in enumerate(all_attributes)}

    for user_id, attributes in user_attributes.items():
        for attr1 in attributes:
            for attr2 in attributes:
                i = attribute_index[attr1]
                j = attribute_index[attr2]
                correlation_matrix[i][j] += 1

    # 计算概率
    for i in range(n):
        total_with_attr_i = correlation_matrix[i][i]
        for j in range(n):
            if total_with_attr_i > 0:
                correlation_matrix[i][j] /= total_with_attr_i
            else:
                correlation_matrix[i][j] = 0.0

    return correlation_matrix, attribute_index


# 将矩阵和属性列表保存为Excel文件
def save_to_excel(correlation_matrix, all_attributes, output_file):
    df = pd.DataFrame(correlation_matrix, index=all_attributes, columns=all_attributes)
    df.to_excel(output_file)


# 主函数
def main(file_path, output_file):
    user_attributes = read_csv(file_path)
    all_attributes = get_all_attributes(user_attributes)
    correlation_matrix, attribute_index = calculate_correlation(user_attributes, all_attributes)

    # 打印结果
    print("所有属性:", all_attributes)

    # 保存到Excel文件
    save_to_excel(correlation_matrix, all_attributes, output_file)



# 示例文件路径
file_path = r'C:\Users\luo20\Desktop\repos_fields.csv'
output_file = r'C:\Users\luo20\Desktop\correlation_matrix.xlsx'
main(file_path,output_file)


# TODO: 等项目爬完,要把main_lanuage表，加入repos_fields表中。这时导出repos_fields的csv，再进行计算NxN的概率矩阵
#  注意：main_lanuage加入加入repos_fields表中，要判断，原本是否项目中就加入了编程语言作为topic