# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2020-12-8
# Description   : openpyxl 应用层
# https://pypi.org/project/openpyxl/#files
# https://foss.heptapod.net/openpyxl/openpyxl/-/issues
# https://www.cnblogs.com/MrLJC/p/3715783.html
# http://www.cnblogs.com/jane0912/p/4195253.html
# https://www.cnblogs.com/zhoujie/p/python18.html
# https://blog.csdn.net/samed/article/details/49936409

# *********************************************************************

from PO.OpenpyxlPO import *

# todo【工作表】

# 1.1 新建 Openpyxl_PO = OpenpyxlPO("1212.xlsx")
# 		Openpyxl_PO = OpenpyxlPO("1212.xlsx",l_sheet=['Sheet1','Sheet2','Sheet3'])
# 1.2 打开 open()
# 1.3 保存 save()
# 1.4 工作表 sh()
# 1.5 获取工作表 getL_sheet()
# 1.6 切换工作表 switchSheet("Sheet2")
# 1.7 添加工作表 addSheet("Sheet1", overwrite=True)
# 1.8 删除工作表 delSheet("Sheet1")
# 1.9 重命名工作表 renameSheet("sheet1", "sheet2")

# print("1.1 新建".center(100, "-"))
Openpyxl_PO = OpenpyxlPO("/Users/linghuchong/Downloads/51/Python/project/PO/data/11.xlsx")
# Openpyxl_PO = OpenpyxlPO("/Users/linghuchong/Downloads/51/Python/project/PO/data/1212.xlsx", l_sheet=['Sheet1','Sheet2','Sheet3'])

# print("1.2 打开".center(100, "-"))
# Openpyxl_PO.open()

# print("1.3 保存".center(100, "-"))
# Openpyxl_PO.save()

# print("1.5 获取工作表".center(100, "-"))
# Openpyxl_PO.getL_sheet()

# print("1.7 添加工作表".center(100, "-"))
# Openpyxl_PO.addSheet("Sheet1", overwrite=True)
# Openpyxl_PO.addSheet("Sheet1", overwrite=False)

# print("1.8 删除工作表".center(100, "-"))
# Openpyxl_PO.delSheet("test")

# print("1.9 重命名工作表".center(100, "-"))
# Openpyxl_PO.renameSheet("hello", "test")


# todo【操作数据】

# 2.0 在第N行前插入多行空白（优化版）
# 	insertNullRow(3)  在第3行前插入1行空白
# 	insertNullRow(3，5)  在第3行前插入5行空白
# 2.1 在第N列前插入多列空白（优化版）
# 	insertNullCol(3) 在第3列前插入1列空白
# 	insertNullCol(3,5)  在第3列前插入5列空白
# 2.2 设置单元格
# 	setCell(1, 2, "hello") # 将第一行B列写入hello
# 	setCell(1, 'B', "john") # 将第一行第三列写入john
# 2.3 插入行数据 insertRow({2: ["金浩", "101", "102"]})
# 2.4 更新行数据 setRows({2: ["金浩", "101", "102"], 5: ["yoyo", "123", "666"]})
# 2.5 追加行数据 appendRows([['姓名', '电话'], ['毛泽东', 15266606298]])
# 2.6 插入列数据 insertCol({"a": ["姓名", "张三", "李四"], "c": ["年龄", "55", "34"]})
# 2.7 更新列数据 setCol({"A": ["公司", "百度"], "F": ["学校", "清华大学"]})
# 2.8 追加列数据 appendCols([["姓名", "张三", "李四"], ["年龄", "55", "34"]])
# 2.9 清空行 clsRow(2)  # 清空第2行
# 2.10 清空列
#     clsCol(2, clear_header=True)  # 清空第2列
#     clsCol(2, clear_header=False)  # 清空第2列,保留列标签
# 2.11 删除连续行 delRow(2, 3)  # 删除从第二行开始连续三行数据 （即删除2，3，4行）
# 2.12 删除连续列 delCol(2, 3)  # 删除从第二列开始连续三列数据 （即删除2，3，4列）
# 2.13 移动区域 moveBlock(rows, cols, 'C1:D2')
# 2.14 将excel中标题（第一行字段）排序（从小打大）sortFields()


