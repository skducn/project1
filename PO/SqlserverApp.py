# -- coding: utf-8 --
# ***************************************************************
# Author     : John
# Data       : 2019-04-16
# Description: SqlServerPO 对象层
# /usr/local/pip3.7 install pymssql
# sql server 查询数据库所有的表名 + 字段  https://www.cnblogs.com/TF12138/p/4064752.html

# todo pymssql
# pymssql官网：http://www.pymssql.org/en/stable/index.html
# 官方API：http://www.pymssql.org/en/stable/ref/pymssql.html
# pymssql是基于_mssql模块做的封装，是为了遵守python的DBAPI规范接口
# python连接sql server数据库实现增删改查 https://www.cnblogs.com/malcolmfeng/p/6909293.html
# pymssql 托管在Github上：https://github.com/pymssql

# todo 乱码
# Q1，dbeaver工具中数据库表中的中文在pymssql查询输出却是乱码。
# 分析：默认情况下SqlServer使用ISO字符集（latin1字符集），而pymssql模块默认utf编码方式解码，数据库中的中文被python以二进制方式读取后以utf8方式解码显示为乱码，其二进制数据未改变。
# 解决：str.encode('latin1').decode('GB2312')
# 注意：windows系统上有此问题，而mac上无此问题。

# Q2：数据库中中文显示乱码，但查询后中文正确显示。
# 解决：在pymssql.Connect中添加 charset='utf8' ,确保 charset 与数据库编码一致，如数据库是gb2312 , 则charset='gb2312'。
# conn = pymssql.Connect(host='localhost', user='root', passwd='root', db='python',charset='utf8')

# Q3：数据库排序规则是Chinese_PRC_CI_AS, 可以使用GB18030读取得到中文。
# 分析：至于为什么不用GB2312呢，因为包含的字符个数：GB2312 < GBK < GB18030，如果用GB2312，在可能报错：“UnicodeDecodeError: 'gb2312' codec can't decode byte 0xa9 in position 0: illegal multibyte sequence”
# create_engine("mssql+pymssql://" + self.user + ":" + self.password + "@" + self.server + "/" + self.database + "?charset=GB18030")

# Q4：读取SQLSERVER数据库中文显示乱码问题。
# 分析：由数据库中的字段的类型问题导致, 如：varchar显示乱码而 ncarchar正常
# 解决：在select语句中直接通过 convert(nvarchar(20), remark) 转换。

# todo 报错
# Q5：Cannot insert explicit value for identity column in table 't' when identity_insert is set to OFF
# 分析：当 identity insert 设置为 off 时，无法为表中的标识列插入显式值，就是自增设置了off后，不能手动在唯一索引上添加值。
# 解决：
# set identity_insert[tableName] on
# inset ...
# set identity_insert[tableName] off

# Errors 1000 - 1999 https://learn.microsoft.com/en-us/previous-versions/sql/sql-server-2008/cc645860(v=sql.100)
# 关于 1753 Column '%.*ls.%.*ls' is not the same length or scale as referencing column '%.*ls.%.*ls' in foreign key '%.*ls'. Columns participating in a foreign key relationship must be defined with the same length and scale.
# 发生在外键关联失败，请检查表结构，是否在关联的字段类型与尺寸一致。


# todo 数据库中的NULL
# SQLserver中，NULL表示缺失或未知的数据
# python中，没有NULL，只有None，None的类型为NoneType ，None是一个对象。
# None不等于0、""(空字符串)、False等。
# 在Python中，None、0、""(空字符串)、[](空列表)、()(空元组)、{}(空字典)都是 False

# Sqlserver中判断NULL值
# select * from table where name IS NOT NULL   //判断name列不为空的值
# select * from table where name IS NULL

# coalesce函数，简化对多个列或表达式进行判断的过程。
# select * from 健康干预 where coalesce(hitQty,'1') = 2  //条件是hitQty=2的值

# todo sqlalchemy中create_engine用法 (https://blog.csdn.net/xc_zhou/article/details/118829588)
# engine = create_engine('数据库类型+驱动://用户名:密码@服务器IP:端口/数据库?charset=utf8')
# pymssql:
# engine = create_engine('mssql+pymssql://scott:tiger@hostname:port/dbname')
# Microsoft SQL Server:
# engine = create_engine('mssql+pyodbc://scott:tiger@mydsn')
# SQLite:
# engine = create_engine('sqlite:///foo.db')
# engine = create_engine('sqlite:absolute/path/to/foo.db')

