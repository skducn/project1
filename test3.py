# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-1-7
#  publicKey: 04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249
#  privateKey: 124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62
# *****************************************************************

import re
import random


def generate_all_cases(conditions, num_samples=1):
    """
    生成所有可能的条件组合情况

    参数:
    conditions (list): 条件列表，例如 ['14<= 年龄＜14.5', '22.3<= BMI', '性别=男']
    num_samples (int): 每种情况生成的样本数量

    返回:
    dict: 包含所有情况的样本字典
    """
    # 分离BMI、年龄和性别条件
    bmi_conditions = [c for c in conditions if 'BMI' in c]
    age_conditions = [c for c in conditions if '年龄' in c]
    gender_conditions = [c for c in conditions if '性别' in c]

    # 生成所有可能的条件组合
    cases = {}

    # 生成所有8种可能的组合 (2^3 = 8)
    for bmi_satisfied in [True, False]:
        for age_satisfied in [True, False]:
            for gender_satisfied in [True, False]:
                case_name = get_case_name(bmi_satisfied, age_satisfied, gender_satisfied)
                # print(case_name)
                if  case_name == 'BMI满足且年龄满足且性别满足':
                    case_name = 'satisfied'
                cases[case_name] = [
                    generate_sample(bmi_conditions, age_conditions, gender_conditions,
                                    bmi_satisfied, age_satisfied, gender_satisfied)
                    for _ in range(num_samples)
                ]

    return cases


def get_case_name(bmi_satisfied, age_satisfied, gender_satisfied):
    """生成条件组合的名称"""
    parts = []
    if bmi_satisfied:
        parts.append("BMI满足")
    else:
        parts.append("BMI不满足")

    if age_satisfied:
        parts.append("年龄满足")
    else:
        parts.append("年龄不满足")

    if gender_satisfied:
        parts.append("性别满足")
    else:
        parts.append("性别不满足")

    return "且".join(parts)


def generate_sample(bmi_conditions, age_conditions, gender_conditions,
                    satisfy_bmi, satisfy_age, satisfy_gender):
    """
    生成一个符合指定条件组合的样本

    参数:
    bmi_conditions (list): BMI相关条件
    age_conditions (list): 年龄相关条件
    gender_conditions (list): 性别相关条件
    satisfy_bmi (bool): 是否满足BMI条件
    satisfy_age (bool): 是否满足年龄条件
    satisfy_gender (bool): 是否满足性别条件

    返回:
    dict: 包含BMI、年龄和性别的字典
    """
    # 生成BMI值
    if satisfy_bmi:
        bmi = generate_valid_bmi(bmi_conditions)
    else:
        bmi = generate_invalid_bmi(bmi_conditions)

    # 生成年龄值
    if satisfy_age:
        age = generate_valid_age(age_conditions)
    else:
        age = generate_invalid_age(age_conditions)

    # 生成性别值
    if satisfy_gender:
        gender = generate_valid_gender(gender_conditions)
    else:
        gender = generate_invalid_gender(gender_conditions)

    return {'BMI': bmi, '年龄': age, '性别': gender}


def generate_valid_bmi(conditions):
    """生成符合所有BMI条件的值"""
    if not conditions:
        return round(random.uniform(10.0, 60.0), 1)

    # 解析条件中的BMI范围
    bmi_min = 10.0
    bmi_max = 60.0

    for condition in conditions:
        # 处理类似 "22.3<= BMI" 或 "BMI<25" 的条件
        if '<=' in condition:
            parts = condition.split('<=')
            if 'BMI' in parts[1]:
                bmi_min = max(bmi_min, float(parts[0].strip()))
        elif '>=' in condition:
            parts = condition.split('>=')
            if 'BMI' in parts[0]:
                bmi_min = max(bmi_min, float(parts[1].strip()))
        elif '<' in condition:
            parts = condition.split('<')
            if 'BMI' in parts[0]:
                bmi_max = min(bmi_max, float(parts[1].strip()))
        elif '>' in condition:
            parts = condition.split('>')
            if 'BMI' in parts[0]:
                bmi_max = min(bmi_max, float(parts[1].strip()))

    return round(random.uniform(bmi_min, bmi_max), 1)


def generate_invalid_bmi(conditions):
    """生成不符合所有BMI条件的值"""
    if not conditions:
        return round(random.uniform(10.0, 60.0), 1)

    # 解析条件中的BMI有效范围
    bmi_min = 10.0
    bmi_max = 60.0

    for condition in conditions:
        if '<=' in condition:
            parts = condition.split('<=')
            if 'BMI' in parts[1]:
                bmi_min = max(bmi_min, float(parts[0].strip()))
        elif '>=' in condition:
            parts = condition.split('>=')
            if 'BMI' in parts[0]:
                bmi_min = max(bmi_min, float(parts[1].strip()))
        elif '<' in condition:
            parts = condition.split('<')
            if 'BMI' in parts[0]:
                bmi_max = min(bmi_max, float(parts[1].strip()))
        elif '>' in condition:
            parts = condition.split('>')
            if 'BMI' in parts[0]:
                bmi_max = min(bmi_max, float(parts[1].strip()))

    # 生成范围外的值
    if random.random() < 0.5:
        return round(random.uniform(10.0, bmi_min - 0.1), 1)
    else:
        return round(random.uniform(bmi_max + 0.1, 60.0), 1)