# print("2.0 在第N行前插入多行空白".center(100, "-"))
# Openpyxl_PO.insertNullRow(3)  # 在第3行前插入1行空白
# Openpyxl_PO.insertNullRow(3, 5)  # 在第3行前插入5行空白

# print("2.1 在第N列前插入多列空白".center(100, "-"))
# Openpyxl_PO.insertNullCol(3)  # 在第3列前插入1列空白
# Openpyxl_PO.insertNullCol(3, 5)  # 在第3列前插入5列空白

# print("2.2 更新单元格".center(100, "-"))
# Openpyxl_PO.setCell(1, 'B', "hello") # 将第一行B列写入hello
# Openpyxl_PO.setCell(1, 3, "john") # 将第一行第三列写入john

# print("2.3 插入行数据".center(100, "-"))
# Openpyxl_PO.insertRow({2: ["金浩", "101", "102"]})

# print("2.4 更新行数据".center(100, "-"))
# Openpyxl_PO.setRow({2: ["金浩", "101", "102"], 5: ["yoyo", "123", "666"]})

# print("2.5 追加行数据".center(100, "-"))
# Openpyxl_PO.appendRow([['姓名', '电话', '成绩', '学科'], ['毛泽东', 15266606298, 14, '化学'], ['周恩来', 15201077791, 78, '美术']])

# print("2.6 插入列数据".center(100, "-"))
# Openpyxl_PO.insertCol({"a": ["姓名", "张三", "李四"], "c": ["年龄", "55", "34"]})
# Openpyxl_PO.insertCol({2: ["姓名", "张三", "李四"], 3: ["年龄2", "552", "343"]})

# print("2.7 更新列数据".center(100, "-"))
# Openpyxl_PO.setCol({"A": [None, "k1", 666, "777"], "C": [None, "888", None, "999"]})
# Openpyxl_PO.setCol({1: [None, "k1", 1212, "777"], 3: [None, "888", None, "56789"]})

# print("2.8 追加列数据".center(100, "-"))
# Openpyxl_PO.appendCol([["test", "张三", "李四"], ["dev", "55", "34"]])

# print("2.9 清空行".center(100, "-"))
# Openpyxl_PO.clsRow(2)  # 清空第2行

# print("2.10 清空列".center(100, "-"))
# Openpyxl_PO.clsCol(2, clear_header=True)  # 清空第2列
# Openpyxl_PO.clsCol(2, clear_header=False)  # 清空第2列,保留列标签

# print("2.11 删除行".center(100, "-"))
# Openpyxl_PO.delRow(2)  # 删除第2行
# Openpyxl_PO.delRow(2, 3)  # 删除第2行之连续3行（删除2，3，4行）
#
# print("2.12 删除列".center(100, "-"))
# Openpyxl_PO.delCol(1, 2)  # 删除第1列之连续2列（删除1，2列）
# Openpyxl_PO.delCol('D', 1)  # 删除第D列之连续1列（删除D列）

# print("2.13 移动区域".center(100, "-"))
# Openpyxl_PO.moveBlock('C1:D2', 3, 2)

# print("2。14 将excel中标题（第一行字段）排序（从小打大）".center(100, "-"))
# Openpyxl_PO.sortColHeader("hello")


# todo【样式】