# sqlalchemy+pandas：错误 'OptionEngine' object has no attribute 'execute'，'str' object has no attribute '_execute_on_connection'
# https://www.cnblogs.com/bruce-he/p/17113269.html

#SqlServer判断表、列不存在则创建 &&ExecuteNonQuery 要求命令拥有事务
# https://blog.csdn.net/Andrewniu/article/details/78028207

# https://blog.51cto.com/u_16213439/7729728
# sys.foreign_keys视图：该视图包含了数据库中所有的外键的信息，包括外键名称、关联表、主表等。

# 获取日期时间为：年-月-日 时：分：秒， 如：2024-01-30 14:50：12
# select CONVERT(nvarchar(20), getdate(),120) as Sdatetime from a_student;
# 获取日期时间为：年-月-日 时：分， 如：2024-01-30 14:50
# select substring(convert(varchar,getdate(),120),1,16) as Sdatetime from a_student;
# 获取日期时间为：年-月-日 时， 如：2024-01-30 14
# select substring(convert(varchar,getdate(),120),1,13) as Sdatetime from a_student;
# ***************************************************************

"""
1.0 查询带参数
1.1 查询 select(sql)
1.2 执行 execute(sql)
1.3 执行多条 executemany(sql, value)
1.4 执行存储过程 execCall(varProcedureName, params=())
1.5 执行sql文件 execSqlFile(varPathSqlFile)
1.6 执行sql文件2 execSqlFile2(varPathSqlFile)
1.7 关闭 close()

2.1 获取所有表名  getTables(self)
2.2 获取所有表的数量 getTablesQTY(self)
2.3 获取所有视图 getViews()
2.4 获取所有视图的数量 getViewsQTY()
2.5 获取所有表名及表注释 getTableAndComment(varTable='all')
2.6 获取表结构信息 getStructure(varTable='all')
2.7 获取字段名  getFields(varTable)
2.8 获取{字段:注释}字典映射 getFieldComment(varTable)
2.9 获取记录数 getRecordQty(varTable)
2.10 获取所有字段及类型 getFieldsAndTypes(varTable)
2.11 获取字段及类型 getFieldAndType(varTable, varField)
2.12 获取必填项字段及类型 getNotNullFieldAndType（varTable）
2.13 获取自增主键 getIdentityPrimaryKey(varTable)
2.14 获取主键  getPrimaryKey（self, varTable）
2.15 获取主键最大值 getPrimaryKeyMaxValue（self, varTable)
2.16 获取所有外键 getForeignKey()

3.1 创建表 crtTable(self, varTable, sql)
3.2 生成类型值 _genTypeValue(self, varTable)
3.3 生成必填项类型值 _genNotNullTypeValue(self, varTable)
3.4 单表自动生成第一条数据 genFirstRecord(self, varTable)
3.5 所有表自动生成第一条数据 genFirstRecordByAll()
3.6 自动生成数据 genRecord(self, varTable)
3.7 自动生成必填项数据 genRecordByNotNull(self, varTable)
3.8 执行insert _execInsert(self, varTable, d_init,{})
3.9 删除表的所有外键关系 dropKey(varTable)
3.10 设置表注释 setTableComment(varTable, varComment)
3.11 修改表注释 reviseTableComment(varTable, varComment)
3.12 设置字段注释 setFieldComment(varTable, varField, varComment)
3.13 修改字段注释  reviseFieldComment(varTable, varField, varComment)
3.14 设置数据类型与备注 setFieldTypeComment(varTable, varField, varType, varComment)
3.15 设置自增主键 setIdentityPrimaryKey(varTable, varField)

4.1 判断表是否存在 isTable(self, varTable)
4.2 判断字段是否存在 isField(self, varTable, varField)
4.3 判断是否有自增主键 isIdentity(self, varTable)

5.1 csv2dbByType()  csv2db自定义字段类型
5.2 csv2dbByAutoType()  csv2db自动生成字段类型
5.3 xlsx2db  excel导入数据库
5.4 dict2db  字典导入数据库
5.5 list2db  列表导入数据库
5.6 df2db    DataFrame导入数据库

6.1 db2csv   数据库sql导出csv
6.2 db2xlsx  数据库sql导出xlsx
6.3 db2dict  数据库sql导出字典
6.4 db2html  数据库sql导出html
6.5 db2df    数据库sql导出DataFrame

7.1 查看表结构（字段、类型、大小、可空、注释），注意，表名区分大小写  desc()   //实例请参考 instance/db/sqlserver.py
7.2 查找记录 record('*', 'money', '%34.5%')  //实例请参考 instance/db/sqlserver.py
7.3 插入记录 insert()

"""
from PO.SqlserverPO import *


