# -*- coding: utf-8 -*-
# ***************************************************************
# Author     : John
# Data       : 2019-04-16
# Description: MysqlPO对象层
# ***************************************************************
# pip3 install mysqlclient  (MySQLdb)
# pip3 install pymysql

# todo 乱码
# Q1：数据库中乱码显示问题，查询后却显示中文？
# 分析：设置 charset 编码，charset 应该与数据库编码一致，如数据库是gb2312 ,则 charset='gb2312'。
# 解决：self.conn = MySQLdb.connect(host=self.varHost, user=self.varUser, passwd=self.varPassword, db=self.db, port=self.varPort, use_unicode=True, charset='utf8')

# todo sqlalchemy中create_engine用法 (https://blog.csdn.net/xc_zhou/article/details/118829588)
# engine = create_engine('数据库类型+驱动://用户名:密码@服务器IP:端口/数据库?charset=utf8')
# Mysql：engine = create_engine('mysql://scott:tiger@localhost/foo')
# mysql-python: engine = create_engine('mysql+mysqldb://scott:tiger@localhost/foo')
# mysql-connector-python: engine = create_engine('mysql+mysqlconnector://scott:tiger@localhost/foo')
#
# ***************************************************************

"""
pandas引擎（pymysql）  getEngine_pymysql()
pandas引擎（mysqldb）  getEngine_mysqldb()

1，查看表结构  dbDesc()
2，搜索记录  dbRecord('*', 'money', '%34.5%')
3，查询表创建时间  dbCreateDate()

4.1，数据库sql导出csv  db2csv()
4.2，数据库sql导出excel  db2xlsx()
4.4，数据库sql导出html  db2html()
4.3 数据库sql导出字典  db2dict()
4.5 数据库sql导出DataFrame db2df()
4.5，将数据库表导出html  Mysql_PO.db2html("erp_开发计划总揽_2022-11-12", "sys_area", "d://123.html",False)

5.1 excel导入数据库 xlsx2db()
5.2 字典导入数据库  dict2db()
5.3 列表导入数据库  list2db()
5.4 DataFrame导入数据库  df2db()

4.4，将数据库表结构导出excel  dbDesc2xlsx()
5 获取单个表的所有字段 getTableField(self, varTable)

6 expain SQL语句的执行计划

7 获取mysql关键字列表 ？

"""

import sys, pymysql

pymysql.install_as_MySQLdb()
import MySQLdb
import pandas as pd
from PO.ExcelPO import *
# from sqlalchemy import create_engine
from sqlalchemy import create_engine, text

from bs4 import BeautifulSoup
from PO.OpenpyxlPO import *
from PO.NewexcelPO import *

from PO.ColorPO import *
Color_PO = ColorPO()