# 3.0 设置列宽
# 	setColWidth(1, 20) # 设置第1列宽度20
# 	setColWidth('C', 30) # 设置第f列宽度30
# 3.1 设置行高与列宽
# 	setRowColSize([(3, 30), (5, 40)], None)  # 设置第三行行高30，第五行行高40
# 	setRowColSize(None, [('a', 22), ('C', 33)])  # 设置第a列宽22, 第c列宽33
# 	setRowColSize([(3, 30), (5, 40)], [('a', 22), ('C', 33)])  # 设置第三行行高30，第五行行高40, 设置第a列宽22, 第c列宽33
# 3.2 设置所有单元格的行高与列宽 setAllSize(30, 20) //设置所有单元格高30，宽20
# 3.3 设置自动换行 setWordWrap()
# 3.4 冻结窗口 setFreezePanes(）
# 	setFreezePanes('A2') # 冻结首行    A表示不冻结列，2表示冻结首行
# 	setFreezePanes('B1')  # 冻结第A列。  B表示冻结A列，1表示不冻结行
# 	setFreezePanes('B2')  # 冻结第1行和第A列。
# 	setFreezePanes('C3')  # 冻结第1、2行和第B列。  C表示冻结A、B列，3表示冻结第1、2行
# 3.5 设置单元格对齐样式  setAlignment(5, 4, 'center', 'center')
# 	setAlignment(5, 4, horizontal="center", vertical="center") # 设置第5行第4列居中对齐
# 	setAlignment(2, "E", vertical="top", wrap_text=True) # 设置第5行F列顶部对齐并自动换行
# 3.6 设置单行多列对齐样式
# 	setRowColAlignment(5, [1,4], 'center', 'center') # 第5行第1,4列居中
# 	setRowColAlignment(1, ["c", "e"], 'center', 'top')  # 第一行第c,e列居中
# 	setRowColAlignment(1, "all", 'center', 'center')  # 第1行全部居中
# 3.7 设置所有单元格对齐样式 setAllAlignment('center', 'center')
# 3.8 设置筛选列
# 	setFilterCol("all") # 全部筛选,
# 	setFilterCol("") # 取消筛选
# 	setFilterCol("A2") # 对A2筛选
# 3.9 设置单元格字体（字体、字号、粗斜体、下划线、颜色）
# setCellFont(1, 1, name=u'微软雅黑', size=16, bold=True, italic=True, color="000000")
# 3.10 设置单行多列字体
# 	setRowColFont(2, ["b", "D"],name="微软雅黑",size=16, bold=False, italic=False, color="000000")  # 第1行第b-h列
# 	setRowColFont(3, "all")  # 第3行
# 3.11 设置所有单元格字体  setAllCellFont(color="000000")
# 3.12 设置单元格边框 setBorder(1, 2, left = ['thin','ff0000'], right = ['thick','ff0000'], top = ['thin','ff0000'],bottom = ['thick','ff0000'])
#
# 3.13 设置单元格填充渐变色 setGradientFill(3, 3, stop=["FFFFFF", "99ccff", "000000"])
#
# 3.14 设置单元格背景色".center(100, "-"))
# 	setBackgroundColor(2, 1, "ff0000")  # 设置第五行第1列设置红色
# 	setBackgroundColor(2, "c", "0000FF")  # 设置第五行e列设置红色
# 	setBackgroundColor(2, 1, clear_color=True)  # 清除第5行第1列的背景色
# 	setBackgroundColor(2, "c", clear_color=True)  # 清除第5行d列的背景色
# 3.15 设置单行多列背景色
# 	setRowColBackgroundColor(2, ['b', 'd'], "ff0000") # 设置第2行第b，c，d列背景色
# 	etRowColBackgroundColor(1, "all", "ff0000")  # 设置第7行所有列背景色
# 	setRowColBackgroundColor(2, ['B', 'D'], clear_color=True)  # 清除第2行第b，c，d列背景色
# 	setRowColBackgroundColor(1, "all", clear_color=True)  #  清除第1行所有列背景色
# 3.16 设置所有单元格背景色
# 	setAllBackgroundColor("ff0000")  # 设置所有单元格背景色
# 	setAllBackgroundColor(clear_color=True)  # 清除所有单元格背景色
# 3.17 设置整行(可间隔)背景色
# 	setBandRowsColor(5, 0, "ff0000")  # 从第5行开始每行颜色标红色
# 	setBandRowsColor(3, 1, "ff0000")  # 从第3行开始每隔1行颜色标红色
# 	setBandRowsColor(3, 1, clear_color=True) # 清除从第3行开始每隔1行的背景色
# 	setBandRowsColor(5, 0, clear_color=True) # 清除从第5行开始每行颜色标红色
# 3.18 设置整列(可间隔)背景色
# 	setBandColsColor(2, 0, "ff0000")  # 从第2列开始每列颜色为红色
# 	setBandColsColor(2, 1, "ff0000")  # 从第2列开始每隔1列设置颜色为红色
# 	setBandColsColor(2, 1, clear_color=True) # 清除从第2列开始每隔1列的背景色
# 	setBandColsColor(2, 0, clear_color=True)  # 从第2列开始每列颜色为红色
# 3.19 设置工作表背景颜色
# 	setSheetColor("FF0000")
# 	setSheetColor(clear_color=True)

