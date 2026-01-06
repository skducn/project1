# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2026-1-6
# Description: 17.2 数据处理案例 370页
# https://gairuo.com/p/pandas-book-dataset
# ********************************************************************************************************************

import pandas as pd
import matplotlib.pyplot as plt
import faker
f = faker.Faker('zh-cn')

# todo 17.2.2 当月最后一个星期三
# 获取指定月份所有日期的功能

# 创建时间戳对象
t = pd.Timestamp('2020-11-11')  # 指定日期为2020年11月11日

# 时间戳操作
t = t.replace(day=1)  # 快速获取月初日期，将日期修改为当月第一天，即2020年11月1日

# 月份边界
# pd.offsets.MonthEnd() 自动计算月末日期（考虑大小月差异）
# t + pd.offsets.MonthEnd() 计算当月最后一天，通过 MonthEnd() 偏移量实现

# 日期范围
# pd.date_range() 生成连续的日期序列，为后续筛选星期三做准备
index = pd.date_range(start=t, end=(t + pd.offsets.MonthEnd()))  # 成从当月第一天到最后一天的完整日期范围
print(index)  # 输出生成的日期索引

# DatetimeIndex(['2020-11-01', '2020-11-02', '2020-11-03', '2020-11-04',
#                '2020-11-05', '2020-11-06', '2020-11-07', '2020-11-08',
#                '2020-11-09', '2020-11-10', '2020-11-11', '2020-11-12',
#                '2020-11-13', '2020-11-14', '2020-11-15', '2020-11-16',
#                '2020-11-17', '2020-11-18', '2020-11-19', '2020-11-20',
#                '2020-11-21', '2020-11-22', '2020-11-23', '2020-11-24',
#                '2020-11-25', '2020-11-26', '2020-11-27', '2020-11-28',
#                '2020-11-29', '2020-11-30'],
#               dtype='datetime64[ns]', freq='D')

print(pd.DataFrame(index.weekday+1, index=index.date, columns=['weekday'])  # 创建DataFrame，weekday列为星期几（1-7，其中3代表星期三），索引为日期
      .query("weekday==3")  # 筛选出所有星期三的记录
      .tail(1)  # 取最后一条记录（即当月最后一个星期三）
      .index[0] # 获取该记录的日期
)  # 2020-11-25
# index.weekday+1 - 将pandas的weekday（0-6，其中0为星期一）转换为常规的1-7表示法
# index.date - 将datetime索引转换为日期格式作为DataFrame的索引


# 获取当月最后一个星期三
def getCurrMonthLastWednesday():
    t = pd.Timestamp(pd.Timestamp('now'))  # 2026-01-06 11:46:44.324388
    t = t.replace(day=1)
    index = pd.date_range(start=t, end=(t + pd.offsets.MonthEnd()))
    return (pd.DataFrame(index.weekday + 1, index=index.date,
                       columns=['weekday'])
          .query("weekday==3")
          .tail(1)
          .index[0]
          )

print(getCurrMonthLastWednesday())  # 2026-01-28