# todo 社区健康平台（静安）
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHC_JINGAN", "GBK")
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHC", "GBK")


# 社区
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHC", "GBK")
# a = Sqlserver_PO.select("select ruleParam from a_test123 where result='john'")
# print(a)
# print(a[0]['ruleParam'])
#
# b = a[0]['ruleParam'].split("\n")
# print(b)
#
# for i,v in enumerate(b,start=1):
#     print(i,v)

# a = Sqlserver_PO.selectParam("select * from a_test where id=%s", 3)
# print(a)

# print("1.2 执行".center(100, "-"))
# 创建表（如存在先删除）
# Sqlserver_PO.execute(""" IF OBJECT_ID('a_test', 'U') IS NOT NULL DROP TABLE a_test
# CREATE TABLE a_test (
#     id INT NOT NULL,
#     name VARCHAR(100),
#     salesrep VARCHAR(100),
#     PRIMARY KEY(id)
# )
# """)

# 插入1条记录
# Sqlserver_PO.execute("INSERT INTO a_test values(4, 'John Smith6662', 'John Doe3')")

# # 插入多条记录
# Sqlserver_PO.executemany("INSERT INTO a_test VALUES (%d, %s, %s)", [(1, 'John Smith2', 'John Doe3'), (2, 'Jane Doe', 'Joe Dog'), (3, 'Mike T.', 'Sarah H.')])

# 更新数据
# Sqlserver_PO.execute("UPDATE a_test set name='john123' where id=1")

# # 删除1条记录
# Sqlserver_PO.execute("DELETE FROM a_test WHERE id = 2")

# 删除所有记录
# Sqlserver_PO.execute("TRUNCATE TABLE a_test")

# # 删除表
# Sqlserver_PO.execute("DROP TABLE a_test")



# # print("2.1 获取所有表名".center(100, "-"))
# print(Sqlserver_PO.getTables())  # ['condition_item', 'patient_demographics', 'patient_diagnosis' ...
#
# # print("2.2 获取所有表数量".center(100, "-"))
# print(Sqlserver_PO.getTablesQTY())  # 105
#
# # print("2.3 获取所有视图名".center(100, "-"))
# print(Sqlserver_PO.getViews())  # ['TB_YFJZ_MYJZJBXX', 'TB_CHSS_GRJKDA', 'TB_CHSS_YWGMS' ...
#
# # print("2.4 获取所有视图数量".center(100, "-"))
# print(Sqlserver_PO.getViewsQTY())  # 42

# # print("2.5 获取所有表和表注释".center(100, "-"))
# print(Sqlserver_PO.getTableComment())  # {'ASSESS_DIAGNOSIS': '门诊数据', 'ASSESS_MEDICATION': '评估用药情况表',...}    #
# print(Sqlserver_PO.getTableComment('a_test%'))
# print(Sqlserver_PO.getTableComment('QYYH'))  # {'QYYH': '1+1+1签约信息表'}

# print("2.6 获取表结构信息".center(100, "-"))
# print(Sqlserver_PO.getStructure('a_test'))
# print(Sqlserver_PO.getStructure())

# print("2.7 获取字段名".center(100, "-"))
# print(Sqlserver_PO.getFields('SYS_USER'))  # ['id', 'name', 'age']

# print("2.8 获取字段和字段注释".center(100, "-"))
# print(Sqlserver_PO.getFieldComment('SYS_USER'))  # {'id': '编号', 'name': None, 'salesrep': None}
#

# print("2.9 获取记录数".center(100, "-"))
# print(Sqlserver_PO.getRecordQTY('a_test'))  # 3

# print("2.10 获取所有字段及类型".center(100, "-"))
# print(Sqlserver_PO.getFieldsAndTypes("a_test"))  # {'ID': 'int', 'NAME': 'text', 'AGE': 'int', 'ADDRESS': 'char', 'SALARY': 'float'}
#
# print("2.11 获取字段及类型".center(100, "-"))
# print(Sqlserver_PO.getFieldAndType("a_test", ["id"]))  # {'ID': 'int'}
# print(Sqlserver_PO.getFieldAndType("a_test", ["id", 'name']))  # {'ID': 'int', 'AGE': 'int'}


