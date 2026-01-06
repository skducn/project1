# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2026-1-6
# Description: 17.1.2同期金额比对 362页
# https://gairuo.com/p/pandas-book-dataset

# 警告：MatplotlibDeprecationWarning: Support for FigureCanvases without a required_interactive_framework
# attribute was deprecated in Matplotlib 3.6 and will be removed two minor releases later. plt.show() 添加这行来显示图形
# 分析：这个警告是由于 matplotlib 版本更新导致的后端框架兼容性问题，matplotlib 3.6 开始弃用不支持 required_interactive_framework 属性的图形后端
# 解决：设置交互式后端 plt.switch_backend('TkAgg')，并分离绘图和显示操作

# date	gmv
# 2020/11/10	100
# 2020/11/9	88
# 2020/11/8	77
# 2020/11/7	65
# 2020/11/6	57
# 2020/11/5	68
# 2019/11/10	44
# 2019/11/9	57
# 2019/11/8	34
# 2019/11/7	88
# 2019/11/6	65
# ********************************************************************************************************************

import pandas as pd
import matplotlib.pyplot as plt

# 需求：实现了同期金额比对的数据处理
# 同期比对原理：将不同年份的相同月日数据分到同一组，通过差值计算实现同期数据对比，用于分析同一时期不同年份的变化趋势

# 设置交互式后端
plt.switch_backend('TkAgg')  # 或 'MacOSX' 等
# TkAgg - 跨平台，兼容性好
# Qt5Agg - 如果安装了 PyQt5
# MacOSX - macOS 系统专用

# 分离绘图和显示操作：先创建图形对象，再显示
result = (pd.read_excel('team.xlsx', sheet_name="Sheet2")
.astype({'date': 'datetime64[ns]'})  # 将date列转换为datetime类型，确保日期格式正确
.set_index('date')  # 设置日期列为索引，便于后续按时间进行分组操作
.groupby([lambda x:x.month, lambda x:x.day], group_keys=False)
# 按月日分组：实现同期对比的关键操作
# lambda x:x.month - 按月份分组
# lambda x:x.day - 按日期分组
# group_keys=False - 避免在索引中添加分组键
.apply(lambda x: x.diff(-1))
# 对每个分组应用差值计算
# diff(-1) - 计算当前值与前一行的差值（向前差分
.loc[lambda x: x.index.year==2020]
# 筛选2020年的数据
# 通过索引的year属性进行年份过滤
)

print(result)
#              gmv
# date
# 2020-11-10  56.0
# 2020-11-09  31.0
# 2020-11-08  43.0
# 2020-11-07 -23.0
# 2020-11-06  -8.0
# 2020-11-05   NaN

# # 显示操作
# ax = result.plot()
# plt.show()




