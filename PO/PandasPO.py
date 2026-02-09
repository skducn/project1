# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-11-13
# Description: pandas
# pandas是基于NumPy数组构建的，使数据预处理、清洗、分析工作变得更快更简单。
# pandas是专门为处理表格和混杂数据设计的，而NumPy更适合处理统一的数值数组数据。
# pandas有两个主要数据结构：Series和DataFrame。
# Python利用pandas处理Excel数据的应用 https://www.cnblogs.com/liulinghua90/p/9935642.html
# to_sql https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
# ********************************************************************************************************************

"""
【转换】
1.0 字典转xlsx  dict2xlsx()
1.1 字典转csv  dict2csv()
1.2 pdf中表格转xlsx pdf2xlsx()
1.3 xlsx转列表 xlsx2list()
1.4 xlsx转字典 xlsx2dict()
1.5 字典转text  dict2text()

2.0 将df输出html
"""

import os,pdfplumber
import pandas as pd
import numpy as np

import logging
logging.basicConfig(level=logging.INFO)

from PO.TimePO import *
Time_PO = TimePO()


class PandasPO:

    def __init__(self):
        pass

    # todo [转换]

    def dict2xlsx(self, varDict, varExcelFile):
        """
        1.0 字典转xlsx

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
        1.1 字典转csv

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
        1.2 pdf中表格转xlsx（优化版）

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
        1.3 xlsx转列表（优化版）

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
        1.4 xlsx转字典（优化版）

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

    def dict2text(self, varDict, varTextFile, format="json", compress=False):
        """
        1.5 字典转text（优化版）

        :param varDict: 输入的字典数据
        :param varTextFile: 输出的文本文件路径
        :param format: 输出格式，支持 "json" 或 "csv"，默认为 "json"
        :param compress: 是否启用压缩（仅对 json 格式生效），默认为 False
        :raises ValueError: 如果输入参数不合法
        :raises IOError: 如果文件写入失败
        """
        # 参数校验
        if not isinstance(varDict, dict):
            raise ValueError("varDict 必须是一个字典")
        if not isinstance(varTextFile, str):
            raise ValueError("varTextFile 必须是一个字符串")
        if format not in ["json", "csv"]:
            raise ValueError("format 必须是 'json' 或 'csv'")

        try:
            # 检查并创建目标文件所在目录
            directory = os.path.dirname(varTextFile)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            # 构造 DataFrame
            df = pd.DataFrame.from_dict(varDict, orient='index').T  # 转置以适配常见字典结构

            # 根据格式写入文件
            if format == "json":
                if compress:
                    varTextFile += ".gz"  # 启用压缩时添加 .gz 后缀
                    df.to_json(varTextFile, compression='gzip')
                else:
                    df.to_json(varTextFile)
            elif format == "csv":
                df.to_csv(varTextFile, index=False, encoding="utf_8_sig")

        except PermissionError as e:
            raise IOError(f"权限不足，无法写入文件: {varTextFile}") from e
        except FileNotFoundError as e:
            raise IOError(f"文件路径不存在: {varTextFile}") from e
        except Exception as e:
            logging.error(f"将字典 {varDict} 转换为 {format} 格式时发生错误: {e}")
            raise IOError(f"写入文件失败: {varTextFile}") from e

    def toHtml(self, df, title, filePrefix):
        # title = "页面标题工作日志"
        # filePrefix = "文件名前缀"

        # 将df输出html
        try:
            pd.set_option('colheader_justify', 'center')  # 对其方式居中
            html = '''<html><head><title>''' + str(title) + '''</title></head>
              <body><b><caption>''' + str(title) + '''_''' + str(
                Time_PO.getDate()) + '''</caption></b><br><br>{table}</body></html>'''
            style = '''<style>.mystyle {font-size: 11pt; font-family: Arial;border-collapse: collapse;border: 1px solid silver;}.mystyle td, 
            th {padding: 5px;}.mystyle tr:nth-child(even) {background: #E0E0E0;}.mystyle tr:hover {background: silver;cursor:pointer;}</style>'''
            # rptNameDate = "report/" + str(filePrefix) + str(Time_PO.getDate()) + ".html"
            rptNameDate = str(filePrefix) + str(Time_PO.getDate()) + ".html"
            with open(rptNameDate, 'w') as f:
                f.write(style + html.format(table=df.to_html(classes="mystyle", col_space=100, index=False)))
        except Exception as e:
            print(f"将df {df} 输出html时发生错误: {e}")
            logging.error(f"将df {df} 输出html时发生错误: {e}")
            raise



if __name__ == "__main__":

    Pandas_PO = PandasPO()

    data = {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [25, 30, 35]}
    # df = pd.DataFrame(data)
    # print(df[df['Age']>26])


    # print("1.0 字典转xlsx".center(100, "-"))
    # Pandas_PO.dict2xlsx({'A': [3, 4, 8, 9], 'B': [1.2, 2.4, 4.5, 7.3], 'C': ["aa", "bb", "cc", "dd"]}, "./data/dict2xlsx.xlsx")

    # print("1.1 字典转csv ".center(100, "-"))
    # Pandas_PO.dict2csv({'A': [3, 4, 8, 9], 'B': [1.2, 2.4, 4.5, 7.3], 'C': ["aa", "bb", "cc", "dd"]}, "./data/dict2csv.csv")

    # print("1.3 xlsx转列表".center(100, "-"))
    # print(Pandas_PO.xlsx2list('./data/dict2xlsx.xlsx', 'Sheet1'))


    # print("1.5 字典转text".center(100, "-"))
    # Pandas_PO.dict2text({'A': [3, 4, 8, 9], 'B': [1.2, 2.4, 4.5, 7.3], 'C': ["aa", "bb", "cc", "dd"]}, "./data/dict2text.txt")
    # Pandas_PO.dict2text(data, "./output/data.json", format="json", compress=True)
    # Pandas_PO.dict2text(data, "./output/data.csv", format="csv")


    # # todo Series类型
    # arr1 = np.arange(10)
    # print(arr1)  # [0 1 2 3 4 5 6 7 8 9]
    # print(type(arr1))  # <类与实例 'numpy.ndarray'>
    # for i in arr1:
    #     print(i)
    #
    # s1 = pd.Series(arr1)
    # print(s1)   # 第一列是索引，第二列是列表值
    # # 0    0
    # # 1    1
    # # 2    2
    # # 3    3
    # # 4    4
    # # 5    5
    # # 6    6
    # # 7    7
    # # 8    8
    # # 9    9
    #
    # # Series和ndarray之间的主要区别在于Series之间的操作会根据索引自动对齐数据。
    #
    #
    # # todo DataFrame类型
    # # DataFrame是一个表格型的数据类型，每列值类型可以不同，是最常用的pandas对象。
    # # DataFrame既有行索引也有列索引，它可以被看做由Series组成的字典（共用同一个索引）。
    # # DataFrame中的数据是以一个或多个二维块存放的（而不是列表、字典或别的一维数据结构）。
    #
    # data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada', 'Nevada'],
    #         'year': [2000, 2001, 2002, 2001, 2002, 2003],
    #         'pop': [1.5, 1.7, 3.6, 2.4, 2.9, 3.2]}
    # df = pd.DataFrame(data)
    # print(df)
    # #     state  year  pop
    # # 0    Ohio  2000  1.5
    # # 1    Ohio  2001  1.7
    # # 2    Ohio  2002  3.6
    # # 3  Nevada  2001  2.4
    # # 4  Nevada  2002  2.9
    # # 5  Nevada  2003  3.2
    #
    # # 输出指定列（columns） , 及指定索引号（index）#，不存在的列debt则输出NaN
    # df2 = pd.DataFrame(data, columns=['year', 'state', 'pop', 'debt'], index=['one', 'two', 'three', 'four', 'five', 'six'])
    # print(df2)
    # #        year   state  pop debt
    # # one    2000    Ohio  1.5  NaN
    # # two    2001    Ohio  1.7  NaN
    # # three  2002    Ohio  3.6  NaN
    # # four   2001  Nevada  2.4  NaN
    # # five   2002  Nevada  2.9  NaN
    # # six    2003  Nevada  3.2  NaN
    #
    # print(df2.columns)
    # # Index(['year', 'state', 'pop', 'debt'], dtype='object')
    #
    # print(df2['state'])
    # # one        Ohio
    # # two        Ohio
    # # three      Ohio
    # # four     Nevada
    # # five     Nevada
    # # six      Nevada
    # # Name: state, dtype: object
    #
    # #列可以通过赋值的方式进行修改。例如，我们可以给那个空的"debt"列赋上一个标量值或一组值
    # df2['debt'] = 16.5
    # print(df2)
    # #        year   state  pop  debt
    # # one    2000    Ohio  1.5  16.5
    # # two    2001    Ohio  1.7  16.5
    # # three  2002    Ohio  3.6  16.5
    # # four   2001  Nevada  2.4  16.5
    # # five   2002  Nevada  2.9  16.5
    # # six    2003  Nevada  3.2  16.5
    #
    #
    #
    # # DataFrame方式是可以使用嵌套字典，如果嵌套字典传给DataFrame，pandas就会被解释为外层字典的键作为列，内层字典键则作为行索引：
    # pop = {'Nevada': {2001: 2.4, 2002: 2.9},'Ohio': {2000: 1.5, 2001: 1.7, 2002: 3.6}}
    # df3 = pd.DataFrame(pop)
    # print(df3)
    # #       Nevada  Ohio
    # # 2001     2.4   1.7
    # # 2002     2.9   3.6
    # # 2000     NaN   1.5
    #
    #
    #
    # # 读取数据
    # data = pd.read_csv('test.csv')
    # print(data)
    # data = pd.read_csv('test.csv', sep=';',  nrows=20, skiprows=[2, 5])    # 读取前 20 行数据，并移除第 2 行和第 5 行
    # print(data)
    #
    # # 保存数据
    # data.to_csv('test.csv', index=None)
    # # data.to_csv('test.csv')   # 如果没有Index=None 则每次保存后会多一列序号。
    #
    # # 查看前三行数据
    # print(data.head(3))
    #
    # # print(data.loc[1,"level"])
    # #
    # # df = pd.read_excel('d:\\cases.xlsx') #这个会直接默认读取到这个Excel的第一个表单
    # # data = df.head()#默认读取前5行的数据
    # # print(data)
    # #
    # # # print("获取到所有的值:\n{0}".format(data))#格式化输出
    # #
    # # df=pd.read_excel('d:\\cases.xlsx',sheet_name='test_case')#可以通过sheet_name来指定读取的表单
    # # data=df.head()#默认读取前5行的数据
    # # print("获取到所有的值:\n{0}".format(data))#格式化输出
    # #
    # #
    # # data=df.iloc[0].values#0表示第一行 这里读取数据并不包含表头，要注意哦！
    # # # .ix is deprecated. Please use
    # # # .loc for label based indexing or
    # # # .iloc for positional indexing
    # # print("读取指定行的数据：\n{0}".format(data))
    # #
    # # data=df.iloc[[1,2]].values#读取指定多行的话，就要在ix[]里面嵌套列表指定行数
    # # print("读取指定行的数据：\n{0}".format(data))
    # #
    # # data=df.iloc[1,1]#读取第一行第1列的值，这里不需要嵌套列表
    # # print("读取指定行的数据：\n{0}".format(data))
    # #
    # #
    # # data=df.loc[[1,2],['年龄','金额']].values#读取第一行第二行的title以及data列的值，这里需要嵌套列表
    # # print("读取指定行的数据：\n{0}".format(data))