# print("2.12 获取必填项字段及类型".center(100, "-"))
# print(Sqlserver_PO.getNotNullFieldAndType('a_test'))  # {'ID': 'int', 'NAME': 'text', 'AGE': 'int', 'ADDRESS': 'char'}
#
# print("2.13 获取自增主键".center(100, "-"))
# print(Sqlserver_PO.getIdentityPrimaryKey('a_test'))  # None // 没有自增主键
# print(Sqlserver_PO.getIdentityPrimaryKey('SYS_DRUG'))  # ID
# #
# print("2.14 获取主键".center(100, "-"))
# print(Sqlserver_PO.getPrimaryKey('bbb'))  # [{'COLUMN_NAME': 'ADDRESS'}, {'COLUMN_NAME': 'ID'}]
# print(Sqlserver_PO.getPrimaryKey('a_test'))  # [{'COLUMN_NAME': 'id'}]

# print("2.15 获取表主键最大值 ".center(100, "-"))
# print(Sqlserver_PO.getPrimaryKeyMaxValue('a_test'))  # {'id': 4}

# print("2.16 获取所有外键 ".center(100, "-"))
# print(Sqlserver_PO.getForeignKey())  # []   //没有返回空列表


# https://www.jb51.net/article/264740.htm

# print("3.1 创建表（自增id主键）".center(100, "-"))
# Sqlserver_PO.crtTable('a_phs2gw', '''
#     id INT IDENTITY(1,1) PRIMARY KEY,
#     phsField VARCHAR(20) NOT NULL,
#     phsValue VARCHAR(20) NOT NULL,
#     phusersField VARCHAR(20) NOT NULL,
#     phusersValue VARCHAR(20) NOT NULL''')

# Sqlserver_PO.crtTable('bbb', ''''CREATE TABLE bbb (
# id INT IDENTITY(1,1) PRIMARY KEY,
# name VARCHAR(20) NOT NULL,
# age INT NOT NULL) go''')

# print("3.1 创建表（ID主键） ".center(100, "-"))
# Sqlserver_PO.crtTable('aaa', '''CREATE TABLE aaa
#        (ID INT PRIMARY KEY     NOT NULL,
#         NAME           TEXT    NOT NULL,
#         AGE            INT     NOT NULL,
#         ADDRESS        CHAR(50),
#         SALARY         REAL);''')

# print("3.2 生成类型值".center(100, "-"))
# print(Sqlserver_PO._genTypeValue("aaa"))  # {'ID': 1, 'NAME': 'a', 'AGE': 1, 'ADDRESS': 'a', 'SALARY': 1.0, 'time': '08:12:23'}

# print("3.3 生成必填项类型值".center(100, "-"))
# print(Sqlserver_PO._genNotNullTypeValue("aaa"))

# print("3.4 单表自动生成第一条数据".center(100, "-"))
# Sqlserver_PO.genFirstRecord('bbb')

# print("3.5 所有表自动生成第一条数据".center(100, "-"))
# Sqlserver_PO.genFirstRecordByAll()

# print("3.6 自动生成数据".center(100, "-"))
# Sqlserver_PO.genRecord('aaa')

# print("3.7 自动生成必填项数据".center(100, "-"))
# Sqlserver_PO.genRecordByNotNull('aaa')



# # print("4.1 判断表是否存在".center(100, "-"))
# print(Sqlserver_PO.isTable("aaa"))
#
# # print("4.2 判断字段是否存在(字段区分大小写)".center(100, "-"))
# print(Sqlserver_PO.isField('bbb', 'id'))
#
# # print("4.3 判断是否有自增主键".center(100, "-"))
# print(Sqlserver_PO.isIdentity('bbb'))
# print(Sqlserver_PO.isIdentity('aaa'))



# # print("5.1 csv2db自定义字段类型".center(100, "-"))
# Sqlserver_PO.csv2dbByType('./data/test12.csv', "test555")

# # print("5.2 csv2db自动生成字段类型".center(100, "-"))
# Sqlserver_PO.csv2dbByAutoType('./data/test12.csv', "test555")

# # print("5.3 excel导入数据库".center(100, "-"))
# Sqlserver_PO.xlsx2db('./data/area.xlsx', "hello", "test333")