# print("3.0 设置列宽".center(100, "-"))
# Openpyxl_PO.setColWidth(1, 20)  # 设置第1列宽度20
# Openpyxl_PO.setColWidth('C', 30)  # 设置第f列宽度30

# print("3.1 设置行高与列宽".center(100, "-"))
# Openpyxl_PO.setRowColSize([(3, 30), (5, 40)], None)  # 设置第三行行高30，第五行行高40
# Openpyxl_PO.setRowColSize(None, [('a', 22), ('C', 33)])  # 设置第a列宽22, 第c列宽33
# Openpyxl_PO.setRowColSize([(3, 30), (5, 40)], [('a', 22), ('C', 33)])  # 设置第三行行高30，第五行行高40, 设置第a列宽22, 第c列宽33

# print("3.2 设置所有单元格的行高与列宽".center(100, "-"))
# Openpyxl_PO.setAllSize(20, 10)  # 设置所有单元格高30，宽20

# print("3.3 设置自动换行".center(100, "-"))
# Openpyxl_PO.setWrapText()

# print(3.4 冻结窗口".center(100, "-"))
# Openpyxl_PO.setFreezePanes('A2') # 冻结首行    A表示不冻结列，2表示冻结首行
# Openpyxl_PO.setFreezePanes('B1')  # 冻结第A列。  B表示冻结A列，1表示不冻结行
# Openpyxl_PO.setFreezePanes('B2')  # 冻结第1行和第A列。
# Openpyxl_PO.setFreezePanes('C3')  # 冻结第1、2行和第B列。  C表示冻结A、B列，3表示冻结第1、2行

# print("3.5 设置单元格对齐样式".center(100, "-"))
# Openpyxl_PO.setAlignment(5, 4, horizontal="center", vertical="center") # 设置第5行第4列居中对齐
# Openpyxl_PO.setAlignment(2, "E", vertical="top", wrap_text=True) # 设置第5行F列顶部对齐并自动换行

# print("3.6 设置单行多列对齐样式".center(100, "-"))
# Openpyxl_PO.setRowColAlignment(1, ["c", "e"], 'center', 'top')  # 第一行第c,e列居中
# Openpyxl_PO.setRowColAlignment(1, "all", 'center', 'center')  # 第1行全部居中

# print("3.7 设置所有单元格对齐样式".center(100, "-"))
# Openpyxl_PO.setAllAlignment('center', 'center')

# print("3.8 设置筛选列".center(100, "-"))
# Openpyxl_PO.setFilterCol("all")  # 全部筛选
# Openpyxl_PO.setFilterCol("") # 取消筛选
# Openpyxl_PO.setFilterCol("B1") # 对A2筛选

# print("3.9 设置单元格字体（字体、字号、粗斜体、下划线、颜色）".center(100, "-"))
# Openpyxl_PO.setCellFont(1, 2)  # 设置第一行第六列字体（默认微软雅黑字号16粗体）
# Openpyxl_PO.setCellFont(2, "f")  # 设置第一行第f列字体（默认微软雅黑字号16粗体）
# Openpyxl_PO.setCellFont(2, "c", name="微软雅黑",size=16, bold=True, color="ff0000")
# Openpyxl_PO.setCellFont(5, "f", size=14, bold=True)

# print("3.10 设置单行多列字体".center(100, "-"))
# Openpyxl_PO.setRowColFont(2, ["b", "D"],name="微软雅黑",size=16, bold=False, italic=False, color="000000")  # 第1行第b-h列
# Openpyxl_PO.setRowColFont(3, "all")  # 第3行

# print("3.11 设置所有单元格字体".center(100, "-"))
# Openpyxl_PO.setAllFont()

# print("3.12 设置单元格边框".center(100, "-"))
# Openpyxl_PO.setBorder(1, 2, left = ['thin','ff0000'], right = ['thick','ff0000'], top = ['thin','ff0000'],bottom = ['thick','ff0000'])

