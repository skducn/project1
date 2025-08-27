# -- coding: utf-8 --
# ***************************************************************
# Author     : John
# Data       : 2019-04-16
# Description: SqlserverPO 对象层
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
# print(b'\xd6\xf7\xbc\xfc\xd7\xd4\xd4\xf6'.decode('gbk'))
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

# SqlServer判断表、列不存在则创建 &&ExecuteNonQuery 要求命令拥有事务
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

# todo【表】
2.1 判断表是否存在 isTable(self, varTable)
2.2 获取表结构信息 getStructure(varTable='all')
2.3 查看表结构（字段、类型、大小、可空、注释），注意，表名区分大小写  desc()   //实例请参考 instance/db/sqlserver.py
2.4 获取表 getTables()
2.5 获取表名与表注释 getTableComment(varTable='all')
2.6 获取视图 getViews()
2.7 创建表（覆盖） crtTableByCover()
2.8 创建表（忽略，如原表存在则忽略不创建） crtTableByExistIgnore()
2.9 设置表注释（添加，修改，删除） setTableComment(varTable, varComment)
2.10 复制表， copyTable(source,target)
2.11 删除表的所有外键关系 dropKey

# todo【字段】
3.1 判断字段是否存在 isField(self, varTable, varField)
3.2 判断自增主键是否存在 isIdentity(self, varTable)
3.3 获取字段 getFields(varTable)
3.4 获取字段名与字段注释 getFieldComment(varTable，varEncoding="GBK")
3.5 获取字段名与字段类型 getFieldType(varTable)
3.6 获取非空（必填）字段与类型 getNotNullFieldType（varTable）
3.7 获取自增主键 getIdentityPrimaryKey(varTable)
3.8 获取主键或组合键  getPrimaryKey（self, varTable）
3.9 获取主键最大值 getPrimaryKeyMaxValue（self, varTable)
3.10 获取所有外键关联表 getForeignKey()
3.11 追加字段 appendField('a_phs_auth_app', 'status123', 'VARCHAR(11)')
3.12 插入字段 insertBeforeField('a_phs_auth_app', 'url', 'case1', 'varchar(111)')
3.13 设置字段注释（添加、修改、删除） setFieldComment(varTable, varField, varComment)
3.14 设置字段类型 setFieldType(varTable, varField, varType)
3.15 设置自增主键 setIdentityPrimaryKey(varTable, varField)
3.16 删除自增主键 delIdentityPrimaryKey(varTable, varField)
3.17 设置字段类型与备注 setFieldTypeComment(varTable, varField, varType, varComment)


# todo【记录】
4.1 获取记录数 getRecordCount(varTable)
4.2 插入记录（1条或多条记录）
4.3 更新
4.4 删除（删除1条或所有记录）
4.5 查找记录 record('*', 'money', '%34.5%')  //实例请参考 instance/db/sqlserver.py
4.6 生成第一条记录 genFirstRecord()
4.7 所有空表自动生成第一条记录 genFirstRecordByAll()
4.8 自动添加一条记录 genRecord()
4.9 自动生成必填项记录 genRecordByNotNull(self, varTable)
 生成类型值 _genTypeValue(self, varTable)
 生成必填项类型值 _genNotNullTypeValue(self, varTable)
 执行insert _execInsert(self, varTable, d_init,{})
4.10 判断记录是否存在 isRecord("QYYH", "SFZH", "310101198004110014"))


# todo【导入、导出】
5.1 csv2dbByType()  csv2db自定义字段类型
5.2 csv2dbByAutoType()  csv2db自动生成字段类型
5.3 xlsx2db  xlsx全量导入数据库
5.4 xlsx2dbByConverters xlsx全量导入数据库，并转换字段类型
5.5 xlsx2dbAppendById xlsx增量导入数据库，id自动提增
5.6 xlsx2dbAppend xlsx增量导入数据库
5.7 dict2db  字典导入数据库
5.8 list2db  列表导入数据库
5.9 df2db    DataFrame导入数据库
5.10 db2csv   数据库sql导出csv
5.11 db2xlsx  数据库sql导出xlsx
5.12 db2dict  数据库sql导出字典
5.13 db2html  数据库sql导出html
5.14 db2df    数据库sql导出DataFrame