# print("5.4 字典导入数据库".center(100, "-"))
# Sqlserver_PO.dict2db({'A': [3, 4, 8, 9], 'B': [1.2, 2.4, 4.5, 7.3], 'C': ["aa", "bb", "cc", "dd"]}, "test99")  # 带index
# Sqlserver_PO.dict2db({'A': [3, 4, 8, 9], 'B': [1.2, 2.4, 4.5, 7.3], 'C': ["aa", "bb", "cc", "dd"]}, "test99", "False")  # 不带index

# print("5.5 列表导入数据库".center(100, "-"))
# Sqlserver_PO.list2db(['name','age','sex'], [['1','2','3'],['a','b','c']], "test99")  # 生成index
# Sqlserver_PO.list2db(['name','age','sex'], [['1','2','3'],['a','b','c']], "test99", "False")  # 不生成index

# print("5.6 DataFrame导入数据库".center(100, "-"))
# df = Sqlserver_PO.db2df("select * from a_test")
# print(df)
# Sqlserver_PO.df2db(df, "a_test1")



# print("6.1 数据库sql导出csv(含字段或不含字段)".center(100, "-"))
# Sqlserver_PO.db2csv("SELECT * FROM test99", './data/test99.csv')
# Sqlserver_PO.db2csv("SELECT * FROM test99", './data/test99.csv', None)  # 不导出字段名

# print("6.2 数据库sql导出xlsx(含字段或不含字段)".center(100, "-"))
# Sqlserver_PO.db2xlsx("SELECT * FROM test99", './data/test99.xlsx')  # 导出字段
# Sqlserver_PO.db2xlsx("SELECT * FROM test99", './data/test99.xlsx', None)  # 不导出字段

# print("6.3 数据库sql导出字典".center(100, "-"))
# print(Sqlserver_PO.db2dict("SELECT * FROM a_phs_auth")) # {'index': [0, 1], 'name': ['1', 'a'], 'age': ['2', 'b'], 'sex': ['3', 'c']}
# print(Sqlserver_PO.db2dict2("SELECT * FROM a_phs_auth")) # {'index': [0, 1], 'name': ['1', 'a'], 'age': ['2', 'b'], 'sex': ['3', 'c']}
# print(Sqlserver_PO.db2dict("SELECT * FROM test99", 'series'))
# {'index': 0    0
# 1    1
# Name: index, dtype: int64, 'name': 0    1
# 1    a
# Name: name, dtype: object, 'age': 0    2
# 1    b
# Name: age, dtype: object, 'sex': 0    3
# 1    c
# Name: sex, dtype: object}

# print("6.4 数据库sql导出html".center(100, "-"))
# Sqlserver_PO.db2html("select ID, pResult as 正向, nResult as 反向, QC_type as 类型, QC_field as 质控字段, QC_rule as 质控规则, QC_desc as 错我描述"
#                      ", pCase as 正向用例, nCase as 反向用例, pCheck as 正向校验 from A_testrule", 'ehr_rule_result.html')

# # print("6.5 数据库sql导出DataFrame".center(100, "-"))
# df = Sqlserver_PO.db2df("select * from a_test")
# print(df)
# df.style.highlight_max(color='lime').highlight_min().to_excel('hello1.xlsx', index=False)  # 输出到excel带颜色


# print("7.1 查看表结构".center(100, "-"))
# Sqlserver_PO.desc()
# Sqlserver_PO.desc(['id', 'page'])
# Sqlserver_PO.desc('a_c%')
# Sqlserver_PO.desc({'a_%':['id','sql']})
# Sqlserver_PO.desc('QYYH')
# Sqlserver_PO.desc({'a_test':['number', 'rule1']})

# print("7.2 查找记录".center(100, "-"))
# Sqlserver_PO.record('t_upms_user', 'varchar', '%e10adc3949ba59abbe56e057f20f883e')  # 搜索 t_upms_user 表中内容包含 admin 的 varchar 类型记录。
# Sqlserver_PO.record('*', 'varchar', '%海鹰居委会%')
# Sqlserver_PO.record('*', 'money', '%34.5%')
# Sqlserver_PO.record('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
# Sqlserver_PO.record('*', 'datetime', u'%2019-07-17 11:19%')  # 模糊搜索所有表中带2019-01的timestamp类型。

# print("7.3 插入记录".center(100, "-"))
# Sqlserver_PO.insert("a_test", {'result': str(Fake_PO.genPhone_number('Zh_CN', 1)), 'createDate': Time_PO.getDateTimeByPeriod(0), 'ruleParam': 'param'})