# print("3.13 设置单元格填充渐变色".center(100, "-"))
# Openpyxl_PO.setGradientFill(3, 3, stop=["FFFFFF", "99ccff", "000000"]) # 设置第3行第3列的渐变色
# Openpyxl_PO.setGradientFill(2, "C", stop=["FF0000", "00FF00", "0000FF"]) # 设置第2行C列的渐变色

# print("3.14 设置单元格背景色".center(100, "-"))
# Openpyxl_PO.setBackgroundColor(2, 1, "ff0000")  # 设置第五行第1列设置红色
# Openpyxl_PO.setBackgroundColor(2, "c", "0000FF")  # 设置第五行e列设置红色
# Openpyxl_PO.setBackgroundColor(2, 1, clear_color=True)  # 清除第5行第1列的背景色
# Openpyxl_PO.setBackgroundColor(2, "c", clear_color=True)  # 清除第5行d列的背景色

# print("3.15 设置单行多列背景色".center(100, "-"))
# Openpyxl_PO.setRowColBackgroundColor(2, ['b', 'd'], "ff0000") # 设置第2行第b，c，d列背景色
# Openpyxl_PO.setRowColBackgroundColor(1, "all", "ff0000")  # 设置第7行所有列背景色
# Openpyxl_PO.setRowColBackgroundColor(2, ['B', 'D'], clear_color=True)  # 清除第2行第b，c，d列背景色
# Openpyxl_PO.setRowColBackgroundColor(1, "all", clear_color=True)  #  清除第1行所有列背景色

# print("3.16 设置所有单元格背景色".center(100, "-"))
# Openpyxl_PO.setAllBackgroundColor("ff0000")  # 设置所有单元格背景色
# Openpyxl_PO.setAllBackgroundColor(clear_color=True)  # 清除所有单元格背景色

# print("3.17 设置整行(可间隔)背景色".center(100, "-"))
# Openpyxl_PO.setBandRowsColor(5, 0, "ff0000")  # 从第5行开始每行颜色标红色
# Openpyxl_PO.setBandRowsColor(3, 1, "ff0000")  # 从第3行开始每隔1行颜色标红色
# Openpyxl_PO.setBandRowsColor(3, 1, clear_color=True) # 清除从第3行开始每隔1行的背景色
# Openpyxl_PO.setBandRowsColor(5, 0, clear_color=True) # 清除从第5行开始每行颜色标红色

# print("3.18 设置整列(可间隔)背景色".center(100, "-"))
# Openpyxl_PO.setBandColsColor(2, 0, "ff0000")  # 从第2列开始每列颜色为红色
# Openpyxl_PO.setBandColsColor(2, 1, "ff0000")  # 从第2列开始每隔1列设置颜色为红色
# Openpyxl_PO.setBandColsColor(2, 1, clear_color=True) # 清除从第2列开始每隔1列的背景色
# Openpyxl_PO.setBandColsColor(2, 0, clear_color=True)  # 从第2列开始每列颜色为红色

# print("3.19 设置工作表背景颜色".center(100, "-"))
# Openpyxl_PO.setSheetColor("FF0000")
# Openpyxl_PO.setSheetColor(clear_color=True)  # 清除工作表标签颜色


# todo 【获取】

