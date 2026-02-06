# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2020-12-8
# Description   : openpyxl 对象层
# *********************************************************************
# 官网：http://openpyxl.readthedocs.org/en/latest/
# openpyxl 工作原理：将整个xlsx读入内存，方便处理。
# openpyxl 操作大文件时可使用 Optimized reader 和 Optimized writer 两种模式，它们提供了流式的接口，速度更快，使我们可以用常量级的内存消耗来读取和写入无限量的数据。
# Optimized reader 可用 use_iterators=True参数打开，如：wb = load_workbook(filename = 'haggle.xlsx',use_iterators=True)
# openpyxl 读取大数据的效率没有 xlrd 高。
# xlsxwriter xlrd xlwt xlutils 这些库都不支持 excel 写操作，一般只能将原excel中的内容读出、做完处理后，再写入一个新的excel文件。
# 扩展学习 xlwings https://blog.csdn.net/qfxietian/article/details/123822358

# 支持excel2010 .xlsx / .xlsm / .xltx / .xltm格式的文件
# 首行、首列 是（1,1）而不是（0,0）
# NULL表示空值，即cell里面没有数据 ，等同于 python中的None
# numberic 数字型 = python中的float
# string 字符串型 = python中的unicode

# 使用方法
# 参考：openpyxl常用模块用法 https://www.debug8.com/python/t_41519.html
# 基础使用方法：https://blog.csdn.net/four91/article/details/106141274
# 高级使用方法：https://blog.csdn.net/m0_47590417/article/details/119082064

# 安装包
# pip3 install openpyxl == 3.0.0
# 注意！：其他版本（如3.0.2使用中会报错）如有报错，请安装3.0.0

# 报错
# 如：File "src\lxml\serializer.pxi", line 1652, in lxml.etree._IncrementalFileWriter.write TypeError: got invalid input value of type <类与实例 'xml.etree.ElementTree.Element'>, expected string or Element
# 解决方法: pip uninstall lxml   及更新 openpyxl 版本，3.0.7以上

# 乱码
# gb2312 文字编码，在读取后会显示乱码，需转换成 Unicode

# 颜色
# 颜色码对照表（RGB与十六进制颜色码互转） https://www.sioe.cn/yingyong/yanse-rgb-16/
# 绿色 = 00E400，黄色 = FFFF00，橙色 = FF7E00，红色 = FF0000，粉色 = 99004C，褐色 =7E0023,'c6efce = 淡绿', '006100 = 深绿'，'ffffff=白色', '000000=黑色'，'ffeb9c'= 橙色

# 表格列 A，B，C 与 1，2，3 互转
from openpyxl.utils import get_column_letter, column_index_from_string
# get_column_letter(2)  # 'B'
# a = column_index_from_string('B')  # 2
# *********************************************************************


"""
1.1 新建 newExcel("./OpenpyxlPO/newfile2.xlsx", "mySheet1", "mySheet2", "mySheet3") 
1.2 打开 open()
1.3 获取所有工作表 getSheets()
1.4 操作工作表 sh()
1.5 切换工作表 switchSheet("Sheet2") 
1.6 添加不覆盖工作表 addSheet("Sheet1")
1.7 添加覆盖工作表 addCoverSheet("Sheet1", 1) 
1.8 删除工作表 delSheet("Sheet1")
1.9 保存 save()

2.0.1 在第N行前插入多行空白 insertNullRows(3, 5) 在第3行前插入5行空白
2.0.2 在第N列前插入多列空白 insertNullCols(3) 在第3列前插入1列空白
2.1 更新单元格值 setCell(1, 2, "hello") 等同于 setCell(1, 'B', "hello")

2.2 插入行数据 insertRows({1: ["100", 101, "102"], 5: ["444", "123", "666"]})
2.3 更新行数据 setRows({7: ["200", 222, "555"], 8: ["777", "345", "888"]})
2.4 追加行数据 appendRows([['姓名', '电话', '成绩', '学科'], ['毛泽东', 15266606298, 14, '化学'], ['周恩来', 15201077791, 78, '美术']])

2.5 插入列数据 insertCols({"a": ["姓名", "张三", "李四"], "c": ["年龄", "55", "34"]})
2.6 更新列数据 setCols({"A": ["公司", "百度", "天猫"], "F": ["学校", "清华大学", "北京大学"]})
2.7 追加列数据 appendCols([["姓名", "张三", "李四"], ["年龄", "55", "34"]])

2.5 设置单元格列宽 setColWidth(1, 100) # 设置第1列宽度100
2.5 设置单元格列宽 setColWidth2('f', 100) # 设置第f列宽度100
2.5 设置单元格行高与列宽 setCellDimensions(3, 30, 'f', 30) //设置第三行行高30，第f列列宽50
2.6 设置工作表所有单元格的行高与列宽 setAllCellDimensions(30, 20) //设置所有单元格高30，宽20
2.7 设置所有单元格自动换行 setAllWordWrap()
2.8 设置冻结首行 setFreeze('A2'）
2.9 设置单元格对齐样式  setCellAlignment(5, 4, 'center', 'center')
2.9.2 设置单行多列对齐样式 setRowColAlignment(5, [1,4], 'center', 'center')
2.9.3 设置所有单元格对齐样式 setAllCellAlignment('center', 'center')
2.10 设置筛选列  setFilterCol("all") # 全部筛选, setFilterCol("") # 取消筛选 , setFilterCol("A2") # 对A2筛选 
2.11 设置单元格字体（字体、字号、粗斜体、下划线、颜色） setCellFont(1, 1, name=u'微软雅黑', size=16, bold=True, italic=True, color="000000")
2.11.2 设置单行多列字体  setRowColFont(1, [1, 5])
2.11.3 设置所有单元格字体  setAllCellFont(color="000000")
2.12 设置单元格边框 setBorder(1, 2, left = ['thin','ff0000'], right = ['thick','ff0000'], top = ['thin','ff0000'],bottom = ['thick','ff0000'])
2.13 设置单元格填充背景色 setPatternFill(2, 2, 'solid', '006100')
2.14 设置单元格填充渐变色 setGradientFill(3, 3, stop=["FFFFFF", "99ccff", "000000"])
2.15 设置单元格背景色 setCellColor(1, 1, "ff0000")  # 第1行第一列设置红色
2.15.2 设置单行多列背景色 setRowColColor(5, ['b', 'd'], "ff0000")
2.15.3 设置所有单元格背景色 setAllCellColor("ff0000")
2.16 设置整行(可间隔)背景色  setRowColor(3, 1, "ff0000")  # 从第3行开始每隔1行颜色标红色
2.17 设置整列(可间隔)背景色  setColColor(2, 1, "ff0000")  # 从第2列开始每隔1列设置颜色为红色
2.18 设置工作表背景颜色 setSheetColor("FF0000")

3.1 获取总行列数 getL_shape()  # [5,10]
3.2 获取单元格的值 getCell(3,2)
3.3 获取一行数据 getL_row(2) # 获取第2行值
3.4 获取一列数据 getL_col(2) 或 getL_col('B') # 获取第2列值
3.5.1 获取行数据 getLL_row()  # [['状态', '名字'],['ok', 'jinhao']...]
3.5.2 获取带行号的行数据 getD_rowNumber_row()  # { 2 : ['状态', '名字'], 3 : ['ok', 'jinhao']...}
3.5.3 获取部分列的行数据 getLL_rowOfPartialCol([1, 3])  # 获取第1，3列的行数据 [['Number具体数', 'jinhaoyoyo'], [2, 30], [3, 25]...]
    支持序号与字母混搭 getLL_rowOfPartialCol(["A", "C"])， getLL_rowOfPartialCol([2, "C"])
    支持去重 getLL_rowOfPartialCol([1, 3, 2, "a", "C", "B"])
3.5.4 获取带行号的部分列的行数据 getD_rowNumber_rowOfpartialCol([1, 3])  # {1: ['Number具体数', 'jinhaoyoyo'], 2: [2, 30], 3: [3, 25]...}
     getD_rowNumber_rowOfpartialCol([1, 'c']) 同上  
3.6.1 获取每列数据 getLL_col()
3.6.2 获取带列序号的每列数据 getD_colNumber_col()  # { 2 : ['状态', '名字'], 3 : ['ok', 'jinhao']...}
3.6.3 获取带列字母的每列数据 getD_colLetter_col()  # { 'a' : ['状态', '名字'], 'b' : ['ok', 'jinhao']...}
3.8.1 获取标题的序号 getL_columnHeaderNumber(['测试'，‘开发’])  # [2，4]
3.8.2 获取标题的字母 getL_columnHeaderLetter(['测试'，‘开发’])  # ['A', 'C']
3.8.3 将标题转列字典序列 getD_colNumber_columnTitle（['测试'，‘开发’]）# {2: '姓名', 5: '性别'}
3.8.4 将标题转列字典字母 getD_colLetter_columnTitle（['测试'，‘开发’]）# {'B': '姓名', 'E': '性别'}

3.9 获取部分列的列值(可忽略多行) getLL_partialColOfPartialCol([1, 3], [1, 2]))   # 获取第二列和第四列的列值，并忽略第1，2行的行值。
3.10 获取单元格的坐标 getCoordinate(2, 5))   # E2
3.11 获取所有数据的坐标 getDimensions())  # A1:E17

4.1 清空行 clsRow(2)  # 清空第2行
4.2 清空列 clsCol(2)  # 清空第2列
4.2.1 清空列保留标题 clsColRetainTitle(2)  # 清空第2列
4.3 删除连续行 delRow(2, 3)  # 删除从第二行开始连续三行数据 （即删除2，3，4行）
4.4 删除连续列 delCol(2, 3)  # 删除从第二列开始连续三列数据 （即删除2，3，4列）

5.1 两表比较，获取差异内容（两表标题与行数必须一致）setColorByDiffByTwoFile(Openpyxl_PO.getLL_row("Sheet2"), Openpyxl_PO2.getLL_row("Sheet2"))
5.2 两工作表比较，对差异内容标注颜色 setColorByDiff("Sheet1", "Sheet2")

6 移动区域 moveValues(rows, cols, 'C1:D2')

7 将excel中标题（第一行字段）排序（从小打大）sortFields()

8 [转换]
8.1 字典转xlsx  dict2xlsx()
8.2 字典转csv  dict2csv()
8.3 pdf中表格转xlsx pdf2xlsx()
8.4 xlsx转列表 xlsx2list()
8.5 xlsx转字典 xlsx2dict()


"""

from openpyxl import load_workbook
from datetime import date
from time import sleep
import psutil
# import xlwings as xw

import openpyxl, platform, os, pdfplumber
import numpy as np
# import openpyxl.styles
from openpyxl.styles import (Font, PatternFill, GradientFill, Border, Side, Protection, Alignment)
from openpyxl.utils import get_column_letter, column_index_from_string

from PO.ListPO import *
List_PO = ListPO()

from PO.ColorPO import *
Color_PO = ColorPO()

# print(openpyxl.__version__)

import pandas as pd


