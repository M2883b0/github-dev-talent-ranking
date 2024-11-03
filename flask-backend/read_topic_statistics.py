import pandas as pd
import random


# 加载Excel文件
def load_excel(file_path):
    df = pd.read_excel(file_path, index_col=0)
    return df


# 查找与指定属性最相关的属性
def find_most_related_attributes(df, target_attribute, num=5):
    if target_attribute not in df.index:
        return []

    target_row = df.loc[target_attribute]
    related_attributes = []

    for attr, prob in target_row.items():
        if prob > 0 and attr != target_attribute:
            related_attributes.append((attr, prob))

    # 按概率从大到小排序
    related_attributes.sort(key=lambda x: x[1], reverse=True)

    # 返回前num个属性
    if len(related_attributes) >= num:
        return related_attributes[:num]
    else:
        # 如果不足num个，随机找其他的属性凑够num个
        remaining_attributes = [attr for attr in df.index if
                                attr != target_attribute and attr not in [a[0] for a in related_attributes]]
        random.shuffle(remaining_attributes)
        additional_attributes = remaining_attributes[:num - len(related_attributes)]
        for attr in additional_attributes:
            related_attributes.append((attr, 0.0))

        return related_attributes


# 主函数
def main(file_path, target_attribute, num=5):
    df = load_excel(file_path)
    related_attributes = find_most_related_attributes(df, target_attribute, num)

    if related_attributes:
        print(f"与属性 '{target_attribute}' 最相关的属性及概率:")
        for attr, prob in related_attributes:
            print(f"{attr}: {prob:.2f}")
    else:
        print(f"没有找到与属性 '{target_attribute}' 相关的其他属性。")


# 示例文件路径
file_path = r'C:\Users\luo20\Desktop\correlation_matrix.xlsx'
target_attribute = 'python'
num = 5
main(file_path, target_attribute, num)