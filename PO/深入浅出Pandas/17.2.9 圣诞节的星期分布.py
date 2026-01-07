# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2026-1-6
# Description: 17.2.9 圣诞节的星期分布 379页
# https://gairuo.com/p/pandas-book-dataset

# ********************************************************************************************************************
import pandas as pd
import faker
import matplotlib.pyplot as plt

result = (pd.Series(pd.date_range('1920', '2025'))
      .loc[lambda s: (s.dt.month==12) & (s.dt.day==25)]
      .dt.day_of_week
      .add(1)
      .value_counts()
      .sort_values()
     )


# # 显示操作
ax = result.plot()
plt.show()