class OpenpyxlPO:

    def __init__(self, pathFile, l_sheet=[]):

        self.file = pathFile

        if os.path.exists(self.file) == False:

            # 创建文件
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Sheet1"
            if l_sheet != []:
                ws.title = "Sheet1"
                for i in range(len(l_sheet)):
                    wb.create_sheet(l_sheet[i])
            wb.save(self.file)
            print('已创建 => ' + self.file)

        # 打开文件

        self.wb = openpyxl.load_workbook(self.file)


        # ws = self.wb.active
        # ws.protection.sheet = False
        # ws.protection.enable()
        # ws.protection.disable()




        # self.wb = openpyxl.load_workbook(self.file, keep_vba=True)
        # self.wb.protect_worksheet(1)
        # self.wb.active = 1
        # self.wb.save(self.file)

        # 获取文档的字符集编码
        # print(self.wb.encoding)  # utf-8

        # 获取文档的元数据，如标题，创建者，创建日期等
        # print(self.wb.properties)
        # <openpyxl.packaging.core.DocumentProperties object>
        # Parameters:
        # creator='openpyxl', title=None, description=None, subject=None, identifier=None, language=None, created=datetime.datetime(2019, 1, 27, 18, 43, 19), modified=datetime.datetime(2024, 4, 11, 3, 55, 45), lastModifiedBy='jh', category=None, contentStatus=None, version=None, revision=None, keywords=None, lastPrinted=None
        # print(self.wb.properties.lastModifiedBy)  # jh

        # 通过索引值设置当前活跃的sheet
        # self.wb.active= 2


    # todo [工作表]



    def open(self):

        '''
        1.2 打开
        :param otherFile: 
        :return:
            # Openpyxl_PO.open(1) # 打开第二个工作表
            # Openpyxl_PO.open() # 打开第一个工作表
            # Openpyxl_PO.open('test')  # 打开test工作表
        '''

        if platform.system() == "Darwin":
            os.system("open " + self.file)
        if platform.system() == "Windows":
            os.system("start " + self.file)


    def getSheets(self):

        ''' 1.1 获取所有工作表
        如 ['mySheet1', 'mySheet2', 'mySheet3']
        '''

        return self.wb.sheetnames

    def sh(self, varSheet):

        '''
        1.4 操作工作表
        :param varSheet: 
        :return: 
        '''
        
        if isinstance(varSheet, int):
            sh = self.wb[self.wb.sheetnames[varSheet]]
            return sh
        elif isinstance(varSheet, str):
            sh = self.wb[varSheet]
            return sh
        else:
            exit(0)

    def switchSheet(self, varSheet=0):
        
        '''
        1.5 切换工作表
        # switchSheet("Sheet2")
        '''

        sh = self.sh(varSheet)
        self.wb.active = 2
        for sheet in self.wb:
            # print(sheet,sh)
            if sheet.title == sh.title:
                sheet.sheet_view.tabSelected = True
            else:
                sheet.sheet_view.tabSelected = False
        self.save()


    def addSheet(self, varSheetName, varIndex=0, overwrite=False):
        '''
        1.6 添加工作表
        # Openpyxl_PO.addSheet("mysheet1")  # 默认在第一个位置上添加工作表
        # Openpyxl_PO.addSheet("mysheet1", 99)   # 当index足够大时，则在最后一个位置添加工作表
        # Openpyxl_PO.addSheet("mysheet1", -1)   # 倒数第二个位置添加工作表
        # Openpyxl_PO.addSheet("mysheet1", 0, overwrite=True)  # 存在则覆盖
        :param varSheetName: 工作表名称
        :param varIndex: 索引位置，默认为0
        :param overwrite: 是否覆盖已存在的工作表，默认False（不覆盖）
        :return:
        '''

        if overwrite:
            # 如果需要覆盖，先删除已存在的工作表
            if varSheetName in self.wb.sheetnames:
                del self.wb[varSheetName]
            self.wb.create_sheet(title=varSheetName, index=varIndex)
        else:
            # 不覆盖模式：如果工作表不存在才创建
            sign = 0
            for i in self.wb.sheetnames:
                if i == varSheetName:
                    sign = 1
                    break
            if sign == 0:
                self.wb.create_sheet(title=varSheetName, index=varIndex)

        self.save()


    def addCoverSheet(self, varSheetName, varIndex=0):
        
        '''
        # 1.7 添加工作表(覆盖)
        # Openpyxl_PO.addCoverSheet("mySheet1")
        # Openpyxl_PO.addCoverSheet("mySheet1", 0 )  # 在第一个工作表前添加工作表
        # Openpyxl_PO.addCoverSheet("mySheet2",99)   # 在第99个位置添加工作表
        # Openpyxl_PO.addCoverSheet("mySheet3", -1)   # 在倒数第二个位置添加工作表。
        :param varSheetName: 
        :param varIndex: 
        :return: 
        '''
        
        for i in self.wb.sheetnames:
            if i == varSheetName:
                del self.wb[i]
                break
        self.wb.create_sheet(title=varSheetName, index=varIndex)
        self.save()

    def delSheet(self, varSheetName):

        '''
        # 1.8 删除工作表
        # Openpyxl_PO.delSheet("mySheet1")
        # 注意:如果工作表只有1个，则不能删除。
        :param varSheetName:
        :return:
        '''

        if len(self.wb.sheetnames) > 1:
            for i in self.wb.sheetnames:
                if i == varSheetName:
                    del self.wb[i]
                    self.save()
        else:
            print("[warning], excel必须保留1个工作表！")

    def save(self):

        '''
        1.9 保存
        '''

        self.wb.save(self.file)

        # try:
        #     self.wb.save(self.file)
        # except PermissionError:
        #     print("没有足够的权限保存文件，请检查权限。")
        # except FileNotFoundError:
        #     print("文件路径不存在，请检查路径是否正确。")
        # except Exception as e:
        #     print(f"发生未知错误：{e}")


    def renameSheet(self, varOldSheet, varNewSheet):

        "1.10 重命名工作表"

        try:
            ws = self.wb[varOldSheet]
            ws.title = varNewSheet
            self.save()
        except Exception as e :
            # print("[ERROR] => renameSheet() => " + str(e))
            Color_PO.consoleColor("31", "31", "[ERROR] => renameSheet() => " + str(e), '')


    # todo [设置]

    def insertNullRows(self, seq, moreRow=1, varSheet=0):

        '''
        2.0.1 在第N行前插入多行空白
        :param seq:
        :param moreRow:
        :param varSheet:
        :return:
        insertNullRows(3)  在第3行前插入1行空白
        insertNullRows(3，5)  在第3行前插入5行空白
        '''

        sh = self.sh(varSheet)
        sh.insert_rows(idx=seq, amount=moreRow)
        self.save()

    def insertNullCols(self, varCol, moreCol=1, varSheet=0):

        '''
        2.0.2 在第N列前插入多列空白
        :param seq:
        :param moreRow:
        :param varSheet:
        :return:
        insertNullCols(3)  在第3列前插入1列空白
        insertNullCols(3，5)  在第3列前插入5列空白
        '''

        sh = self.sh(varSheet)
        if isinstance(varCol, int):
            sh.insert_cols(idx=varCol, amount=moreCol)
        else:
            sh.insert_cols(idx=column_index_from_string(varCol), amount=moreCol)
        self.save()

    def setCell(self, varRow, varCol, varContent, varSheet=0):

        # 2.1 设置单元格值
        # e.g.setCell(2,"b","123")  # 将第二行B列的值改为123
        sh = self.sh(varSheet)
        if isinstance(varCol, str):
            varCol = column_index_from_string(varCol)  # 将'B'转换成2
        sh.cell(row=varRow, column=varCol, value=varContent)
        # self.save()


    def insertRows(self, d_var, varSheet=0):

        '''2.2 插入行数据'''

        for k, v in d_var.items():
            self.insertNullRows(int(k), varSheet=varSheet)
        self.setRows(d_var, varSheet=varSheet)
        self.save()

    def setRows(self, d_var, varSheet=0):

        '''
        # 2.3 更新行数据
        # Openpyxl_PO.setRows({7:[1,2,3],8:["44",66]})  # 更新第7、8行内容
        # Openpyxl_PO.setRows({7: ["你好", 12345, "7777"], 8: ["44", None, "777777777"]}, -1)  # 对最后一个sheet表，对第7，8行分别写入内容，如遇None则跳过该单元格
        :param d_var:
        :param varSheet:
        :return:
        '''

        sh = self.sh(varSheet)
        for k, v in d_var.items():
            for i in range(len(v)):
                if v[i] != None:
                    sh.cell(row=k, column=i + 1, value=str(v[i]))
        self.save()

    def appendRows(self, l_l_rows, varSheet=0):

        '''
        2.4 追加行数据
        appendRows([['姓名', '电话', '成绩', '学科'], ['毛泽东', 15266606298, 14, '化学'], ['周恩来', 15201077791, 78, '美术']])
        :param l_l_rows:
        :param varSheet:
        :return:
        '''

        sh = self.sh(varSheet)
        for r in range(len(l_l_rows)):
            sh.append(l_l_rows[r])
        self.save()


    def insertCols(self, d_var, varSheet=0):

        '''
        2.5 插入列数据".center(100, "-"))
        Openpyxl_PO.insertCols({1: ["姓名", "张三", "李四"], 5: ["年龄", "55", "34"]})
        :param d_var:
        :param varSheet:
        :return:
        '''

        for k, v in d_var.items():
            self.insertNullCols(k, varSheet=varSheet)
        self.setCols(d_var, varSheet=varSheet)

    def setCols(self, d_var, varSheet=0):

        # 2.3 设置整列值
        # Openpyxl_PO.setCols({"A": ["k1", 666, "777"], "F": ["name", None, "888"]}, -1)
        # Openpyxl_PO.setCols({3: ["k1", 666, "777"], 4: ["name", None, "888"]}, -1)
        sh = self.sh(varSheet)
        for k, v in d_var.items():
            for i in range(len(v)):
                if v[i] != None and k.isalpha():
                    sh.cell(row=i + 1, column=column_index_from_string(k), value=v[i])
                elif v[i] != None and k.isdigit():
                    sh.cell(row=i + 1, column=int(k), value=v[i])
        self.save()

    def appendCols(self, l_l_cols, varSheet=0):

        '''
        2.7 追加列数据
        :param l_l_cols:
        :param varSheet:
        :return:
        '''
        l_colLetter = []
        l_row_col = self.getL_shape(varSheet=varSheet)
        totalCol = l_row_col[1]
        for i in range(len(l_l_cols)):
            l_colLetter.append(get_column_letter(totalCol+i+1))
        # print(l_colLetter)
        # d = List_PO.twoList2dict(l_colLetter, l_l_cols)
        d = (dict(zip(l_colLetter, l_l_cols)))
        self.setCols(d)

    def setColWidth(self, col, colQty, varSheet=0):

        # 2.5 设置列列宽
        # Openpyxl_PO.setColWidth(10, 50) // 设置第十列的宽50
        sh = self.sh(varSheet)
        sh.column_dimensions[get_column_letter(col)].width = colQty  # 列宽
        self.save()

    def setColWidth2(self, col, colQty, varSheet=0):

        # 2.5 设置列列宽
        # Openpyxl_PO.setColWidth2('f', 50) // 设置第f列的宽50
        sh = self.sh(varSheet)
        sh.column_dimensions[col].width = colQty  # 列宽
        self.save()

    def setCellDimensions(self, row, rowQty, col, colQty, varSheet=0):

        # 2.5 设置单元格行高与列宽
        # Openpyxl_PO.setCellDimensions(3, 30, 'f', 50) //第三行行高30，第f列列宽50
        sh = self.sh(varSheet)
        sh.row_dimensions[row].height = rowQty  # 行高
        sh.column_dimensions[col].width = colQty  # 列宽
        self.save()

    def setRowColDimensions(self, row, rowQty, l_col, colQty, varSheet=0):

        # 2.5.2 设置单行多列行高与列宽
        # Openpyxl_PO.setRowColDimensions(5, 30, ['f', 'h'], 30)  #
        sh = self.sh(varSheet)
        cols = sh.max_column
        sh.row_dimensions[row].height = rowQty  # 行高
        if l_col == "all":
            for i in range(1, cols + 1):
                sh.column_dimensions[get_column_letter(i)].width = colQty  # 列宽
        else:
            # print(column_index_from_string(l_col[0]))  # 6
            # print(column_index_from_string(l_col[1]))  # 8
            for i in range(
                column_index_from_string(l_col[0]),
                int(column_index_from_string(l_col[1])) + 1,
            ):
                sh.column_dimensions[get_column_letter(i)].width = colQty  # 列宽
        self.save()

    def setAllCellDimensions(self, rowQty, colQty, varSheet=0):

        # 2.6 设置所有单元格的行高与列宽
        sh = self.sh(varSheet)
        rows = sh.max_row
        columns = sh.max_column
        for i in range(1, rows + 1):
            sh.row_dimensions[i].height = rowQty  # 行高
        for i in range(1, columns + 1):
            sh.column_dimensions[get_column_letter(i)].width = colQty  # 列宽
        self.save()

    def setAllCellDimensionsHeight(self, rowQty, varSheet=0):

        # 2.6 设置所有单元格的行高与列宽
        sh = self.sh(varSheet)
        rows = sh.max_row
        columns = sh.max_column
        for i in range(1, rows + 1):
            sh.row_dimensions[i].height = rowQty  # 行高
        self.save()

    def setAllWordWrap(self, varSheet=0):

        # 2.7 设置所有单元格自动换行
        sh = self.sh(varSheet)
        # print(list(sh._cells.keys())) # [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 3), (5, 1), (5, 2), (5, 3), (6, 1), (6, 2), (6, 3), (7, 1), (7, 2), (7, 3)]
        for key in list(sh._cells.keys()):
            sh._cells[key].alignment = Alignment(wrapText=True)
        self.save()

    def setFreeze(self, coordinate, varSheet=0):

        # 2.8 冻结窗口
        # setFreeze('A2'）
        sh = self.sh(varSheet)
        sh.freeze_panes = coordinate
        self.save()

    def setCellAlignment(
        self,
        row,
        col,
        horizontal="center",
        vertical="center",
        text_rotation=0,
        wrap_text=False,
        varSheet=0,
    ):

        # 2.9 设置单元格对齐样式
        # Openpyxl_PO.setCellAlignment(5, 4, 'center', 'top')
        # Openpyxl_PO.setCellAlignment(5, "f", 'center', 'top')
        # Alignment(horizonta水平对齐模式, vertical=垂直对齐模式, text_rotation=旋转角度, wrap_text=是否自动换行)
        # horizontal = ("general", "left", "center", "right", "fill", "justify", "centerContinuous", "distributed",)
        # vertical = ("top", "center", "bottom", "justify", "distributed")
        sh = self.sh(varSheet)
        if isinstance(col, int):
            sh.cell(row=row, column=col).alignment = Alignment(
                horizontal=horizontal,
                vertical=vertical,
                text_rotation=text_rotation,
                wrap_text=wrap_text,
            )
        else:
            sh.cell(row, column_index_from_string(col)).alignment = Alignment(
                horizontal=horizontal,
                vertical=vertical,
                text_rotation=text_rotation,
                wrap_text=wrap_text,
            )
        self.save()

    def setRowColAlignment(
        self,
        row,
        l_col,
        horizontal="center",
        vertical="center",
        text_rotation=0,
        wrap_text=False,
        varSheet=0,
    ):

        # 2.9.2 设置单行多列对齐样式
        # Openpyxl_PO.setRowColAlignment(1, [4, 6], 'center', 'center')  # 第一行第四五六列居中
        # Openpyxl_PO.setRowColAlignment(9, "all", 'center', 'center')  # 第九行全部居中
        # Alignment(horizonta水平对齐模式, vertical=垂直对齐模式, text_rotation=旋转角度, wrap_text=是否自动换行)
        # horizontal = ("general", "left", "center", "right", "fill", "justify", "centerContinuous", "distributed",)
        # vertical = ("top", "center", "bottom", "justify", "distributed")
        sh = self.sh(varSheet)
        cols = sh.max_column
        if l_col == "all":
            for i in range((cols)):
                sh.cell(row=row, column=i + 1).alignment = Alignment(
                    horizontal=horizontal,
                    vertical=vertical,
                    text_rotation=text_rotation,
                    wrap_text=wrap_text,
                )
        else:
            for i in range(
                column_index_from_string(l_col[0]),
                int(column_index_from_string(l_col[1])) + 1,
            ):
                sh.cell(row=row, column=i).alignment = Alignment(
                    horizontal=horizontal,
                    vertical=vertical,
                    text_rotation=text_rotation,
                    wrap_text=wrap_text,
                )
        self.save()

    def setAllCellAlignment(
        self,
        horizontal="center",
        vertical="center",
        text_rotation=0,
        wrap_text=False,
        varSheet=0,
    ):

        # 2.9.3 设置所有单元格对齐样式
        # Openpyxl_PO.setAllCellAlignment('center', 'center')
        # Alignment(horizonta水平对齐模式, vertical=垂直对齐模式, text_rotation=旋转角度, wrap_text=是否自动换行)
        # horizontal = ("general", "left", "center", "right", "fill", "justify", "centerContinuous", "distributed",)
        # vertical = ("top", "center", "bottom", "justify", "distributed")
        sh = self.sh(varSheet)
        rows = sh.max_row
        cols = sh.max_column
        for r in range(rows):
            for c in range(cols):
                sh.cell(row=r + 1, column=c + 1).alignment = Alignment(
                    horizontal=horizontal,
                    vertical=vertical,
                    text_rotation=text_rotation,
                    wrap_text=wrap_text,
                )
        self.save()

    def setFilterCol(self, varCell="all", varSheet=0):

        # 2.10 设置筛选列
        # setFilterCol("all")  # 全部筛选
        # setFilterCol("")  # 取消筛选
        # setFilterCol("A2") # 对A2筛选
        sh = self.sh(varSheet)
        if varCell == "all":
            sh.auto_filter.ref = sh.dimensions
        elif varCell == "":
            sh.auto_filter.ref = None
        else:
            sh.auto_filter.ref = varCell
        self.save()

    def setCellFont(
        self,
        row,
        col,
        name="微软雅黑",
        size=10,
        bold=False,
        italic=False,
        color=None,
        varSheet=0,
    ):

        # 2.11 设置单元格字体（字体、字号、粗斜体、下划线、颜色）
        # setCellFont(1, 1)
        # setCellFont(1, "f")
        # setCellFont(1, "f", size=16, bold=True, color="ff0000")
        sh = self.sh(varSheet)
        if isinstance(col, int):
            sh.cell(row, col).font = Font(
                name=name, size=size, bold=bold, italic=italic, color=color
            )
        else:
            sh.cell(row, column_index_from_string(col)).font = Font(
                name=name, size=size, bold=bold, italic=italic, color=color
            )
        self.save()

    def setRowColFont(
        self,
        row,
        l_col,
        name="微软雅黑",
        size=16,
        bold=False,
        italic=False,
        color="000000",
        varSheet=0,
    ):

        # 2.11.2 设置单行多列字体（字体、字号、粗斜体、下划线、颜色）
        # setRowColFont(1, ["e", "h"])
        # setRowColFont(1, "all", color="000000")
        sh = self.sh(varSheet)
        cols = sh.max_column
        if l_col == "all":
            for i in range((cols)):
                sh.cell(row=row, column=i + 1).font = Font(
                    name=name, size=size, bold=bold, italic=italic, color=color
                )
        else:
            for i in range(
                column_index_from_string(l_col[0]),
                int(column_index_from_string(l_col[1])) + 1,
            ):
                sh.cell(row=row, column=i).font = Font(
                    name=name, size=size, bold=bold, italic=italic, color=color
                )
        self.save()

    def setAllCellFont(
        self, name="微软雅黑", size=16, bold=False, italic=False, color="000000", varSheet=0
    ):

        # 2.11.2 设置所有单元格字体（字体、字号、粗斜体、下划线、颜色）
        # setAllCellFont()
        sh = self.sh(varSheet)
        rows = sh.max_row
        cols = sh.max_column

        for r in range(rows):
            for c in range(cols):
                sh.cell(row=r + 1, column=c + 1).font = Font(
                    name=name, size=size, bold=bold, italic=italic, color=color
                )
        self.save()

    def setBorder(
        self,
        row,
        col,
        left=["thin", "ff0000"],
        right=["thick", "ff0000"],
        top=["thin", "ff0000"],
        bottom=["thick", "ff0000"],
        varSheet=0,
    ):

        """
        2.12 设置单元格边框
        # 设置边框样式，上下左右边框
        Side(style=边线样式，color=边线颜色)
         * style 参数的种类： 'double, 'mediumDashDotDot', 'slantDashDot','dashDotDot','dotted','hair', 'mediumDashed, 'dashed', 'dashDot', 'thin','mediumDashDot','medium', 'thick'

        setBorder(1, 2, left = ['thin','ff0000'], right = ['thick','ff0000'], top = ['thin','ff0000'],bottom = ['thick','ff0000'])
        """

        sh = self.sh(varSheet)
        border = Border(
            left=Side(style=left[0], color=left[1]),
            right=Side(style=right[0], color=right[1]),
            top=Side(style=top[0], color=top[1]),
            bottom=Side(style=bottom[0], color=bottom[1]),
        )
        sh.cell(row=row, column=col).border = border
        self.save()

    def setPatternFill(self, row, col, fill_type="solid", fgColor="99ccff", varSheet=0):

        """
        2.13 设置单元格填充背景色
        patternType = {'lightVertical', 'mediumGray', 'lightGrid', 'darkGrid', 'gray125', 'lightHorizontal', 'gray0625','lightTrellis', 'darkUp', 'lightGray', 'darkVertical', 'darkGray', 'solid', 'darkTrellis', 'lightUp','darkHorizontal', 'darkDown', 'lightDown'}
        PatternFill(fill_type=填充样式，fgColor=填充颜色）
        setPatternFill(2, 2, 'solid', '006100')
        """

        sh = self.sh(varSheet)
        pattern_fill = PatternFill(fill_type=fill_type, fgColor=fgColor)
        sh.cell(row=row, column=col).fill = pattern_fill
        self.save()
        # return PatternFill(patternType='' + patternType + '', fgColor='' + fgColor + '')  # 背景色

    def setGradientFill(
        self, row, col, stop=["FFFFFF", "99ccff", "000000"], varSheet=0
    ):

        # 2.14 设置单元格填充渐变色
        # GradientFill(stop=(渐变颜色 1，渐变颜色 2……))
        # setGradientFill(3, 3, stop=["FFFFFF", "99ccff", "000000"])
        sh = self.sh(varSheet)
        gradient_fill = GradientFill(stop=(stop[0], stop[1], stop[2]))
        sh.cell(row=row, column=col).fill = gradient_fill
        self.save()

    def setCellColor(self, row, col, varColor=None, varSheet=0):

        # 2.15 设置单元格背景色
        # Openpyxl_PO.setCellColor(5, 1)  # 清除第5行第1列的背景色
        # Openpyxl_PO.setCellColor(5, "d")  # 清除第5行d列的背景色
        # Openpyxl_PO.setCellColor(5, 1, "ff0000")  # 设置第五行第1列设置红色
        # Openpyxl_PO.setCellColor(5, "e", "ff0000")  # 设置第五行e列设置红色
        # Openpyxl_PO.setCellColor(None, None)  # 清除所有背景色
        sh = self.sh(varSheet)
        rows = sh.max_row
        cols = sh.max_column
        # 清除表格里所有单元格的背景色
        if row == None and col == None:
            style = PatternFill(fill_type=None)
            for i in range(1, rows + 1):
                for j in range(1, cols + 1):
                    sh.cell(i, j).fill = style
        else:
            if varColor == None:
                style = PatternFill(fill_type=None)  # 消除单元格颜色
            else:
                style = PatternFill("solid", fgColor=varColor)
            if isinstance(col, int):
                sh.cell(row, col).fill = style
            else:
                sh.cell(row, column_index_from_string(col)).fill = style
        self.save()

    def setRowColColor(self, row, l_col, varColor, varSheet=0):

        # 2.15.2 设置单行多列背景色
        # Openpyxl_PO.setRowColColor(5, ['b', 'd'], "ff0000")
        # Openpyxl_PO.setRowColColor(5, "all", "ff0000")
        sh = self.sh(varSheet)
        cols = sh.max_column
        style = PatternFill("solid", fgColor=varColor)

        if l_col == "all":
            for i in range((cols)):
                sh.cell(row=row, column=i + 1).fill = style
        else:
            for i in range(
                column_index_from_string(l_col[0]),
                int(column_index_from_string(l_col[1])) + 1,
            ):
                sh.cell(row=row, column=i).fill = style
        self.save()

    def setAllCellColor(self, varColor=None, varSheet=0):

        # 2.15.3 设置所有单元格背景色
        # setAllCellColor("ff0000")
        # setAllCellColor()
        sh = self.sh(varSheet)
        rows = sh.max_row
        cols = sh.max_column
        if varColor == None:
            style = PatternFill(fill_type=None)  # 消除单元格颜色
        else:
            style = PatternFill("solid", fgColor=varColor)

        for r in range(rows):
            for c in range(cols):
                sh.cell(row=r + 1, column=c + 1).fill = style
        self.save()

    def setRowColor(self, row, varSkip, varColor, varSheet=0):

        # 2.16 设置整行(可间隔)背景色
        # Openpyxl_PO.setRowColor(6, 1, "FF0000")
        sh = self.sh(varSheet)
        rows = sh.max_row
        cols = sh.max_column
        # 清除表格里所有单元格的背景色
        style = PatternFill(fill_type=None)
        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                sh.cell(i, j).fill = style
        style = PatternFill("solid", fgColor=varColor)
        for i in range(row, rows + 1, varSkip + 1):
            for j in range(1, cols + 1):
                sh.cell(i, j).fill = style
        self.save()

    def setColColor(self, col, varSkip, varColor, varSheet=0):

        # 2.17 设置整列(可间隔)背景色
        # Openpyxl_PO.setColColor(6, 1, "FF0000")
        sh = self.sh(varSheet)
        rows = sh.max_row
        cols = sh.max_column
        style = PatternFill(fill_type=None)  # 消除单元格颜色
        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                sh.cell(i, j).fill = style
        style = PatternFill("solid", fgColor=varColor)
        for i in range(1, rows + 1):
            for j in range(col, cols + 1, varSkip + 1):
                sh.cell(i, j).fill = style
        self.save()

    def setSheetColor(self, varColor, varSheet=0):

        # 2.18 设置工作表背景颜色
        # Openpyxl_PO.setSheetColor("FF0000")
        sh = self.sh(varSheet)
        sh.sheet_properties.tabColor = varColor
        self.save()

    def clsSheetColor(self, i, j , varSheet=0):

        # 2.19 清除工作表背景颜色
        # clsSheetColor(2,4) # 清除第二行第四列背景色
        sh = self.sh(varSheet)
        sh.cell(i,j).fill = None
        self.save()


    # todo [获取]

    def getL_shape(self, varSheet=0):
        """
        3.1 获取总行列数（优化版）

        :param varSheet: 工作表索引或名称，默认为0
        :return: 总行数和总列数组成的列表，如 [4, 3]
        :raises ValueError: 如果参数不合法
        :raises IOError: 如果操作失败
        """
        # 参数校验
        if not isinstance(varSheet, (int, str)):
            raise ValueError("varSheet 必须是整数（索引）或字符串（名称）")

        try:
            # 获取工作表对象
            sh = self.sh(varSheet)

            # 获取总行数和总列数
            total_rows = sh.max_row
            total_cols = sh.max_column

            # 容错处理：如果工作表为空，返回默认值
            if total_rows is None or total_cols is None:
                return [0, 0]

            return [total_rows, total_cols]

        except Exception as e:
            raise IOError(f"获取总行列数失败: {e}") from e

    def getCell(self, varRow, varCol, varSheet=0):
        """
        3.2 获取单元格的值（优化版）

        :param varRow: 行号，必须是大于0的整数
        :param varCol: 列号，必须是大于0的整数
        :param varSheet: 工作表索引或名称，默认为0
        :return: 单元格的值，如 "hello"
        :raises ValueError: 如果参数不合法
        :raises IOError: 如果操作失败
        """
        # 参数校验
        if not isinstance(varRow, int) or varRow <= 0:
            raise ValueError("varRow 必须是大于0的整数")
        if not isinstance(varCol, int) or varCol <= 0:
            raise ValueError("varCol 必须是大于0的整数")
        if not isinstance(varSheet, (int, str)):
            raise ValueError("varSheet 必须是整数（索引）或字符串（名称）")

        try:
            # 获取工作表对象
            sh = self.sh(varSheet)

            # 边界检查
            max_row = sh.max_row
            max_col = sh.max_column
            if varRow > max_row:
                raise ValueError(f"行号 {varRow} 超出范围，最大行数为 {max_row}")
            if varCol > max_col:
                raise ValueError(f"列号 {varCol} 超出范围，最大列数为 {max_col}")

            # 获取单元格值
            return sh.cell(row=varRow, column=varCol).value

        except Exception as e:
            raise IOError(f"获取单元格值失败: {e}") from e

    def getL_row(self, varSeq, varSheet=0):
        """
        3.3 获取一行数据（优化版）

        :param varSeq: 行号，必须是大于0的整数
        :param varSheet: 工作表索引或名称，默认为0
        :return: 指定行的数据列表，如 [10, 5, 10]
        :raises ValueError: 如果参数不合法
        :raises IOError: 如果操作失败
        """
        # 参数校验
        if not isinstance(varSeq, int) or varSeq <= 0:
            raise ValueError("varSeq 必须是大于0的整数")
        if not isinstance(varSheet, (int, str)):
            raise ValueError("varSheet 必须是整数（索引）或字符串（名称）")

        try:
            # 获取工作表对象
            sh = self.sh(varSheet)

            # 检查行号是否超出范围
            total_rows = sh.max_row
            if varSeq > total_rows:
                raise ValueError(f"行号 {varSeq} 超出范围，最大行数为 {total_rows}")

            # 获取指定行数据
            target_row = list(sh.rows)[varSeq - 1]
            l_row = [cell.value for cell in target_row]

            return l_row

        except Exception as e:
            raise IOError(f"获取行数据失败: {e}") from e

    def getL_col(self, varCol, varSheet=0, include_header=True):
        """
        3.4 获取一列的值（优化版）

        :param varCol: 列标识，可以是整数（如2）或字符串（如'B'）
        :param varSheet: 工作表索引或名称，默认为0
        :param include_header: 是否包含标题行，默认为True
        :return: 指定列的数据列表，如 ['山丘', 30, 25, 30, 10, 5, 10]
        :raises ValueError: 如果参数不合法
        :raises IOError: 如果操作失败
        """
        # 参数校验
        if not isinstance(varCol, (int, str)):
            raise ValueError("varCol 必须是整数或字符串")
        if not isinstance(varSheet, (int, str)):
            raise ValueError("varSheet 必须是整数（索引）或字符串（名称）")
        if not isinstance(include_header, bool):
            raise ValueError("include_header 必须是布尔值")

        try:
            # 获取工作表对象
            sh = self.sh(varSheet)

            # 转换列标识为索引（如果是字符串）
            if isinstance(varCol, str):
                varCol = column_index_from_string(varCol)

            # 获取列数据
            col_data = [cell.value for cell in list(sh.columns)[varCol - 1]]

            # 根据 include_header 参数决定是否包含标题行
            if not include_header:
                col_data = col_data[1:]  # 跳过第一行（标题行）

            return col_data

        except Exception as e:
            raise IOError(f"获取列数据失败: {e}") from e

    def getLL_row(self, varSheet=0, include_header=True):
        """
        3.5.1 获取每行数据（优化版）

        :param varSheet: 工作表索引或名称，默认为0
        :param include_header: 是否包含标题行，默认为True
        :return: 每行数据组成的二维列表，如 [['Number具体数', '高地', 'jinhaoyoyo'], [2, 40, 30], ...]
        :raises ValueError: 如果参数不合法
        :raises IOError: 如果操作失败
        """
        # 参数校验
        if not isinstance(varSheet, (int, str)):
            raise ValueError("varSheet 必须是整数（索引）或字符串（名称）")
        if not isinstance(include_header, bool):
            raise ValueError("include_header 必须是布尔值")

        try:
            # 获取工作表对象
            sh = self.sh(varSheet)

            # 根据 include_header 参数决定是否包含标题行
            start_index = 0 if include_header else 1

            # 构建每行数据
            l_l_row = [
                [cell.value for cell in row] for row in list(sh.rows)[start_index:]
            ]

            return l_l_row

        except Exception as e:
            raise IOError(f"获取行数据失败: {e}") from e

    def getD_rowNumber_row(self, varSheet=0, include_header=True):
        """
        3.5.2 获取带行号的每行数据（优化版）

        :param varSheet: 工作表索引或名称，默认为0
        :param include_header: 是否包含标题行，默认为True
        :return: 行号为键、行数据为值的字典，如 {1: ['Number具体数', '高地', 'jinhaoyoyo'], 2: [2, 40, 30], ...}
        :raises ValueError: 如果参数不合法
        :raises IOError: 如果操作失败
        """
        # 参数校验
        if not isinstance(varSheet, (int, str)):
            raise ValueError("varSheet 必须是整数（索引）或字符串（名称）")
        if not isinstance(include_header, bool):
            raise ValueError("include_header 必须是布尔值")

        try:
            # 获取所有行数据
            l_l_row = self.getLL_row(varSheet)
            if not l_l_row:
                raise ValueError("工作表中没有数据")

            # 根据 include_header 参数决定是否包含标题行
            start_index = 0 if include_header else 1

            # 构建行号到行数据的映射
            d_seq_row = {
                i + 1: l_l_row[i] for i in range(start_index, len(l_l_row))
            }

            return d_seq_row

        except Exception as e:
            raise IOError(f"获取行数据失败: {e}") from e

    def getLL_rowOfPartialCol(self, l_col, varSheet=0):
        """
        3.5.3 获取部分列的行数据（优化版）

        :param l_col: 需要获取的列标识列表，如 [1, 3] 或 ['A', 'C']
        :param varSheet: 工作表索引或名称，默认为0
        :return: 每行指定列的数据组成的二维列表，如 [['Number具体数', 'jinhaoyoyo'], [2, 30], ...]
        :raises ValueError: 如果参数不合法
        :raises IOError: 如果操作失败
        """
        # 参数校验
        if not isinstance(l_col, list) or not l_col:
            raise ValueError("l_col 必须是一个非空列表")
        if not isinstance(varSheet, (int, str)):
            raise ValueError("varSheet 必须是整数（索引）或字符串（名称）")

        try:
            # 获取工作表对象
            sh = self.sh(varSheet)

            # 转换列标识为索引（如果是字符串）
            col_indices = []
            for col in l_col:
                if isinstance(col, str):
                    col_indices.append(column_index_from_string(col))
                elif isinstance(col, int):
                    col_indices.append(col)
                else:
                    raise ValueError(f"列标识 '{col}' 类型不合法，应为整数或字符串")

            # 去重（保留首次出现的值）
            col_indices = sorted(set(col_indices), key=col_indices.index)

            # 构建每行指定列的数据
            l_l_row = [
                [sh.cell(row, col).value for col in col_indices]
                for row in range(1, sh.max_row + 1)
            ]

            return l_l_row

        except Exception as e:
            raise IOError(f"获取行数据失败: {e}") from e

    def getD_rowNumber_rowOfpartialCol(self, l_col, varSheet=0):
        """
        3.5.4 获取带行号的部分列的行数据（优化版）

        :param l_col: 需要获取的列标识列表，如 [1, 3] 或 ['A', 'C']
        :param varSheet: 工作表索引或名称，默认为0
        :return: 行号为键、行数据为值的字典，如 {1: ['Number具体数', 'jinhaoyoyo'], 2: [2, 30], ...}
        :raises ValueError: 如果参数不合法
        :raises IOError: 如果操作失败
        """
        # 参数校验
        if not isinstance(l_col, list) or not l_col:
            raise ValueError("l_col 必须是一个非空列表")
        if not isinstance(varSheet, (int, str)):
            raise ValueError("varSheet 必须是整数（索引）或字符串（名称）")

        try:
            # 获取部分列的行数据
            l_l_col = self.getLL_rowOfPartialCol(l_col, varSheet)
            if not l_l_col:
                raise ValueError("工作表中没有数据")

            # 构建行号到行数据的映射
            d_seq_row = {i + 1: l_l_col[i] for i in range(len(l_l_col))}

            return d_seq_row

        except Exception as e:
            raise IOError(f"获取行数据失败: {e}") from e

    def getLL_col(self, varSheet=0, include_header=True):
        """
        3.6.1 获取每列数据（优化版）

        :param varSheet: 工作表索引或名称，默认为0
        :param include_header: 是否包含标题行，默认为True
        :return: 每列数据组成的二维列表，如 [['age', 2, 12], ['city', 'shanghai', 'beijin']]
        :raises ValueError: 如果参数不合法
        :raises IOError: 如果操作失败
        """
        # 参数校验
        if not isinstance(varSheet, (int, str)):
            raise ValueError("varSheet 必须是整数（索引）或字符串（名称）")
        if not isinstance(include_header, bool):
            raise ValueError("include_header 必须是布尔值")

        try:
            # 获取工作表对象
            sh = self.sh(varSheet)

            # 根据 include_header 参数决定是否包含标题行
            start_index = 0 if include_header else 1

            # 构建每列数据
            l_l_col = [
                [cell.value for cell in col][start_index:] for col in sh.columns
            ]

            return l_l_col

        except Exception as e:
            raise IOError(f"获取列数据失败: {e}") from e

    def getD_colNumber_col(self, varSheet=0, include_header=True):
        """
        3.6.2 获取带列序号的每列数据（优化版）

        :param varSheet: 工作表索引或名称，默认为0
        :param include_header: 是否包含标题行，默认为True
        :return: 列序号为键、列数据为值的字典，如 {1: ['age', 2, 12], 2: ['city', 'shanghai', 'beijin']}
        :raises ValueError: 如果参数不合法
        :raises IOError: 如果操作失败
        """
        # 参数校验
        if not isinstance(varSheet, (int, str)):
            raise ValueError("varSheet 必须是整数（索引）或字符串（名称）")
        if not isinstance(include_header, bool):
            raise ValueError("include_header 必须是布尔值")

        try:
            # 获取所有列数据
            l_l_col = self.getLL_col(varSheet)
            if not l_l_col:
                raise ValueError("工作表中没有数据")

            # 根据 include_header 参数决定是否包含标题行
            start_index = 0 if include_header else 1

            # 构建列序号到列数据的映射
            d_seq_col = {
                i + 1: l_l_col[i][start_index:] for i in range(len(l_l_col))
            }

            return d_seq_col

        except Exception as e:
            raise IOError(f"获取列数据失败: {e}") from e

    def getD_colLetter_col(self, varSheet=0, include_header=True):
        """
        3.6.3 获取带列字母的每列数据（优化版）

        :param varSheet: 工作表索引或名称，默认为0
        :param include_header: 是否包含标题行，默认为True
        :return: 列字母为键、列数据为值的字典，如 {'A': [1, 2, 3], 'B': ['a', 'b', 'c']}
        :raises ValueError: 如果参数不合法
        :raises IOError: 如果操作失败
        """
        # 参数校验
        if not isinstance(varSheet, (int, str)):
            raise ValueError("varSheet 必须是整数（索引）或字符串（名称）")
        if not isinstance(include_header, bool):
            raise ValueError("include_header 必须是布尔值")

        try:
            # 获取所有列数据
            l_l_col = self.getLL_col(varSheet)
            if not l_l_col:
                raise ValueError("工作表中没有数据")

            # 根据 include_header 参数决定是否包含标题行
            start_index = 0 if include_header else 1

            # 构建列字母到列数据的映射
            d_seq_col = {
                get_column_letter(i + 1): l_l_col[i][start_index:] for i in range(len(l_l_col))
            }

            return d_seq_col

        except Exception as e:
            raise IOError(f"获取列数据失败: {e}") from e


    def getL_columnHeaderNumber(self, l_partialTitle, varSheet=0):
        """
        3.8.1 获取列标签的列标number（优化版）

        :param l_partialTitle: 部分标题列表，如 ['姓名', '性别']
        :param varSheet: 工作表索引或名称，默认为0
        :return: 标题对应的列序号列表，如 [1, 3]
        :raises ValueError: 如果参数不合法
        :raises IOError: 如果操作失败
        """
        # 参数校验
        if not isinstance(l_partialTitle, list):
            raise ValueError("l_partialTitle 必须是一个列表")
        if not all(isinstance(item, str) for item in l_partialTitle):
            raise ValueError("l_partialTitle 中的所有元素必须是字符串")
        if not isinstance(varSheet, (int, str)):
            raise ValueError("varSheet 必须是整数（索引）或字符串（名称）")

        try:
            # 获取第一行标题
            l_title = self.getL_row(1, varSheet)
            if not l_title:
                raise ValueError("工作表中没有找到标题行")

            # 构建标题到列索引的映射（使用字典加速查找）
            title_to_index = {title: idx for idx, title in enumerate(l_title)}

            # 查找匹配的标题并转换为列序号
            result = []
            for title in l_partialTitle:
                if title in title_to_index:
                    col_index = title_to_index[title] + 1  # 列索引从1开始
                    result.append(col_index)
                else:
                    # 如果标题未找到，可以选择跳过或抛出警告
                    print(f"[Warning] 标题 '{title}' 未在表格中找到")

            return result

        except Exception as e:
            raise IOError(f"获取标题列序号失败: {e}") from e

    def getL_columnHeaderLetter(self, l_partialTitle, varSheet=0):
        """
        3.8.2 获取列标签的列标letter（优化版）

        :param l_partialTitle: 部分标题列表，如 ['姓名', '性别']
        :param varSheet: 工作表索引或名称，默认为0
        :return: 标题对应的列字母列表，如 ['A', 'C']
        :raises ValueError: 如果参数不合法
        :raises IOError: 如果操作失败
        """
        # 参数校验
        if not isinstance(l_partialTitle, list):
            raise ValueError("l_partialTitle 必须是一个列表")
        if not all(isinstance(item, str) for item in l_partialTitle):
            raise ValueError("l_partialTitle 中的所有元素必须是字符串")
        if not isinstance(varSheet, (int, str)):
            raise ValueError("varSheet 必须是整数（索引）或字符串（名称）")

        try:
            # 获取第一行标题
            l_title = self.getL_row(1, varSheet)
            if not l_title:
                raise ValueError("工作表中没有找到标题行")

            # 构建标题到列索引的映射（使用字典加速查找）
            title_to_index = {title: idx for idx, title in enumerate(l_title)}

            # 查找匹配的标题并转换为列字母
            result = []
            for title in l_partialTitle:
                if title in title_to_index:
                    col_index = title_to_index[title] + 1  # 列索引从1开始
                    result.append(get_column_letter(col_index))
                else:
                    # 如果标题未找到，可以选择跳过或抛出警告
                    print(f"[Warning] 标题 '{title}' 未在表格中找到")

            return result

        except Exception as e:
            raise IOError(f"获取标题列字母失败: {e}") from e

    def getD_colNumber_columnTitle(self, l_partialTitle, varSheet=0):
        """
        3.8.3 将标题转列字典序列（优化版）

        :param l_partialTitle: 部分标题列表，如 ['姓名', '性别']
        :param varSheet: 工作表索引或名称，默认为0
        :return: 标题与列序号的字典，如 {1: '姓名', 2: '性别'}
        :raises ValueError: 如果参数不合法
        :raises IOError: 如果操作失败
        """
        # 参数校验
        if not isinstance(l_partialTitle, list):
            raise ValueError("l_partialTitle 必须是一个列表")
        if not all(isinstance(item, str) for item in l_partialTitle):
            raise ValueError("l_partialTitle 中的所有元素必须是字符串")
        if not isinstance(varSheet, (int, str)):
            raise ValueError("varSheet 必须是整数（索引）或字符串（名称）")

        try:
            # 获取第一行标题
            l_title = self.getL_row(1, varSheet)
            if not l_title:
                raise ValueError("工作表中没有找到标题行")

            # 构建标题到列序号的映射
            d_title_to_seq = {}
            title_set = set(l_title)  # 使用集合加速查找
            for title in l_partialTitle:
                if title in title_set:
                    index = l_title.index(title) + 1
                    d_title_to_seq[index] = title

            return d_title_to_seq

        except Exception as e:
            raise IOError(f"处理标题转列字典序列失败: {e}") from e

    def getD_colLetter_columnTitle(self, l_partialTitle, varSheet=0):
        """
        3.8.4 将标题转列字典字母（优化版）

        :param l_partialTitle: 部分标题列表，如 ['姓名', '性别']
        :param varSheet: 工作表索引或名称，默认为0
        :return: 标题与列字母的字典，如 {'B': '姓名', 'E': '性别'}
        :raises ValueError: 如果参数不合法
        :raises IOError: 如果操作失败
        """
        # 参数校验
        if not isinstance(l_partialTitle, list):
            raise ValueError("l_partialTitle 必须是一个列表")
        if not all(isinstance(item, str) for item in l_partialTitle):
            raise ValueError("l_partialTitle 中的所有元素必须是字符串")
        if not isinstance(varSheet, (int, str)):
            raise ValueError("varSheet 必须是整数（索引）或字符串（名称）")

        try:
            # 获取第一行标题
            l_title = self.getL_row(1, varSheet)
            if not l_title:
                raise ValueError("工作表中没有找到标题行")

            # 构建标题到列字母的映射
            d_title_to_letter = {}
            for title in l_partialTitle:
                if title in l_title:
                    index = l_title.index(title) + 1
                    letter = get_column_letter(index)
                    d_title_to_letter[letter] = title

            return d_title_to_letter

        except Exception as e:
            raise IOError(f"处理标题转列字典字母失败: {e}") from e

    def getLL_partialColOfPartialCol(self, l_getCol, l_ignoreRow, varSheet=0):
        """
        3.9 获取部分列的列值（可忽略多行）（优化版）

        :param l_getCol: 需要获取的列标识列表，如 [1, 3] 或 ['A', 'C']
        :param l_ignoreRow: 需要忽略的行号列表，如 [1, 2]
        :param varSheet: 工作表索引或名称，默认为0
        :return: 每列的值组成的二维列表，如 [[10, 20], [30, 40]]
        :raises ValueError: 如果参数不合法
        :raises IOError: 如果操作失败
        """
        # 参数校验
        if not isinstance(l_getCol, list):
            raise ValueError("l_getCol 必须是一个列表")
        if not isinstance(l_ignoreRow, list):
            raise ValueError("l_ignoreRow 必须是一个列表")
        if not isinstance(varSheet, (int, str)):
            raise ValueError("varSheet 必须是整数（索引）或字符串（名称）")

        try:
            # 获取工作表对象
            sh = self.sh(varSheet)

            # 转换列标识为索引（如果是字符串）
            col_indices = []
            for col in l_getCol:
                if isinstance(col, str):
                    col_indices.append(column_index_from_string(col))
                elif isinstance(col, int):
                    col_indices.append(col)
                else:
                    raise ValueError(f"列标识 '{col}' 类型不合法，应为整数或字符串")

            # 转换忽略行号为集合（提升查找效率）
            ignore_rows = set(l_ignoreRow)

            # 初始化结果容器
            result = []

            # 遍历每一列
            for col_idx in col_indices:
                col_values = []
                # 遍历每一行
                for row in range(1, sh.max_row + 1):
                    if row not in ignore_rows:
                        col_values.append(sh.cell(row, col_idx).value)
                result.append(col_values)

            return result

        except Exception as e:
            raise IOError(f"获取列值失败: {e}") from e


    def getCoordinate(self, varRow, varCol, varSheet=0):
        """
        3.10 获取单元格的坐标（优化版）

        :param varRow: 行号，必须是大于0的整数
        :param varCol: 列号，必须是大于0的整数
        :param varSheet: 工作表索引或名称，默认为0
        :return: 单元格的坐标字符串，如 'A1'
        :raises ValueError: 如果参数不合法
        :raises IOError: 如果操作失败
        """
        # 参数校验
        if not isinstance(varRow, int) or varRow <= 0:
            raise ValueError("varRow 必须是大于0的整数")
        if not isinstance(varCol, int) or varCol <= 0:
            raise ValueError("varCol 必须是大于0的整数")
        if not isinstance(varSheet, (int, str)):
            raise ValueError("varSheet 必须是整数（索引）或字符串（名称）")

        try:
            # 获取工作表对象
            sh = self.sh(varSheet)

            # 获取单元格坐标
            return sh.cell(row=varRow, column=varCol).coordinate

        except Exception as e:
            raise IOError(f"获取单元格坐标失败: {e}") from e

    def getDimensions(self, varSheet=0):

        # 3.11 获取所有数据的坐标
        sh = self.sh(varSheet)
        return sh.dimensions


    # todo [清除]

    def clsRow(self, varNums, varSheet=0):
        """
        4.1 清空行（优化版）

        :param varNums: 行号，必须是大于0的整数
        :param varSheet: 工作表索引或名称，默认为0
        :raises ValueError: 如果参数不合法
        :raises IOError: 如果操作失败
        """
        # 参数校验
        if not isinstance(varNums, int) or varNums <= 0:
            raise ValueError("varNums 必须是大于0的整数")
        if not isinstance(varSheet, (int, str)):
            raise ValueError("varSheet 必须是整数（索引）或字符串（名称）")

        try:
            # 获取工作表对象
            sh = self.sh(varSheet)

            # 检查行号是否超出范围
            if varNums > sh.max_row:
                raise ValueError(f"行号 {varNums} 超出范围，最大行数为 {sh.max_row}")

            # 备份原始文件（可选）
            backup_path = self.file.replace(".xlsx", "_backup.xlsx")
            self.wb.save(backup_path)

            # 清空指定行的数据
            for col in range(1, sh.max_column + 1):
                cell = sh.cell(row=varNums, column=col)
                cell.value = None  # 清除值
                cell.font = None  # 清除字体样式
                cell.fill = PatternFill()  # 正确清除背景色
                cell.border = None  # 清除边框
                cell.alignment = None  # 清除对齐方式
                cell.number_format = ''  # 设置为空字符串，避免 None 错误
                cell.protection = None  # 清除保护设置

            # 保存更改
            self.save()

        except ValueError as ve:
            raise ValueError(f"参数错误: {ve}") from ve
        except IOError as ioe:
            raise IOError(f"文件操作失败: {ioe}") from ioe
        except Exception as e:
            raise IOError(f"清空行失败: {e}") from e

    def clsCol(self, varCol, varSheet=0, clear_header=True):
        """
        4.2 清空列（优化版）

        :param varCol: 列号，可以是整数（如2）或字符串（如'B'）
        :param varSheet: 工作表索引或名称，默认为0
        :param clear_header: 是否清除列标签（第一行），默认为True
        :raises ValueError: 如果参数不合法
        :raises IOError: 如果操作失败
        """
        # 参数校验
        if not isinstance(varCol, (int, str)):
            raise ValueError("varCol 必须是整数或字符串")
        if not isinstance(varSheet, (int, str)):
            raise ValueError("varSheet 必须是整数（索引）或字符串（名称）")
        if not isinstance(clear_header, bool):
            raise ValueError("clear_header 必须是布尔值")

        try:
            # 获取工作表对象
            sh = self.sh(varSheet)

            # 转换列标识为索引
            if isinstance(varCol, str):
                varCol = column_index_from_string(varCol)

            # 确定起始行
            start_row = 1 if clear_header else 2

            # 清空列数据
            for i in range(start_row, sh.max_row + 1):
                sh.cell(row=i, column=varCol).value = None

            # 保存更改
            self.save()

        except Exception as e:
            raise IOError(f"清空列失败: {e}") from e


    def delRow(self, varFrom, varSeries=1, varSheet=0):
        """
        4.3 删除连续行（优化版）

        :param varFrom: 起始行号，必须是大于0的整数
        :param varSeries: 删除的行数，默认为1
        :param varSheet: 工作表索引或名称，默认为0
        :raises ValueError: 如果参数不合法
        :raises IOError: 如果操作失败
        """
        # 参数校验
        if not isinstance(varFrom, int) or varFrom <= 0:
            raise ValueError("varFrom 必须是大于0的整数")
        if not isinstance(varSeries, int) or varSeries <= 0:
            raise ValueError("varSeries 必须是大于0的整数")
        if not isinstance(varSheet, (int, str)):
            raise ValueError("varSheet 必须是整数（索引）或字符串（名称）")

        try:
            # 获取工作表对象
            sh = self.sh(varSheet)

            # 执行删除操作
            sh.delete_rows(idx=varFrom, amount=varSeries)

            # 保存更改
            self.save()

        except Exception as e:
            raise IOError(f"删除行失败: {e}") from e

    def delCol(self, varFrom, varSeries=1, varSheet=0):
        """
        4.4 删除连续列（优化版）

        :param varFrom: 起始列，可以是整数（如2）或字符串（如'U'）
        :param varSeries: 删除的列数，默认为1
        :param varSheet: 工作表索引或名称，默认为0
        :raises ValueError: 如果参数不合法
        :raises IOError: 如果操作失败
        """
        # 参数校验
        if not isinstance(varFrom, (int, str)):
            raise ValueError("varFrom 必须是整数或字符串")
        if not isinstance(varSeries, int) or varSeries <= 0:
            raise ValueError("varSeries 必须是大于0的整数")
        if not isinstance(varSheet, (int, str)):
            raise ValueError("varSheet 必须是整数（索引）或字符串（名称）")

        try:
            # 获取工作表对象
            sh = self.sh(varSheet)

            # 转换列标识为索引
            if isinstance(varFrom, str):
                varFrom = column_index_from_string(varFrom)

            # 执行删除操作
            sh.delete_cols(idx=varFrom, amount=varSeries)

            # 保存更改
            self.save()

        except Exception as e:
            raise IOError(f"删除列失败: {e}") from e


    # todo [多表]


    def setColorByDiffByTwoFile(self, l_file1row, l_file2row):
        """
        5.2 对两个文件的工作表比较，对差异内容标注颜色（优化版）
        
        # print(Openpyxl_PO.setColorByDiffByTwoFile(Openpyxl_PO.getLL_row("Sheet2"), Openpyxl_PO2.getLL_row("Sheet2")))

        :param l_file1row: 第一个文件的行数据列表
        :param l_file2row: 第二个文件的行数据列表
        :return: 包含差异内容的字典，格式为 {"left": {...}, "right": {...}}；若无差异则返回 None
        :raises ValueError: 如果输入参数不合法
        :raises IOError: 如果操作失败
        """
        # 参数校验
        if not isinstance(l_file1row, list) or not isinstance(l_file2row, list):
            raise ValueError("输入参数必须是列表类型")

        try:
            # 初始化结果容器
            d_left = {}
            d_right = {}
            d_all = {}

            # 检查行数是否一致
            if len(l_file1row) != len(l_file2row):
                raise ValueError("两个文件的行数不一致，无法比较")

            # 遍历每一行，查找差异
            for i in range(len(l_file1row)):
                if l_file1row[i] != l_file2row[i]:
                    d_left_sub = {}
                    d_right_sub = {}
                    for j in range(len(l_file1row[i])):
                        if l_file1row[i][j] != l_file2row[i][j]:
                            # 记录差异字段及其值
                            d_left_sub[l_file1row[0][j]] = l_file1row[i][j]
                            d_right_sub[l_file2row[0][j]] = l_file2row[i][j]
                    if d_left_sub or d_right_sub:
                        d_left[i + 1] = d_left_sub
                        d_right[i + 1] = d_right_sub

            # 构造最终结果
            if d_left or d_right:
                d_all["left"] = d_left
                d_all["right"] = d_right
                return d_all
            else:
                return None  # 无差异时返回 None

        except Exception as e:
            raise IOError(f"比较文件时发生错误: {e}") from e


    def setColorByDiff(self, varSheet1, varSheet2):

        # 5.2 两工作表比较，对差异内容标注颜色
        # 前提条件，两sheet表的行列数一致，字段位置一致
        # Openpyxl_PO.setColorByDiff("Sheet1", "Sheet2")

        l_sheetOneRow = self.getLL_row(varSheet1)
        l_sheetTwoRow = self.getLL_row(varSheet2)

        if l_sheetOneRow == None or l_sheetTwoRow == None:
            print("[Error], " + varSheet1 + " 或 " + varSheet2 + " 不存在！")
            sys.exit(0)

        if len(l_sheetOneRow) == len(l_sheetTwoRow):
            for i in range(len(l_sheetOneRow)):
                for j in range(len(l_sheetOneRow[i])):
                    if l_sheetOneRow[i][j] != l_sheetTwoRow[i][j]:
                        self.setCellColor(i + 1, j + 1, "FF0000", varSheet1)
                        self.setCellColor(i + 1, j + 1, "ffeb9c", varSheet2)
                print("检查第" + str(i + 1) + "行")

            self.save()
        else:
            print("[warning], 两sheet的行数不一致！")
            sys.exit(0)

    def genSheetByDiff(self, varSheet1, varSheet2):
        """
        5.3 比较两工作表，对差异内容标注颜色，生成新表Sheet1&Sheet2，（优化版）
        # 支持灵活应对标题位置不一致的问题

        :param varSheet1: 第一个工作表名称
        :param varSheet2: 第二个工作表名称
        :return: 生成的新工作表名称
        :raises ValueError: 如果输入参数不合法
        :raises IOError: 如果操作失败
        """
        # 参数校验
        if varSheet1 not in self.wb.sheetnames:
            raise ValueError(f"工作表 '{varSheet1}' 不存在于当前文件中。可用的工作表包括：{self.wb.sheetnames}")
        if varSheet2 not in self.wb.sheetnames:
            raise ValueError(f"工作表 '{varSheet2}' 不存在于当前文件中。可用的工作表包括：{self.wb.sheetnames}")

        try:
            # 获取两个工作表的所有数据
            l_sheetOneRow = self.getLL_row(varSheet1)
            l_sheetTwoRow = self.getLL_row(varSheet2)

            if not l_sheetOneRow or not l_sheetTwoRow:
                raise ValueError("其中一个工作表为空，无法进行比较")

            # 提取标题行并建立列映射
            title1 = l_sheetOneRow[0]
            title2 = l_sheetTwoRow[0]

            # 构建标题到列索引的映射
            map1 = {title: idx for idx, title in enumerate(title1)}
            map2 = {title: idx for idx, title in enumerate(title2)}

            # 生成新工作表名称
            varSheet = f"{varSheet1}&{varSheet2}"
            self.delSheet(varSheet)
            self.addCoverSheet(varSheet, 99)

            # 写入标题行
            merged_title = list(map1.keys()) + [key for key in map2.keys() if key not in map1]
            self.setRows({1: merged_title}, varSheet)

            # 比较数据行
            max_rows = max(len(l_sheetOneRow), len(l_sheetTwoRow))
            for i in range(1, max_rows):  # 从第二行开始比较
                row_data = []
                for title in merged_title:
                    val1 = l_sheetOneRow[i][map1[title]] if i < len(l_sheetOneRow) and title in map1 else ""
                    val2 = l_sheetTwoRow[i][map2[title]] if i < len(l_sheetTwoRow) and title in map2 else ""

                    if val1 == "" and val2 == "":
                        row_data.append("")
                    elif val1 != val2:
                        row_data.append(f"{val1}/{val2}")
                        self.setCellColor(i + 1, len(row_data), "FF0000", varSheet)
                    else:
                        row_data.append(val1)
                self.setRows({i + 1: row_data}, varSheet)

            self.save()
            return varSheet

        except Exception as e:
            raise IOError(f"处理工作表失败: {e}") from e

    def moveValues(self, varFrom, varRows, varCols, varSheet=0):
        """
        6 移动区域数据（优化版）

        # Openpyxl_PO.moveValues('C1:D2', 3, -2)  # 把'C1:D2'区域移动到 下三行左二列
        # Openpyxl_PO.moveValues('A1:C14', 0, 3)  # 把'A1:C14'区域向右移动3列

        :param varFrom: 起始区域，如 'C1:D2'
        :param varRows: 移动的行数，正数向下移动，负数向上移动
        :param varCols: 移动的列数，正数向右移动，负数向左移动
        :param varSheet: 工作表索引或名称，默认为0
        :raises ValueError: 如果参数不合法
        :raises IOError: 如果操作失败
        """
        # 参数校验
        if not isinstance(varFrom, str) or not varFrom:
            raise ValueError("varFrom 必须是一个非空字符串，表示起始区域")
        if not isinstance(varRows, int) or not isinstance(varCols, int):
            raise ValueError("varRows 和 varCols 必须是整数")
        if not isinstance(varSheet, (int, str)):
            raise ValueError("varSheet 必须是整数（索引）或字符串（名称）")

        try:
            # 获取工作表对象
            sh = self.sh(varSheet)

            # 执行移动操作
            sh.move_range(varFrom, rows=varRows, cols=varCols)

            # 保存更改
            self.save()
        except Exception as e:
            raise IOError(f"移动区域数据失败: {e}") from e

    def sortFields(self, varSheetName):
        """
        7 将表格第一行（标题）排序（从小打大）（优化版）

        :param varSheet1: 工作表名称
        :raises ValueError: 如果输入参数不合法
        :raises IOError: 如果文件读取或写入失败
        return：生成 {表名}_标题升序, 如表名字：sheet1， 结果：sheet1_标题升序
        """

        if varSheetName not in self.wb.sheetnames:
            raise ValueError(f"工作表 '{varSheetName}' 不存在于当前文件中。可用的工作表包括：{self.wb.sheetnames}")

        # 参数校验
        if not isinstance(varSheetName, str):
            raise ValueError("varSheet1 必须是一个字符串")

        try:
            # 获取第一行标题
            l_title = self.getL_row(1, varSheetName)
            if not l_title:
                raise ValueError("工作表中没有找到标题行")

            # 排序标题
            l_sortAsc = sorted(l_title)

            # 创建新工作表并写入排序后的标题
            varNewSheet = varSheetName + "_" + "标题升序"
            self.addSheet(varNewSheet)
            self.setRows({1: l_sortAsc}, varNewSheet)

            # 获取原始列数据
            col = self.getLL_col(varSheetName)

            # 根据排序后的标题重新排列列数据
            for i in range(len(col)):
                for j in range(len(l_sortAsc)):
                    if col[i][0] == l_sortAsc[j]:
                        self.setCols({str(j + 1): col[i]}, varNewSheet)

            self.save()

        except FileNotFoundError as e:
            raise IOError(f"文件未找到: {varSheetName}") from e
        except Exception as e:
            raise IOError(f"处理工作表失败: {varSheetName}") from e


    # todo [转换]


    def dict2xlsx(self, varDict, varExcelFile):
        """
        8.1 字典转xlsx

        :param varDict: 输入的字典数据
        :param varExcelFile: 输出的Excel文件路径
        :raises ValueError: 如果输入参数不合法
        :raises IOError: 如果文件写入失败
        """
        # 参数校验
        if not isinstance(varDict, dict):
            raise ValueError("varDict 必须是一个字典")
        if not isinstance(varExcelFile, str) or not varExcelFile.endswith('.xlsx'):
            raise ValueError("varExcelFile 必须是一个以 .xlsx 结尾的有效文件路径")

        try:
            # 检查文件路径是否存在，如果不存在则创建目录
            directory = os.path.dirname(varExcelFile)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            # 将字典转换为DataFrame并写入Excel文件
            df = pd.DataFrame(varDict)
            df.to_excel(varExcelFile, encoding="utf_8_sig", index=False)

        except PermissionError as e:
            raise IOError(f"权限不足，无法写入文件: {varExcelFile}") from e
        except Exception as e:
            raise IOError(f"写入Excel文件失败: {varExcelFile}") from e
    def dict2csv(self, varDict, varExcelFile):
        """
        8.2 字典转csv

        :param varDict: 输入的字典数据
        :param varExcelFile: 输出的CSV文件路径
        :raises ValueError: 如果输入参数不合法
        :raises IOError: 如果文件写入失败
        """
        # 参数校验
        if not isinstance(varDict, dict):
            raise ValueError("varDict 必须是一个字典")
        if not isinstance(varExcelFile, str) or not varExcelFile.endswith('.csv'):
            raise ValueError("varExcelFile 必须是一个以 .csv 结尾的有效文件路径")

        try:
            # 检查文件路径是否存在，如果不存在则创建目录
            directory = os.path.dirname(varExcelFile)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            # 将字典转换为DataFrame并写入Excel文件
            df = pd.DataFrame(varDict)
            df.to_csv(varExcelFile, encoding="utf_8_sig", index=False)

        except PermissionError as e:
            raise IOError(f"权限不足，无法写入文件: {varExcelFile}") from e
        except Exception as e:
            raise IOError(f"写入csv文件失败: {varExcelFile}") from e
    def pdf2xlsx(self, varPdfFile, varExcelPath):
        """
        8.3 pdf中表格转xlsx（优化版）

        :param varPdfFile: 输入的PDF文件路径
        :param varExcelPath: 输出的Excel文件路径前缀
        :raises ValueError: 如果输入参数不合法
        :raises IOError: 如果文件读取或写入失败
        """
        # 参数校验
        if not isinstance(varPdfFile, str) or not os.path.isfile(varPdfFile):
            raise ValueError("varPdfFile 必须是一个有效的文件路径")
        if not isinstance(varExcelPath, str):
            raise ValueError("varExcelPath 必须是一个字符串")

        try:
            # 检查输出目录是否存在，如果不存在则创建
            output_dir = os.path.dirname(varExcelPath)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # 打开PDF文件
            with pdfplumber.open(varPdfFile) as pdf:
                for i, page in enumerate(pdf.pages):
                    tables = page.extract_tables()
                    if tables:
                        for j, table in enumerate(tables):
                            df = pd.DataFrame(table)
                            # 获取 df 的第一行数据作为表头（列名）
                            df_header = df.iloc[0]
                            # 将之前保存的第一行数据设置为新的列名
                            df.columns = df_header
                            # 从第二行开始截取数据，去掉原来的第一行（表头行）
                            df = df.iloc[1:].reset_index(drop=True)
                            # 写入Excel文件
                            output_file = f'{varExcelPath}_第{i + 1}页第{j + 1}张表.xlsx'
                            df.to_excel(output_file, index=False)
        except FileNotFoundError as e:
            raise IOError(f"文件未找到: {varPdfFile}") from e
        except Exception as e:
            raise IOError(f"处理PDF文件失败: {varPdfFile}") from e
    def xlsx2list(self, varExcelFile, sheetName):
        """
        8.4 xlsx转列表（优化版）

        :param varExcelFile: 输入的Excel文件路径
        :param sheetName: 工作表名称
        :return: 转换后的列表，如果失败则返回None
        :raises ValueError: 如果输入参数不合法
        :raises IOError: 如果文件读取失败
        """
        # 参数校验
        if not isinstance(varExcelFile, str) or not os.path.isfile(varExcelFile):
            raise ValueError("varExcelFile 必须是一个有效的文件路径")
        if not isinstance(sheetName, str):
            raise ValueError("sheetName 必须是一个字符串")

        try:
            # 读取Excel文件
            df = pd.read_excel(varExcelFile, sheet_name=sheetName, header=None)
            # 转换为NumPy数组再转为列表
            t = np.array(df)
            return t.tolist()
        except FileNotFoundError as e:
            raise IOError(f"文件未找到: {varExcelFile}") from e
        except Exception as e:
            raise IOError(f"读取Excel文件失败: {varExcelFile}") from e
    def xlsx2dict(self, varExcelFile, varType, sheetName):
        """
        8.5 xlsx转字典（优化版）

        :param varExcelFile: 输入的Excel文件路径
        :param varType: 返回字典的类型，"col" 表示按列返回，"row" 表示按行返回
        :param sheetName: 工作表名称
        :return: 转换后的字典，如果失败则返回None
        :raises ValueError: 如果输入参数不合法
        :raises IOError: 如果文件读取失败
        """
        # 参数校验
        if not isinstance(varExcelFile, str) or not os.path.isfile(varExcelFile):
            raise ValueError("varExcelFile 必须是一个有效的文件路径")
        if varType not in ["col", "row"]:
            raise ValueError("varType 必须是 'col' 或 'row'")
        if not isinstance(sheetName, str):
            raise ValueError("sheetName 必须是一个字符串")

        try:
            # 读取Excel文件
            df = pd.read_excel(varExcelFile, sheet_name=sheetName, header=None)

            # 根据varType选择返回格式
            if varType == "col":
                d_ = df.to_dict()  # 以列形式返回
                # 以列形式返回, 如：
                # {0: {0: ' 与户主关系 ', 1: '子', 2: '父亲', 3: '女儿'},
                # 1: {0: ' 性别 ', 1: '女', 2: '男', 3: '无法识别'},
                # 2: {0: ' 民族 ', 1: '回族', 2: '汉族', 3: '壮族'}
            elif varType == "row":
                d_ = df.to_dict(orient='index')  # 以行形式返回
                # 以行形式返回，如：
                # {0: {0: ' 与户主关系 ', 1: ' 性别 ', 2: ' 民族 '},
                # 1: {0: '子', 1: '女', 2: '回族'},
                # 2: {0: '父亲', 1: '男', 2: '汉族'},
                # 3: {0: '女儿', 1: '无法识别', 2: '壮族'}}

            return d_

        except FileNotFoundError as e:
            raise IOError(f"文件未找到: {varExcelFile}") from e
        except Exception as e:
            raise IOError(f"读取Excel文件失败: {varExcelFile}") from e