def generate_valid_age(conditions):
    """生成符合所有年龄条件的值"""
    if not conditions:
        return random.randint(0, 120)

    # 解析条件中的年龄范围
    age_min = 0
    age_max = 120

    for condition in conditions:
        # 处理类似 "14<= 年龄＜14.5" 的条件
        if '<=' in condition and '＜' in condition:
            parts = condition.split('＜')
            lower_part = parts[0].split('<=')
            age_min = max(age_min, float(lower_part[0].strip()))
            age_max = min(age_max, float(parts[1].strip()))
        elif '<=' in condition:
            parts = condition.split('<=')
            if '年龄' in parts[1]:
                age_min = max(age_min, float(parts[0].strip()))
        elif '>=' in condition:
            parts = condition.split('>=')
            if '年龄' in parts[0]:
                age_min = max(age_min, float(parts[1].strip()))
        elif '<' in condition:
            parts = condition.split('<')
            if '年龄' in parts[0]:
                age_max = min(age_max, float(parts[1].strip()))
        elif '>' in condition:
            parts = condition.split('>')
            if '年龄' in parts[0]:
                age_max = min(age_max, float(parts[1].strip()))

    # 生成范围内的随机年龄（保留一位小数）
    return round(random.uniform(age_min, age_max), 1)


def generate_invalid_age(conditions):
    """生成不符合所有年龄条件的值"""
    if not conditions:
        return random.randint(0, 120)

    # 解析条件中的年龄有效范围
    age_min = 0
    age_max = 120

    for condition in conditions:
        if '<=' in condition and '＜' in condition:
            parts = condition.split('＜')
            lower_part = parts[0].split('<=')
            age_min = max(age_min, float(lower_part[0].strip()))
            age_max = min(age_max, float(parts[1].strip()))
        elif '<=' in condition:
            parts = condition.split('<=')
            if '年龄' in parts[1]:
                age_min = max(age_min, float(parts[0].strip()))
        elif '>=' in condition:
            parts = condition.split('>=')
            if '年龄' in parts[0]:
                age_min = max(age_min, float(parts[1].strip()))
        elif '<' in condition:
            parts = condition.split('<')
            if '年龄' in parts[0]:
                age_max = min(age_max, float(parts[1].strip()))
        elif '>' in condition:
            parts = condition.split('>')
            if '年龄' in parts[0]:
                age_max = min(age_max, float(parts[1].strip()))

    # 生成范围外的值
    if random.random() < 0.5:
        return round(random.uniform(0, age_min - 0.1), 1)
    else:
        return round(random.uniform(age_max + 0.1, 120), 1)


def generate_valid_gender(conditions):
    """生成符合所有性别条件的值"""
    if not conditions:
        return random.choice(['男', '女'])

    # 提取性别条件中的值
    valid_genders = set()
    for condition in conditions:
        if '=' in condition:
            parts = condition.split('=')
            if '性别' in parts[0]:
                valid_genders.add(parts[1].strip())

    if valid_genders:
        return random.choice(list(valid_genders))
    else:
        return random.choice(['男', '女'])


def generate_invalid_gender(conditions):
    """生成不符合所有性别条件的值"""
    if not conditions:
        return random.choice(['男', '女'])

    # 提取性别条件中的值
    invalid_genders = {'男', '女'}
    for condition in conditions:
        if '=' in condition:
            parts = condition.split('=')
            if '性别' in parts[0]:
                invalid_genders.discard(parts[1].strip())

    if invalid_genders:
        return random.choice(list(invalid_genders))
    else:
        return random.choice(['其他'])


# 使用示例
if __name__ == "__main__":
    # 条件列表
    conditions = ['14<= 年龄＜14.5', '22.3<= BMI', '性别=男']

    try:
        # 生成每种情况的样本
        cases = generate_all_cases(conditions)
        print(cases)

        # # 打印结果
        # for case_name, samples in cases.items():
        #     print(f"\n情况: {case_name}")
        #     for i, sample in enumerate(samples, 1):
        #         print(f"样本 {i}: {sample}")

    except ValueError as e:
        print(f"错误: {e}")




# import json
# d_query = {'id': 123}
# # d_query = json.dumps(d_query)
# # print(d_query['id'])
# key = list(d_query.keys())[0]
# print(key)
# d_query = {'id':123}
# print(list(d_query.keys())[0])

# pip install selenium tensorflow numpy scikit-learn
# # 3. 数据准备
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder
#
#
# # 3. 数据准备
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder
#
# # 2. 使用Selenium提取网页元素特征
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import numpy as np
# from PO.WebPO import *
#
# Web_PO = WebPO("chrome")
#
# # # print("1.1 打开网站".center(100, "-"))
# # Web_PO.openURL("http://192.168.0.243:5000/")
# Web_PO.openURL("http://192.168.0.203:30080/login?redirect=/index")
#
#
# # 3. 数据准备
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder
#
#
# # 4. 构建RNN模型
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense
#
#
# # 提取按钮元素的特征
# # 提取按钮元素的特征
# buttons = Web_PO.test1()
# predicted_labels = []
#
# for button in buttons:
#     text = button.text
#     size = button.size
#     location = button.location
#
#     # 将特征转换为数值
#     feature = [len(text), size['width'], size['height'], location['x'], location['y']]
#     feature = np.array(feature).reshape(1, -1)
#
#     # 使用模型进行预测
#     model = Sequential()
#     prediction = model.predict(feature)
#     label_encoder = LabelEncoder()
#     predicted_label = label_encoder.inverse_transform([np.argmax(prediction)])
#     predicted_labels.append(predicted_label[0])
#
# # 输出预测结果
# for i, button in enumerate(buttons):
#     print(f'Button {i}: Predicted Label = {predicted_labels[i]}')
#
# # 关闭浏览器
# Web_PO.quit()