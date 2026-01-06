# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2026-1-6
# Description: 17.1.1 链式方法 360页
# https://gairuo.com/p/pandas-book-dataset
# ********************************************************************************************************************

import pandas as pd

# 需求1：找出各团队第一位同学，然后从中筛选出平均分大于60分的同学，输出团队和团队平均分。
# todo 普通方法
df = pd.read_excel('https://gairuo.com/file/data/dataset/team.xlsx')
df = df.groupby('team').first()
print(18, df)
# name  Q1  Q2  Q3  Q4
# team
# A       Ack  57  60  18  84
# B      Acob  61  95  94   8
# C      Arry  36  37  37  57
# D       Oah  65  49  61  86
# E     Liver  89  21  24  64

# 方法1：使用 numeric_only 参数指定只对数值列计算平均值
df['avg'] = df.mean(axis=1, numeric_only=True)  # df['avg'] = df.mean(1)
# # 方法2：只选择数值列来计算平均值
# numeric_cols = df.select_dtypes(include='number').columns
# df['avg'] = df[numeric_cols].mean(axis=1)
print(26, df)
# name  Q1  Q2  Q3  Q4    avg
# team
# A       Ack  57  60  18  84  54.75
# B      Acob  61  95  94   8  64.50
# C      Arry  36  37  37  57  41.75
# D       Oah  65  49  61  86  65.25
# E     Liver  89  21  24  64  49.50

df = df.reset_index().set_index('name')
print(29, df)
# team  Q1  Q2  Q3  Q4    avg
# name
# Ack      A  57  60  18  84  54.75
# Acob     B  61  95  94   8  64.50
# Arry     C  36  37  37  57  41.75
# Oah      D  65  49  61  86  65.25
# Liver    E  89  21  24  64  49.50

df = df[df.avg > 60]
print(32, df)
# team  Q1  Q2  Q3  Q4    avg
# name
# Acob    B  61  95  94   8  64.50
# Oah     D  65  49  61  86  65.25


df = df.loc[:, ['team', 'avg']]
print(df)
# name
# Acob    B  64.50
# Oah     D  65.25

print("~~~~~~~~~~~~~~~~~~~~~~")

# todo 链式方法
# print(pd.read_excel('https://gairuo.com/file/data/dataset/team.xlsx')
print(pd.read_excel('team.xlsx')
.groupby('team').first()
.assign(avg=lambda x:x.mean(axis=1, numeric_only=True))
.reset_index().set_index('name')
.query('avg>60')
.loc[:, ['team', 'avg']]
)