class MysqlPO:

    def __init__(self, varHost, varUser, varPassword, varDB, varPort=3336):

        self.host = varHost
        self.user = varUser
        self.password = varPassword
        self.db = varDB
        self.port = varPort
        self.conn = MySQLdb.connect(
            host=varHost,
            user=varUser,
            passwd=varPassword,
            db=varDB,
            port=int(varPort),
            use_unicode=True,
        )
        self.cur = self.conn.cursor()
        if not self.cur:
            raise (NameError, "error，创建游标失败！")


    def getEngine(self):
        # mysql 引擎
        return create_engine("mysql://" + self.user + ":" + self.password + "@" + self.host + ":" + str(self.port) + "/" + self.db)

    def getEngine_pymysql(self):
        # pymysql 引擎
        return create_engine("mysql+pymysql://" + self.user + ":" + self.password + "@" + self.host + ":" + str(self.port) + "/" + self.db)
        # return create_engine('mysql+pymysql://' + self.user + ":" + self.password + "@" + self.host + ":" + str(self.port) + "/" + self.db + "?charset=utf8")

    def getEngine_mysqlconnector(self):
        # mysqlconnector 引擎
        return create_engine("mysql+mysqlconnector://" + self.user + ":" + self.password + "@" + self.host + ":" + str(self.port) + "/" + self.db)

    def getEngine_mysqldb(self):
        # mysqldb 引擎
        return create_engine("mysql+mysqldb://" + self.user + ":" + self.password + "@" + self.host + ":" + str(self.port) + "/" + self.db)

    def getEngine_oursql(self):
        # oursql 引擎
        return create_engine("mysql+oursql://" + self.user + ":" + self.password + "@" + self.host + ":" + str(self.port) + "/" + self.db)


    def execQuery(self, sql):

        """查询sql"""

        try:
            self.conn.commit()
            self.cur.execute(sql)
            result = self.cur.fetchall()

            d = {}
            l1 = []
            # 获取字段名称
            l_fields = [i[0] for i in self.cur.description]
            # print(l_fields)  # ['name', 'age', 'sex']
            for i in range(len(result)):
                # print(list(result[i]))
                l1.append(dict(zip(list(l_fields), list(result[i]))))
            # print(l1)

            return l1
        except Exception as e:
            # print(e.args)  # ('table hh already exists',)
            # print(str(e))  # table hh already exists
            # print(NameError(e))  # table hh already exists
            print(repr(e))  # OperationalError('table hh already exists')


    def execute(self, sql):

        '''
        执行sql （insert，update）
        :param sql:
        :return:
        '''

        try:
            self.cur.execute(sql)
            self.conn.commit()
            return "ok"
        except Exception as e:
            # print(e.args)  # ('table hh already exists',)
            # print(str(e))  # table hh already exists
            # print(NameError(e))  # table hh already exists
            # print(repr(e))  # OperationalError('table hh already exists')
            return str(e)


    def execCall(self, varProcedure, varList = []):

        # 执行存储过程

        self.cur.callproc(varProcedure, varList)
        result = self.cur.fetchone()

        self.conn.commit()
        self.cur.close()
        self.conn.close()

        return result

    def close(self):
        self.cur.close()
        self.conn.close()

    def _dbDesc_search(self, varTable, var_l_field=0):

        """dbDesc函数中子查询"""

        l_field = []
        l_type = []
        l_isnull = []
        l_isKey = []
        l_comment = []
        tmp = 0

        t_table_comment = self.execQuery(
            'select table_name,table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" '
            % (self.db, varTable)
        )
        # print(t_table_comment)
        # print(t_table_comment[0])
        if t_table_comment[0]['table_name'] == varTable:
            t_field_type_isnull_key_comment = self.execQuery(
                'select column_name,column_type,is_nullable,column_key,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" '
                % (self.db, varTable)
            )
            # print(t_field_type_isnull_key_comment)  # (('id', 'int(11)', 'PRI', 'NO', '主键'),

            # 字段与类型对齐
            a = b = c = d = e = 0
            for i in t_field_type_isnull_key_comment:
                # print(i)
                if len(i['column_name']) > a:
                    a = len(i['column_name'])
                if len(i['column_type']) > b:
                    b = len(i['column_type'])
                if len(i['is_nullable']) > c:
                    c = len(i['is_nullable'])
                if len(i['column_key']) > d:
                    d = len(i['column_key'])
                if len(i['column_comment']) > e:
                    e = len(i['column_comment'])

            if var_l_field != 0:
                # 可选字段
                for l in range(len(var_l_field)):
                    for m in range(len(t_field_type_isnull_key_comment)):
                        # print(t_field_type_key_isnull_comment[m][0])
                        if var_l_field[l] == t_field_type_isnull_key_comment[m][0]:
                            l_field.append(
                                t_field_type_isnull_key_comment[m][0]
                                + " "
                                * (a - len(t_field_type_isnull_key_comment[m][0]) + 1)
                            )
                            l_type.append(
                                t_field_type_isnull_key_comment[m][1]
                                + " "
                                * (b - len(t_field_type_isnull_key_comment[m][1]) + 1)
                            )
                            l_isnull.append(
                                t_field_type_isnull_key_comment[m][2]
                                + " "
                                * (c - len(t_field_type_isnull_key_comment[m][2]) + 8)
                            )
                            l_isKey.append(
                                t_field_type_isnull_key_comment[m][3]
                                + " "
                                * (d - len(t_field_type_isnull_key_comment[m][3]) + 1)
                            )
                            l_comment.append(
                                t_field_type_isnull_key_comment[m][4]
                                + " "
                                * (e - len(t_field_type_isnull_key_comment[m][4]) + 1)
                            )
            else:
                # 所有字段
                for i in t_field_type_isnull_key_comment:
                    # print(i)
                    l_field.append(i['column_name'] + " " * (a - len(i['column_name']) + 1))
                    l_type.append(i['column_type'] + " " * (b - len(i['column_type']) + 1))
                    l_isnull.append(i['is_nullable'] + " " * (c - len(i['is_nullable']) + 8))
                    l_isKey.append(i['column_key'] + " " * (d - len(i['column_key']) + 1))
                    l_comment.append(i['column_comment'] + " " * (e - len(i['column_comment'])))

            # 只输出找到字段的表
            if len(l_field) != 0:
                print("- - " * 50)
                # print(t_table_comment)
                Color_PO.consoleColor(
                    "31",
                    "36",
                    "["
                    + t_table_comment[0]['table_name']
                    + " ("
                    + t_table_comment[0]['table_comment']
                    + ") - "
                    + str(len(t_field_type_isnull_key_comment))
                    + "个字段]",
                    "",
                )
                tmp = 1
                print(
                    "字段名" + " " * (a - 4),
                    "数据类型" + " " * (b - 6),
                    "允许空值" + " " * (c + 1),
                    "主键" + " " * (d - 2),
                    "字段说明",
                )
                for i in range(len(l_field)):
                    print(l_field[i], l_type[i], l_isnull[i], l_isKey[i], l_comment[i])

            l_field = []
            l_type = []
            l_isKey = []
            l_isnull = []
            l_comment = []
        else:
            Color_PO.consoleColor("31", "31", "[ERROR], 没有找到'" + varTable + "'表!]", "")

        return tmp

    def dbDesc(self, *args):
        """查看数据库表结构（字段、类型、DDL）
        第1个参数：表名或表头*（通配符*）
        第2个参数：字段名（区分大小写），指定查看的字段名，多个字段名用逗号分隔，不支持通配符*
        """

        if len(args) == 0:
            # 1, 所有表结构(ok)
            t_tables = self.execQuery(
                'SELECT TABLE_NAME FROM information_schema.`TABLES` WHERE table_type = "BASE TABLE" AND table_schema = "%s"'
                % self.db
            )
            # print(t_tables)
            for t in range(len(t_tables)):
                # print(t_tables[t])
                self._dbDesc_search(t_tables[t]['TABLE_NAME'])
            Color_PO.consoleColor(
                "31",
                "31",
                "\n结果：当前数据库（" + self.db + "）共有 " + str(len(t_tables)) + " 张表。 ",
                "",
            )

        elif len(args) == 1:
            varTable = args[0]
            if "%" not in varTable:
                # 2, 单表结构（ok）
                self._dbDesc_search(varTable)
            elif "%" in varTable:
                # 3, 带通配符表结构（ok）
                t_tables = self.execQuery(
                    'select table_name from information_schema.`TABLES` where table_type = "BASE TABLE" AND table_schema="%s" and table_name like "%s"'
                    % (self.db, varTable)
                )
                if len(t_tables) != 0:
                    for t in range(len(t_tables)):
                        self._dbDesc_search(t_tables[t][0])
                    Color_PO.consoleColor(
                        "31", "31", "\n结果：符合条件的有 " + str(len(t_tables)) + " 张表。 ", ""
                    )
                else:
                    Color_PO.consoleColor(
                        "31", "31", "[ERROR], 没有找到'" + str(varTable) + "'前缀的表!", ""
                    )

        elif len(args) == 2:
            varTable = args[0]
            var_l_field = args[1]
            temp1 = 0
            if varTable == "*":
                # 6, 所有表结构的可选字段(只输出找到字段的表)
                t_tables = self.execQuery(
                    'SELECT TABLE_NAME FROM information_schema.`TABLES` WHERE table_type = "BASE TABLE" AND table_schema = "%s"'
                    % self.db
                )
                for t in range(len(t_tables)):
                    temp = self._dbDesc_search(t_tables[t][0], var_l_field)
                    temp1 = temp1 + temp
                Color_PO.consoleColor(
                    "31", "31", "\n结果：符合条件的有 " + str(temp1) + " 张表。 ", ""
                )
            elif "%" not in varTable:
                # 4, 单表结构可选字段（ok）
                self._dbDesc_search(varTable, var_l_field)
            elif "%" in varTable:
                # 5, 带通配符表结构可选字段（ok）
                t_tables = self.execQuery(
                    'select table_name from information_schema.`TABLES` where table_type = "BASE TABLE" AND table_schema="%s" and table_name like "%s"'
                    % (self.db, varTable)
                )
                if len(t_tables) != 0:
                    for t in range(len(t_tables)):
                        temp = self._dbDesc_search(t_tables[t][0], var_l_field)
                        temp1 = temp1 + temp
                    Color_PO.consoleColor(
                        "31", "31", "\n结果：符合条件的有 " + str(temp1) + " 张表。 ", ""
                    )
                else:
                    Color_PO.consoleColor(
                        "31", "31", "[ERROR], 没有找到'" + str(varTable) + "'前缀的表!", ""
                    )

    def _dbRecord_search(self, varDB, varTable, varType, varValue, varMysqlKeywordFile):

        """dbRecord函数中子查询"""

        # mysql关键字和保留字，涉及的关键字将不处理 l_keyword = ['desc', 'limit', 'key', 'group', 'usage', 'read']

        l_keyword = ['desc', 'limit', 'key', 'group', 'usage', 'read']

        # Openpyxl_PO = OpenpyxlPO(varMysqlKeywordFile)
        # l_keyword = Openpyxl_PO.getColValueByCol([1], [])
        l_keyword = [str(i).lower() for i in l_keyword[0]]

        l_field = []
        l_fieldComment = []

        # 表注释
        t_comment = self.execQuery(
            'select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" '
            % (varDB, varTable)
        )
        # print(t_comment)  # (('系统用户详情信息表 ',),)

        # 字段，类型，字段注释
        t_field_type = self.execQuery(
            'select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" '
            % (varDB, varTable)
        )
        # print(t_field_type)  # (('userNo', 'varchar(50)'))

        # 过滤掉不符合类型的字段
        for j in t_field_type:
            # print(j)
            if varType in j['column_type']:
                l_field.append(j['column_name'])
                l_fieldComment.append(j['column_comment'])
        # print(l_field)  # ['userNo', 'userName', 'cardNo', 'email', 'mobile', 'shortName']
        # print(l_fieldComment)  # ['用户工号', '用户姓名', '证件号码', '邮箱', '手机号', '姓名首字母缩写（如张三：zs）']

        varSign = 0
        for i in range(len(l_field)):
            # 过滤mysql关键字
            for j in range(len(l_keyword)):
                if l_field[i] == l_keyword[j]:
                    varSign = 1

            if varSign == 0:
                t_record = self.execQuery(
                    'select * from `%s` where %s LIKE "%s" '
                    % (varTable, l_field[i], varValue)
                )
                if len(t_record) != 0:
                    print("- - " * 30)
                    # print(t_comment[0])
                    Color_PO.consoleColor(
                        "31",
                        "36",
                        self.db
                        + "."
                        + varTable
                        + "("
                        + str(t_comment[0]['table_comment'])
                        + ")."
                        + l_field[i]
                        + "("
                        + str(l_fieldComment[i])
                        + ")",
                        "",
                    )
                    Color_PO.consoleColor(
                        "31",
                        "36",
                        'select * from `%s` where %s LIKE "%s"'
                        % (varTable, l_field[i], varValue),
                        "",
                    )
                    for j in range(len(t_record)):
                        print(str(t_record[j]).encode("gbk", "ignore").decode("gbk"))
            else:
                print("- - " * 30)
                Color_PO.consoleColor(
                    "31",
                    "33",
                    "[warning, "
                    + self.db
                    + "."
                    + varTable
                    + "("
                    + str(t_comment[0][0])
                    + ")."
                    + l_field[i]
                    + "("
                    + str(l_fieldComment[i])
                    + ")是关键字, 忽略不处理!]",
                    "",
                )
                varSign = 0
        l_fields = []
        l_fieldComment = []

    def dbRecord(self, varTable, varType, varValue, varMysqlKeywordFile="D:\\51\\python\\project\\PO\\mysqlKeyword.xlsx"):
        """
        # 2, 搜索表记录
        # 参数1：varTable = 表名（*表示所有的表）
        # 参数2：varType = 数据类型(char,int,double,timestamp)
        # 参数3：varValue = 值 (支持%模糊查询，如 %yy%)
        """
        # dbRecord('*','char', u'%yoy%')  # 模糊搜索所有表中带yoy的char类型。
        # dbRecord('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
        # dbRecord('*','timestamp', u'%2019-01%')  # 模糊搜索所有表中带2019-01的timestamp类型。
        # dbRecord('myclass','char', 'yoyo')

        if varType in "float,money,int,nchar,nvarchar,datetime,timestamp":
            if "*" in varTable:
                t_tables = self.execQuery(
                    'SELECT TABLE_NAME FROM information_schema. TABLES WHERE table_type = "BASE TABLE" AND table_schema ="%s" '
                    % (self.db)
                )
                # print(t_tables)  # (('af_preoperative_counseling_detail',), ('af_preoperative_counseling_info',))

                if len(t_tables) != 0:
                    for t in range(len(t_tables)):
                        # print(t_tables[t])
                        self._dbRecord_search(
                            self.db,
                            t_tables[t]['TABLE_NAME'],
                            varType,
                            varValue,
                            varMysqlKeywordFile,
                        )
                else:
                    Color_PO.consoleColor(
                        "31",
                        "31",
                        "[ERROR], 没有找到 " + varTable.split("*")[0] + " 前缀的表!",
                        "",
                    )
            elif "*" not in varTable:
                self._dbRecord_search(
                    self.db, varTable, varType, varValue, varMysqlKeywordFile
                )

    def dbCreateDate(self, *args):

        """
        3，查表的创建时间及时间区间
        无参：查看所有表的创建时间
        一个参数：表名
        二个参数：第一个是时间前后，如 before指定日期之前创建、after指定日期之后创建，第二个是日期
        """
        # Mysql_PO.dbCreateDate()   # 查看所有表的创建时间
        # Mysql_PO.dbCreateDate('app_code')   # 查看book表创建时间
        # Mysql_PO.dbCreateDate('fact*')   # 查看所有b开头表的创建时间，通配符*
        # Mysql_PO.dbCreateDate('after', '2019-02-18')  # 查看所有在2019-02-18之后创建的表
        # Mysql_PO.dbCreateDate('>', '2019-02-18')  # 查看所有在2019-02-18之后创建的表
        # Mysql_PO.dbCreateDate('before', "2019-04-10")  # 显示所有在2019-12-08之前创建的表
        # Mysql_PO.dbCreateDate('<', "2019-02-18")  # 显示所有在2019-12-08之前创建的表
        if len(args) == 0:
            try:
                tbl = self.execQuery(
                    'select table_name,create_time from information_schema.`TABLES` where table_schema="%s"'
                    % (self.db)
                )
                print(
                    "\n当前数据库（"
                    + self.db
                    + "）中所有表（"
                    + str(len(tbl))
                    + "张）的创建时间"
                    + "\n"
                    + "-" * 60
                )
                for r in range(len(tbl)):
                    print(str(tbl[r][1]) + " => " + tbl[r][0])
                Color_PO.consoleColor(
                    "31",
                    "31",
                    "\n当前数据库（" + self.db + "）中所有表（" + str(len(tbl)) + "张）的创建时间。",
                    "",
                )

            except:
                print("[warning , 数据库为空!]")
        elif len(args) == 1:
            if "*" in args[0]:
                varTable = args[0].split("*")[0] + "%"  # t_store_%
                tbl = self.execQuery(
                    'select table_name,create_time from information_schema.`TABLES` where table_schema="%s" and table_name like "%s" '
                    % (self.db, varTable)
                )
                print("\n符合通配符条件（" + args[0] + "）表的创建时间" + "\n" + "-" * 60)
                for r in range(len(tbl)):
                    print(str(tbl[r][1]) + " => " + tbl[r][0])
                Color_PO.consoleColor(
                    "31", "31", "\n符合通配符条件（" + args[0] + "）表的创建时间" + "\n", ""
                )
            else:
                try:
                    tbl = self.execQuery(
                        'select create_time from information_schema.`TABLES` where table_schema="%s" and table_name="%s" '
                        % (self.db, args[0])
                    )
                    print("\n" + args[0] + " 表的创建时间" + "\n" + "-" * 60)
                    print(str(tbl[0]) + " => " + args[0])
                except:
                    # print("[warning , " + args[0] + "表不存在!]")
                    Color_PO.consoleColor(
                        "31", "31", "[warning], " + args[0] + " 表不存在!" + "\n", ""
                    )
        elif len(args) == 2:
            if args[0] == "after" or args[0] == ">":
                tbl = self.execQuery(
                    'select table_name,create_time from information_schema.`TABLES` where table_schema="%s" and create_time>"%s"'
                    % (self.db, args[1])
                )
                print(
                    "\n"
                    + str(args[1])
                    + " 之后创建的表共有 "
                    + str(len(tbl))
                    + " 张\n"
                    + "-" * 60
                )
                for r in range(len(tbl)):
                    print(str(tbl[r][1]) + " => " + tbl[r][0])
                Color_PO.consoleColor(
                    "31",
                    "31",
                    "\n" + str(args[1]) + " 之后创建的表共有 " + str(len(tbl)) + " 张\n",
                    "",
                )

            elif args[0] == "before" or args[0] == "<":
                tbl = self.execQuery(
                    'select table_name,create_time from information_schema.`TABLES` where table_schema="%s" and create_time<"%s"'
                    % (self.db, args[1])
                )
                print(
                    "\n"
                    + str(args[1])
                    + " 之前创建的表共有 "
                    + str(len(tbl))
                    + " 张\n"
                    + "-" * 60
                )
                for r in range(len(tbl)):
                    print(str(tbl[r][1]) + " => " + (tbl[r][0]))
                Color_PO.consoleColor(
                    "31",
                    "31",
                    "\n" + str(args[1]) + " 之前创建的表共有 " + str(len(tbl)) + " 张\n",
                    "",
                )

            else:
                print("[errorrrrrrr , 参数1必须是 after 或 before ]")
        else:
            print("[errorrrrrrr , 参数溢出！]")


    def db2csv(self, varSql, varCSV, index=True):

        """
        4.1，数据库sql导出csv
        # Mysql_PO.db2csv("select * from sys_menu", "d:\\111.csv")
        """

        df = pd.read_sql(sql=varSql, con=self.getEngine_pymysql())
        df.to_csv(varCSV, encoding="gbk", index=index)

    def db2xlsx(self, varSql, varXlsx, index=True):

        """
        4.2，数据库sql导出excel
        # Mysql_PO.db2xlsx("select * from sys_menu", "d:\\111.xlsx")
        """

        df = pd.read_sql(sql=varSql, con=self.getEngine_pymysql())
        df.to_excel(varXlsx, index=index)

    def db2dict(self, varSql, orient='list'):

        """4.3 数据库sql导出字典"""

        try:
            # df = pd.read_sql(sql=varSql, con=self.getEngine_pymysql())
            engine = self.getEngine_pymysql()
            df = pd.read_sql(text(varSql), con=engine.connect())
            return df.to_dict(orient=orient)
        except Exception as e:
            print(e)

    def db2html(self, sql, htmlFile, index=True):

        """
        4.4，数据库sql导出html
                # Mysql_PO.db2html("select * from sys_menu", "d:\\index1.html")
                参考：https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_html.html
                css加载，https://blog.csdn.net/qq_38316655/article/details/104663077
                颜色，https://www.jianshu.com/p/946481cd288a
                https://www.jianshu.com/p/946481cd288a
        """

        df = pd.read_sql(sql=sql, con=self.getEngine_pymysql())
        df.to_html(htmlFile, col_space=100, na_rep="0", index=index)

    def db2df(self, sql):

        # 4.5 数据库sql导出DataFrame
        # db2df("select * from a_test")

        l_d_data = self.execQuery(sql)
        # print(l_d_data)  # [{'id': 1, 'name': 'John Smith2', 'salesrep': 'John Doe3'}, {'id': 2, 'name': 'Jane Doe', 'salesrep': 'Joe Dog'},...
        # print(l_d_data[0])
        # print(list(l_d_data[0].keys()))
        df = pd.DataFrame(l_d_data, columns=list(l_d_data[0].keys()))
        # df.to_string(index=False)
        return df


    def dbDesc2xlsx(self, varFileName):

        """
        4.4，将数据库表结构导出excel
        """

        listSub = []
        listMain = []
        dict1 = {}
        tblName = self.execQuery(
            'select TABLE_NAME,TABLE_COMMENT from information_schema.`TABLES` where table_schema="%s" '
            % self.db
        )
        # print(tblName)
        listSub.append("表名")
        listSub.append("表说明")
        listSub.append("名称")
        listSub.append("数据类型(长度)")
        listSub.append("允许空值")
        listSub.append("主键")
        listSub.append("默认值")
        listSub.append("说明")
        dict1[1] = listSub
        for k in range(len(tblName)):
            tblFields = self.execQuery(
                'select column_name,column_type,is_nullable,column_key,column_default,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" '
                % (self.db, tblName[k][0])
            )
            for i in range(len(tblFields)):
                list3 = list(tblName[k]) + list(tblFields[i])
                listMain.append(list3)
        for i in range(len(listMain)):
            dict1[i + 2] = listMain[i]
        NewexcelPO(varFileName)
        Openpyxl_PO = OpenpyxlPO(varFileName)
        Openpyxl_PO.setRowValue(dict1)
        Openpyxl_PO.save()

    def db2html(self, varTitle, varTable, varFile, index=True):

        """
        4.5 将数据库表导出html
        # db2html("erp_开发计划总揽_","2022-11-12","12345")
        # db2html("erp_开发计划总揽_",str(Time_PO.getDateTime()),"12345")
        """

        df = pd.read_sql(
            sql="select * from `%s`" % varTable, con=self.getEngine_pymysql()
        )
        pd.set_option("colheader_justify", "center")  # 对其方式居中
        html = (
            """<html><head><title>"""
            + varTitle
            + """</title></head>
        <body><b><caption>"""
            + varTitle
            + """</caption></b><br><br>{table}</body></html>"""
        )
        style = """<style>.mystyle {font-size: 11pt; font-family: Arial;    border-collapse: collapse;     border: 1px solid silver;}.mystyle td, th {    padding: 5px;}.mystyle tr:nth-child(even) {    background: #E0E0E0;}.mystyle tr:hover {    background: silver;    cursor: pointer;}</style>"""

        # File_PO.createFolder("report")
        with open(varFile, "w") as f:
            f.write(
                style
                + html.format(
                    table=df.to_html(classes="mystyle", col_space=100, index=index)
                )
            )

        # # 优化report.html, 去掉None、修改颜色
        # html_text = BeautifulSoup(open(rptNameDate), features='html.parser')
        # tf = open(rptNameDate, 'w', encoding='utf-8')
        # tf.write(str(html_text))
        # tf.close()



    def getTableField(self, varTable):

        """5, 获取单个表的所有字段"""
        # Mysql_PO.getTableField('HrCover')

        l_field = []
        try:
            t_table = self.execQuery(
                'select column_name from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" '
                % (self.db, varTable)
            )

            for i in range(len(t_table)):
                l_field.append(t_table[i][0])
            return l_field

        except Exception as e:
            print(e)
            # print(e, ",很抱歉，出现异常您搜索的<" + varTable + ">不存在！")

    def explainSingle(self, sql):

        # 6 expain SQL语句的执行计划

        execExplain = "explain " + sql
        db_result = self.execQuery(execExplain)
        print(execExplain)
        print(
            "(id, selecrt_type, table, partitions, type, possible_keys, key, key_len, ref, rows, filtered, Extra)"
        )
        for i in range(len(db_result)):
            print(db_result[i])


    def explainMore(self, varFile, varSheet, getCol, varCol, varRow):

        # 6 expain SQL语句的执行计划

        Openpyxl_PO = OpenpyxlPO(varFile)
        x = Openpyxl_PO.getColValueByCol([getCol], [], varSheet)
        l_sql = x[0][1:]
        print(l_sql)
        for i in range(len(l_sql)):
            if l_sql[i] != None:
                execExplain = "explain " + str(l_sql[i])
                if "select " in execExplain:
                    db_result = self.execQuery(execExplain)
                    print(execExplain)
                    print(
                        "(id, selecrt_type, table, partitions, type, possible_keys, key, key_len, ref, rows, filtered, Extra)"
                    )
                    for j in range(len(db_result)):
                        print(db_result[j])
                        Openpyxl_PO.setCellValue(
                            i + varRow, j + varCol, str(db_result[j])
                        )
                    print("\n")
        Openpyxl_PO.save()

    def getKeyword(self, xlsxFile):

        # 7 获取mysql关键字列表
        Openpyxl_PO = OpenpyxlPO(xlsxFile)
        x = Openpyxl_PO.getColValueByCol([1], [])
        return x


    def xlsx2db(self, varPathFile, varDbTable, varSheetName=0):

        '''
        5.1，xlsx导入数据库
        xlsx2db('2.xlsx', "tableName", "sheet1")
        excel表格第一行数据对应db表中字段，建议用英文
        '''

        try:
            df = pd.read_excel(varPathFile, sheet_name=varSheetName)
            engine = self.getEngine_pymysql()
            df.to_sql(varDbTable, con=engine, if_exists="replace", index=False)
        except Exception as e:
            print(e)

    def dict2db(self, varDict, varDbTable, index="True"):

        """5.2 字典导入数据库"""

        try:
            df = pd.DataFrame(varDict)
            engine = self.getEngine_pymysql()
            if index == "False":
                df.to_sql(name=varDbTable, con=engine, if_exists="replace", index=False)
            else:
                df.to_sql(name=varDbTable, con=engine, if_exists="replace")
        except Exception as e:
            print(e)

    def list2db(self, l_col, l_value, varDbTable, index="True"):

        """5.3 列表导入数据库
        l_col = 列名，如 ['id','name','age']
        l_value= 值,如 [['1','john','44],['2','ti','4']]
        """

        try:
            df = pd.DataFrame(l_value, columns=l_col)
            engine = self.getEngine_pymysql()
            if index == "False":
                df.to_sql(name=varDbTable, con=engine, if_exists="replace", index=False)
            else:
                df.to_sql(name=varDbTable, con=engine, if_exists="replace")
        except Exception as e:
            print(e)

    def df2db(self, varDF, varDbTable):

        '''5.4，dataframe导入数据库'''

        try:
            engine = self.getEngine_pymysql()
            varDF.to_sql(varDbTable, con=engine, if_exists="replace", index=False)
        except Exception as e:
            print(e)