# todo【ROW_NUMBER()定位行号】
# 6.1 获取某列中为Null值的行号集合，如获取body列中为空值的行号集合
# 6.2 更改第N行的字段值，如修改第三行的query和body值
"""

from collections import Counter, ChainMap
import pandas as pd
import petl as etl
import sys,json
from collections.abc import Iterable, Iterator
# from collections.abc import pymssql
import pymssql
from time import sleep
# print(pymssql.__version__)
# from adodbapi import connect
from sqlalchemy import create_engine, text
import sqlalchemy
from sqlalchemy import types as sqltypes

from PO.ColorPO import *
Color_PO = ColorPO()

from PO.TimePO import *
Time_PO = TimePO()

from PO.FilePO import *
File_PO = FilePO()
from sqlalchemy import TIMESTAMP

class SqlserverPO:

    def __init__(self, server, user, password, database, charset="utf8"):

        self.server = server
        self.user = user
        self.password = password
        self.database = database
        self.conn = pymssql.connect(
            server=server, user=user, password=password, database=database, charset=charset,
            as_dict=True, tds_version="7.3", autocommit=True,
        )
        # 注意：autocommit=True
        # pymssql默认关闭自动模式开启事务行为浅析 https://www.cnblogs.com/kerrycode/p/11391832.html
        # self.conn = pymssql.connect(server=server, user=user, password=password, database=database, charset='GB2312', autocommit=True)
        # self.conn = pymssql.connect(server=server, user=user, password=password, database=database, charset='GB18030', autocommit=True)
        # self.conn = pymssql.connect(server=server, user=user, password=password, database=database, charset='GBK', autocommit=True)
        # self.conn = pymssql.connect(server=server, user=user, password=password, database=database, charset='CP936', autocommit=True, login_timeout=10)
        # self.conn = connect('Provider=SQLOLEDB.1;Data Source=%s;Initial Catalog=%s;UserID = %s;Password = %s;'%(server, database, user, password))

        self.cur = self.conn.cursor()
        if not self.cur:
            raise (NameError, "error，创建游标失败！")

    def getEngine_pyodbc(self):
        ''' pyodbc 引擎 '''
        return create_engine("mssql+pyodbc://" + self.user + ":" + self.password + "@mydsn")

    def getEngine_pymssql(self):
        ''' pymssql 引擎 '''
        # return create_engine("mssql+pymssql://" + self.user + ":" + self.password + "@" + self.server + ":" + str(self.port) + "/" + self.database)
        return create_engine(
            "mssql+pymssql://" + self.user + ":" + self.password + "@" + self.server + "/" + self.database)

        # 确保连接字符串包含了 charset=utf8 或 charset=utf8mb4，以便支持非 gbk 字符
        # return create_engine(
        #     "mssql+pymssql://" + self.user + ":" + self.password + "@" + self.server + "/" + self.database + "?charset=utf8mb4"
        # )

    def getCursor(self):
        return self.cur


    def selectParam(self, sql, param):

        ''' 1.0 查询带参数 '''

        try:
            self.conn.commit()
            self.cur.execute(sql, param)
            result = self.cur.fetchall()
            return result
        except Exception as e:
            print(repr(e))

    def selectOne(self, sql):

        ''' 1.1 查询 '''

        try:
            self.cur.execute(sql)
            result = self.cur.fetchone()
            return result
        except Exception as e:
            # print(e.args)  # ('table hh already exists',)
            # print(str(e))  # table hh already exists
            # print(NameError(e))  # table hh already exists
            print(repr(e))  # OperationalError('table hh already exists')

    def select(self, sql):

        ''' 1.1 查询 '''

        try:
            self.conn.commit()
            self.cur.execute(sql)
            result = self.cur.fetchall()
            return result
        except Exception as e:
            # print(e.args)  # ('table hh already exists',)
            # print(str(e))  # table hh already exists
            # print(NameError(e))  # table hh already exists
            print(repr(e))  # OperationalError('table hh already exists')
    def select2(self, sql):

        ''' 1.1 查询 '''

        try:
            self.conn.commit()
            self.cur.execute(sql)
            result = self.cur.fetchall()
            # 获取 PRINT 消息
            print("\nPRINT 输出内容:")
            for message in self.cur.messages:
                print(message[1])  # message[1] 是实际的字符串信息


            return result
        except Exception as e:
            # print(e.args)  # ('table hh already exists',)
            # print(str(e))  # table hh already exists
            # print(NameError(e))  # table hh already exists
            print(repr(e))  # OperationalError('table hh already exists')

    def executeParams(self, sql, params=None):
        with self.conn.cursor() as cursor:
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            self.conn.commit()


    def execute(self, sql):

        ''' 1.2 执行 '''

        try:
            # self.conn.commit()
            self.cur.execute(sql)
            # self.conn.commit()
        except Exception as e:
            print(repr(e))

    def execute2(self, sql, value):

        ''' 1.2 执行 '''

        try:
            # self.conn.commit()
            self.cur.execute(sql, value)
            self.conn.commit()
        except Exception as e:
            print(repr(e))

    def executemany(self, sql, value):

        ''' 1.3 执行多条 '''

        try:
            self.conn.commit()
            self.cur.executemany(sql, value)
            self.conn.commit()
        except Exception as e:
            print(repr(e))

    def execCall(self, varProcedureName, params=()):

        ''' 1.4 执行存储过程
        # 定义要执行的存储过程及其参数（若有）
            # varProcedureName = '存储过程名'
            # params = ('参数1值', '参数2值', ...)'''
        # Sqlserver_PO.execCall("CreateTestData100", (3,))

        try:
            self.cur.callproc(varProcedureName, params)
            self.conn.commit()
        except Exception as e:
            print(repr(e))

    def execSqlFile(self, varPathSqlFile):

        '''
        1.5 执行sql文件
        # execSqlFile('D:\\51\\python\\project\\instance\\zyjk\\EHR\\controlRule\\mm.sql')
        '''

        with open(varPathSqlFile) as f:
            sql = f.read()
            self.cur.execute(sql)
            self.conn.commit()
            self.conn.close()

    def execSqlFile2(self, varPathSqlFile):

        """ 1.6 执行sql文件2 """

        with open(varPathSqlFile) as f:
            sql = f.read()
            self.cur.execute(sql)
            self.cur.nextset()
            self.conn.commit()
            self.conn.close()

    def close(self):

        ''' 1.7 关闭 '''

        self.cur.close()
        self.conn.close()



    # todo 表

    def delTable(self, varTable):

        # #-- 创建新表（结构与原表相同）
        # self.execute("SELECT * INTO NewTable FROM %s WHERE 1=0;" % (varTable))
        #
        # # -- 禁用索引和约束
        # self.execute("ALTER TABLE %s DISABLE TRIGGER ALL;" % (varTable))
        # self.execute("ALTER TABLE %s DISABLE CONSTRAINT ALL;" % (varTable))
        #
        # # -- 交换表名（原子操作，几乎瞬间完成）
        # self.execute("EXEC sp_rename '" + varTable + "', OldTable';")
        # self.execute("EXEC sp_rename 'NewTable', '" + varTable + "';")

        # -- （可选）异步删除旧表
        self.execute(f"DROP TABLE {varTable};")


    def isTable(self, varTable):

        # 2.1 判断表是否存在

        r = self.select("SELECT COUNT(*) c FROM SYSOBJECTS WHERE XTYPE = 'U' AND NAME='%s'" % (varTable))
        # print(r)  # [{'c': 1}]
        if r[0]['c'] == 1:
            return True
        else:
            return False

    def getStructure(self, varTable="all"):

        ''' 2.2 获取表结构信息
        :param varTable: 所有表或单表
        :return: [{表：'','表注释:'', '字段序号':'', '字段':'', '': '', '主键': '√', '类型': 'int', '占用字节数': 4, '长度': 10, '小数位数': 0, '允许空': '', '默认值': '', '字段注释': b''},{}...]
        其他用法：将如下查询内容，在navicate中执行，并导出excel文档。
        '''

        try:
            if varTable == "all":
                list1 = self.select('''
                SELECT 表 = d.name,
                  表注释 = isnull(f.value, ''),
                  字段序号 = a.colorder,
                  字段 = a.name,
                  标识 = case when COLUMNPROPERTY(a.id, a.name, 'IsIdentity')= 1 then '√' else '' end,
                  主键 = case when exists(SELECT 1 FROM sysobjects where xtype = 'PK' and parent_obj = a.id and name in (SELECT name FROM sysindexes WHERE indid in(SELECT indid FROM sysindexkeys WHERE id = a.id AND colid = a.colid))) then '√' else '' end,
                  类型 = b.name,
                  占用字节数 = a.length,
                  长度 = COLUMNPROPERTY(a.id, a.name, 'PRECISION'),
                  小数位数 = isnull(COLUMNPROPERTY(a.id, a.name, 'Scale'),0),
                  允许空 = case when a.isnullable = 1 then '√' else '' end,
                  默认值 = isnull(e.text, ''),
                  字段注释 = isnull(g.[value], '')
                FROM
                  syscolumns a
                  left join systypes b on a.xusertype = b.xusertype
                  inner join sysobjects d on a.id = d.id
                  and d.xtype = 'U'
                  and d.name<>'dtproperties'
                  left join syscomments e on a.cdefault = e.id
                  left join sys.extended_properties g on a.id = G.major_id
                  and a.colid = g.minor_id
                  left join sys.extended_properties f on d.id = f.major_id
                  and f.minor_id = 0
                order by
                  a.id,
                  a.colorder
                ''')
            else:
                list1 = self.select('''
                SELECT 表 = d.name ,
                  表注释 =  isnull(f.value, '') ,
                  字段序号 = a.colorder,
                  字段 = a.name,
                  标识 = case when COLUMNPROPERTY(a.id, a.name, 'IsIdentity')= 1 then '√' else '' end,
                  主键 = case when exists(SELECT 1 FROM sysobjects where xtype = 'PK' and parent_obj = a.id and name in (SELECT name FROM sysindexes WHERE indid in(SELECT indid FROM sysindexkeys WHERE id = a.id AND colid = a.colid))) then '√' else '' end,
                  类型 = b.name,
                  占用字节数 = a.length,
                  长度 = COLUMNPROPERTY(a.id, a.name, 'PRECISION'),
                  小数位数 = isnull(COLUMNPROPERTY(a.id, a.name, 'Scale'),0),
                  允许空 = case when a.isnullable = 1 then '√' else '' end,
                  默认值 = isnull(e.text, ''),
                  字段注释 = isnull(g.value, '')
                FROM
                  syscolumns a
                  left join systypes b on a.xusertype = b.xusertype
                  inner join sysobjects d on a.id = d.id
                  and d.xtype = 'U'
                  and d.name<>'dtproperties'
                  left join syscomments e on a.cdefault = e.id
                  left join sys.extended_properties g on a.id = G.major_id
                  and a.colid = g.minor_id
                  left join sys.extended_properties f on d.id = f.major_id
                  and f.minor_id = 0
                where
                    d.name = \'''' + varTable + '''\'
                order by
                  a.id,
                  a.colorder
                ''')

            for index, i in enumerate(list1):
                for k, v in i.items():
                    if isinstance(v, bytes):
                        list1[index][k] = v.decode(encoding="GBK", errors="strict")

            return list1
        except Exception as e:
            print(e, ",[error], SqlserverPO.getTableComment()异常!")
            self.conn.close()

    def desc2(self, args=''):

        # 2.3.1 查看表结构

        # 注意，表名区分大小写
        # 1，所有表结构, desc()
        # 2，所有表结构，可选字段, 如：desc(['id', 'page'])
        # 3，模糊搜索所有表结构，如：desc('tb%')
        # 4，模糊搜索所有表结构，可选字段，如：desc({'tb%' : ['id', 'page']})
        # 5，单表结构, desc('tb_code_value')
        # 6，单表结构，可选字段  desc({'tb_code_value' : ['id', 'page']})

        d_tableComment = {}
        l_columnName = []
        l_dataType = []
        l_maxLength = []
        l_datetimePrecison = []
        l_numericPrecision = []
        l_isNull = []
        l_columnDefault = []
        l_columnComment = []

        s_info = ''
        # 获取表和注释
        if len(args) == 0 or isinstance(args, list):
            # 1，所有表结构, desc()
            # 2，所有表结构，可选字段, 如：desc(['id', 'page'])
            d_tableComment = self.getTableComment()
            # print(d_tableComment)  # {'a_ceshiguize': '(测试用例)测试规则', 'a_chc_auth': None,...
        elif isinstance(args, str) and "%" in args:
            # 3，模糊搜索所有表结构，如：desc('tb%')
            d_tableComment = self.getTableComment(args)
        elif isinstance(args, dict):
            # 4，模糊搜索所有表结构，可选字段，如：desc({'tb%' : ['id', 'page']})
            # 6，单表结构，可选字段  desc({'tb_code_value' : ['id', 'page']})
            d_tableComment = self.getTableComment(list(args.keys())[0])
        else:
            if isinstance(args, str):
                # 5，单表结构, desc('tb_code_value')
                d_tableComment = self.getTableComment(args)
                # print(d_tableComment)  # {'QYYH': '1+1+1签约信息表'}

        # 遍历表，输出：列名columnName，类型dataType，长度maxLength，
        # 标度datetimePrecision，精度numericPrecison，非空isNull，默认columnDefault，描述columnComment
        for k, v in d_tableComment.items():
            varTable = k

            # 获取字段名COLUMN_NAME、日期精度DATETIME_PRECISION、数字精度numericPrecision，是否为空isNull，默认columnDefault
            l_d_1 = self.select(
                "SELECT COLUMN_NAME,DATETIME_PRECISION,NUMERIC_PRECISION,IS_NULLABLE,COLUMN_DEFAULT FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s' ORDER BY ORDINAL_POSITION" % (
                    varTable))
            # print(l_d_1)  # [{'COLUMN_NAME': 'id', 'DATETIME_PRECISION': None, 'NUMERIC_PRECISION': 19, 'IS_NULLABLE': 'YES', 'COLUMN_DEFAULT': None}, ...

            # 获取字段名COLUMN_NAME、数据类型DATA_TYPE、长度MAX_LENGTH、描述COLUMN_COMMENT
            l_d_2 = self.select(
                "SELECT d.name as DATA_TYPE, B.max_length as MAX_LENGTH, C.value as COLUMN_COMMENT FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s' order by B.column_id asc"
                % (varTable))
            # print(l_d_2)  # [{'DATA_TYPE': 'bigint', 'MAX_LENGTH': 8, 'COLUMN_COMMENT': None},...

            # 合并l_d_1 和 l_d_2
            for i in range(len(l_d_1)):
                l_d_1[i].update(l_d_2[i])
            # print(l_d_1)

            try:
                # 字段与类型对齐
                columnName = dataType = maxLength = datetimePrecison = numericPrecision = isNull = columnDefault = columnComment = 0
                for i in l_d_1:
                    if len(str(i['COLUMN_NAME'])) > columnName:
                        columnName = len(i['COLUMN_NAME'])
                    if len(str(i['DATA_TYPE'])) > dataType:
                        dataType = len(i['DATA_TYPE'])
                    if len(str(i['MAX_LENGTH'])) > maxLength:
                        maxLength = len(str(i['MAX_LENGTH']))
                    if len(str(i['DATETIME_PRECISION'])) > datetimePrecison:
                        datetimePrecison = len(str(i['DATETIME_PRECISION']))
                    if len(str(i['NUMERIC_PRECISION'])) > numericPrecision:
                        numericPrecision = len(str(i['NUMERIC_PRECISION']))
                    if len(str(i['IS_NULLABLE'])) > isNull:
                        isNull = len(str(i['IS_NULLABLE']))
                    if len(str(i['COLUMN_DEFAULT'])) > columnDefault:
                        columnDefault = len(str(i['COLUMN_DEFAULT']))
                    if len(str(i['COLUMN_COMMENT'])) > columnComment:
                        columnComment = len(str(i['COLUMN_COMMENT']))

                # 2，所有表结构，可选字段, 如：desc(['id', 'page'])
                if isinstance(args, list):
                    for i in range(len(args)):
                        for m in range(len(l_d_1)):
                            if args[i] == l_d_1[m]['COLUMN_NAME']:
                                l_columnName.append(
                                    str(l_d_1[m]['COLUMN_NAME']))
                                l_dataType.append(
                                    str(l_d_1[m]['DATA_TYPE']))
                                l_maxLength.append(str(l_d_1[m]['MAX_LENGTH']))
                                l_datetimePrecison.append(str(l_d_1[m]['DATETIME_PRECISION']))
                                l_numericPrecision.append(str(l_d_1[m]['NUMERIC_PRECISION']))
                                l_isNull.append(
                                    str(l_d_1[m]['IS_NULLABLE']))
                                l_columnDefault.append(str(l_d_1[m]['COLUMN_DEFAULT']))
                                if l_d_1[m]['COLUMN_COMMENT'] == None:
                                    l_columnComment.append(str(l_d_1[m]['COLUMN_COMMENT']))
                                else:
                                    l_columnComment.append(str(l_d_1[m]['COLUMN_COMMENT'].decode("GBK")))
                # 4，模糊搜索所有表结构，可选字段，如：desc({'tb%' : ['id', 'page']})
                # 6，单表结构，可选字段  desc({'tb_code_value' : ['id', 'page']}) ???
                elif isinstance(args, dict):
                    args = list(args.values())[0]
                    # print(args)
                    for i in range(len(args)):
                        for m in range(len(l_d_1)):
                            if args[i] == l_d_1[m]['COLUMN_NAME']:
                                l_columnName.append(str(l_d_1[m]['COLUMN_NAME']))
                                l_dataType.append(str(l_d_1[m]['DATA_TYPE']))
                                l_maxLength.append(str(l_d_1[m]['MAX_LENGTH']))
                                l_datetimePrecison.append(str(l_d_1[m]['DATETIME_PRECISION']))
                                l_numericPrecision.append(str(l_d_1[m]['NUMERIC_PRECISION']))
                                l_isNull.append(str(l_d_1[m]['IS_NULLABLE']))
                                l_columnDefault.append(str(l_d_1[m]['COLUMN_DEFAULT']))
                                if l_d_1[m]['COLUMN_COMMENT'] == None:
                                    l_columnComment.append(str(l_d_1[m]['COLUMN_COMMENT']))
                                else:
                                    l_columnComment.append(str(l_d_1[m]['COLUMN_COMMENT'].decode("GBK")))

                else:
                    # 所有字段
                    for i in l_d_1:
                        l_columnName.append(str(i['COLUMN_NAME']))
                        l_dataType.append(str(i['DATA_TYPE']))
                        l_maxLength.append(str(i['MAX_LENGTH']))
                        l_datetimePrecison.append(str(i['DATETIME_PRECISION']))
                        l_numericPrecision.append(str(i['NUMERIC_PRECISION']))
                        l_isNull.append(str(i['IS_NULLABLE']))
                        l_columnDefault.append(str(i['COLUMN_DEFAULT']))
                        if i['COLUMN_COMMENT'] == None:
                            l_columnComment.append(str(i['COLUMN_COMMENT']))
                        else:
                            l_columnComment.append(str(i['COLUMN_COMMENT'].decode("GBK")))

                # 只输出找到字段的表
                s_value = ''

                if len(l_columnName) != 0:
                    # s_info = str(k) + "(" + str(d_tableComment[k]) + ") - " + str(len(l_d_1)) + "个字段<br>"
                    # s_info = s_info + "列名[1], 类型[2], 长度[3], 时精[4], 数精[5], 非空[6], 默认值[7], 注释[8] " + "<br>"
                    s_info = s_info + "列名, 类型, 长度, 时精, 数精, 非空, 默认值, 注释" + "<br>"
                    # s_info = s_info + "列名" + " " * (columnName - len("COLUMN_NAME") + 9) + \
                    #          "类型" + " " * (dataType - len("DATA_TYPE") + 6) + \
                    #          "长度" + " " * (maxLength - len("MAX_LENGTH") + 13) + \
                    #          "时精" + " " * (datetimePrecison - len("DATETIME_PRECISION") + 17) + \
                    #          "数精" + " " * (numericPrecision - len("NUMERIC_PRECISION") + 15) + \
                    #          "非空" + " " * (isNull - len("IS_NULLABLE") + 12) + \
                    #          "默认值" + " " * (columnDefault - len("COLUMN_DEFAULT") + 11) + \
                    #          "注释" + " " * (columnComment - len("COLUMN_COMMENT")) + "<br>"
                    for i in range(len(l_columnName)):
                        s_value = s_value + l_columnName[i] + ", " + l_dataType[i] + ", " + l_maxLength[i] + ", " + \
                                  l_datetimePrecison[i] + ", " + \
                                  l_numericPrecision[i] + ", " + l_isNull[i] + ", " + l_columnDefault[
                                      i] + ", " + l_columnComment[i] + "<br>"
                        # s_value = s_value + l_columnName[i] + ", " + l_dataType[i] + ", " + l_maxLength[i] + "[3], " + \
                        #           l_datetimePrecison[i] + "[4], " + \
                        #           l_numericPrecision[i] + "[5], " + l_isNull[i] + "[6], " + l_columnDefault[
                        #               i] + "[7], " + l_columnComment[i] + "<br>"
                    s_info = s_info + s_value
                    s_info = s_info[:-4]  # 删除最后4个字符 <br>

                l_columnName = []
                l_dataType = []
                l_maxLength = []
                l_datetimePrecison = []
                l_numericPrecision = []
                l_isNull = []
                l_columnDefault = []
                l_columnComment = []

            except Exception as e:
                raise e
        return s_info
        # return len(d_tableComment)
    def desc(self, args=''):

        # 2.3 查看表结构

        # 注意，表名区分大小写
        # 1，所有表结构, desc()
        # 2，所有表结构，可选字段, 如：desc(['id', 'page'])
        # 3，模糊搜索所有表结构，如：desc('tb%')
        # 4，模糊搜索所有表结构，可选字段，如：desc({'tb%' : ['id', 'page']})
        # 5，单表结构, desc('tb_code_value')
        # 6，单表结构，可选字段  desc({'tb_code_value' : ['id', 'page']})

        d_tableComment = {}

        l_columnName = []
        l_dataType = []
        l_maxLength = []
        l_datetimePrecison = []
        l_numericPrecision = []
        l_isNull = []
        l_columnDefault = []
        l_columnComment = []

        # 获取表和注释
        if len(args) == 0 or isinstance(args, list):
            # 1，所有表结构, desc()
            # 2，所有表结构，可选字段, 如：desc(['id', 'page'])
            d_tableComment = self.getTableComment()
            # print(d_tableComment)  # {'a_ceshiguize': '(测试用例)测试规则', 'a_chc_auth': None,...
        elif isinstance(args, str) and "%" in args:
            # 3，模糊搜索所有表结构，如：desc('tb%')
            d_tableComment = self.getTableComment(args)
        elif isinstance(args, dict):
            # 4，模糊搜索所有表结构，可选字段，如：desc({'tb%' : ['id', 'page']})
            # 6，单表结构，可选字段  desc({'tb_code_value' : ['id', 'page']})
            d_tableComment = self.getTableComment(list(args.keys())[0])
        else:
            if isinstance(args, str):
                # 5，单表结构, desc('tb_code_value')
                d_tableComment = self.getTableComment(args)
                # print(d_tableComment)  # {'QYYH': '1+1+1签约信息表'}

        # 遍历表，输出：列名columnName，类型dataType，长度maxLength，
        # 标度datetimePrecision，精度numericPrecison，非空isNull，默认columnDefault，描述columnComment
        for k, v in d_tableComment.items():
            varTable = k

            # 获取字段名COLUMN_NAME、日期精度DATETIME_PRECISION、数字精度numericPrecision，是否为空isNull，默认columnDefault
            l_d_1 = self.select(
                "SELECT COLUMN_NAME,DATETIME_PRECISION,NUMERIC_PRECISION,IS_NULLABLE,COLUMN_DEFAULT FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s' ORDER BY ORDINAL_POSITION" % (
                    varTable))
            # print(l_d_1)  # [{'COLUMN_NAME': 'id', 'DATETIME_PRECISION': None, 'NUMERIC_PRECISION': 19, 'IS_NULLABLE': 'YES', 'COLUMN_DEFAULT': None}, ...

            # 获取字段名COLUMN_NAME、数据类型DATA_TYPE、长度MAX_LENGTH、描述COLUMN_COMMENT
            l_d_2 = self.select(
                "SELECT d.name as DATA_TYPE, B.max_length as MAX_LENGTH, C.value as COLUMN_COMMENT FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s' order by B.column_id asc"
                % (varTable))
            # print(l_d_2)  # [{'DATA_TYPE': 'bigint', 'MAX_LENGTH': 8, 'COLUMN_COMMENT': None},...

            # 合并l_d_1 和 l_d_2
            for i in range(len(l_d_1)):
                l_d_1[i].update(l_d_2[i])
            # print(l_d_1)

            try:
                # 字段与类型对齐
                columnName = dataType = maxLength = datetimePrecison = numericPrecision = isNull = columnDefault = columnComment = 0
                for i in l_d_1:
                    if len(str(i['COLUMN_NAME'])) > columnName:
                        columnName = len(i['COLUMN_NAME'])
                    if len(str(i['DATA_TYPE'])) > dataType:
                        dataType = len(i['DATA_TYPE'])
                    if len(str(i['MAX_LENGTH'])) > maxLength:
                        maxLength = len(str(i['MAX_LENGTH']))
                    if len(str(i['DATETIME_PRECISION'])) > datetimePrecison:
                        datetimePrecison = len(str(i['DATETIME_PRECISION']))
                    if len(str(i['NUMERIC_PRECISION'])) > numericPrecision:
                        numericPrecision = len(str(i['NUMERIC_PRECISION']))
                    if len(str(i['IS_NULLABLE'])) > isNull:
                        isNull = len(str(i['IS_NULLABLE']))
                    if len(str(i['COLUMN_DEFAULT'])) > columnDefault:
                        columnDefault = len(str(i['COLUMN_DEFAULT']))
                    if len(str(i['COLUMN_COMMENT'])) > columnComment:
                        columnComment = len(str(i['COLUMN_COMMENT']))

                # 2，所有表结构，可选字段, 如：desc(['id', 'page'])
                if isinstance(args, list):
                    for i in range(len(args)):
                        for m in range(len(l_d_1)):
                            if args[i] == l_d_1[m]['COLUMN_NAME']:
                                l_columnName.append(
                                    str(l_d_1[m]['COLUMN_NAME']) + " " * (columnName - len(l_d_1[m]['COLUMN_NAME'])))
                                l_dataType.append(
                                    str(l_d_1[m]['DATA_TYPE']) + " " * (dataType - len(l_d_1[m]['DATA_TYPE']) + 1))
                                l_maxLength.append(str(l_d_1[m]['MAX_LENGTH']) + " " * (
                                        maxLength - len(str(l_d_1[m]['MAX_LENGTH'])) + 4))
                                l_datetimePrecison.append(str(l_d_1[m]['DATETIME_PRECISION']) + " " * (
                                        datetimePrecison - len(str(l_d_1[m]['DATETIME_PRECISION'])) + 2))
                                l_numericPrecision.append(str(l_d_1[m]['NUMERIC_PRECISION']) + " " * (
                                        numericPrecision - len(str(l_d_1[m]['NUMERIC_PRECISION']))))
                                l_isNull.append(
                                    str(l_d_1[m]['IS_NULLABLE']) + " " * (isNull - len(l_d_1[m]['IS_NULLABLE']) + 3))
                                l_columnDefault.append(str(l_d_1[m]['COLUMN_DEFAULT']) + " " * (
                                        columnDefault - len(str(l_d_1[m]['COLUMN_DEFAULT'])) + 1))
                                if l_d_1[m]['COLUMN_COMMENT'] == None:
                                    l_columnComment.append(str(l_d_1[m]['COLUMN_COMMENT']) + " " * (
                                            columnComment - len(str(l_d_1[m]['COLUMN_COMMENT']))))
                                else:
                                    l_columnComment.append(str(l_d_1[m]['COLUMN_COMMENT'].decode("GBK")) + " " * (
                                            columnComment - len(str(l_d_1[m]['COLUMN_COMMENT']))))
                # 4，模糊搜索所有表结构，可选字段，如：desc({'tb%' : ['id', 'page']})
                # 6，单表结构，可选字段  desc({'tb_code_value' : ['id', 'page']}) ???
                elif isinstance(args, dict):
                    args = list(args.values())[0]
                    # print(args)
                    for i in range(len(args)):
                        for m in range(len(l_d_1)):
                            if args[i] == l_d_1[m]['COLUMN_NAME']:
                                l_columnName.append(
                                    str(l_d_1[m]['COLUMN_NAME']) + " " * (columnName - len(l_d_1[m]['COLUMN_NAME'])))
                                l_dataType.append(
                                    str(l_d_1[m]['DATA_TYPE']) + " " * (dataType - len(l_d_1[m]['DATA_TYPE']) + 1))
                                l_maxLength.append(str(l_d_1[m]['MAX_LENGTH']) + " " * (
                                        maxLength - len(str(l_d_1[m]['MAX_LENGTH'])) + 4))
                                l_datetimePrecison.append(str(l_d_1[m]['DATETIME_PRECISION']) + " " * (
                                        datetimePrecison - len(str(l_d_1[m]['DATETIME_PRECISION'])) + 2))
                                l_numericPrecision.append(str(l_d_1[m]['NUMERIC_PRECISION']) + " " * (
                                        numericPrecision - len(str(l_d_1[m]['NUMERIC_PRECISION']))))
                                l_isNull.append(
                                    str(l_d_1[m]['IS_NULLABLE']) + " " * (isNull - len(l_d_1[m]['IS_NULLABLE']) + 3))
                                l_columnDefault.append(str(l_d_1[m]['COLUMN_DEFAULT']) + " " * (
                                        columnDefault - len(str(l_d_1[m]['COLUMN_DEFAULT'])) + 1))
                                if l_d_1[m]['COLUMN_COMMENT'] == None:
                                    l_columnComment.append(str(l_d_1[m]['COLUMN_COMMENT']) + " " * (
                                            columnComment - len(str(l_d_1[m]['COLUMN_COMMENT']))))
                                else:
                                    l_columnComment.append(str(l_d_1[m]['COLUMN_COMMENT'].decode("GBK")) + " " * (
                                            columnComment - len(str(l_d_1[m]['COLUMN_COMMENT']))))

                else:
                    # 所有字段
                    for i in l_d_1:
                        l_columnName.append(str(i['COLUMN_NAME']) + " " * (columnName - len(i['COLUMN_NAME'])))
                        l_dataType.append(str(i['DATA_TYPE']) + " " * (dataType - len(i['DATA_TYPE'])))
                        l_maxLength.append(str(i['MAX_LENGTH']) + " " * (maxLength - len(str(i['MAX_LENGTH'])) + 5))
                        l_datetimePrecison.append(str(i['DATETIME_PRECISION']) + " " * (
                                datetimePrecison - len(str(i['DATETIME_PRECISION'])) + 1))
                        l_numericPrecision.append(str(i['NUMERIC_PRECISION']) + " " * (
                                numericPrecision - len(str(i['NUMERIC_PRECISION'])) + 1))
                        l_isNull.append(str(i['IS_NULLABLE']) + " " * (isNull - len(str(i['IS_NULLABLE'])) + 3))
                        l_columnDefault.append(
                            str(i['COLUMN_DEFAULT']) + " " * (columnDefault - len(str(i['COLUMN_DEFAULT'])) + 1))
                        if i['COLUMN_COMMENT'] == None:
                            l_columnComment.append(
                                str(i['COLUMN_COMMENT']) + " " * (columnComment - len(str(i['COLUMN_COMMENT']))))
                        else:
                            l_columnComment.append(str(i['COLUMN_COMMENT'].decode("GBK")) + " " * (
                                    columnComment - len(str(i['COLUMN_COMMENT'])) + 1))

                # 只输出找到字段的表
                if len(l_columnName) != 0:
                    print("- - " * 20)
                    Color_PO.outColor(
                        [{"36": str(k) + "(" + str(d_tableComment[k]) + ") >> " + str(len(l_d_1)) + "个字段"}])
                    Color_PO.outColor([{"35": "列名" + " " * (columnName - len("COLUMN_NAME") + 9) +
                                              "类型" + " " * (dataType - len("DATA_TYPE") + 6) +
                                              "长度" + " " * (maxLength - len("MAX_LENGTH") + 13) +
                                              "时精" + " " * (datetimePrecison - len("DATETIME_PRECISION") + 17) +
                                              "数精" + " " * (numericPrecision - len("NUMERIC_PRECISION") + 15) +
                                              "非空" + " " * (isNull - len("IS_NULLABLE") + 12) +
                                              "默认值" + " " * (columnDefault - len("COLUMN_DEFAULT") + 11) +
                                              "注释" + " " * (columnComment - len("COLUMN_COMMENT"))}])

                    for i in range(len(l_columnName)):
                        print(l_columnName[i], l_dataType[i], l_maxLength[i], l_datetimePrecison[i],
                              l_numericPrecision[i], l_isNull[i], l_columnDefault[i], l_columnComment[i])

                l_columnName = []
                l_dataType = []
                l_maxLength = []
                l_datetimePrecison = []
                l_numericPrecision = []
                l_isNull = []
                l_columnDefault = []
                l_columnComment = []

            except Exception as e:
                raise e
        return len(d_tableComment)

    def getTables(self):

        ''' 2.4 获取表 '''

        try:
            l_d_table = self.select("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES where TABLE_TYPE='BASE TABLE'")
            # l_d_table = self.select("SELECT NAME FROM SYSOBJECTS WHERE TYPE='U'")  # 同上
            # print(l_d_table)  # [{'TABLE_NAME': 'T_CHILD_HOME_VISIT'}, {'TABLE_NAME': 'TB_GXY_HZSFK'},...]
            l_tables = []
            for i in range(len(l_d_table)):
                l_tables.append(l_d_table[i]['TABLE_NAME'])
            return l_tables
        except Exception as e:
            print(e, ",[error], SqlserverPO.getTables()异常!")
            self.conn.close()

    def _getTableComment(self, l_d_):

        l_table = []
        l_comment = []

        for i in range(len(l_d_)):
            l_table.append(l_d_[i]['name'])
            if l_d_[i]['value'] == None:
                l_comment.append(l_d_[i]['value'])
            else:
                # l_comment.append(l_d_[i]['value'].decode(encoding="utf-8", errors="strict"))  # encoding="utf-8"
                l_comment.append(l_d_[i]['value'].decode(encoding="GBK", errors="strict"))  # GBK
        return dict(zip(l_table, l_comment))
    def getTableComment(self, varTable="all"):

        ''' 2.5 获取表名与表注释
        :return: {'ASSESS_DIAGNOSIS': '门诊数据', 'ASSESS_MEDICATION': '评估用药情况表'}
        # print(Sqlserver_PO.getTableComment())
        # print(Sqlserver_PO.getTableComment('a_test%'))
        # print(Sqlserver_PO.getTableComment('QYYH'))
        '''

        # try:
        if varTable == "all":
            # 所有表
            l_d_ = self.select(
                "SELECT DISTINCT d.name,f.value FROM syscolumns a LEFT JOIN systypes b ON a.xusertype= b.xusertype INNER JOIN sysobjects d ON a.id= d.id AND d.xtype= 'U' AND d.name<> 'dtproperties' LEFT JOIN syscomments e ON a.cdefault= e.id LEFT JOIN sys.extended_properties g ON a.id= G.major_id AND a.colid= g.minor_id LEFT JOIN sys.extended_properties f ON d.id= f.major_id AND f.minor_id= 0")
            # print(l_d_)  # [{'name': 'ASSESS_DIAGNOSIS', 'value': b'\xc3\xc5\xd5\xef\xca\xfd\xbe\xdd'},...
            return self._getTableComment(l_d_)
        elif '%' in varTable:
            # 模糊表
            l_d_ = self.select(
                "SELECT DISTINCT d.name,f.value FROM syscolumns a LEFT JOIN systypes b ON a.xusertype= b.xusertype INNER JOIN sysobjects d ON a.id= d.id AND d.xtype= 'U' AND d.name<> 'dtproperties' LEFT JOIN syscomments e ON a.cdefault= e.id LEFT JOIN sys.extended_properties g ON a.id= G.major_id AND a.colid= g.minor_id LEFT JOIN sys.extended_properties f ON d.id= f.major_id AND f.minor_id= 0 where d.name like '%s'" % (
                    varTable))
            # print(l_d_)  # [{'name': 'ASSESS_DIAGNOSIS', 'value': b'\xc3\xc5\xd5\xef\xca\xfd\xbe\xdd'},...
            return self._getTableComment(l_d_)
        else:
            # 单表
            l_d_ = self.select(
                "SELECT DISTINCT d.name,f.value FROM syscolumns a LEFT JOIN systypes b ON a.xusertype= b.xusertype INNER JOIN sysobjects d ON a.id= d.id AND d.xtype= 'U' AND d.name<> 'dtproperties' LEFT JOIN syscomments e ON a.cdefault= e.id LEFT JOIN sys.extended_properties g ON a.id= G.major_id AND a.colid= g.minor_id LEFT JOIN sys.extended_properties f ON d.id= f.major_id AND f.minor_id= 0 where d.name = '%s'" % (
                    varTable))
            # print(l_d_)  # [{'name': 'QYYH', 'value': b'1+1+1\xc7\xa9\xd4\xbc\xd0\xc5\xcf\xa2\xb1\xed'}]
            return self._getTableComment(l_d_)
        # except Exception as e:
        #     print(e, ",[error], SqlserverPO.getTableComment()异常!")
        #     self.conn.close()

    def getViews(self):

        ''' 2.6 获取视图 '''

        try:
            l_d_table = self.select("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES where TABLE_TYPE='VIEW'")
            # print(l_d_table)  # [{'TABLE_NAME': 'T_CHILD_HOME_VISIT'}, {'TABLE_NAME': 'TB_GXY_HZSFK'},...]
            l_tables = []
            for i in range(len(l_d_table)):
                l_tables.append(l_d_table[i]['TABLE_NAME'])
            return l_tables
        except Exception as e:
            print(e, ",[error], SqlserverPO.getViews()异常!")
            self.conn.close()

    def crtTableByCover(self, varTable, varFieldSets):

        # 2.7 创建表(覆盖，即如表存在先删除再创建)
        # 自增id主键
        # Sqlserver_PO.crtTableByCover('a_autoIdcard',
        #                            '''id INT IDENTITY(1,1) PRIMARY KEY,
        #                             tblName NVARCHAR(50),
        #                             idcard VARCHAR(18),
        #                             category VARCHAR(10),
        #                             userInfo VARCHAR(300)
        #                           ''')
        sql = " IF OBJECT_ID('" + varTable + "', 'U') IS NOT NULL DROP TABLE " + varTable + " CREATE TABLE " + varTable + "(" + varFieldSets + ")"
        self.execute(sql)

    def crtTableByExistIgnore(self, varTable, varFieldSets):

        # 2.8 创建表(忽略，如原表存在则忽略不创建)
        sql = "if not exists (select * from sysobjects where id = object_id('" + varTable + "') and OBJECTPROPERTY(id, 'IsUserTable') = 1)create table " + varTable + "(" + varFieldSets + ")"
        self.execute(sql)
        # self.conn.commit()

    def setTableComment(self, varTable, varComment, isDrop=False):

        # 2.9 设置表注释（添加，修改，删除）
        # setTableComment('t_user', '用户表')
        # setTableComment('t_user', '用户表', True)  删除注释

        if isDrop == True:
            #  删除注释
            self.execute(
                "EXECUTE sp_dropextendedproperty N'MS_Description', N'user', N'dbo', N'table', N'%s', NULL, NULL" % (
                    varTable))
        else:
            d_table_comment = self.getTableComment(varTable)
            if d_table_comment[varTable] == None:
                # 如果表没有注释则添加注释
                self.execute(
                    "EXECUTE sp_addextendedproperty N'MS_Description', N'%s', N'user', N'dbo', N'table', N'%s', NULL, NULL" % (
                    varComment, varTable))
            else:
                # 如果原来表有注释，则修改注释
                self.execute(
                    "EXECUTE sp_updateextendedproperty N'MS_Description', N'%s', N'user', N'dbo', N'table', N'%s', NULL, NULL" % (
                    varComment, varTable))

    def copyTable(self, source_table, target_table):
        # 2.10 复制表

        try:
            # 检查目标表是否存在，若存在则删除
            self.execute(f"IF OBJECT_ID('{target_table}', 'U') IS NOT NULL DROP TABLE {target_table}")
            self.conn.commit()

            # 创建目标表（结构与源表相同）
            create_table_query = f"SELECT * INTO {target_table} FROM {source_table} WHERE 1 = 0"
            self.execute(create_table_query)

            # 复制数据
            insert_data_query = f"INSERT INTO {target_table} SELECT * FROM {source_table}"
            self.execute(insert_data_query)
            self.conn.commit()

            print("ok =>", source_table, "生成的副表", target_table)
        except Exception as e:
            print(f"发生错误: {e}")
            self.conn.rollback()
        # finally:
        #     # 关闭连接
        #     self.close()
        #     self.conn.close()

    def dropKey(self, varFk, varTable):

        # 2.11 删除表的所有外键关系
        # fk = Sqlserver_PO.getForeignKey()  # 获取所有外键关联表
        #     Sqlserver_PO.dropKey(fk, varTable)  # 删除外键关系

        for i in range(len(varFk)):
            if varFk[i]['table'] == varTable:
                self.execute("ALTER table %s DROP %s" % (varTable, varFk[i]['foreignKey']))
            if varFk[i]['relatingTable'] == varTable:
                self.execute("ALTER table %s DROP %s" % (varFk[i]['table'], varFk[i]['foreignKey']))




    # todo 字段

    def isField(self, varTable, varField):

        # 3.1 判断字段是否存在

        r = self.select(
            "SELECT B.name as field FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'"
            % (varTable)
        )
        # print(r)  # [{'field': 'name'}, {'field': 'age'}, {'field': 'id'}]
        for i in range(len(r)):
            if r[i]['field'] == varField:
                return True
        return False

    def isIdentity(self, varTable):

        # 3.2 判断是否有自增主键, 如果有则返回1，无则返回0

        qty = self.select("Select OBJECTPROPERTY(OBJECT_ID('" + varTable + "'),'TableHasIdentity') as qty")
        # print(qty)  # [{'qty': 1}]
        # print(qty[0]['qty'])  # 1
        if qty[0]['qty'] == 1:
            return True
        else:
            return False

    def getFields(self, varTable):

        ''' 3.3 获取字段 '''

        try:
            l_d_ = self.select(
                "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s'" % (varTable))
            # print(l_d_)  # [{'COLUMN_NAME': 'id'}, {'COLUMN_NAME': 'name'}, {'COLUMN_NAME': 'salesrep'}]
            l_field = []
            for i in range(len(l_d_)):
                l_field.append(l_d_[i]['COLUMN_NAME'])
            return l_field
        except Exception as e:
            print(e, ",[error], getFields()异常!")
            self.conn.close()

    # def getFieldComment(self, varTable, varEncoding="utf-8"):
    def getFieldComment(self, varTable, varEncoding="GBK"):

        l_d_ = self.select(
            "SELECT B.name as FIELD_NAME, C.value as COMMENT FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'"
            % (varTable)
        )
        # print(l_d_)  # [{'FIELD_NAME': 'GHRQ', 'COMMENT': b'\xe6\x8c\x8...]
        l_field = []
        l_comment = []
        for i in range(len(l_d_)):
            l_field.append(l_d_[i]['FIELD_NAME'])
            if l_d_[i]['COMMENT'] == None:
                l_comment.append(l_d_[i]['COMMENT'])
            else:
                l_comment.append(l_d_[i]['COMMENT'].decode(encoding=varEncoding, errors="strict"))  # 用于上传\导入数据库
                # l_comment.append(l_d_[i]['COMMENT'].decode(encoding=varEncoding, errors="strict"))  # 用于打开页面
        return dict(zip(l_field, l_comment))


    def getFieldComment2(self, varTable, varEncoding="utf-8"):
    # def getFieldComment(self, varTable, varEncoding="GBK"):

        ''' 3.4 获取字段名与字段注释 '''
        # getFieldComment(varTable, varEncoding="utf-8")

        # print("11varEncoding:", varEncoding)
        try:
            l_d_ = self.select(
                "SELECT B.name as FIELD_NAME, C.value as COMMENT FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'"
                % (varTable)
            )
            # print(l_d_)  # [{'FIELD_NAME': 'GHRQ', 'COMMENT': b'\xe6\x8c\x8...]
            l_field = []
            l_comment = []
            for i in range(len(l_d_)):
                l_field.append(l_d_[i]['FIELD_NAME'])
                if l_d_[i]['COMMENT'] == None:
                    l_comment.append(l_d_[i]['COMMENT'])
                else:
                    l_comment.append(l_d_[i]['COMMENT'].decode(encoding=varEncoding, errors="strict"))  # 用于上传\导入数据库
                    # l_comment.append(l_d_[i]['COMMENT'].decode(encoding=varEncoding, errors="strict"))  # 用于打开页面
            return dict(zip(l_field, l_comment))
        except Exception as e:
            print("varEncoding:",varEncoding)
            print(e, ",[error2], getFields()异常!")
            self.conn.close()

    def getFieldType(self, varTable, l_field=[]):

        ''' 3.5 获取字段名与字段类型 '''

        d_fields_types = {}
        result = self.select(
            "SELECT A.name as tableName, B.name as Name, d.name as Type, B.max_length as Size, B.is_nullable as NotNull, C.value as Comment FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s' order by B.column_id asc"
            % (varTable)
        )
        # print(result) # [{'tableName': 'aaa', 'Name': 'ID', 'Type': 'int', 'Size': 4, 'NotNull': False, 'Comment': None},...]
        try:
            for i in result:
                d_fields_types[str(i['Name'])] = str(i['Type'])
        except Exception as e:
            raise e

        if l_field == []:
            return d_fields_types
        else:
            d_field_type = {}
            for k, v in d_fields_types.items():
                for j in range(len(l_field)):
                    if k == l_field[j]:
                        d_field_type[k] = v
            return d_field_type

    def getNotNullFieldType(self, varTable):

        # 3.6 获取非空（必填）字段与类型

        d_field_type = {}
        result = self.select(
            "SELECT A.name as tableName, B.name as Name, d.name as Type, B.max_length as Size, B.is_nullable as NotNull, C.value as Comment FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s' order by B.column_id asc"
            % (varTable)
        )
        try:
            for i in result:
                if i['NotNull'] == False:
                    d_field_type[str(i['Name'])] = str(i['Type'])
        except Exception as e:
            raise e
        return d_field_type  # {'ID': 'int', 'NAME': 'text', 'AGE': 'int', 'ADDRESS': 'char'}

    def getIdentityPrimaryKey(self, varTable):

        ''' 3.7 获取自增主键 '''

        l_field = self.select("select * from sys.identity_columns where [object_id]= OBJECT_ID('" + varTable + "')")
        if l_field != []:
            return (l_field[0]['name'])  # id
        else:
            return None

    def getPrimaryKey(self, varTable):

        # 3.8 获取主键或组合键

        l_d_PK = self.select(
            "SELECT COLUMN_NAME FROM information_schema.key_column_usage where table_name='" + varTable + "'")
        # print(l_d_PK)  # [{'COLUMN_NAME': 'ADDRESS'}, {'COLUMN_NAME': 'ID'}]
        if l_d_PK == []:
            return None
        else:
            return l_d_PK

    def getPrimaryKeyMaxValue(self, varTable):

        # 3.9 获取表主键最大值（条件是主键是整型）

        # 判断表中是否有记录
        varQty = self.getRecordCount(varTable)
        if varQty != 0:
            # 判断是否有主键
            l_d_PK = self.getPrimaryKey(varTable)
            if l_d_PK != None:
                # 一个主键时，# [{'COLUMN_NAME': 'id'}]
                if len(l_d_PK) == 1:
                    d = {}

                    # 获取字段与类型
                    d_fieldType = self.getFieldType(varTable)
                    # print(d_fieldType)
                    # 遍历判断主键的类型（因为主键可以是整型或字符型）
                    for k, v in d_fieldType.items():
                        # print(l_d_PK[0]['COLUMN_NAME'])  # id
                        if k == l_d_PK[0]['COLUMN_NAME'] and v == 'int':
                            maxValue = self.select(
                                "select max(" + str(l_d_PK[0]['COLUMN_NAME']) + ") as maxValue from " + varTable)
                            d[l_d_PK[0]['COLUMN_NAME']] = maxValue[0]['maxValue']
                    return (d)  # {'ID': 100}
                else:
                    # 多个主键时
                    pass
                    # print(l_d_PK)  # [{'name': 'ID'}, {'name': 'ADDRESS'}]  //1个主键

    def getForeignKey(self):

        # 3.10 获取所有外键关联表
        l_d_fk = self.select(
            "select OBJECT_NAME(fk.parent_object_id) as 'table', fk.name as 'foreignKey', OBJECT_NAME(fk.referenced_object_id) as 'relatingTable' FROM sys.foreign_keys fk")
        return l_d_fk

    def appendField(self, varTable, column_name, column_type):

        # 3.11 追加字段
        # setField('a_phs_auth_app','status','VARCHAR(11)')
        # 表名和要添加的字段信息
        # table_name = 'your_table_name'
        # column_name = 'status'
        # column_type = 'VARCHAR(11)'

        try:
            # 执行 ALTER TABLE 语句添加字段
            alter_table_query = f"ALTER TABLE {varTable} ADD {column_name} {column_type}"
            self.execute(alter_table_query)

            # 提交更改
            self.conn.commit()
            print(f"成功为表 {varTable} 添加字段 {column_name}。")
        except Exception as e:
            print(f"发生错误: {e}")
            self.conn.rollback()
        # finally:
        #     # 关闭连接
        #     self.close()
        #     self.conn.close()




    def insertBeforeField(self, table_name, reference_column, new_column_name, new_column_type):

        # 3.12 插入字段，在参考字段前插入新字段
        # 表名，参考字段，新字段，新字段类型
        # Sqlserver_PO.insertBeforeField('a_phs_auth_app', 'tags', 'status', 'VARCHAR(12)')
        # table_name = 'your_table_name'
        # new_column_name = 'new_column'
        # new_column_type = 'VARCHAR(255)'
        # reference_column = 'existing_column'

        try:
            # 获取表的所有列名
            l_d_column_type_max = self.select(
                f"SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")
            # print(l_d_column_type_max)  # [{'COLUMN_NAME': 'status', 'DATA_TYPE': 'varchar', 'CHARACTER_MAXIMUM_LENGTH': 12}, {'
            l_column = []
            l_column_type = []
            for i in range(len(l_d_column_type_max)):
                l_column.append(l_d_column_type_max[i]['COLUMN_NAME'])
                l_column_type.append(
                    l_d_column_type_max[i]['COLUMN_NAME'] + " " + l_d_column_type_max[i]['DATA_TYPE'] + '(' + str(
                        l_d_column_type_max[i]['CHARACTER_MAXIMUM_LENGTH']) + ')')
            # print(l_column)  # ['tags', 'summary', 'path', 'method', 'consumes', 'query', 'body', 'url']
            # print(l_column_type)  # ['tags varchar(-1)', 'summary varchar(-1)', 'path varchar(-1)'...

            # 找到参考字段的索引
            try:
                ref_index = l_column.index(reference_column)
                # print(ref_index)
            except ValueError:
                raise ValueError(f"参考字段 {reference_column} 不存在于表 {table_name} 中。")

            # 构建新表的列定义
            l_new_column_type = l_column_type[:ref_index] + [f"{new_column_name} {new_column_type}"] + l_column_type[
                                                                                                       ref_index:]
            # print(l_new_column_type)  # ['status varchar(66)', 'tags varchar(255)', 'summary varchar(255)',
            s_new_column_type = ', '.join(l_new_column_type)
            # print(s_new_column_type)  # status varchar(66), tags varchar(255), summary varchar(255), path varchar(255)

            # 创建临时新表 XXX_new
            create_new_table_query = f"CREATE TABLE {table_name}_new ({s_new_column_type})"
            self.execute(create_new_table_query)

            # 插入数据的列
            l_new_column = l_column[:ref_index] + [f"{new_column_name}"] + l_column[ref_index:]
            # print(l_new_column)  # ['status', 'tags', 'summary', 'path', 'method', 'consumes', 'query', 'body', 'url']
            s_new_column = ', '.join([col if col != new_column_name else new_column_name for col in l_new_column])
            # print(s_new_column)  # status, tags, summary, path, method, consumes, query, body, case1, url

            # insert_columns = ', '.join(new_columns)
            select_columns = l_column[:ref_index] + ["NULL"] + l_column[ref_index:]
            # print(select_columns)  # ['NULL', 'tags', 'summary', 'path', 'method', 'consumes', 'query', 'body', 'case1', 'url']
            select_columns_str = ', '.join(select_columns)
            insert_query = f"INSERT INTO {table_name}_new ({s_new_column}) SELECT {select_columns_str} FROM {table_name}"
            self.execute(insert_query)

            # 删除原表
            drop_table_query = f"DROP TABLE {table_name}"
            self.execute(drop_table_query)

            # 重命名新表为原表名
            rename_table_query = f"EXEC sp_rename '{table_name}_new', '{table_name}'"
            self.execute(rename_table_query)
            self.conn.commit()
            print(f"ok => {table_name} 表，在 {reference_column} 列名前插入 {new_column_name} {new_column_type}")
        except Exception as e:
            print(f"发生错误: {e}")
            self.conn.rollback()
        # finally:
        #     # 关闭连接
        #     self.close()
        #     self.conn.close()

    def setFieldComment(self, varTable, varField, varComment, varEncoding="GBK"):

        # 3.13 设置字段注释
        # setFieldComment('t_user','ID','编号')   //表名，字段，注释
        # setFieldComment('t_user','ID','编号', True) //表名，字段，注释，True表示删除此注释


        # # 删除注释
        # self.execute(
        #     "EXECUTE sp_dropextendedproperty N'MS_Description', N'SCHEMA', N'dbo',N'TABLE', N'%s', N'COLUMN', N'%s'" % (
        #         varTable, varField))

        d_field_comment = self.getFieldComment(varTable, varEncoding=varEncoding)
        for k, v in d_field_comment.items():
            if k == varField and v == None:
                # 添加注释
                self.execute(
                    "EXECUTE sp_addextendedproperty N'MS_Description', N'%s', N'SCHEMA', N'dbo',N'TABLE', N'%s', N'COLUMN', N'%s'" % (
                        varComment, varTable, varField))
            elif k == varField and v != None:
                # 修改注释
                self.execute(
                    "EXECUTE sp_updateextendedproperty N'MS_Description', N'%s', N'SCHEMA', N'dbo',N'TABLE', N'%s', N'COLUMN', N'%s'" % (
                        varComment, varTable, varField))

    def setFieldType(self, varTable, varField, varType):

        # 3.14 设置字段类型
        # Sqlserver_PO.setFieldType(varTable, 'pResult', 'varchar(100)')  //修改pResult数据类型
        try:
            self.execute("ALTER table %s alter column %s %s" % (varTable, varField, varType))
        except Exception as e:
            print(e)

    def setIdentityPrimaryKey(self, varTable, varField):

        # 3.15 设置自增主键
        # 新的主键在最后列
        self.execute("alter table %s ADD %s INT identity(1,1) primary key" % (varTable, varField))
        # self.execute("alter table %s ADD CONSTRAINT PK_a_weight10_EFRB_id PRIMARY KEY (%s)" % (varTable, varField))
        # ALTER TABLE a_weight10_EFRB ADD CONSTRAINT PK_a_weight10_EFRB_id PRIMARY KEY (id);
    def delIdentityPrimaryKey(self, varTable, varField):

        # 3.16 删除自增主键
        # self.execute("alter table %s alter column %s DROP IDENTITY" % (varTable, varField))
        self.execute("alter table %s DROP CONSTRAINT %s" % (varTable, varField))


    def setFieldTypeComment(self, varTable, varField, varType, varComment, varEncoding='utf-8'):

        # 3.17 设置字段类型与备注
        # 应用于pandas带入数据
        # Sqlserver_PO.setFieldTypeComment(varTable, 'pResult', 'varchar(100)', '正向测试结果')  //修改pResult数据类型和备注
        self.execute("ALTER table %s alter column %s %s" % (varTable, varField, varType))

        try:
            # 1 获取所有字段的备注
            d_comments = self.getFieldComment(varTable, varEncoding)
            # d_comments = self.getFieldComment(varTable, "utf-8")

            if d_comments[varField] == None:
                self.setFieldComment(varTable, varField, varComment, varEncoding)
            else:
                self.reviseFieldComment(varTable, varField, varComment)
        except Exception as e:
            print(e)


    # todo 记录

    def getRecordCount(self, varTable):

        #4.1 获取记录数（特别适合大数据）

        qty = self.select("SELECT rows FROM sysindexes WHERE id = OBJECT_ID('" + varTable + "') AND indid < 2")
        return qty[0]['rows']

    def insert(self, varTable, d_param):

        # 4.2 插入记录
        # 将d_param字段合并覆盖到表字段中，并插入表
        # 自动获取表数字主键（如id）最大值，并+1
        # 自动填写表的默认值，d_param字段可覆盖默认值
        # 返回值：主键最大值+1，d_param修改字段值，默认字段值。
        # 获取没有默认值值的字段，字典
        # 无默认值字段中取值优先顺序（重复最多、重复相同取最早的、不重复取最早的）

        # 1,获取字段与类型
        d_fieldType = self.getFieldType(varTable)
        # print(d_fieldType)  # {'result': 'varchar', 'updateDate': 'date', 'rule': 'varchar', 'ruleParam': 'varchar', 'id': 'int'}

        # 2,字段值使用默认值
        dd = {}
        # 获取字段与默认值
        l_d_fieldDefault = self.select(
            "SELECT COLUMN_NAME, COLUMN_DEFAULT FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s'" % (varTable))
        # print(l_d_fieldDefault)  # [{'COLUMN_NAME': 'ID', 'COLUMN_DEFAULT': None}, {'COLUMN_NAME': 'ID_CARD', 'COLUMN_DEFAULT': "('')"}, ...
        for d in l_d_fieldDefault:
            # print(d)
            if d['COLUMN_DEFAULT'] == None:
                for k, v in d_fieldType.items():
                    if k == d['COLUMN_NAME']:
                        if v == 'varchar' or v == 'nvarchar' or v == 'date' or v == 'datetime2' or v == 'datetime':
                            dd[d['COLUMN_NAME']] = ''
                        elif v == 'int' or v == 'decimal' or v == 'tinyint' or v == 'float':
                            dd[d['COLUMN_NAME']] = 0
            else:
                if d['COLUMN_DEFAULT'] == "('')":
                    dd[d['COLUMN_NAME']] = ''
                else:
                    COLUMN_DEFAULT = d['COLUMN_DEFAULT'].replace("(", "").replace(")", "")
                    for k, v in d_fieldType.items():
                        if k == d['COLUMN_NAME']:
                            if v == 'varchar' or v == 'nvarchar':
                                dd[d['COLUMN_NAME']] = COLUMN_DEFAULT
                            # 注意：不获取时间的默认值，因为可能是函数结构
                            elif v == 'date' or v == 'datetime' or v == 'datetime2':
                                dd[d['COLUMN_NAME']] = ''
                            elif v == 'int' or v == 'decimal' or v == 'tinyint' or v == 'float':
                                dd[d['COLUMN_NAME']] = int(COLUMN_DEFAULT)
        # print(dd)
        # sys.exit(0)

        # 3,获取没有默认值的字段列表
        l_noDefault = []
        for d_tmp in l_d_fieldDefault:
            # print(d_tmp)
            if d_tmp['COLUMN_DEFAULT'] == None:
                l_noDefault.append(d_tmp['COLUMN_NAME'])
        # print("无默认值字段 =>", l_noDefault)  # ['ruleParam', 'id', 'createDate', 'number']
        s_fields = ",".join(l_noDefault)
        # print(s_fields)  # updateDate,ruleParam,id,createDate,number
        # sys.exit(0)

        # 4,获取没有默认值的字段列表中字段重复值最多（最多，相等，1个）的那个值，更新此值
        l_d_ = self.select("select %s from %s" % (s_fields, varTable))
        # print(l_d_)  # [{'ruleParam': "'高血压'", 'id': 3, 'createDate': None, 'number': 22.0},...
        l_tmp = []
        d_tmp = {}
        for field in l_noDefault:
            for i in range(len(l_d_)):
                l_tmp.append(l_d_[i][field])
            d_tmp[field] = l_tmp
            l_tmp = []
        # print(d_tmp)
        for k, v in d_tmp.items():
            counts = Counter(v)
            # print(counts.most_common(1)[0][0])
            if counts.most_common(1)[0][0] != None:
                d_tmp[k] = counts.most_common(1)[0][0]
                d_tmp6 = self.getFieldType(varTable, [k])
                # print(d_tmp6)  # {'DOWNLOADSTATUS': 'tinyint'}
                if d_tmp6[k] == 'datetime' or d_tmp6[k] == 'date' or d_tmp6[k] == 'datetime2':
                    d_tmp[k] = ''
            else:
                # 获取字段和类型
                d_tmp6 = self.getFieldType(varTable, [k])
                # print(d_tmp6)  # {'DOWNLOADSTATUS': 'tinyint'}
                if d_tmp6[k] == 'int' or d_tmp6[k] == 'tinyint' or d_tmp6[k] == 'decimal' or d_tmp6[k] == 'float':
                    d_tmp[k] = 0
                else:
                    d_tmp[k] = ''
        # print("无默认值字段中取值优先顺序（重复最多、相同数量取最早的、不重复取最早的）=>", d_tmp)
        # print(dd)
        # sys.exit(0)
        dd.update(d_tmp)
        # print(dd)

        # 5,主键最大值+1
        l_d_PK = self.getPrimaryKey(varTable)  # 获取主键
        # print(l_d_PK) # # [{'COLUMN_NAME': 'ID'}]
        if l_d_PK != None:
            if len(l_d_PK) == 1:
                # 获取主键的类型
                d_PK = self.getFieldType(varTable, [l_d_PK[0]['COLUMN_NAME']])
                # print(d_PK)  # {'GUID': 'varchar'}
                # print(list(d_PK.values())[0])  #  'varchar'
                s_PK_type = list(d_PK.values())[0]
                if s_PK_type == 'int':
                    # print(l_d_PK[0]['COLUMN_NAME'])    # ID
                    d_PK_maxValue = self.getPrimaryKeyMaxValue(varTable)  # 获取主键最大值
                    # print(d_PK_maxValue) # {'ID': 503135}
                    # print(d_PK_maxValue[l_d_PK[0]['COLUMN_NAME']])  # 503136
                    dd[l_d_PK[0]['COLUMN_NAME']] = d_PK_maxValue[l_d_PK[0]['COLUMN_NAME']] + 1  # 主键最大值+1
                    # 移除参数中的主键
                    for k, v in d_param.items():
                        if l_d_PK[0]['COLUMN_NAME'] == k:
                            d_param.pop(k)
                            break
                # else:
            # 组合键（未处理）
            elif len(l_d_PK) > 1:
                print("[warning], 组合键（未处理）")
                sys.exit(0)

        # 6,更新字段值（覆盖默认值）
        dd.update(d_param)
        Color_PO.outColor([{"35": varTable + " => " + str(dd)}])
        # print("插入数据 => ", dd)

        # 7,插入数据
        try:
            if self.getIdentityPrimaryKey(varTable) != None:
                self.execute('set identity_insert %s on' % (varTable))
            # 字段，列表转字符串
            l_fields = list(ChainMap(dd))
            # print(l_fields)  # ['result', 'updateDate', 'rule1', 'ruleParam', 'id']
            s_fields = ",".join(l_fields)
            # s_fields = s_fields.replace(',rule,',',[rule],')  # //转义关键字
            # print(s_fields)  # result,updateDate,[rule],ruleParam,id
            # 值，列表转元祖
            l_values = list(dd.values())
            # print(l_values)  # ['15104020755', '2010-11-12', '12', 'param', 9]
            t_values = tuple(l_values)
            # print(t_values)  # ('14598577279', '2010-11-12', '12', 'param', 10)
            self.execute("insert into %s(%s) values %s" % (varTable, s_fields, t_values))
            if self.getIdentityPrimaryKey(varTable) != None:
                self.execute('set identity_insert %s off' % (varTable))

            # print(d_param)
            # a = {"CZRYBM": 123, "CZRYXM": 456}
            for i, v in enumerate(list(d_param.keys())):
                if 'SFZH' == v:
                    # print(list(a.values())[i])
                    Color_PO.outColor([{
                        "36": "[OK] => select * from " + varTable + " where SFZH = '" + str(
                            list(d_param.values())[i]) + "'\n"}])

                elif 'IDCARDNO' == v:
                    # print(list(a.values())[i])
                    Color_PO.outColor([{
                        "36": "[OK] => select * from " + varTable + " where IDCARDNO = '" + str(
                            list(d_param.values())[i]) + "'\n"}])

                elif 'IDCARD' == v:
                    # print(list(a.values())[i])
                    Color_PO.outColor([{
                        "36": "[OK] => select * from " + varTable + " where IDCARD = '" + str(
                            list(d_param.values())[i]) + "'\n"}])

        except:
            Color_PO.outColor([{"31": "[ERROR] => " + varTable + " => 创建记录失败!"}])

    def record2(self, varTable, varType, varValue, l_filterTbl, varIsRecord=True):

        """ 4.5.1 查找记录
        # 参数1：varTable = 表名（*表示所有的表）
        # 参数2：varType = 数据类型(char,int,double,timestamp)
        # 参数3：varValue = 值 (支持%模糊查询，如 %yy%)
        参数4：l_filterTbl = 表名，过滤不需要的表（[table1,table2]）
        参数4:varIsRecord = True / False  (False表示不显示数据)
        """
        # Sqlserver_PO.record('t_upms_user', 'varchar', '%e10adc3949ba59abbe56e057f20f883e')  # 搜索 t_upms_user 表中内容包含 admin 的 varchar 类型记录。
        # Sqlserver_PO.record('*', 'varchar', '%海鹰居委会%')
        # Sqlserver_PO.record('*', 'money', '%34.5%')
        # Sqlserver_PO.record('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
        # Sqlserver_PO.record('*', 'datetime', u'%2019-07-17 11:19%')  # 模糊搜索所有表中带2019-01的timestamp类型。

        # 支持的类型
        if (varType in "double,timestamp,float,money,int,nchar,nvarchar,datetime,varchar"):
            # 所有表
            if "*" in varTable:
                l_d_tbl = self.select("SELECT name as TABLE_NAME FROM SYSOBJECTS WHERE TYPE='U'")
                # print(l_d_tbl)  # [{'TABLE_NAME': 'TB_RIS_REPORT2'}, {'TABLE_NAME': 'jh_jkpg'}, {'TABLE_NAME': 'jh_jkgy'},,...]
                s = ''
                # 遍历所有表
                for b in range(len(l_d_tbl)):

                    # 表名
                    dboTable = l_d_tbl[b]['TABLE_NAME']

                    # 过滤不要遍历的表
                    if dboTable not in l_filterTbl:

                        # 表名:注释
                        d_tableComment = self.getTableComment(dboTable)  # {'ASSESS_DIAGNOSIS': '门诊数据',...

                        # 获取表名和类型
                        l_d_field_type = self.select(
                            "select syscolumns.name as FIELD_NAME,systypes.name as TYPE from syscolumns,systypes where syscolumns.xusertype=systypes.xusertype and syscolumns.id=object_id('%s')"
                            % (dboTable))
                        # print(l_d_field_type)  # [{'FIELD_NAME': 'GUID', 'TYPE': 'varchar'}, {'FIELD_NAME': 'VISITSTRNO', 'TYPE': 'varchar'},...]
                        l_field = []
                        l_type = []
                        for j in l_d_field_type:
                            if varType in j['TYPE']:
                                l_field.append(j['FIELD_NAME'])
                                l_type.append(j['TYPE'])
                        # print(l_field)  # ['GUID', 'VISITSTRNO', 'ORGCODE', 'ORGNAME',...]
                        # print(l_type)  # ['varchar', 'varchar', 'varchar', 'varchar' ...]

                        # 遍历所有字段
                        for i in range(len(l_field)):
                            l_result = self.select(
                                "select * from %s where [%s] like '%s'" % (dboTable, l_field[i], varValue))
                            if len(l_result) != 0:
                                # print("--" * 50)
                                s = s + "<br><textOk>" + str(l_field[i]) + " = " + str(
                                    varValue) + " >> " + dboTable + "(" + d_tableComment[dboTable] + ")" + " >> " + str(
                                    len(l_result)) + "条</textOk><br>"
                                Color_PO.consoleColor("31", "36",
                                                      str(l_field[i]) + " = " + str(
                                                          varValue) + " >> " + dboTable + "(" +
                                                      d_tableComment[dboTable] + ")" + " >> " + str(
                                                          len(l_result)) + "条 ",
                                                      "")

                                # 输出字段注释
                                s = s + "<textErr>" + str(self.getFieldComment(dboTable)) + "</textErr><br>"
                                Color_PO.consoleColor2({"35": self.getFieldComment(dboTable)})

                                if varIsRecord == True:

                                    for j in range(len(l_result)):
                                        print(l_result[j])
                                        s = s + str(l_result[j]) + "<br>"
                                        # print(str(l_result[j]).decode("utf8"))
                                        # print(l_result[j].encode('latin-1').decode('utf8'))
                return s
            elif "*" not in varTable:
                # 搜索指定表（单表）符合条件的记录.  ，获取列名称、列类别、类注释
                # 获取表的Name和Type
                l_d_field_type = self.select(
                    "select syscolumns.name as FIELD_NAME,systypes.name as TYPE from syscolumns,systypes where syscolumns.xusertype=systypes.xusertype and syscolumns.id=object_id('%s')"
                    % (varTable))
                # print(l_d_field_type)  # [{'FIELD_NAME': 'ID', 'TYPE': 'int'}, {'FIELD_NAME': 'ARCHIVENUM', 'TYPE': 'varchar'}...]

                # 筛选符合条件（包含指定type）的field
                l_field = []
                for j in l_d_field_type:
                    if varType in j['TYPE']:
                        l_field.append(j['FIELD_NAME'])
                # print(l_field)  # ['CZRYBM', 'CZRYXM', 'JMXM', 'SJHM', 'SFZH', 'JJDZ',...]

                # 遍历所有字段
                s = ''
                for i in range(len(l_field)):
                    l_result = self.select("select * from %s where [%s] like '%s'" % (varTable, l_field[i], varValue))
                    if len(l_result) != 0:
                        # print("--" * 50)
                        Color_PO.consoleColor("31", "36",
                                              "[result] => " + str(varValue) + " => " + varTable + " => " + l_field[
                                                  i] + " => " + str(len(l_result)) + "条 ", "")

                        # 输出字段注释
                        Color_PO.consoleColor2({"35": self.getFieldComment(varTable)})
                        # print(self.getFieldComment(dboTable))

                        for j in range(len(l_result)):
                            l_value = [value for value in l_result[j].values()]
                            # print(l_value)  # ['1015', '李*琳', '常*梅', '17717925118', '132222196702240429',...]
                            print(l_result[
                                      j])  # {'CZRYBM': '1015', 'CZRYXM': '李*琳', 'JMXM': '常*梅', 'SJHM': '17717925118', 'SFZH': '132222196702240429'...}

        else:
            print("\n" + varType + "类型不存在，如：float,money,int,nchar,nvarchar,datetime,timestamp")
        # self.conn.close()
    def record(self, varTable, varType, varValue, varIsRecord=True):

        """ 4.5 查找记录
        # 参数1：varTable = 表名（*表示所有的表）
        # 参数2：varType = 数据类型(char,int,double,timestamp)
        # 参数3：varValue = 值 (支持%模糊查询，如 %yy%)
        参数4:varIsRecord = True / False  (False表示不显示数据)
        """
        # Sqlserver_PO.record('t_upms_user', 'varchar', '%e10adc3949ba59abbe56e057f20f883e')  # 搜索 t_upms_user 表中内容包含 admin 的 varchar 类型记录。
        # Sqlserver_PO.record('*', 'varchar', '%海鹰居委会%')
        # Sqlserver_PO.record('*', 'money', '%34.5%')
        # Sqlserver_PO.record('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
        # Sqlserver_PO.record('*', 'datetime', u'%2019-07-17 11:19%')  # 模糊搜索所有表中带2019-01的timestamp类型。

        # 支持的类型
        if (varType in "double,timestamp,float,money,int,nchar,nvarchar,datetime,varchar"):
            if "*" in varTable:
                # 遍历所有表
                l_d_tbl = self.select("SELECT name as TABLE_NAME FROM SYSOBJECTS WHERE TYPE='U'")
                # print(l_d_tbl)  # [{'TABLE_NAME': 'TB_RIS_REPORT2'}, {'TABLE_NAME': 'jh_jkpg'}, {'TABLE_NAME': 'jh_jkgy'},,...]

                for b in range(len(l_d_tbl)):
                    # 获取表的Name和Type
                    dboTable = l_d_tbl[b]['TABLE_NAME']

                    # 获取表注释
                    d_tableComment = self.getTableComment(dboTable)  # {'ASSESS_DIAGNOSIS': '门诊数据',...

                    l_d_field_type = self.select(
                        "select syscolumns.name as FIELD_NAME,systypes.name as TYPE from syscolumns,systypes where syscolumns.xusertype=systypes.xusertype and syscolumns.id=object_id('%s')"
                        % (dboTable))
                    # print(l_d_field_type)  # [{'FIELD_NAME': 'GUID', 'TYPE': 'varchar'}, {'FIELD_NAME': 'VISITSTRNO', 'TYPE': 'varchar'},...]

                    l_field = []
                    l_type = []
                    for j in l_d_field_type:
                        if varType in j['TYPE']:
                            l_field.append(j['FIELD_NAME'])
                            l_type.append(j['TYPE'])
                    # print(l_field)  # ['GUID', 'VISITSTRNO', 'ORGCODE', 'ORGNAME',...]
                    # print(l_type)  # ['varchar', 'varchar', 'varchar', 'varchar' ...]

                    # 遍历所有字段
                    for i in range(len(l_field)):
                        l_result = self.select(
                            "select * from %s where [%s] like '%s'" % (dboTable, l_field[i], varValue))
                        # print(dboTable, l_field[i], varValue)
                        # print(l_result)
                        if len(l_result) != 0:
                            print("--" * 50)
                            # Color_PO.consoleColor("31", "36", str(varValue) + " >> " + tbl + "(" + l_field[i] + ") " + str(len(l_result)) + "条 ", "")
                            # print(dboTable, d_tableComment[str(dboTable)])
                            Color_PO.consoleColor("31", "36",
                                                  str(l_field[i]) + " = " + str(varValue) + " >> " + str(
                                                      dboTable) + "(" +
                                                  str(d_tableComment[dboTable]) + ")" + " >> " + str(
                                                      len(l_result)) + "条 ",
                                                  "")

                            # 输出字段注释
                            Color_PO.consoleColor2({"35": self.getFieldComment(dboTable)})

                            if varIsRecord == True:
                                for j in range(len(l_result)):
                                    print(l_result[j])
                                    # print(str(l_result[j]).decode("utf8"))
                                    # print(l_result[j].encode('latin-1').decode('utf8'))

            elif "*" not in varTable:
                # 搜索指定表（单表）符合条件的记录.  ，获取列名称、列类别、类注释
                # 获取表的Name和Type
                l_d_field_type = self.select(
                    "select syscolumns.name as FIELD_NAME,systypes.name as TYPE from syscolumns,systypes where syscolumns.xusertype=systypes.xusertype and syscolumns.id=object_id('%s')"
                    % (varTable))
                # print(l_d_field_type)  # [{'FIELD_NAME': 'ID', 'TYPE': 'int'}, {'FIELD_NAME': 'ARCHIVENUM', 'TYPE': 'varchar'}...]

                # 筛选符合条件（包含指定type）的field
                l_field = []
                for j in l_d_field_type:
                    if varType in j['TYPE']:
                        l_field.append(j['FIELD_NAME'])
                # print(l_field)  # ['CZRYBM', 'CZRYXM', 'JMXM', 'SJHM', 'SFZH', 'JJDZ',...]

                # 遍历所有字段
                for i in range(len(l_field)):
                    l_result = self.select("select * from %s where [%s] like '%s'" % (varTable, l_field[i], varValue))
                    if len(l_result) != 0:
                        print("--" * 50)
                        Color_PO.consoleColor("31", "36",
                                              "[result] => " + str(varValue) + " => " + varTable + " => " + l_field[
                                                  i] + " => " + str(len(l_result)) + "条 ", "")

                        # 输出字段注释
                        Color_PO.consoleColor2({"35": self.getFieldComment(varTable)})
                        # print(self.getFieldComment(dboTable))

                        for j in range(len(l_result)):
                            l_value = [value for value in l_result[j].values()]
                            # print(l_value)  # ['1015', '李*琳', '常*梅', '17717925118', '132222196702240429',...]
                            print(l_result[
                                      j])  # {'CZRYBM': '1015', 'CZRYXM': '李*琳', 'JMXM': '常*梅', 'SJHM': '17717925118', 'SFZH': '132222196702240429'...}

        else:
            print("\n" + varType + "类型不存在，如：float,money,int,nchar,nvarchar,datetime,timestamp")
        # self.conn.close()

    def genFirstRecord(self, varTable):

        # 4.6 生成第一条记录

        # 判断表是否存在
        if self.isTable(varTable) == True:
            # 判断是否有记录
            qty = self.getRecordCount(varTable)
            if qty == 0:
                # print(varTable)
                # 获取生成类型值
                d_init = self._genTypeValue(varTable)
                # print(d_init)
                # 执行insert
                self._execInsert(varTable, d_init, {})
                return True
            else:
                return False

    def genFirstRecordByAll(self):

        # 4.7 所有空表自动生成第一条记录

        r = self.getTables()
        # print(r)
        for i in range(len(r)):
            self.genFirstRecord(r[i])

    def genRecord(self, varTable, d_field={}):

        '''
        4.8 自动添加一条记录
        :param varTbl:
        :param d_field: 可以设置字段的值，如："ID = 123" ， 但不能设置主键
        Sqlserver_PO.genRecord("TB_HIS_MZ_Reg", {"GTHBZ": None, "GHRQ":"777"})  # 自动生成数据
        :return:
        '''

        if self.genFirstRecord(varTable) == False:

            # 判断表是否存在
            if self.isTable(varTable) == True:

                # 获取生成类型值
                d_init = self._genTypeValue(varTable)

                # 获取主键
                l_primaryKey = self.getPrimaryKey(varTable)
                # 没有主键
                if l_primaryKey != None:
                    primaryKey = l_primaryKey[0]['COLUMN_NAME']

                    # 获取主键最大值
                    d_primaryKey = self.getPrimaryKeyMaxValue(varTable)
                    # print(d_primaryKey)  # {'id': 39}
                    # print(d_primaryKey[primaryKey])  # 39
                    # 修改主键最大值+1
                    d_init[primaryKey] = d_primaryKey[primaryKey] + 1
                    # print(d1)  # {'id': 40, 'name': 'a', 'age': 1}

                # 执行insert
                self._execInsert(varTable, d_init, d_field)

    def genRecordByNotNull(self, varTable):

        # 4.9 自动生成必填项记录

        if self.genFirstRecord(varTable) == False:

            # 判断表是否存在
            if self.isTable(varTable) == True:
                # 生成必填项类型值
                d_init = self._genNotNullTypeValue(varTable)

                # 获取主键
                l_primaryKey = self.getPrimaryKey(varTable)
                # print(l_primaryKey[0]['COLUMN_NAME'])  # ID
                primaryKey = l_primaryKey[0]['COLUMN_NAME']

                # 获取主键最大值
                d_primaryKey = self.getPrimaryKeyMaxValue(varTable)
                # print(d_primaryKey)  # {'id': 39}
                # print(d_primaryKey[primaryKey])  # 39
                # 修改主键最大值+1
                d_init[primaryKey] = d_primaryKey[primaryKey] + 1
                # print(d_init)  # {'id': 40, 'name': 'a', 'age': 1}

                # 执行insert
                self._execInsert(varTable, d_init, {})
    def _genTypeValue(self, varTable):

        # 生成类型值

        # 获取所有字段和类型
        d = self.getFieldType(varTable)
        # print(d)  # {'id': 'int', 'name': 'varchar', 'age': 'int'}

        # 初始化对应类型的值
        d_init = {}
        for k, v in d.items():
            if v == 'tinyint' or v == 'smallint' or v == 'int' or v == 'bigint':
                d_init[k] = 1
            elif v == 'float' or v == 'real':
                d_init[k] = 1.00
            elif v == 'numeric' or v == 'decimal':
                d_init[k] = 1
            elif v == 'money' or v == 'smallmoney':
                d_init[k] = 1
            elif v == 'char' or v == 'varchar' or v == 'nchar' or v == 'nvarchar' or v == 'text':
                d_init[k] = 'a'
            elif v == 'datetime' or v == 'smalldatetime' or v == 'datetime2':
                d_init[k] = Time_PO.getDateTimeByPeriod(0)
            elif v == 'time':
                d_init[k] = '08:12:23'
            elif v == 'date':
                d_init[k] = Time_PO.getDateByMinus()
        # print(d1)  # {'id': 1, 'name': 'a', 'age': 1}
        return d_init
    def _genNotNullTypeValue(self, varTable):

        # 生成必填项类型值

        # 获取所有字段和类型
        d = self.getNotNullFieldType(varTable)
        # print(d)  # {'id': 'int', 'name': 'varchar', 'age': 'int'}

        # 初始化对应类型的值
        d_init = {}
        for k, v in d.items():
            if v == 'tinyint' or v == 'smallint' or v == 'int' or v == 'bigint':
                d_init[k] = 1
            elif v == 'float' or v == 'real':
                d_init[k] = 1.00
            elif v == 'numeric' or v == 'decimal':
                d_init[k] = 1
            elif v == 'money' or v == 'smallmoney':
                d_init[k] = 1
            elif v == 'char' or v == 'varchar' or v == 'nchar' or v == 'nvarchar' or v == 'text':
                d_init[k] = 'a'
            elif v == 'datetime' or v == 'smalldatetime' or v == 'datetime2':
                d_init[k] = '2020-12-12 09:12:23'
            elif v == 'time':
                d_init[k] = '08:12:23'
            elif v == 'date':
                d_init[k] = '2019-11-27'
        # print(d1)  # {'id': 1, 'name': 'a', 'age': 1}
        return d_init
    def _execInsert(self, varTable, d_init, d_field):

        # 执行insert

        if d_field != {}:
            for k, v in d_field.items():
                for k1, v1 in d_init.items():
                    if k == k1:
                        d_init[k] = v
            # print(d_init)  # {'GHRQ': 'a', 'GHBM': 'a', 'GTHBZ': 'a', ...}

        # 将d_init转换成insert语句的字段名及值
        s = ""
        u = ""
        for k, v in d_init.items():
            s = s + k + ","
            u = u + "'" + str(v) + "',"
        s = s[:-1]
        u = u[:-1]

        # 判断是否有自增列，如果有则返回1，无则返回0
        qty = self.select("Select OBJECTPROPERTY(OBJECT_ID('" + varTable + "'),'TableHasIdentity') as qty")
        if qty[0]['qty'] == 1:
            self.execute('set identity_insert ' + str(varTable) + ' on')
            sql = "INSERT INTO " + str(varTable) + " (" + s + ") VALUES (" + u + ")"
            print(varTable)
            print(sql)
            self.execute(sql)
            # self.execute(varTable, sql)
            self.conn.commit()
            print("[ok], " + str(sql))
            self.execute('set identity_insert ' + str(varTable) + ' off')
        else:
            if 'None' in u:
                u = u.replace(",'None',", ",null,")
                sql = "INSERT INTO " + str(varTable) + " (" + s + ") VALUES (" + u + ")"
            else:
                sql = "INSERT INTO " + str(varTable) + " (" + s + ") VALUES (" + u + ")"
            self.execute(sql)
            self.conn.commit()
            print("[ok], " + str(sql))


    def isRecord(self, varTable, varField, varValue):

        # 4.10 判断记录是否存在
        # 如：isRecord("QYYH","SFZH","310101198004110014") ， 返回1表示存在，返回0表示不存在

        d_table_field = self.selectOne("IF EXISTS (SELECT 1 FROM %s WHERE %s = '%s') SELECT 1 AS RecordExists ELSE SELECT 0 AS RecordExists" % (varTable, varField, varValue))
        # print(d_table_field)
        return d_table_field['RecordExists']


    # todo 导入导出

    def csv2dbByType(self, varPathFile, varDbTable, varFieldAndType):

        '''
        5.1 csv2db 自定义字段类型
        varPathFile = './data/test.csv'
        varDbTable = 'tableName'
        varFieldAndType = 'id INTEGER PRIMARY KEY, name TEXT, age INTEGER'
        csv2dbBy
        '''

        try:
            data = etl.fromcsv(varPathFile)
            self.crtTable(varDbTable, varFieldAndType)  # 创建表
            etl.todb(data, self.conn, varDbTable)
        except Exception as e:
            print(e)

    def csv2dbByAutoType(self, varPathFile, varDbTable):

        '''
        5.2 csv2db 自动生成字段类型
        varPathFile = './data/test.csv'
        varDbTable = 'tableName'
        '''

        try:
            df = pd.read_csv(varPathFile, encoding='gbk')
            engine = self.getEngine_pymssql()
            df.to_sql(varDbTable, con=engine, if_exists="replace", index=False)
        except Exception as e:
            print(e)

    def xlsx2db_deduplicated(self, varExcel, varDbTable, varDropDuplicatesField, varSheetName=0):

        '''
        5.3，xlsx导入数据库（保留原来字段，追加数据）
        作用是将 Excel 数据导入 SQL Server 数据库，同时根据指定字段去除重复数据。它确保了数据的唯一性，避免了重复记录被插入到数据库中。
        xlsx2db('2.xlsx', "tableName", "字段", "sheet1")
        注意excel表格第一行数据对应db表中字段，建议用英文
        '''

        try:
            df = pd.read_excel(varExcel, sheet_name=varSheetName)
            df_deduplicated = df.drop_duplicates(subset=[varDropDuplicatesField])  # 去重
            engine = self.getEngine_pymssql()
            df_deduplicated.to_sql(varDbTable, con=engine, if_exists='append', index=False)
        except Exception as e:
            print(e)

    def xlsx2db_append(self, varPathFile, varDbTable, varSheetName=0):

        '''
        5.3，xlsx导入数据库（清空原表数据后追加数据）
        xlsx2db_append('2.xlsx', "tableName", "sheet1")
        excel表格第一行数据对应db表中字段，建议用英文
        '''

        try:
            df = pd.read_excel(varPathFile, sheet_name=varSheetName)
            engine = self.getEngine_pymssql()
            df.to_sql(varDbTable, con=engine, if_exists='append', index=False, chunksize=1000)
        except Exception as e:
            print(e)

    def xlsx2db_replace(self, varPathFile, varDbTable, varSheetName=0):

        '''
        5.3，xlsx导入数据库（删除原表后再创建）
        xlsx2db_replace('2.xlsx', "tableName", "sheet1")
        excel表格第一行数据对应db表中字段，建议用英文
        '''

        try:
            df = pd.read_excel(varPathFile, sheet_name=varSheetName)
            engine = self.getEngine_pymssql()
            df.to_sql(varDbTable, con=engine, if_exists="replace", index=False)
        except Exception as e:
            print(e)


    def xlsx2db2(self, varPathFile, varDbTable, varSheetName, varColName):

        '''
        5.3，xlsx全量导入数据库（覆盖）
        # 定义列的数据类型
        xlsx2db2('2.xlsx', "tableName", "sheet1", "colName")
        excel表格第一行数据对应db表中字段，建议用英文
        '''

        try:
            df = pd.read_excel(varPathFile, sheet_name=varSheetName)
            engine = self.getEngine_pymssql()
            # df.to_sql(varDbTable, con=engine, if_exists="replace", index=False)

            # # 定义列的数据类型
            dtype = {
                varColName : sqltypes.VARCHAR(length=255, collation='utf8mb4_unicode_ci')  # 自定义字符集
                # 'other_column': sqltypes.INTEGER()
            }

            df.to_sql(varDbTable, con=engine, if_exists="replace", index=False, dtype=dtype)

        except Exception as e:
            print(e)

    def df2db3(self, df, varTable):

        '''
        5.3，xlsx全量导入数据库（覆盖）
        xlsx2db('2.xlsx', "tableName", "sheet1")
        excel表格第一行数据对应db表中字段，建议用英文
        '''

        engine = self.getEngine_pymssql()

        try:

            # 开始数据库事务
            with engine.begin() as connection:
                # 使用 pandas 的 to_sql 方法将数据写入数据库
                # 如果表已存在，可以选择 'fail', 'replace', 或 'append' 模式
                df.to_sql(
                    name=varTable,
                    con=connection,
                    if_exists='replace',  # 根据需要修改此参数
                    index=False
                )

            return True

        except Exception as e:
            print(e)


    def xlsx2dbByConverters(self, varPathFile, varDbTable, var_d, varSheetName=0):

        '''
        5.4，xlsx全量导入数据库，并转换字段类型
        # 如：将idcard字段转换为字符串类型，idcard本身是数字类型
        如果idcard不存在则忽略。
        xlsx2dbByConverters('2.xlsx', "tableName", {"idcard": str}, "sheet1")
        '''

        try:
            df = pd.read_excel(varPathFile, converters=var_d, sheet_name=varSheetName)
            engine = self.getEngine_pymssql()
            df.to_sql(varDbTable, con=engine, if_exists="replace", index=False)
        except Exception as e:
            print(e)

    def xlsx2dbAppendById(self, varPathFile, varDbTable, maxId, varSheetName=0):

        '''
        5.5，xlsx增量导入数据库，id自动提增
        xlsx2dbAppend('2.xlsx', "tableName", maxId, "sheet1")
        maxId = 表中最大id , 追加的记录中id无需填写自动提增。
        '''

        try:
            df = pd.read_excel(varPathFile, sheet_name=varSheetName)
            temp = 0
            for index, value in df['id'].items():
                temp = temp + 1
                df.at[index, 'id'] = maxId + temp
            engine = self.getEngine_pymssql()
            df.to_sql(varDbTable, con=engine, if_exists="append", index=False)
        except Exception as e:
            print(e)

    def xlsx2dbAppend(self, varPathFile, varDbTable, varSheetName=0):

        '''
        5.6，xlsx增量导入数据库
        xlsx2dbAppend('2.xlsx', "tableName", "sheet1")
        '''

        try:
            df = pd.read_excel(varPathFile, sheet_name=varSheetName)
            engine = self.getEngine_pymssql()
            df.to_sql(varDbTable, con=engine, if_exists="append", index=False)
        except Exception as e:
            print(e)



    def dict2db(self, varDict, varDbTable, index="True"):

        # 5.7 字典导入数据库

        try:
            df = pd.DataFrame(varDict)
            engine = self.getEngine_pymssql()
            if index == "False":
                df.to_sql(name=varDbTable, con=engine, if_exists="replace", index=False)
            else:
                df.to_sql(name=varDbTable, con=engine, if_exists="replace")
        except Exception as e:
            print(e)

    def list2db(self, l_col, l_value, varDbTable, index="False"):

        # 5.8 列表导入数据库
        # l_col = 字段，如 ['id','name','age']
        # l_value= 值,如 [['1','john','44],['2','ti','4']]

        try:
            df = pd.DataFrame(l_value, columns=l_col)
            engine = self.getEngine_pymssql()

            # 定义数据类型字典，假设所有列都是 varchar(255)，如果没有dtype语句，则默认varchar（-1）
            dtype = {col: sqlalchemy.types.VARCHAR(length=255) for col in df.columns}

            if index == "False":
                df.to_sql(name=varDbTable, con=engine, if_exists="replace", index=False, dtype=dtype)
            else:
                df.to_sql(name=varDbTable, con=engine, if_exists="replace", dtype=dtype)
        except Exception as e:
            print(e)

    def df2db(self, varDF, varTable):

        # 5.9，dataframe导入数据库
        engine = self.getEngine_pymssql()

        try:
            varDF.to_sql(name=varTable, con=engine, if_exists="replace", index=False, chunksize=1000)
        except Exception as e:
            print(e)


    def db2csv(self, sql, varExcelFile, header=1):

        # 5.10 数据库sql导出csv(含字段或不含字段)

        try:
            engine = self.getEngine_pymssql()
            df = pd.read_sql(text(sql), con=engine.connect())
            # header=None表示不含列名
            if header == None:
                df.to_csv(varExcelFile, index=None, header=None)
            else:
                df.to_csv(varExcelFile, index=None)
        except Exception as e:
            print(e)

    def db2xlsx(self, sql, varExcelFile, header=1):

        # 5.11 数据库sql导出xlsx(含字段或不含字段)

        try:
            engine = self.getEngine_pymssql()
            df = pd.read_sql(text(sql), con=engine.connect())
            # header=None表示不含列名
            if header == None:
                df.to_excel(varExcelFile, index=None, header=None)
            else:
                df.to_excel(varExcelFile, index=None)
        except Exception as e:
            print(e)

    def db2dict(self, sql, orient='list'):

        # 5.12 数据库sql导出字典 pymssql

        try:
            engine = self.getEngine_pymssql()
            df = pd.read_sql(text(sql), con=engine.connect())
            return df.to_dict(orient=orient)
        except Exception as e:
            print(e)

    def db2dict2(self, sql, orient='list'):

        # 5.12 数据库sql导出字典 pyodbc

        try:
            engine = self.getEngine_pyodbc()
            df = pd.read_sql(text(sql), con=engine.connect())
            return df.to_dict(orient=orient)
        except Exception as e:
            print(e)

    def db2html(self, sql, varHtml):

        # 5.13 数据库sql导出html
        # Sqlserver_PO.db2html("select ID, pResult as 正向, nResult as 反向, QC_type as 类型, QC_field as 质控字段, QC_rule as 质控规则, QC_desc as 错我描述"
        #                      ", pCase as 正向用例, nCase as 反向用例, pCheck as 正向校验 from A_testrule", 'ehr_rule_result.html')
        try:
            engine = self.getEngine_pymssql()
            df = pd.read_sql(text(sql), con=engine.connect())
            pd.set_option('colheader_justify', 'center')

            # html标题、title
            html = '''<html><head><title>EHR规则自动化报表</title></head>
            <body><b><caption>EHR规则自动化_''' + str(
                strftime("%Y-%m-%d %H:%M:%S", localtime())) + '''</caption></b><br><br>{table}</body></html>'''
            html_string = '''<style>.mystyle {font-size: 11pt; font-family: Arial;    border-collapse: collapse;     border: 1px solid silver;}.mystyle td, th {    padding: 5px;}.mystyle tr:nth-child(even) {    background: #E0E0E0;}.mystyle tr:hover {    background: silver;    cursor: pointer;}</style>'''

            with open(varHtml, 'w') as f:
                f.write(html_string + html.format(table=df.to_html(classes="mystyle", col_space=100, index=False)))
                # f.write(html.format(table=df.to_html(classes="mystyle", col_space=50)))

            # 修改菜单颜色 - 优化
            # 绿色 = 00E400，黄色 = FFFF00，橙色 = FF7E00，红色 = FF0000，粉色 = 99004C，
            # 褐色 =7E0023,'c6efce = 淡绿', '006100 = 深绿'，'ffffff=白色', '000000=黑色'，'ffeb9c'= 橙色
            from bs4 import BeautifulSoup
            html_text = BeautifulSoup(open(varHtml), features='html.parser')
            html_text = str(html_text).replace("<td>None</td>", "<td></td>") \
                .replace(">正向结果</th>", 'bgcolor="#ffeb9c">正向结果</th>') \
                .replace(">反向结果</th>", 'bgcolor="#ffeb9c">反向结果</th>') \
                .replace("<td>error</td>", '<td bgcolor="#ff0000">error</td>')

            # 另存为report.html
            tf = open(varHtml, 'w', encoding='utf-8')
            tf.write(str(html_text))
            tf.close()

            count = self.select(sql)
            return (len(count))


        except Exception as e:
            print(e)

    def db2df(self, sql):

        # 5.14 db转dataframe
        # db2df("select * from a_test")

        l_d_data = self.select(sql)
        print(
            l_d_data)  # [{'id': 1, 'name': 'John Smith2', 'salesrep': 'John Doe3'}, {'id': 2, 'name': 'Jane Doe', 'salesrep': 'Joe Dog'},...
        # print(l_d_data[0])
        # print(list(l_d_data[0].keys()))
        df = pd.DataFrame(l_d_data, columns=list(l_d_data[0].keys()))
        # df.to_string(index=False)
        return df


    def get_row_number_with_null(self, tableName, colName):
        # 6.1 获取某列中为Null值的行号集合，如获取body列中为空值的行号集合
        # 获取某字段为Null值的集结行号
        # 执行 SQL 查询，使用 ROW_NUMBER() 函数为结果集添加行号
        # print(get_row_number_with_null('a_phs_auth_app', 'body')) # [{'_body': 4}, {'_body': 5}]

        query = f"""
            SELECT _{colName}
            FROM (
                SELECT ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS _{colName}, {colName}
                FROM {tableName}
            ) subquery
            WHERE {colName} IS NULL
        """
        rows = Sqlserver_PO.select(query)
        return rows


    def setValue_with_row_number(self,tableName, row_number, d_value, valid_field):
        # 6.2 更改第N行的字段值，如修改第三行的query和body值
        # valid_field 是一个有效的列名，用于连接，必须要有值。如果表中没有唯一标识列，需要根据实际表结构选择合适的列进行连接
        # 构造 SET 子句
        set_clause = ', '.join([f"{column} = '{value}'" for column, value in d_value.items()])
        print(set_clause)  # query = 'test', body = 'hello'
        # 执行更新操作
        update_query = f"""
            UPDATE {tableName}
            SET {set_clause}
            FROM {tableName} t
            JOIN (
                SELECT ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS rn, *
                FROM {tableName}
            ) subquery ON t.[{valid_field}] = subquery.[{valid_field}]
            WHERE subquery.rn = {row_number}
        """
        Sqlserver_PO.execute(update_query)



if __name__ == "__main__":

    # todo 社区健康平台（静安）
    # Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CHC_JINGAN", "GBK")

    # todo 社区健康平台（全市）
    # Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CHC", "GBK")
    # Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CHC_5G", "GBK")
    Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CDRD_PT", "GBK")

    # Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "PHUSERS", "GBK")
    # print(Sqlserver_PO.isTable("a_phs_auth"))



    # 复制表(覆盖)
    # Sqlserver_PO.copyTable('a_phs_auth', 'a_phs_auth_app')
    #
    # # 在url前插入字段case1
    # Sqlserver_PO.insertBeforeField('a_weight10_EFRB', 'id', 'id_pk', 'int(5)')
    # # 在tags前插入字段status
    # Sqlserver_PO.insertBeforeField('a_phs_auth_app', 'tags', 'status', 'varchar(66)')

    # 追加字段
    # Sqlserver_PO.appendField('a_phs_auth_app', 'status123', 'VARCHAR(11)')

    # Sqlserver_PO.setField('a_phs_auth_app', 'status', 'VARCHAR(11)')
    # # print("4.1 判断表是否存在".center(100, "-"))
    # print(Sqlserver_PO.isTable("aaa"))
    #
    # # print("4.2 判断字段是否存在(字段区分大小写)".center(100, "-"))
    # print(Sqlserver_PO.isField('bbb', 'id'))
    #
    # # print("4.3 判断是否有自增主键".center(100, "-"))
    # print(Sqlserver_PO.isIdentity('bbb'))
    # print(Sqlserver_PO.isIdentity('aaa'))

    # # print("4.10 判断记录是否存在".center(100, "-"))
    print(Sqlserver_PO.isRecord("sys_category_mapping", "category_key", "cdrd_patient_diag1_info"))


    # # print("5.1 csv2db自定义字段类型".center(100, "-"))
    # Sqlserver_PO.csv2dbByType('./data/test12.csv', "test555")

    # # print("5.2 csv2db自动生成字段类型".center(100, "-"))
    # Sqlserver_PO.csv2dbByAutoType('./data/test12.csv', "test555")

    # # print("5.3 excel导入数据库".center(100, "-"))
    Sqlserver_PO.xlsx2db_replace('/Users/linghuchong/Desktop/test.xlsx', "sys_category", "sheet")


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
    # Sqlserver_PO.record('*', 'varchar', '%测试测试2%', False)
    # Sqlserver_PO.record('*', 'money', '%34.5%')
    # Sqlserver_PO.record('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
    # Sqlserver_PO.record('*', 'datetime', u'%2019-07-17 11:19%')  # 模糊搜索所有表中带2019-01的timestamp类型。

    # print("7.3 插入记录".center(100, "-"))
    # Sqlserver_PO.insert("a_test", {'result': str(Fake_PO.genPhone_number('Zh_CN', 1)), 'createDate': Time_PO.getDateTimeByPeriod(0), 'ruleParam': 'param'})





