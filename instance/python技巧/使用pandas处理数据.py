# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-1
# Description: 　　pandas是一个强大的数据分析库，特别适合处理表格数据。
# *****************************************************************

import pandas as pd

# 不推荐：使用纯Python字典和列表处理数据
data = {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [25, 30, 35]}
ages = [age for age in data['Age'] if age > 30]

# 推荐：使用pandas处理数据
df = pd.DataFrame(data)
filtered_df = df[df['Age'] > 30]
print(ages)  # 输出: [35]
print(filtered_df)  # 输出:      Name  Age
                 # 2  Charlie   35






