# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2026-1-6
# Description: 17.2.3 同组数据转为同一行 372页
# https://gairuo.com/p/pandas-book-dataset

# 分组聚合：使用 groupby().apply() 将同组的多个值合并为一个字符串
# 字符串操作：','.join() 将多个值连接成逗号分隔的字符串
# 展开操作：str.split(expand=True) 将字符串列展开为多个列
# ********************************************************************************************************************

import pandas as pd
df = pd.read_excel('team.xlsx', sheet_name="Sheet3")
# 数据透视规则方法
# df = df.pivot(index=['A','B','C'], columns='D', values='D')
# print(df)

# D         2001    2002    2003    2004    2005
# A B  C
# a b1 c  2001.0     NaN  2003.0     NaN  2005.0
#   b2 c  2001.0  2002.0  2003.0  2004.0     NaN

# 链式方法
print(df.groupby(['A','B','C'])
      .apply(lambda x: ','.join(x.D.astype(str)))
      )
# A  B   C
# a  b1  c         2001,2003,2005
#    b2  c    2001,2002,2003,2004
# dtype: object

# 链式方法，优化
print(df.groupby(['A','B','C'])
      .apply(lambda x: ','.join(x.D.astype(str)))  # 对每个分组应用函数，将D列的值转换为字符串并用逗号连接成一个字符串
      .str.split(",",expand=True)  # 将连接的字符串按逗号分割，并展开为多列
)
#            0     1     2     3
# A B  C
# a b1 c  2001  2003  2005  None
#   b2 c  2001  2002  2003  2004


