# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2026-1-6
# Description: 17.2 数据处理案例 370页
# https://gairuo.com/p/pandas-book-dataset

# 警告：MatplotlibDeprecationWarning: Support for FigureCanvases without a required_interactive_framework
# attribute was deprecated in Matplotlib 3.6 and will be removed two minor releases later. plt.show() 添加这行来显示图形
# 分析：这个警告是由于 matplotlib 版本更新导致的后端框架兼容性问题，matplotlib 3.6 开始弃用不支持 required_interactive_framework 属性的图形后端
# 解决：设置交互式后端 plt.switch_backend('TkAgg')，并分离绘图和显示操作
# ********************************************************************************************************************

import pandas as pd
import matplotlib.pyplot as plt
import faker
f = faker.Faker('zh-cn')

# todo 17.2.1 剧组表格道具
df = pd.DataFrame({
    '客户姓名': [f.name() for i in range(10)],
    '年龄': [f.random_int(25, 40) for i in range(10)],
    '最后去电时间': [f.date_between(start_date='-1y', end_date='today').strftime('%Y年%m月%d日') for i in range(10)],
    '意向': [f.random_element(('有', '无')) for i in range(10)],
    '地址': [f.street_address() for i in range(10)],
})
print(df)


# print(pd.DataFrame()
#     .assign(客户姓名= [f.name() for i in range(10)])
#     .assign(年龄= [f.random_int(25, 40) for i in range(10)])
#     .assign(最后去电时间= [f.date_between(start_date='-1y', end_date='today').strftime('%Y年%m月%d日') for i in range(10)])
#     .assign(意向= [f.random_element(('有', '无')) for i in range(10)])
#     .assign(地址= [f.street_address() for i in range(10)])
# )

# 覆盖
# df.to_excel('team.xlsx', sheet_name='客户信息', index=False)

# 追加，使用ExcelWriter以追加模式写入指定工作表
# mode='a'：以追加模式打开文件，不会影响其他工作表
# engine='openpyxl'：指定Excel引擎，支持追加模式
# if_sheet_exists='replace'：如果工作表已存在则替换，但不影响其他工作表 ， 如果new，不替换。
with pd.ExcelWriter('team.xlsx', mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
    df.to_excel(writer, sheet_name='客户信息', index=False)