if __name__ == "__main__":


    # docker mysql ————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # Mysql_PO = MysqlPO("127.0.0.1", "root", "root", "test", 3306)

    # # 创建users表，没有设置id主键
    # Mysql_PO.execute("CREATE TABLE users(id int not null,name varchar(10),age int(4))")
    # # 在users表上，创建id主键
    # Mysql_PO.execute("alter table users add primary key(id)")
    #
    # # 创建teacher表，设置id主键
    # Mysql_PO.execute("CREATE TABLE teather(id int auto_increment primary key, name varchar(10),age int(4))")

    # # 删除teacher表的id主键(需要注意的是主键如果设置了自动递增，需要先将自动递增去掉，再删除主键。)
    # Mysql_PO.execute("alter table teather change id id int not null")  # 取消id的自动递增
    # Mysql_PO.execute("alter table teather DROP PRIMARY KEY")  # 取消所有主键


    # # 创建haha表，如果不存在的话。
    # Mysql_PO.execute("CREATE TABLE if not exists haha(id int auto_increment primary key, name varchar(10),age int(4))")

    # Mysql_PO.execute("INSERT INTO haha (name, age) VALUES ('john', 12)")


    # t_userNo = Mysql_PO.execQuery('select * from sys_user_detail where userNo="%s"' % ("16766667777"))
    # print(t_userNo)
    # print(t_userNo[0][0])  # 278
    #
    # t_userNo = Mysql_PO.execQuery('select * from sys_user_detail where id="%s"' % ("277"))
    # print(t_userNo)
    #
    # Mysql_PO.close()

    # # # 238 erp (测试) ————————————————————————————————————————————————————————————————————————————————————————————————————————————
    Mysql_PO = MysqlPO("192.168.0.234", "root", "Zy_123456", "crm", 3306)


    # Mysql_PO = MysqlPO("192.168.0.234", "root", "Zy123456", "crmtest", 3306)
    # # crm小程序清空账号权限
    # # Mysql_PO.execQuery("update user SET VX_MARK='', IMEI='', MODEL='',PLATFORM='', NOT_LOGIN=0, LIMIT_LOGIN=0 ")
    # l_result = Mysql_PO.execQuery('select USER_NAME from user where USER_PRIV_NO=%s ' % (999))
    # print(l_result)  # (('测试',), ('系统管理员',))
    # print(l_result[0][0])  # 测试


    # *****************************************************************************************************************************
    # *****************************************************************************************************************************

    # print("1 查看数据库表结构（字段名、数据类型、主键、允许空值、字段说明）".center(100, "-"))
    # Mysql_PO.dbDesc()  # 1，所有表结构
    # Mysql_PO.dbDesc('sys_user_detail')  # 2，单表结构
    # Mysql_PO.dbDesc('sys_user_%')  # 3，带通配符表结构
    # Mysql_PO.dbDesc('sys_user_detail', ['id', 'sex', 'title'])  # 4,单表结构的可选字段
    # Mysql_PO.dbDesc('sys_user_%', ['id'])  # 5，带通配符表结构的可选字段(只输出找到字段的表)
    # Mysql_PO.dbDesc("*", ['sex', 'title', 'org_name'])  # 6，所有表结构的可选字段(只输出找到字段的表)

    # print("2，搜索表记录".center(100, "-"))
    # Mysql_PO.dbRecord('sys_user_detail', 'varchar', '16766667777')
    # Mysql_PO.dbRecord('sys_user_detail', 'varchar', '1676666%')
    # Mysql_PO.dbRecord('*', 'varchar', '16766667%')
    # Mysql_PO.dbRecord('sys_user', 'char', '%金%')  # 搜索user表中内容包含金丽娜的char类型记录。
    # Mysql_PO.dbRecord('*', 'varchar', u'%招远疫情防控公告123456%')   # 搜索所有表中带金丽娜的char类型记录。
    # Mysql_PO.dbRecord('*', 'datetime', '2010%')  # 模糊搜索所有表中日期类型为datetime的2019-04-12 15:13:23记录。
    # Mysql_PO.dbRecord('sys_user_detail', 'datetime', '2015-04-13%')  # 模糊搜索所有表中日期类型为datetime的2019-04-12 15:13:23记录。

    # print("3，查表的创建时间及时间区间".center(100, "-"))
    # Mysql_PO.dbCreateDate()   # 查看所有表的创建时间
    # Mysql_PO.dbCreateDate('test1')   # 查看book表创建时间
    # Mysql_PO.dbCreateDate('task*')   # 查看所有b开头表的创建时间，通配符*
    # Mysql_PO.dbCreateDate('after', '2022-10-1')  # 查看所有在2019-02-18之后创建的表
    # Mysql_PO.dbCreateDate('>', '2021-11-14')  # 查看所有在2019-02-18之后创建的表
    # Mysql_PO.dbCreateDate('before', "2022-10-1")  # 显示所有在2019-12-08之前创建的表
    # Mysql_PO.dbCreateDate('<', "2021-11-14")  # 显示所有在2019-12-08之前创建的表



    # print("4.1 数据库sql导出csv".center(100, "-"))
    # Mysql_PO.db2csv("select * from sys_area", "d:\\sys_user_detail.csv")
    # Mysql_PO.db2csv("select * from sys_area", "d:\\sys_user_detail.cav", False)

    # print("4.2 数据库sql导出excel".center(100, "-"))
    # Mysql_PO.db2xlsx("select * from sys_area", "d:\\sys_area.xlsx")
    # Mysql_PO.db2xlsx("select * from sys_area", "d:\\sys_area.xlsx", False)

    # print("4.3 数据库sql导出字典".center(100, "-"))
    # d = Mysql_PO.db2dict("select * from user where UID=81")
    # print(d)  # {'UID': [81], 'USER_ID': ['81'], 'USER_NAME': ['钮学彬'], 'USER_NAME_INDEX'...

    # print("4.4 数据库sql导出html".center(100, "-"))
    # Mysql_PO.db2html("select * from sys_area", "d:\\sys_user_detail.html")
    # Mysql_PO.db2html("select * from sys_area", "d:\\sys_user_detail.html", False)

    # print("4.5 数据库sql导出DataFrame".center(100, "-"))
    # df = Mysql_PO.db2df("select * from test99")
    # print(df)


    # print("5.1 excel导入数据库".center(100, "-"))
    # Mysql_PO.xlsx2db("hello1.xlsx", 'hello123')

    # print("5.2 字典导入数据库".center(100, "-"))
    # Mysql_PO.dict2db({'A': [3, 4, 8, 9], 'B': [1.2, 2.4, 4.5, 7.3], 'C': ["aa", "bb", "cc", "dd"]}, "test99")  # 带index
    # Mysql_PO.dict2db({'A': [3, 4, 8, 9], 'B': [1.2, 2.4, 4.5, 7.3], 'C': ["aa", "bb", "cc", "dd"]}, "test99", "False")  # 不带index

    # print("5.3 列表导入数据库".center(100, "-"))
    # Mysql_PO.list2db(['name','age','sex'], [['1','2','3'],['a','b','c']], "test99")  # 生成index
    # Mysql_PO.list2db(['name','age','sex'], [['1','2','3'],['a','b','c']], "test99", "False")  # 不生成index

    # print("5.4 DataFrame导入数据库".center(100, "-"))
    # df = Mysql_PO.db2df("select * from test99")
    # print(df)
    # Mysql_PO.df2db(df, "a_test1")




    # print("4.4 将数据库表查询结果导出htmll".center(100, "-"))
    # Mysql_PO.dbDesc2xlsx("d:\\crmtest.xlsx")
    # Mysql_PO.dbDesc2xlsx("/Users/linghuchong/Desktop/mac/sassDesc.xlsx")

    # print("4.5 将数据库表导出html".center(100, "-"))
    # Mysql_PO.db2html("erp_开发计划总揽_2022-11-12", "sys_area", "d://123.html")
    # Mysql_PO.db2html("erp_开发计划总揽_2022-11-12", "sys_area", "d://123.html",False)
    # Mysql_PO.db2html("erp_开发计划总揽_2022-11-12", "sys_area", "d://11/123.html", False)



    # print("4.4 excel导入数据库表".center(100, "-"))
    # Mysql_PO.xlsx2db("data/testcase2.xlsx", "testcase2", sheet_name="case")
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", usecols=eval("range(4)"), nrows=6, dtype={'No.': str, '金额': float},parse_dates=['isRun'], date_parser=lambda x: pd.to_datetime(x, format='%Y%m'))  # 读取表格中前3列、前6行数据写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", usecols=eval("range(4)"), nrows=6, converters={'isRun': lambda x: pd.to_datetime(x, format='%Y%m')})  # 读取表格中前3列、前6行数据写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", eval("range(3)"), 6, skiprows=range(1, 100, 2), sheet_name="case")  # 读取表格中前3列、前6行数据写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", eval("range(3)"), 6, range(1, 100, 2))  # 读取表格中前3列、前6行数据写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", "A,C,E", None)  # 读取表格中A,C,E3列数据写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", "A:F", None)  # 读取表格中A-F 列数据写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", [0,3,4,5], None)  # 读取表格中4列数据写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", ['interURL','一级属性'], None)  # 读取表格中['interURL','一级属性']列数据写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", lambda x: x in ['班级', 'interURL', '语文'], None)  # 读取表格中符合（存在）['班级', 'interURL', '语文']列数据，并写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", lambda x: x in ['班级', 'interURL', '语文'], None, sheet_name="case")  # 读取表格中符合（存在）['班级', 'interURL', '语文']列数据，并写入数据库表

    # print("5 将所有表结构导出到excel(覆盖)".center(100, "-"))
    # print(Mysql_PO.getTableField('test_interface'))

    # print("6 expain SQL语句的执行计划".center(100, "-"))
    # Mysql_PO.explainSingle("select sum(双A客户实际拜访人数) from(SELECT count(DISTINCT customer_id) 双A客户实际拜访人数 from t_visit WHERE user_id=84 and double_a_mark=1 and state=3 and valid_status=1 and created_at>='2022-06-01' and  created_at<='2022-06-30 23:59:59' GROUP BY  customer_id  HAVING(count(*)>=6))双A客户实际拜访人数")

    # print("6.2 expain SQL语句的执行计划文件".center(100, "-"))
    # Mysql_PO.explainMore("./data/i_erp_reportField_case.xlsx", "拜访分析报表", 4, 5, 2)