# 4.1 获取总行列数 getL_shape()  # [5,10]
# 4.2 获取单元格的值 getCell(3,2)  //获取第3行第2列的值
# 4.3 获取一行数据 getL_row(2) # 获取第2行值
# 4.4 获取一列数据
# 	getL_col(2))  # ['高地', 40, 44, 50, 30, 25, 150]
# 	getL_col('B'))  # ['高地', 40, 44, 50, 30, 25, 150]
# 4.5 获取行数据 getLL_row()  # [['状态', '名字'],['ok', 'jinhao']...]
#
# 4.6 获取带行号的行数据 getD_rowNumber_row()  # { 2 : ['状态', '名字'], 3 : ['ok', 'jinhao']...}
# 4.7 获取部分列的行数据
# 	getLL_rowOfPartialCol([1, 3])   # [['Number具体数', 'jinhaoyoyo'], [2, 30], [3, 10]] //获取1和3列的行数据
# 	getLL_rowOfPartialCol(['a', 'C']))  # 同上
# 	getLL_rowOfPartialCol(["A", 3]))   # 同上
# 4.8 获取带行号的部分列的行数据
# 	getD_rowNumber_rowOfpartialCol([1, 3]))   # {1: ['Number具体数', 'jinhaoyoyo'], 2: [2, 30], 3: [3, 25], 4: [4, 30], 5: [5, 10], 6: [6, 5], 7: [7, 10]}
# 	getD_rowNumber_rowOfpartialCol([1, 'C'])
# 	getD_rowNumber_rowOfpartialCol(['a', 'C']))
# 4.9 获取每列数据 getLL_col()
# 4.10 获取带列序号的每列数据 getD_colNumber_col()  # { 2 : ['状态', '名字'], 3 : ['ok', 'jinhao']...}
# 4.11 获取带列字母的每列数据 getD_colLetter_col()  # { 'a' : ['状态', '名字'], 'b' : ['ok', 'jinhao']...}
# 4.12 获取列标签的序号 getL_columnHeaderNumber(['测试'，‘开发’])  # [2，4]
# 4.13 获取列标签的字母 getL_columnHeaderLetter(['测试'，‘开发’])  # ['A', 'C']
# 4.14 将标题转列字典序列 getD_colNumber_columnTitle(['测试'，‘开发’]）# {2: '姓名', 5: '性别'}
# 4.15 将标题转列字典字母 getD_colLetter_columnTitle(['测试'，‘开发’]）# {'B': '姓名', 'E': '性别'}
# 4.16 获取部分列的列值(可忽略多行) getLL_partialColOfPartialCol([1, 3], [1, 2]))   # 获取第二列和第四列的列值，并忽略第1，2行的行值。
# 4.17 获取单元格的坐标 getCoordinate(2, 5))   # E2
# 4.18 获取所有数据的坐标 getDimensions())  # A1:E17


# print("4.1 获取总行列数".center(100, "-"))
# print(Openpyxl_PO.getL_shape())  # [7,5]

# print("4.2 获取单元格值".center(100, "-"))
# print(Openpyxl_PO.getCell(3, 2))  # 获取第3行第2列的值

# print("4.3 获取一行数据".center(100, "-"))
# print(Openpyxl_PO.getL_row(2))  # ['Number具体数', '高地', 'jinhaoyoyo', '状态', '名字']
#
# print("4.4 获取一列数据".center(100, "-"))
# print(Openpyxl_PO.getL_col(2))  # ['高地', 40, 44, 50, 30, 25, 150]
# print(Openpyxl_PO.getL_col('B'))  # ['高地', 40, 44, 50, 30, 25, 150]

# print("4.5 获取每行数据".center(100, "-"))
# print(Openpyxl_PO.getLL_row())  # [['Number具体数', '高地', 'jinhaoyoyo', '状态', '名字'], [2, 40, 30, 'ok', 'jinhao'],...]
#
# print("4.6 获取带行号的每行数据".center(100, "-"))
# print(Openpyxl_PO.getD_rowNumber_row())  # {1: ['Number具体数', '高地', 'jinhaoyoyo', '状态', '名字'], 2: [2, 40, 30, 'ok', 'jinhao'],...}

# print("4.7 获取部分列的行数据".center(100, "-"))
# print(Openpyxl_PO.getLL_rowOfPartialCol([1, 3]))   # [['Number具体数', 'jinhaoyoyo'], [2, 30], [3, 25], [4, 30], [5, 10], [6, 5], [7, 10]] //获取1和3列的行数据
# print(Openpyxl_PO.getLL_rowOfPartialCol(['a', 'C']))  # 同上
# print(Openpyxl_PO.getLL_rowOfPartialCol(["A", 3]))   # 同上

# print("4.8 获取带行号的部分列的行数据".center(100, "-"))
# print(Openpyxl_PO.getD_rowNumber_rowOfpartialCol([1, 3]))   # {1: ['Number具体数', 'jinhaoyoyo'], 2: [2, 30], 3: [3, 25], 4: [4, 30], 5: [5, 10], 6: [6, 5], 7: [7, 10]}
# print(Openpyxl_PO.getD_rowNumber_rowOfpartialCol([1, 'C']))   # {1: ['Number具体数', 'jinhaoyoyo'], 2: [2, 30], 3: [3, 25], 4: [4, 30], 5: [5, 10], 6: [6, 5], 7: [7, 10]}
# print(Openpyxl_PO.getD_rowNumber_rowOfpartialCol(['a', 'C']))   # {1: ['Number具体数', 'jinhaoyoyo'], 2: [2, 30], 3: [3, 25], 4: [4, 30], 5: [5, 10], 6: [6, 5], 7: [7, 10]}

