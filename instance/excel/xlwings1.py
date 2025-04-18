# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-4-198
# Description:
# xlwings 是一个用于在 Python 和 Excel 之间进行交互的库。它允许你使用 Python 代码来自动化 Excel 任务，也可以在 Excel 中调用 Python 脚本。
# 主要功能
# 读写 Excel 文件：能够读取和修改 Excel 文件中的数据，包括单元格、工作表、图表等。
# 自动化操作：可以自动化执行重复性的 Excel 任务，如数据处理、格式设置等。
# Excel 与 Python 交互：在 Excel 中调用 Python 函数，或者在 Python 中控制 Excel 应用程序。
# *****************************************************************

import xlwings as xw

# 打开一个新的 Excel 应用程序实例
app = xw.App(visible=True)
# 新建一个工作簿
wb = app.books.add()
# 选择第一个工作表
sheet = wb.sheets[0]
# 在 A1 单元格写入数据
sheet.range('A1').value = 'Hello, xlwings!'
# 保存工作簿
wb.save('example.xlsx')
# 关闭工作簿
wb.close()
# 退出 Excel 应用程序
app.quit()












