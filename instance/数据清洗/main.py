# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-12-23
# Description: 数据清洗
# http://www.51testing.com/html/47/n-7803847.html
# *****************************************************************

import pandas as pd, numpy as np

df = pd.read_excel("data.xlsx")

print(df.head())

# todo 检查数据基本信息
# 查看数据形状
# print(f"数据形状: {df.shape}")
# # 查看列名
# print(f"列名: {df.columns.tolist()}")
# # 查看数据类型
# print(f"数据类型: \n{df.dtypes}")


# todo 　　处理缺失值

# 检查缺失值
print(df.isnull().sum())

# 填充缺失值
df['计划拜访人次'].fillna(df['计划拜访人次'].mean(), inplace=True)  # 用平均值填充年龄列的缺失值
df['实际拜访人次'].fillna(0, inplace=True)  # 用 0 填充收入列的缺失值

print(df['计划拜访人次'])
print(df['实际拜访人次'])

# 删除含有缺失值的行
df.dropna(subset=['代表'], inplace=True)  # 删除地址列中含有缺失值的行
print(df['代表'])


# todo 　　处理重复值
# 检查重复值
print(df.duplicated().sum())
# 删除重复值
# df.drop_duplicates(inplace=True)


# todo 数据类型转换
# # 将 age 列转换为整数类型
# df['实际拜访率'] = df['实际拜访率'].astype(int)
# # 将 income 列转换为浮点数类型
# df['双A客户实际拜访人次'] = df['双A客户实际拜访人次'].astype(float)

# todo 处理异常值
# 使用 Z-score 方法检测异常值
from scipy import stats
z_scores = np.abs(stats.zscore(df['计划拜访人次']))
df = df[z_scores < 20]  # 保留 Z-score 小于 3 的数据
print(df)


# todo 保存清洗后的数据
# df.to_excel('data.xlsx', index=False)