# print("4.9 获取每列数据".center(100, "-"))
# print(Openpyxl_PO.getLL_col())  # [['Number具体数', 2, 3, 4, 5, 6, 7], ['高地', 40, 44, 50, 30, 25, 150],...]
#
# print("4.10 获取带列序号的每列数据".center(100, "-"))
# print(Openpyxl_PO.getD_colNumber_col())

# print("4.11 获取带列字母的每列数据".center(100, "-"))
# print(Openpyxl_PO.getD_colLetter_col())

# print("4.12 获取列标签的序号".center(100, "-"))
# print(Openpyxl_PO.getL_columnHeaderNumber(["no", "name"]))  # [2, 5]
#
# print("4.13 获取列标签的字母".center(100, "-"))
# print(Openpyxl_PO.getL_columnHeaderLetter(["no", "name"]))  # ['A', 'E']

# print("4.14 将标题转列字典序列".center(100, "-"))
# print(Openpyxl_PO.getD_colNumber_columnTitle(["no", "name"]))  # {2: '高地', 5: '名字'}
#
# print("4.15 将标题转列字典字母".center(100, "-"))
# print(Openpyxl_PO.getD_colLetter_columnTitle(["no", "name"]))  # {'A': '高地', 'C': '名字'}

# print("4.16 获取部分列的列值(可忽略多行)".center(100, "-"))
# print(Openpyxl_PO.getLL_partialColOfPartialCol([1, 3], [1, 4]))   # 获取第二列和第四列的列值，并忽略第1，4行的行值。
# print(Openpyxl_PO.getColByPartialColByUnwantedRow([2], [], "上海"))  # 获取第2列所有值。

# print("4.17 获取单元格的坐标".center(100, "-"))
# print(Openpyxl_PO.getCoordinate(2, 5))   # E2

# print("4.18 获取工作表数据的坐标".center(100, "-"))
# print(Openpyxl_PO.getDimensions())  # A1:E17


# todo 【两表比较】

# print("5.1 两个excel的sheet进行比较，输出有差异值。（两表标题与行数必须一致） ".center(100, "-"))
# Openpyxl_PO = OpenpyxlPO("./data/11.xlsx")
# Openpyxl_PO2 = OpenpyxlPO("./data/22.xlsx")
# print(Openpyxl_PO.getD_excel_cell_By_Diff(Openpyxl_PO.getLL_row("hello_标题升序"), Openpyxl_PO2.getLL_row("hello_标题升序")))
#{'left': {4: {'no': 1}, 5: {'name': '张三'}, 6: {'age': 90}, 7: {'goal': '你好'}}, 'right': {4: {'no': 34}, 5: {'name': '李四'}, 6: {'age': 345}, 7: {'goal': 100}}}

# # print("5.2 对一张表的两个sheet进行数据比对，差异数据标注颜色 ".center(100, "-"))
# Openpyxl_PO = OpenpyxlPO("./data/11.xlsx")
# Openpyxl_PO.setColorByDiff("hello1", "hello2")
# 示例1：默认配置（跳过空值，红色和橙色标注差异）
# Openpyxl_PO.setColorByDiff("hello1", "hello2")

# 示例2：自定义颜色（绿色和蓝色标注差异）
Openpyxl_PO.setColorByDiff("hello1", "hello2", color1="00FF00", color2="0000FF")

# 示例3：不禁用空值比较
# Openpyxl_PO.setColorByDiff("Sheet1", "Sheet2", skip_empty=False)
# print(f"[DEBUG] 差异单元格 ({i + 1}, {j + 1}): '{val1}' vs '{val2}'")



# # print("5.3 对一张表的两个sheet进行数据比对，将结果写入第一个sheet ".center(100, "-"))
# Openpyxl_PO.setSheetByDiff("browser", "interface")

