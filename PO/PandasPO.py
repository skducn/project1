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
1 执行sql  execute()

2.1 xlsx转数据库 xlsx2db()
2.2 字典转数据库  dict2db()
2.3 列表转数据库  list2db()  默认标签如 0，1，2，3，4为字段名

3.1 数据库转xlsx(含字段或不含字段)  db2xlsx()
3.2 字典转xlsx  dict2xlsx()
3.3 字典转csv  dict2csv()
3.4 字典转text  dict2text()

4 xlsx转列表

将df输出html
"""


from PO.MysqlPO import *
from sqlalchemy import create_engine
import numpy

from PO.TimePO import *
Time_PO = TimePO()

class PandasPO:
    def __init__(self):

        pass

    # def __init__(self, host, name, password, db, port):
    #
    #     self.host = host
    #     self.name = name
    #     self.password = password
    #     self.db = db
    #     self.port = port
    #     self.Mysql_PO = MysqlPO(self.host, self.name, self.password, self.db, self.port)
    #     self.engine = create_engine('mysql+mysqldb://' + self.name + ':' + self.password + '@' + self.host + ':' + str(self.port) + '/' + self.db)
    #     # self.engine = create_engine('mysql+mysqldb://root:Zy123456@192.168.0.234:3306/crmtest?charset=utf8')

    def execute(self, varSql):

        """
        1 执行sql
        """

        try:
            if "SELECT" in varSql or "select" in varSql:
                return self.engine.execute(varSql).fetchall()
            else:
                self.engine.execute(varSql)
        except Exception as e:
            print(e)

    def xlsx2dbXXX(
        self,
        varExcelFile,
        varTable,
        usecols=None,
        nrows=None,
        skiprows=None,
        dtype=None,
        parse_dates=None,
        date_parser=None,
        converters=None,
        sheet_name=None,
        index=False,
    ):

        """
        4.4 excel导入数据库表(覆盖)
        :return:
        参数参考：https://zhuanlan.zhihu.com/p/96203752
        """

        df = pd.read_excel(
            varExcelFile,
            usecols=usecols,
            nrows=usecols,
            skiprows=skiprows,
            dtype=dtype,
            parse_dates=parse_dates,
            date_parser=date_parser,
            converters=converters,
            sheet_name=sheet_name,
        )
        df.to_sql(
            varTable, con=self.getEngine_mysqldb(), if_exists="replace", index=index
        )

    def xlsx2db(self, varExcelFile, varTable):

        """2.1 xlsx导入数据库"""
        try:
            df = pd.read_excel(varExcelFile)
            engine = self.Mysql_PO.getMysqldbEngine()
            df.to_sql(varTable, con=engine, if_exists="replace", index=False)
        except Exception as e:
            print(e)

    def dict2db(self, varDict, varDbTable, index):

        """2.2 字典导入数据库"""

        try:
            df = pd.DataFrame(varDict)
            engine = self.Mysql_PO.getMysqldbEngine()
            if index == "False":
                df.to_sql(name=varDbTable, con=engine, if_exists="replace", index=False)
            else:
                df.to_sql(name=varDbTable, con=engine, if_exists="replace")
        except Exception as e:
            print(e)

    def list2db(self, varList, varDbTable, index):

        """2.3 列表导入数据库"""

        try:
            df = pd.DataFrame(varList, columns=None)
            engine = self.Mysql_PO.getMysqldbEngine()
            if index == "False":
                df.to_sql(name=varDbTable, con=engine, if_exists="replace", index=False)
            else:
                df.to_sql(name=varDbTable, con=engine, if_exists="replace")
        except Exception as e:
            print(e)

    def db2xlsx(self, sql, varExcelFile, header=1):

        """3.1 数据库转xlsx(含字段或不含字段)"""

        try:
            df = pd.read_sql(sql, self.engine)
            # header=None表示不含列名
            if header == None:
                df.to_excel(varExcelFile, index=None, header=None)
            else:
                df.to_excel(varExcelFile, index=None)
        except Exception as e:
            print(e)

    def dict2xlsx(self, varDict, varExcelFile):

        """3.2 字典转xlsx"""

        try:
            df = pd.DataFrame(varDict)
            df.to_excel(varExcelFile, encoding="utf_8_sig", index=False)
        except Exception as e:
            print(e)

    def dict2csv(self, varDict, varExcelFile):

        """3.3 字典转csv"""

        try:
            df = pd.DataFrame(varDict)
            df.to_csv(varExcelFile, encoding="utf_8_sig", index=False)
        except Exception as e:
            print(e)

    def dict2text(self, varDict, varTextFile):

        """3.4 字典转text"""

        try:
            df = pd.DataFrame(varDict)
            df.to_json(varTextFile)
        except Exception as e:
            print(e)

    def xlsx2list(self, pathFile, sheetName):

        """4 xlsx转列表"""

        try:
            df = pd.read_excel(pathFile, sheet_name=sheetName, header=None)
            t = numpy.array(df)
            return t.tolist()
        except Exception as e:
            print(e)


    def toHtml(self, df, title, filePrefix):
        # title = "页面标题工作日志"
        # filePrefix = "文件名前缀"

        # 将df输出html
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


if __name__ == "__main__":

    # Pandas_PO = PandasPO("192.168.0.234", "root", "Zy123456", "mcis", 3306)

    Pandas_PO = PandasPO()
    #
    # # print("1 执行sql".center(100, "-"))
    # # 查询
    # print(
    #     Pandas_PO.execute("select * FROM t_third_user where id=%s" % "89")
    # )  # [(89, '37068500001', 'wenyonghong', '370627197007140240', '温永红')]
    # # print(Pandas_PO.execute("SELECT * FROM t_third_user where id=%s" % "89")[0][1])  # 37068500001
    # # 更新
    # Pandas_PO.execute("UPDATE test2 SET B = '5.6' WHERE A = %s" % "4")
    # # 批量修改字段名和字段类型
    # Pandas_PO.execute(
    #     "alter table test55 change `index` id int(100), change `0` `name` varchar(30) ,change `1` ssn char(30), change `2` phone_number char(30), change `3` genEmail varchar(30),"
    #     " change `4` genAddress varchar(50), change `5` genPostcode char(30), change `6` genCompany varchar(30), change `7` genUrl char(50), "
    #     "change `8` genIpv4 char(30),change `9` genText text(330)"
    # )
    # # 设置id主键
    # Pandas_PO.execute("alter table test55 add primary key(id)")

    # print("2.1 xlsx转数据库".center(100, "-"))
    # Pandas_PO.xlsx2db("./data/xlsx2db.xlsx", 'test2')

    # print("2.2 字典转数据库".center(100, "-"))
    Pandas_PO.dict2db({'A': [3, 4, 8, 9], 'B': [1.2, 2.4, 4.5, 7.3], 'C': ["aa", "bb", "cc", "dd"]}, "test33", "")
    # Pandas_PO.dict2db({'A': [3, 4, 8, 9], 'B': [1.2, 2.4, 4.5, 7.3], 'C': ["aa", "bb", "cc", "dd"]}, "test33", "False")

    # print("2.3 列表转数据库".center(100, "-"))
    # Pandas_PO.list2db([[1,2,3],['a','b','c']], "test44", "")  # 生成index
    # Pandas_PO.list2db([[1,2,3],['a','b','c']], "test44", "False")  # 不生成index

    # print("3.1 数据库转xlsx(含字段或不含字段)".center(100, "-"))
    Pandas_PO.db2xlsx("SELECT * FROM t_pregnancy_evaluate_advice", './data/db2xlsx.xlsx')
    # Pandas_PO.db2xlsx("SELECT * FROM t_pregnancy_evaluate_advic1e", './data/db2xlsx_notitle.xlsx', None)  # 不导出字段名

    # print("3.2 字典转xlsx".center(100, "-"))
    # Pandas_PO.dict2xlsx({'A': [3, 4, 8, 9], 'B': [1.2, 2.4, 4.5, 7.3], 'C': ["aa", "bb", "cc", "dd"]}, "./data/dict2xlsx.xlsx")

    # print("3.3 字典转csv ".center(100, "-"))
    # Pandas_PO.dict2csv({'A': [3, 4, 8, 9], 'B': [1.2, 2.4, 4.5, 7.3], 'C': ["aa", "bb", "cc", "dd"]}, "./data/dict2csv.csv")

    # print("3.4 字典转text".center(100, "-"))
    # Pandas_PO.dict2text({'A': [3, 4, 8, 9], 'B': [1.2, 2.4, 4.5, 7.3], 'C': ["aa", "bb", "cc", "dd"]}, "./data/dict2text.txt")

    # print("4 xlsx转列表".center(100, "-"))
    # print(Pandas_PO.xlsx2list('./data/dict2xlsx.xlsx', 'Sheet1'))

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