if __name__ == "__main__":

    Openpyxl_PO = OpenpyxlPO("/Users/linghuchong/Downloads/51/Python/project/PO/data/11.xlsx")
    # Openpyxl_PO = OpenpyxlPO("d:\\51\\python\\project\\PO\\data\\11.xlsx")
    # Openpyxl_PO.sortFields("job")
    # Openpyxl_PO.renameSheet("1231", "444")
    # Openpyxl_PO.open()


    # print("1.1 新建".center(100, "-"))
    # OpenpyxlPO("/Users/linghuchong/Downloads/51/Python/project/PO/data/qq1.xlsx", 'new')
    # Openpyxl_PO = OpenpyxlPO("/Users/linghuchong/Downloads/51/Python/project/PO/data/qq1.xlsx")
    # Openpyxl_PO.open()


    # print("1.1 新建".center(100, "-"))
    # Openpyxl_PO.newExcel("./OpenpyxlPO/newfile2.xlsx", ["mySheet1", "mySheet2", "mySheet3"])  # 新建excel，生成三个工作表（mySheet1,mySheet2,mySheet3），默认定位在第一个mySheet1表。
    # Openpyxl_PO.newExcel("d://t44.xlsx", ["mySheet661", "mySheet552", "mySheet32"])  # 新建excel，生成三个工作表（mySheet1,mySheet2,mySheet3），默认定位在第一个mySheet1表。

    # print("1.2 打开".center(100, "-"))
    # Openpyxl_PO.open(1)  # 打开第二个工作表
    # Openpyxl_PO.open() # 打开第一个工作表
    # Openpyxl_PO.open('test')  # 打开test工作表

    # print("1.6 添加工作表(不覆盖)".center(100, "-"))
    # Openpyxl_PO.addSheet("saasuser1")

    # print("1.7 添加工作表(覆盖)".center(100, "-"))
    # Openpyxl_PO.addCoverSheet("Sheet0", 0)    # 第一个位置添加工作表
    # Openpyxl_PO.addCoverSheet("Sheet100", 100)    # 第100个位置添加工作表  //当index足够大时，则在最后一个位置添加工作表
    # Openpyxl_PO.open()

    # print("1.8 删除工作表".center(100, "-"))
    # Openpyxl_PO.delSheet("Sheet1")
    # Openpyxl_PO.delSheet("mySheet1")



    # print("2.0.1 在第N行前插入多行空白".center(100, "-"))
    # Openpyxl_PO.insertNullRows(5)  # 在第5行前插入一行空白

    # print("2.0.2 在第N列前插入多列空白".center(100, "-"))
    # Openpyxl_PO.insertCols(3)  # 在第3列前插入1列空白， 等同于 insertCols(3, 1)
    # Openpyxl_PO.insertCols(3, 2)  # 在第3列前插入2列空白， 等同于 insertCols(3, 1)

    # print("2.1 更新单元格值".center(100, "-"))
    # Openpyxl_PO.setCell(1, 'B', "hello")
    # Openpyxl_PO.setCell(1, 3, "hello")

    # print("2.2 插入行数据".center(100, "-"))
    # Openpyxl_PO.insertRows({2: ["金浩", "101", "102"]}, "Sheet1")

    # print("2.3 更新行数据".center(100, "-"))
    # Openpyxl_PO.setRows({2: ["金浩", "101", "102"], 5: ["yoyo", "123", "666"]})
    # Openpyxl_PO.setRows({7: ["你好", 12345, "7777"], 8: ["44", None, "777777777"]})  # 对最后一个sheet表，对第7，8行分别写入内容，如遇None则跳过该单元格
    # Openpyxl_PO.setRows({7: ["你好", 12345, "7777"], 8: ["44", "None", "777777777"]}, -1)  # 对最后一个sheet表，对第7，8行分别写入内容
    # Openpyxl_PO.open()

    # print("2.4 追加行数据".center(100, "-"))
    # Openpyxl_PO.appendRows([['姓名', '电话', '成绩', '学科'], ['毛泽东', 15266606298, 14, '化学'], ['周恩来', 15201077791, 78, '美术']])


    # print("2.5 插入列数据".center(100, "-"))
    # Openpyxl_PO.insertCols({"a": ["姓名", "张三", "李四"], "c": ["年龄", "55", "34"]})

    # print("2.6 更新列数据".center(100, "-"))
    # Openpyxl_PO.setCols({"A": [None, "k1", 666, "777"], "C": [None, "888", None, "999"]})  # 对最后一个sheet表，对第7，8行分别写入内容，如遇None则跳过该单元格

    # print("2.7 追加列数据".center(100, "-"))
    # Openpyxl_PO.appendCols([["test", "张三", "李四"], ["dev", "55", "34"]])



    # print("2.5 设置单元格行高与列宽".center(100, "-"))
    # Openpyxl_PO.setCellDimensions(3, 30, 'f', 34)  # 设置第三行行高30，第f列宽34

    # print("2.5.2 设置单行多列行高与列宽".center(100, "-"))
    # Openpyxl_PO.setRowColDimensions(5, 30, ['f', 'h'], 33)  # 设置第五行行高30，f - h列宽33

    # print("2.6 设置所有单元格的行高与列宽".center(100, "-"))
    # Openpyxl_PO.setAllCellDimensions(30, 20)

    # print("2.7 设置所有单元格自动换行".center(100, "-"))
    # Openpyxl_PO.setAllWordWrap()
    # Openpyxl_PO.setAllWordWrap("Sheet1")

    # print("2.8 设置冻结首行".center(100, "-"))
    # Openpyxl_PO.setFreeze('A2', "saasuser")

    # print("2.9 设置单元格对齐样式".center(100, "-"))
    # Openpyxl_PO.setCellAlignment(5, 4, 'center', 'top')
    # Openpyxl_PO.setCellAlignment(1, "e", 'center', 'top', 45)
    # Openpyxl_PO.setCellAlignment(1, 1, 'center', 'top', 45, True)
    # Openpyxl_PO.setCellAlignment(5, 4, 'center', 'center', "saasuser1")

    # print("2.9.2 设置单行多列对齐样式".center(100, "-"))
    # Openpyxl_PO.setRowColAlignment(1, ["c", "e"], 'center', 'center')  # 第一行第c,d,e列居中
    # Openpyxl_PO.setRowColAlignment(9, "all", 'center', 'center')  # 第九行全部居中

    # print("2.9.3 设置所有单元格对齐样式".center(100, "-"))
    # Openpyxl_PO.setAllCellAlignment('center', 'center')

    # print("2.10 设置筛选列".center(100, "-"))
    # Openpyxl_PO.setFilterCol("all")  # 全部筛选
    # Openpyxl_PO.setFilterCol("") # 取消筛选
    # Openpyxl_PO.setFilterCol("A2") # 对A2筛选

    # print("2.11 设置单元格字体（字体、字号、粗斜体、下划线、颜色）".center(100, "-"))
    # Openpyxl_PO.setCellFont(1, 6)  # 设置第一行第六列字体（默认微软雅黑字号16粗体）
    # Openpyxl_PO.setCellFont(2, "f")  # 设置第一行第f列字体（默认微软雅黑字号16粗体）
    # Openpyxl_PO.setCellFont(5, "f", size=14, bold=True, color="red")
    # Openpyxl_PO.setCellFont(5, "f", size=14, bold=True)

    # print("2.11.2 设置单行多列字体".center(100, "-"))
    # Openpyxl_PO.setRowColFont(1, ["b", "h"])  # 第一行第b-h列
    # Openpyxl_PO.setRowColFont(9, "all")  # 第九行

    # print("2.11.3 设置所有单元格字体".center(100, "-"))
    # Openpyxl_PO.setAllCellFont()

    # print("2.12 设置单元格边框".center(100, "-"))
    # Openpyxl_PO.setBorder(1, 2, left = ['thin','ff0000'], right = ['thick','ff0000'], top = ['thin','ff0000'],bottom = ['thick','ff0000'])

    # print("2.13 设置单元格填充背景色".center(100, "-"))
    # Openpyxl_PO.setPatternFill(2, 2, 'solid', '006100')  # 单元格背景色

    # print("2.14 设置单元格填充渐变色".center(100, "-"))
    # Openpyxl_PO.setGradientFill(3, 3, stop=["FFFFFF", "99ccff", "000000"])

    # print("2.15 设置单元格背景色".center(100, "-"))
    # Openpyxl_PO.setCellColor(5, 1)  # 清除第5行第1列的背景色
    # Openpyxl_PO.setCellColor(5, "d")  # 清除第5行d列的背景色
    # Openpyxl_PO.setCellColor(5, 1, "ff0000", "Sheet2")  # 设置第五行第1列设置红色
    # Openpyxl_PO.setCellColor(5, "e", "ff0000")  # 设置第五行e列设置红色
    # Openpyxl_PO.setCellColor(None, None)  # 清除所有背景色

    # print("2.15.2 设置单行多列背景色".center(100, "-"))
    # Openpyxl_PO.setRowColColor(5, ['b', 'd'], "ff0000") # 设置第五行第b，c，d列背景色
    # Openpyxl_PO.setRowColColor(7, "all", "ff0000")  # 设置第五行所有列背景色

    # print("2.15.3 设置所有单元格背景色".center(100, "-"))
    # Openpyxl_PO.setAllCellColor("ff0000")  # 设置所有单元格背景色
    # Openpyxl_PO.setAllCellColor(None)  # 清除所有单元格背景色

    # print("2.16 设置整行(可间隔)背景色".center(100, "-"))
    # Openpyxl_PO.setRowColor(5, 0, "ff0000")  # 从第3行开始每行颜色标红色
    # Openpyxl_PO.setRowColor(3, 1, "ff0000")  # 从第3行开始每隔1行颜色标红色

    # print("2.17 设置整列(可间隔)背景色".center(100, "-"))
    # Openpyxl_PO.setColColor(2, 0, "ff0000")  # 从第2列开始每列颜色为红色
    # Openpyxl_PO.setColColor(2, 1, "ff0000")  # 从第2列开始每隔1列设置颜色为红色

    # print("2.18 设置工作表背景颜色".center(100, "-"))
    # Openpyxl_PO.setSheetColor("FF0000")



    # print("3.1 获取总行列数".center(100, "-"))
    # print(Openpyxl_PO.getL_shape())  # [7,5]

    # print("3.2 获取单元格值".center(100, "-"))
    # print(Openpyxl_PO.getCell(3, 2))  # 获取第3行第2列的值

    # print("3.3 获取一行数据".center(100, "-"))
    # print(Openpyxl_PO.getL_row(1))  # ['Number具体数', '高地', 'jinhaoyoyo', '状态', '名字']
    #
    # print("3.4 获取一列数据".center(100, "-"))
    # print(Openpyxl_PO.getL_col(1, include_header=True))  # ['高地', 40, 44, 50, 30, 25, 150]
    # print(Openpyxl_PO.getL_col('B',include_header=False))  # ['高地', 40, 44, 50, 30, 25, 150]

    # print("3.5.1 获取每行数据".center(100, "-"))
    # print(Openpyxl_PO.getLL_row(include_header=True))  # [['age', 'city', 'hello', 'name'], [2, 'shanghai', 'wow', 'jinhao'],
    # print(Openpyxl_PO.getLL_row(include_header=False))  # [[2, 'shanghai', 'wow', 'jinhao'],
    #
    # print("3.5.2 获取带行号的每行数据".center(100, "-"))
    # print(Openpyxl_PO.getD_rowNumber_row(include_header=True))  # {1: ['age', 'city', 'hello', 'name'], 2: [2, 'shanghai', 'wow', 'jinhao'],
    # print(Openpyxl_PO.getD_rowNumber_row(include_header=False))  # {2: [2, 'shanghai', 'wow', 'jinhao'],

    # print("3.5.3 获取部分列的行数据".center(100, "-"))
    # print(Openpyxl_PO.getLL_rowOfPartialCol([1, 3]))   # [['Number具体数', 'jinhaoyoyo'], [2, 30], [3, 25], [4, 30], [5, 10], [6, 5], [7, 10]] //获取1和3列的行数据
    # print(Openpyxl_PO.getLL_rowOfPartialCol(['a', 'C']))  # 同上
    # print(Openpyxl_PO.getLL_rowOfPartialCol(["A", 3]))   # 同上
    # print(Openpyxl_PO.getLL_rowOfPartialCol([1, 3, 2, "a", "C", "B"]))   # [['Number具体数', '山丘', '高地'], [2, 30, 40], [3, 25, 44], [4, 30, 50], [5, 10, 30], [6, 5, 25], [7, 10, 150]] //获第1，3，2列的行数据，"a", "C", "B"忽略
    #
    # print("3.5.4 获取带行号的部分列的行数据".center(100, "-"))
    # print(Openpyxl_PO.getD_rowNumber_rowOfpartialCol([1, 3]))   # {1: ['Number具体数', 'jinhaoyoyo'], 2: [2, 30], 3: [3, 25], 4: [4, 30], 5: [5, 10], 6: [6, 5], 7: [7, 10]}
    # print(Openpyxl_PO.getD_rowNumber_rowOfpartialCol([1, 4, 3]))   # {1: ['Number具体数', 'jinhaoyoyo'], 2: [2, 30], 3: [3, 25], 4: [4, 30], 5: [5, 10], 6: [6, 5], 7: [7, 10]}
    # print(Openpyxl_PO.getD_rowNumber_rowOfpartialCol([1, 'C']))   # {1: ['Number具体数', 'jinhaoyoyo'], 2: [2, 30], 3: [3, 25], 4: [4, 30], 5: [5, 10], 6: [6, 5], 7: [7, 10]}
    # print(Openpyxl_PO.getD_rowNumber_rowOfpartialCol(['a', 'C']))   # {1: ['Number具体数', 'jinhaoyoyo'], 2: [2, 30], 3: [3, 25], 4: [4, 30], 5: [5, 10], 6: [6, 5], 7: [7, 10]}



    # print("3.6.1 获取每列数据".center(100, "-"))
    # print(Openpyxl_PO.getLL_col(include_header=True))  # [['age', 2, 12, 4, 5], ['city', 'shanghai', 'beijin', 'nanjin', 'henei'],
    # print(Openpyxl_PO.getLL_col(include_header=False))  # [[2, 12, 4, 5], ['shanghai', 'beijin', 'nanjin', 'henei'],
    #
    # print("3.6.2 获取带列序号的每列数据".center(100, "-"))
    # print(Openpyxl_PO.getD_colNumber_col(include_header=True))
    # print(Openpyxl_PO.getD_colNumber_col(include_header=False))
    # print(d_seq_row)  # {1: ['Number具体数', 2, 3, 4, 5, 6, 7], 2: ['高地', 40, 44, 50, 30, 25, 150],,...}
    # del d_seq_row[1]  # 删除第一行，一般用于去掉标题
    # print(d_seq_row)  # {2: ['高地', 40, 44, 50, 30, 25, 150], 3: ['jinhaoyoyo', 30, 25, 30, 10, 5, 10],...}
    #
    # print("3.6.3 获取带列字母的每列数据".center(100, "-"))
    # print(Openpyxl_PO.getD_colLetter_col(include_header=True))  # {'A': ['age', 2, 12, 4, 5], 'B': ['city', 'shanghai', 'beijin', 'nanjin', 'henei'], ...
    # print(Openpyxl_PO.getD_colLetter_col(include_header=False))  # {'A': [2, 12, 4, 5], 'B': ['shanghai', 'beijin', 'nanjin', 'henei'],...

    # print("3.8.1 获取标题的序号".center(100, "-"))
    # print(Openpyxl_PO.getL_columnHeaderNumber(["age", "name"]))  # [2, 5]
    #
    # print("3.8.2 获取标题的字母".center(100, "-"))
    # print(Openpyxl_PO.getL_columnHeaderLetter(["age", "name"]))  # ['B', 'E']

    # print("3.8.3 将标题转列字典序列".center(100, "-"))
    # print(Openpyxl_PO.getD_colNumber_columnTitle(["age", "name"]))  # {2: '高地', 5: '名字'}
    #
    # print("3.8.4 将标题转列字典字母".center(100, "-"))
    # print(Openpyxl_PO.getD_colLetter_columnTitle(["age", "name"]))  # {'A': '高地', 'C': '名字'}

    # l_colSeq = (Openpyxl_PO.title2colSeq(["高地", "名字"]))
    # print(l_colSeq)  # [2, 5]
    # print(Openpyxl_PO.getLL_rowOfPartialCol(l_colSeq)) # [['高地', '名字'], [40, 'jinhao'], [44, 'yoyo'], [50, 'titi'], [30, 'mama'], [25, 'baba'], [150, 'yeye']]
    #
    # l_colSeq = (Openpyxl_PO.getTitleCol(["高地", "名字"]))
    # print(l_colSeq)  # [2, 5]

    # print("3.9 获取部分列的列值(可忽略多行)".center(100, "-"))
    # print(Openpyxl_PO.getLL_partialColOfPartialCol([1, 3], [1, 4]))   # 获取第1,3列列值，并忽略第1，4行的行值。
    # print(Openpyxl_PO.getLL_partialColOfPartialCol([2], [], "job_标题升序"))  # 获取第2列所有值。

    # print("3.10 获取单元格的坐标".center(100, "-"))
    # print(Openpyxl_PO.getCoordinate(2, 5))   # E2

    # print("3.11 获取工作表数据的坐标".center(100, "-"))
    # print(Openpyxl_PO.getDimensions())  # A1:E17



    # print("4.1 清空行".center(100, "-"))
    # Openpyxl_PO.clsRow(2)  # 清空第2行

    # print("4.2 清空列".center(100, "-"))
    # Openpyxl_PO.clsCol(2, clear_header=True)  # 清空第2列
    # Openpyxl_PO.clsCol(2, clear_header=False)  # 清空第2列


    # print("4.3 删除行".center(100, "-"))
    # Openpyxl_PO.delRow(2)  # 删除第2行
    # Openpyxl_PO.delRow(2, 3)  # 删除第2行之连续3行（删除2，3，4行）
    #
    # print("4.4 删除列".center(100, "-"))
    # Openpyxl_PO.delCol(1, 2)  # 删除第1列之连续2列（删除1，2列）
    # # Openpyxl_PO.delCol(2, 1, "python")  # 删除第2列之连续1列（删除2列）
    # Openpyxl_PO.delCol('D', 1)  # 删除第D列之连续1列（删除D列）

    # print("5.1 两表比较获取差异内容（两表标题与行数必须一致） ".center(100, "-"))
    # Openpyxl_PO = OpenpyxlPO("./data/loanStats.xlsx")
    # Openpyxl_PO2 = OpenpyxlPO("./data/loanStats2.xlsx")
    print(Openpyxl_PO.setColorByDiffByTwoFile(Openpyxl_PO.getLL_row("Sheet2"), Openpyxl_PO2.getLL_row("Sheet2")))

    # # print("5.2 对一张表的两个sheet进行数据比对，差异数据标注颜色 ".center(100, "-"))
    # Openpyxl_PO = OpenpyxlPO("./data/loanStats.xlsx")
    # Openpyxl_PO.setColorByDiff("job", "job1")

    # # print("5.3 对一张表的两个sheet进行数据比对，将结果写入第一个sheet ".center(100, "-"))
    # Openpyxl_PO.genSheetByDiff("job", "job1")

    # # print("6 移动区域".center(100, "-"))
    # Openpyxl_PO.moveValues('C1:D2', 3, -2)  # 把'C1:D2'区域移动到 下三行左二列
    # Openpyxl_PO.moveValues('A1:C14', 0, 3)  # 把'A1:C14'区域向右移动3列

    # # print("7 将excel中标题（第一行字段）排序（从小打大）".center(100, "-"))
    # Openpyxl_PO.sortFields("Sheet1")


    # Openpyxl_PO.open()