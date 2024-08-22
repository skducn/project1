# -- coding: utf-8 --
# ***************************************************************
# Author     : John
# Data       : 2019-04-16
# Description: DmPO 对象层  达梦dmPython
# https://blog.csdn.net/qqQi_/article/details/133064594
# pip install SQLAplchemy==1.3.23
# cd\ c:\dmdbms\drivers\python\sqlalchemy
# python setup.py install
# ***************************************************************

import dmPython
from sqlalchemy import create_engine

from PO.ColorPO import *
Color_PO = ColorPO()

from PO.TimePO import *
Time_PO = TimePO()

class DmPO:

    def __init__(self, server, user, password, port):
        self.server = server
        self.user = user
        self.password = password
        self.port = str(port)
        self.conn = dmPython.connect(server=server, user=user, password=password, port=self.port)
        self.cur = self.conn.cursor()
        if not self.cur:
            raise (NameError, "error，创建游标失败！")


    def execute(self, sql):

        '''
        执行sql （insert，update）
        :param sql:
        :return:
        '''

        try:
            # self.conn.commit()
            self.cur.execute(sql)
            self.conn.commit()
            return "ok"
        except Exception as e:
            return str(e)

    def execQuery(self, sql):

        '''
        查询sql
        :param sql:
        :return:
        '''

        try:
            self.cur.execute(sql)
            result = self.cur.fetchall()
            return result
        except Exception as e:
            # print(e.args)  # ('table hh already exists',)
            # print(str(e))  # table hh already exists
            # print(NameError(e))  # table hh already exists
            print(repr(e))  # OperationalError('table hh already exists')

    def close(self):
        self.cur.close()
        self.conn.close()



    def xlsx2db(self, varPathFile, varSheetName, varTableName):

        '''
        5，xlsx导入数据库
        :param varExcelFile:
        :param varTable:
        :return:
        xlsx2db('./data/2.xlsx',"sheet3", "jh123")
        excel表格第一行数据对应db表中字段，建议用英文
        '''


        df = pd.read_excel(varPathFile, sheet_name=varSheetName)
        engine = create_engine("dm+dmPython://" + self.user + ":" + self.password + "@" + self.server + ":" + self.port)
        df.to_sql(varTableName, con=engine, if_exists="replace", index=False)


    # 2.1.1 获取所有表
    def getTables(self):

        '''
        获取所有表
        :return:
        '''

        try:
            r = self.execQuery("SELECT DISTINCT d.name FROM syscolumns a LEFT JOIN systypes b ON a.xusertype= b.xusertype INNER JOIN sysobjects d ON a.id= d.id AND d.xtype= 'U' AND d.name<> 'dtproperties' LEFT JOIN syscomments e ON a.cdefault= e.id LEFT JOIN sys.extended_properties g ON a.id= G.major_id AND a.colid= g.minor_id LEFT JOIN sys.extended_properties f ON d.id= f.major_id AND f.minor_id= 0")
            # print(r)  # [{'name': 'EMR_ADMISSION_ASSESSMENT'}, {'name': 'EMR_ADMISSION_DEAD_RECORD_TF'},...]
            l_tables = []
            for i in range(len(r)):
                l_tables.append(r[i]['name'])
            return l_tables
        except Exception as e:
            print(e, ",[error], SqlserverPO.getTables()异常!")
            self.conn.close()

    # 2.1.2 获取所有表和表注释
    def getTableAndComment(self):

        '''
        获取所有表和表注释
        :return:
        '''

        try:
            r = self.execQuery("SELECT DISTINCT d.name,f.value FROM syscolumns a LEFT JOIN systypes b ON a.xusertype= b.xusertype INNER JOIN sysobjects d ON a.id= d.id AND d.xtype= 'U' AND d.name<> 'dtproperties' LEFT JOIN syscomments e ON a.cdefault= e.id LEFT JOIN sys.extended_properties g ON a.id= G.major_id AND a.colid= g.minor_id LEFT JOIN sys.extended_properties f ON d.id= f.major_id AND f.minor_id= 0")
            # print(r)  # [{'name': 'aaa', 'value': None}, {'name': 'bbb', 'value': None}...]
            l_table = []
            l_comment = []
            d = {}
            for i in range(len(r)):
                l_table.append(r[i]['name'])
                if r[i]['value'] == None:
                    l_comment.append(r[i]['value'])
                else:
                    l_comment.append(r[i]['value'].decode(encoding="utf-8", errors="strict"))
            d = dict(zip(l_table, l_comment))
            # print(d)
            return d
        except Exception as e:
            print(e, ",[error], SqlserverPO.getTableAndComment()异常!")
            self.conn.close()

    # 2.1.3 获取表的结构信息
    def getTableInfor(self, varTable="allTables"):

        '''
        获取表的结构信息 (查询表的列名称、说明、备注、类型等)
        :param varTable: 如果有表名就获取一个表的信息，否则所有表的信息
        :return:
        其他用法：将如下查询内容，在navicate中执行，并导出excel文档。
        '''

        if varTable == "allTables":

            r = self.execQuery('''
            SELECT 表名 = case when a.colorder = 1 then d.name else '' end,
              表说明 = case when a.colorder = 1 then isnull(f.value, '') else '' end,
              字段序号 = a.colorder,
              字段名 = a.name,
              标识 = case when COLUMNPROPERTY(a.id, a.name, 'IsIdentity')= 1 then '√' else '' end,
              主键 = case when exists(SELECT 1 FROM sysobjects where xtype = 'PK' and parent_obj = a.id and name in (SELECT name FROM sysindexes WHERE indid in(SELECT indid FROM sysindexkeys WHERE id = a.id AND colid = a.colid))) then '√' else '' end,
              类型 = b.name,
              占用字节数 = a.length,
              长度 = COLUMNPROPERTY(a.id, a.name, 'PRECISION'),
              小数位数 = isnull(COLUMNPROPERTY(a.id, a.name, 'Scale'),0),
              允许空 = case when a.isnullable = 1 then '√' else '' end,
              默认值 = isnull(e.text, ''),
              字段说明 = isnull(g.[value], '')
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
            r = self.execQuery('''
            SELECT 表名 = case when a.colorder = 1 then d.name else '' end,
              表说明 = case when a.colorder = 1 then isnull(f.value, '') else '' end,
              字段序号 = a.colorder,
              字段名 = a.name,
              标识 = case when COLUMNPROPERTY(a.id, a.name, 'IsIdentity')= 1 then '√' else '' end,
              主键 = case when exists(SELECT 1 FROM sysobjects where xtype = 'PK' and parent_obj = a.id and name in (SELECT name FROM sysindexes WHERE indid in(SELECT indid FROM sysindexkeys WHERE id = a.id AND colid = a.colid))) then '√' else '' end,
              类型 = b.name,
              占用字节数 = a.length,
              长度 = COLUMNPROPERTY(a.id, a.name, 'PRECISION'),
              小数位数 = isnull(COLUMNPROPERTY(a.id, a.name, 'Scale'),0),
              允许空 = case when a.isnullable = 1 then '√' else '' end,
              默认值 = isnull(e.text, ''),
              字段说明 = isnull(g.[value], '')
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

        return r

    # 2.2.1 获取字段
    def getFields(self, varTable):

        '''
        获取字段
        :param varTable:
        :return:
        '''

        try:
            r = self.execQuery(
                "SELECT B.name as name FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'"
                % (varTable)
            )
            # print(r)  # [{'name': 'CF_XM'}, {'name': 'CF_FMKS'},...]
            l_fields = []
            for i in range(len(r)):
                l_fields.append(r[i]['name'])
            return l_fields
        except Exception as e:
            print(e, ",[error], SqlserverPO.getFields()异常!")
            self.conn.close()

    # 2.2.2 获取字段和字段注释
    def getFieldAndComment(self, varTable):

        '''
        获取字段和字段注释
        :param varTable:
        :return:
        '''

        try:
            r = self.execQuery(
                "SELECT B.name as name, C.value as comment FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'"
                % (varTable)
            )
            # print(r)  # [{'name': 'GHRQ', 'comment': b'\xe6\x8c\x8...]
            l_field = []
            l_comment = []
            d = {}
            for i in range(len(r)):
                l_field.append(r[i]['name'])
                if r[i]['comment'] == None:
                    l_comment.append(r[i]['comment'])
                else:
                    l_comment.append(r[i]['comment'].decode(encoding="utf-8", errors="strict"))
            d = dict(zip(l_field, l_comment))
            return d
        except Exception as e:
            print(e, ",[error], SqlserverPO.getFields()异常!")
            self.conn.close()


    # 2.3 获取记录数
    def getRecordQty(self, varTable):

        '''
        获取记录数（特别适合大数据）
        :param varTable:
        :return:
        '''

        qty = self.execQuery(
            "SELECT rows FROM sysindexes WHERE id = OBJECT_ID('" + varTable + "') AND indid < 2")
        return qty[0]['rows']

    # 2.4.1 获取所有字段和类型
    def getFieldAndType(self, varTable):

        '''
        获取字段和类型
        :param varTable:
        :return:
        '''

        d_fields = {}
        result = self.execQuery(
            "SELECT A.name as tableName, B.name as Name, d.name as Type, B.max_length as Size, B.is_nullable as NotNull, C.value as Comment FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s' order by B.column_id asc"
            % (varTable)
        )
        # print(result) # [{'tableName': 'aaa', 'Name': 'ID', 'Type': 'int', 'Size': 4, 'NotNull': False, 'Comment': None},...]
        try:
            for i in result:
                 d_fields[str(i['Name'])] = str(i['Type'])
        except Exception as e:
            raise e
        return d_fields

    # 2.4.2 获取N个字段和类型
    def getMoreFieldAndType(self, varTable, l_field):

        '''
        获取单个字段和类型
        :param varTable:
        :param varField:
        :return:
        '''

        d_result = self.getFieldAndType(varTable)
        # print(d_result) # {'ID': 'int', 'NAME': 'text', 'AGE': 'int', 'ADDRESS': 'char', 'SALARY': 'float'}

        list1 = []
        d = {}
        for k, v in d_result.items():
            for j in range(len(l_field)):
                if k == l_field[j]:
                    d[k] = v
        return d  # [{'field': 'ID', 'type': 'int'}, {'field': 'AGE', 'type': 'int'}]

    # 2.4.3 获取所有必填项字段和类型
    def getNotNullFieldAndType(self, varTable):

        '''
        获取必填项字段和类型
        :param varTable:
        :return:
        '''

        d_fields = {}
        result = self.execQuery(
            "SELECT A.name as tableName, B.name as Name, d.name as Type, B.max_length as Size, B.is_nullable as NotNull, C.value as Comment FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s' order by B.column_id asc"
            % (varTable)
        )
        try:
            for i in result:
                if i['NotNull'] == False :
                    d_fields[str(i['Name'])] = str(i['Type'])
        except Exception as e:
            raise e
        return d_fields  # {'ID': 'int', 'NAME': 'text', 'AGE': 'int', 'ADDRESS': 'char'}

    # 2.5 获取自增主键
    def getIdentityPrimaryKey(self, varTable):

        '''
        获取自增主键
        :param varTable:
        :return:
        '''

        l_field = self.execQuery("select * from sys.identity_columns where [object_id]= OBJECT_ID('" + varTable + "')")
        # print(l_field)
        if l_field != []:
            return (l_field[0]['name'])  # id
        else:
            return None

    # 2.6 获取主键
    def getPrimaryKey(self, varTable):

        '''
        获取主键
        :param varTable:
        :return:
        '''

        l_primaryKey = self.execQuery("SELECT COLUMN_NAME FROM information_schema.key_column_usage where table_name='" + varTable + "'")
        # print(l_primaryKey)  # [{'COLUMN_NAME': 'ADDRESS'}, {'COLUMN_NAME': 'ID'}]
        if l_primaryKey == [] :
            return None
        else:
            return l_primaryKey

    # 2.7 获取主键最大值
    def getPrimaryKeyMaxValue(self, varTable):

        '''
        获取表主键最大值
        :param varTable:
        :return:
        '''

        # 判断表中是否有记录
        varQty = self.getRecordQty(varTable)
        if varQty != 0 :
            # 判断是否有主键
            l_primaryKey = self.getPrimaryKey(varTable)
            if l_primaryKey != None:
                # 当有一个主键时，
                # print(l_primaryKey)  # [{'COLUMN_NAME': 'id'}]
                if len(l_primaryKey) == 1 :
                    d = {}
                    # print(l_primaryKey[0]['COLUMN_NAME'])  # id
                    maxValue = self.execQuery("select max(" + str(l_primaryKey[0]['COLUMN_NAME']) + ") as name from " + varTable)
                    d[l_primaryKey[0]['COLUMN_NAME']] = maxValue[0]['name']
                    return (d)  # {'ID': 1}
                else:
                    # 多个主键
                    pass
                    # print(l_primaryKey)  # [{'name': 'ID'}, {'name': 'ADDRESS'}]  //1个主键



    # 3.1 创建表
    def crtTable(self, varTable, sql):

        '''
        创建表
        :param sql: 
        :return: 
        '''

        # 判断表是否存在
        if self.isTable(varTable) == False:
            try:
                c_cur = self.conn.cursor()
                c_cur.execute(sql)
                print("[ok], 表<" + varTable + "> 创建成功")
            except Exception as e:
                print("表创建失败")
                # print(f"表创建失败，失败信息为:{e}")
        else:
            print("[warning], 创建<" + str(varTable) + ">表失败，表已存在！")

    # 3.2.1 生成类型值
    def _genTypeValue(self, varTable):

        '''
        初始化对应类型的值
        :param varTable:
        :return:
        '''

        # 获取所有字段和类型
        d = self.getFieldAndType(varTable)
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

    # 3.2.2 生成必填项类型值
    def _genNotNullTypeValue(self, varTable):

        '''
        生成必填项类型值
        :param varTable:
        :return:
        '''
        # 获取所有字段和类型
        d = self.getNotNullFieldAndType(varTable)
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


    # 3.2.3 单表自动生成第一条数据
    def genFirstRecord(self, varTable):

        '''
        自动生成第一条数据
        :param varTable:
        :return:
        '''

        # 判断表是否存在
        if self.isTable(varTable) == True:
            # 判断是否有记录
            qty = self.getRecordQty(varTable)
            if qty == 0:

                print(varTable)

                # 获取生成类型值
                d_init = self._genTypeValue(varTable)
                # print(d_init)
                # 执行insert
                self._execInsert(varTable, d_init,{})



                return True
            else:
                return False

    # 3.2.3(2)所有表自动生成第一条数据
    def genFirstRecordByAll(self):

        '''
        所有表自动生成第一条数据
        :return:
        '''
        r = self.getTables()
        # print(r)
        for i in range(len(r)):
            self.genFirstRecord(r[i])


    # 3.2.4 自动生成数据
    def genRecord(self, varTable, d_field={}):

        '''
        自动生成数据
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

    # 3.2.5 自动生成必填项数据
    def genRecordByNotNull(self, varTable):

        '''
        自动生成必填项数据（非必填项忽略）
        :param varTbl:
        :return:
        '''

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
                self._execInsert(varTable, d_init,{})

    # 3.2.6 执行insert
    def _execInsert(self, varTable, d_init, d_field):

        '''
        执行insert
        :param varTable:
        :param d_init:
        :return:
        '''

        if d_field != {}:
            for k, v in d_field.items():
                for k1, v1 in d_init.items():
                    if k == k1 :
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
        qty = self.execQuery("Select OBJECTPROPERTY(OBJECT_ID('" + varTable + "'),'TableHasIdentity') as qty")
        if qty[0]['qty'] == 1:
            self.execute('set identity_insert ' + str(varTable) + ' on')
            sql = "INSERT INTO " + str(varTable) + " (" + s + ") VALUES (" + u + ")"
            self.execute(varTable, sql)
            self.conn.commit()
            print("[ok], " + str(sql))
            self.execute('set identity_insert ' + str(varTable) + ' off')
        else:
            if 'None' in u :
                u = u.replace(",'None',", ",null,")
                sql = "INSERT INTO " + str(varTable) + " (" + s + ") VALUES (" + u + ")"
            else:

                sql = "INSERT INTO " + str(varTable) + " (" + s + ") VALUES (" + u + ")"
            self.execute(varTable, sql)
            self.conn.commit()
            print("[ok], " + str(sql))



    # 4.1 判断表是否存在
    def isTable(self, varTable):

        '''
        判断表是否存在
        :param varTable:
        :return: 返回True或False
        '''

        r = self.execQuery("SELECT COUNT(*) c FROM SYSOBJECTS WHERE XTYPE = 'U' AND NAME='%s'" % (varTable))
        # print(r)  # [{'c': 1}]
        if r[0]['c'] == 1:
            return True
        else:
            return False

    # 4.2 判断字段是否存在
    def isField(self, varTable, varField):

        '''
        判断字段是否存在
        :param varTable:
        :param varField:
        :return: 返回True或False
        '''

        r = self.execQuery(
            "SELECT B.name as field FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'"
            % (varTable)
        )
        # print(r)  # [{'field': 'name'}, {'field': 'age'}, {'field': 'id'}]
        for i in range(len(r)):
            if r[i]['field'] == varField:
                return True
        return False

    # 4.3 判断是否有自增主键
    def isIdentity(self, varTable):

        '''
        判断是否有自增主键, 如果有则返回1，无则返回0
        :param varTable:
        :return:
        '''

        qty = self.execQuery("Select OBJECTPROPERTY(OBJECT_ID('" + varTable + "'),'TableHasIdentity') as qty")
        # print(qty)  # [{'qty': 1}]
        # print(qty[0]['qty'])  # 1
        if qty[0]['qty'] == 1 :
            return True
        else:
            return False



    def _dbDesc_search(self, varTable=0, var_l_field=0):

        d_tableComment = {}
        l_field = []
        l_type = []
        l_isKey = []
        l_isnull = []
        l_comment = []

        if varTable == 0 and var_l_field == 0:
            # 1，所有表结构（ok）
            l_table_comment = self.execQuery(
                "SELECT DISTINCT d.name,f.value FROM syscolumns a LEFT JOIN systypes b ON a.xusertype= b.xusertype INNER JOIN sysobjects d ON a.id= d.id AND d.xtype= 'U' AND d.name<> 'dtproperties' LEFT JOIN syscomments e ON a.cdefault= e.id LEFT JOIN sys.extended_properties g ON a.id= G.major_id AND a.colid= g.minor_id LEFT JOIN sys.extended_properties f ON d.id= f.major_id AND f.minor_id= 0"
            )
            # print(l_table_comment)

            # print(l_table_comment.decode('gbk')

        elif varTable == 0 and var_l_field != 0:
            # 6，所有表结构的可选字段(只输出找到字段的表) （ok）
            l_table_comment = self.execQuery(
                "SELECT DISTINCT d.name,f.value FROM syscolumns a LEFT JOIN systypes b ON a.xusertype= b.xusertype INNER JOIN sysobjects d ON a.id= d.id AND d.xtype= 'U' AND d.name<> 'dtproperties' LEFT JOIN syscomments e ON a.cdefault= e.id LEFT JOIN sys.extended_properties g ON a.id= G.major_id AND a.colid= g.minor_id LEFT JOIN sys.extended_properties f ON d.id= f.major_id AND f.minor_id= 0"
            )
        else:
            if "%" not in varTable:
                # 2，单表结构（ok）
                # 4，单表结构可选字段（ok）
                l_table_comment = self.execQuery(
                    "SELECT A.name, C.value FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'"
                    % (varTable)
                )
                # print(l_table_comment)

            elif "%" in varTable:
                # 3，带通配符表结构(ok)
                # 5，带通配符表结构可选字段(只输出找到字段的表) （ok）
                l_table_comment = self.execQuery(
                    "SELECT DISTINCT d.name,f.value FROM syscolumns a LEFT JOIN systypes b ON a.xusertype= b.xusertype INNER JOIN sysobjects d ON a.id= d.id AND d.xtype= 'U' AND d.name<> 'dtproperties' LEFT JOIN syscomments e ON a.cdefault= e.id LEFT JOIN sys.extended_properties g ON a.id= G.major_id AND a.colid= g.minor_id LEFT JOIN sys.extended_properties f ON d.id= f.major_id AND f.minor_id= 0 where d.name like '%s'"
                    % (varTable)
                )
        # print(b'\xd6\xf7\xbc\xfc\xd7\xd4\xd4\xf6'.decode('gbk'))
        for t in l_table_comment:

            if t['value'] != None:
                d_tableComment[t['name']] = t['value'].decode("gbk")
            else:
                d_tableComment[t['name']] = str(t['value'])

        # 字典表名 {Name：Comment}
        # print(d_tableComment)  # {'BACKUP_HISTORY': 'None', 'BACKUPINTERFACE': '拉取ITF的临时表', 'BACKUPQUALITYCONTROL': '拉取ITF数据使用的临时表')'

        # 遍历每个表，获取6个信息分别是： 表名，字段名，类型，大小，是否为空，注释
        for k, v in d_tableComment.items():
            varTable = k
            l_table_field_type_size_isNull_comment = self.execQuery(
                # "SELECT A.name, B.name, d.name, B.max_length, B.is_nullable, C.value FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'"
                "SELECT A.name as tableName, B.name as Name, d.name as Type, B.max_length as Size, B.is_nullable as NotNull, C.value as Comment FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s' order by B.column_id asc"
                % (varTable)
            )
            try:
                # 字段与类型对齐
                # print(l_table_field_type_size_isNull_comment)

                tblTableName = tblName = tblType = tblSize = tblNotNull = tblComment = 0
                # tblTableName = tblName = tblType = tblSize = tblNotNull = tblComment = 0
                for i in l_table_field_type_size_isNull_comment:

                    tblTableName = len(i['tableName'])
                    if len(str(i['Name'])) > tblName:
                        tblName = len(i['Name'])
                    if len(str(i['Type'])) > tblType:
                        tblType = len(i['Type'])
                    if len(str(i['Size'])) > tblSize:
                        tblSize = len(str(i['Size']))
                    if len(str(i['NotNull'])) > tblNotNull:
                        tblNotNull = len(str(i['NotNull']))
                    if len(str(i['Comment'])) > tblComment:
                        tblComment = len(str(i['Comment']))

                # print(tblName)

                if var_l_field != 0:
                    # print(var_l_field)
                    # print(l_table_field_type_size_isNull_comment)
                    # 可选字段
                    for l in range(len(var_l_field)):
                        for m in range(len(l_table_field_type_size_isNull_comment)):
                            if (
                                    var_l_field[l]
                                    == l_table_field_type_size_isNull_comment[m]['Name']
                            ):
                                l_field.append(
                                    str(l_table_field_type_size_isNull_comment[m]['Name'])
                                    + " "
                                    * (
                                            tblName
                                            - len(
                                        l_table_field_type_size_isNull_comment[m]['Name']
                                    )
                                            + 1
                                    )
                                )
                                l_type.append(
                                    str(l_table_field_type_size_isNull_comment[m]['Type'])
                                    + " "
                                    * (
                                            tblType
                                            - len(
                                        l_table_field_type_size_isNull_comment[m]['Type']
                                    )
                                            + 1
                                    )
                                )
                                l_isKey.append(
                                    str(l_table_field_type_size_isNull_comment[m]['Size'])
                                    + " "
                                    * (
                                            tblSize
                                            - len(
                                        str(
                                            l_table_field_type_size_isNull_comment[
                                                m
                                            ]['Size']
                                        )
                                    )
                                            + 1
                                    )
                                )
                                l_isnull.append(
                                    str(l_table_field_type_size_isNull_comment[m]['NotNull'])
                                    + " "
                                    * (
                                            tblNotNull
                                            - len(
                                        str(
                                            l_table_field_type_size_isNull_comment[
                                                m
                                            ]['NotNull']
                                        )
                                    )
                                            + 7
                                    )
                                )
                                if l_table_field_type_size_isNull_comment[m]['Comment'] == None:
                                    l_comment.append(
                                        str(
                                            l_table_field_type_size_isNull_comment[m]['Comment']
                                        )
                                        + " "
                                        * (
                                                tblComment
                                                - len(
                                            str(
                                                l_table_field_type_size_isNull_comment[
                                                    m
                                                ][
                                                    'Comment'
                                                ]
                                            )
                                        )
                                                + 1
                                        )
                                    )
                                else:
                                    l_comment.append(
                                        str(
                                            l_table_field_type_size_isNull_comment[m][
                                                'Comment'
                                            ].decode("GBK")
                                        )
                                        + " "
                                        * (
                                                tblComment
                                                - len(
                                            str(
                                                l_table_field_type_size_isNull_comment[
                                                    m
                                                ][
                                                    'Comment'
                                                ]
                                            )
                                        )
                                                + 1
                                        )
                                    )
                else:
                    # 所有字段
                    for i in l_table_field_type_size_isNull_comment:
                        l_field.append(str(i['Name']) + " " * (tblName - len(i['Name'])))
                        l_type.append(str(i['Type']) + " " * (tblType - len(i['Type'])))
                        l_isKey.append(str(i['Size']) + " " * (tblSize - len(str(i['Size'])) + 5))
                        l_isnull.append(str(i['NotNull']) + " " * (tblNotNull - len(str(i['NotNull'])) + 3))
                        if i['Comment'] == None:
                            l_comment.append(str(i['Comment']) + " " * (tblComment - len(str(i['Comment']))))
                        else:
                            l_comment.append(
                                str(i['Comment'].decode("GBK"))
                                + " " * (tblComment - len(str(i['Comment'])))
                            )

                # 只输出找到字段的表
                if len(l_field) != 0:
                    print("- - " * 20)
                    Color_PO.consoleColor(
                        "31",
                        "36",
                        "[Result] => TableName: "
                        + str(k)
                        + " ("
                        + str(d_tableComment[k])
                        + ") , "
                        + str(len(l_table_field_type_size_isNull_comment))
                        + "个字段",
                        "",
                    )

                    # print(
                    #     "Name" + " " * (tblName - len("Name")),
                    #     "Type" + " " * (tblType - len("Type")),
                    #     "Size" + " " * (tblSize - len("Size")+5),
                    #     "isNull" + " " * (tblNotNull - len("isNull")+3),
                    #     "Comment"
                    # )

                    Color_PO.consoleColor(
                        "31",
                        "36",
                        "Name" + " " * (tblName - len("Name") + 1) +
                        "Type" + " " * (tblType - len("Type") + 1) +
                        "Size" + " " * (tblSize - len("Size") + 6) +
                        "isNull" + " " * (tblNotNull - len("isNull") + 4) +
                        "Comment",
                        "",
                    )

                    for i in range(len(l_field)):
                        print(
                            l_field[i], l_type[i], l_isKey[i], l_isnull[i], l_comment[i]
                        )

                l_field = []
                l_type = []
                l_isKey = []
                l_isnull = []
                l_comment = []

            except Exception as e:
                raise e
        return len(d_tableComment)

    # 1, 查看数据库表结构（字段名、数据类型、大小、允许空值、字段说明）
    def dbDesc(self, *args):

        """1, 查看数据库表结构（字段名、数据类型、大小、允许空值、字段说明）"""
        # 注意，表名区分大小写
        # Sqlserver_PO.dbDesc()  # 1，所有表结构
        # Sqlserver_PO.dbDesc('tb_code_value')   # 2，某个表结构
        # Sqlserver_PO.dbDesc('tb_code_value', 'code,id,value')  # 3，某表的部分字段
        # Sqlserver_PO.dbDesc('tb*')  # 4，查看所有tb开头的表结构（通配符*）
        # Sqlserver_PO.dbDesc('tb*', 'id,page')  # 5，查看所有b开头的表中id字段的结构（通配符*）

        if len(args) == 0:
            # 1，所有表结构（ok）
            result = self._dbDesc_search()
            Color_PO.consoleColor(
                "31",
                "31",
                "\n[Result] => " + self.database + "数据库合计" + str(result) + "张表。",
                "",
            )
        elif len(args) == 1:
            # 2，单表结构 和 3，带通配符表结构 （ok）
            self._dbDesc_search(args[0])
        elif len(args) == 2:
            # 4，单表结构的可选字段 、 5，带通配符表结构的可选字段、6，所有表结构的可选字段
            self._dbDesc_search(args[0], args[1])



    def dbRecord(self, varTable, varType, varValue):

        """ 查找记录
        # 参数1：varTable = 表名（*表示所有的表）
        # 参数2：varType = 数据类型(char,int,double,timestamp)
        # 参数3：varValue = 值 (支持%模糊查询，如 %yy%)
        """
        # Sqlserver_PO.dbRecord('t_upms_user', 'varchar', '%e10adc3949ba59abbe56e057f20f883e')  # 搜索 t_upms_user 表中内容包含 admin 的 varchar 类型记录。
        # Sqlserver_PO.dbRecord('*', 'varchar', '%海鹰居委会%')
        # Sqlserver_PO.dbRecord('*', 'money', '%34.5%')
        # Sqlserver_PO.dbRecord('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
        # Sqlserver_PO.dbRecord('*', 'datetime', u'%2019-07-17 11:19%')  # 模糊搜索所有表中带2019-01的timestamp类型。


        # 支持的类型
        if (varType in "double,timestamp,float,money,int,nchar,nvarchar,datetime,varchar"):
            if "*" in varTable:
                # 遍历所有表
                l_d_tbl = self.execQuery("SELECT NAME FROM SYSOBJECTS WHERE TYPE='U'")
                # print(l_d_tbl)  # [{'NAME': 'TB_RIS_REPORT2'}, {'NAME': 'jh_jkpg'}, {'NAME': 'jh_jkgy'},,...]

                for b in range(len(l_d_tbl)):
                    # 遍历所有表的 列名称、列类别、类注释
                    tbl = l_d_tbl[b]['NAME']
                    l_d_field_type = self.execQuery(
                        "select syscolumns.name as field,systypes.name as type from syscolumns,systypes where syscolumns.xusertype=systypes.xusertype and syscolumns.id=object_id('%s')"
                        % (tbl)
                    )
                    # print(l_d_field_type)  # [{'field': 'GUID', 'type': 'varchar'}, {'field': 'VISITSTRNO', 'type': 'varchar'},...]

                    l_field = []
                    l_type = []
                    for j in l_d_field_type:
                        if varType in j['type']:
                            l_field.append(j['field'])
                            l_type.append(j['type'])

                    # print(l_field)  # ['GUID', 'VISITSTRNO', 'ORGCODE', 'ORGNAME',...]
                    # print(l_type)  # ['varchar', 'varchar', 'varchar', 'varchar' ...]

                    # 遍历所有字段
                    for i in range(len(l_field)):
                        l_result = self.execQuery("select * from %s where [%s] like '%s'" % (tbl, l_field[i], varValue))

                        if len(l_result) != 0:
                            print("--" * 50)
                            Color_PO.consoleColor("31", "36", "[result] => " + str(varValue) + " => " + tbl + " => " + l_field[i] + " => " + str(len(l_result)) + "条 ", "")

                            for j in range(len(l_result)):
                                print(l_result[j])
                                # print(str(l_result[j]).decode("utf8"))
                                # print(l_result[j].encode('latin-1').decode('utf8'))


            elif "*" not in varTable:
                # 搜索指定表（单表）符合条件的记录.  ，获取列名称、列类别、类注释

                # 获取表的Name和Type
                l_d_field_type = self.execQuery(
                    "select syscolumns.name as field,systypes.name as type from syscolumns,systypes where syscolumns.xusertype=systypes.xusertype and syscolumns.id=object_id('%s')"
                    % (varTable)
                )
                # print(l_d_field_type)  # [{'field': 'ID', 'type': 'int'}, {'field': 'ARCHIVENUM', 'type': 'varchar'}...]

                # 筛选符合条件（包含指定type）的field
                l_field = []
                for j in l_d_field_type:
                    if varType in j['type']:
                        l_field.append(j['field'])
                print(l_field)  # ['CZRYBM', 'CZRYXM', 'JMXM', 'SJHM', 'SFZH', 'JJDZ',...]

                # 遍历所有字段
                for i in range(len(l_field)):
                    l_result = self.execQuery("select * from %s where [%s] like '%s'" % (varTable, l_field[i], varValue))

                    if len(l_result) != 0:
                        print("--" * 50)
                        Color_PO.consoleColor("31", "36",
                                              "[result] => " + str(varValue) + " => " + varTable + " => " + l_field[
                                                  i] + " => " + str(len(l_result)) + "条 ", "")

                        for j in range(len(l_result)):
                            l_value = [value for value in l_result[j].values()]
                            # print(l_value)  # ['1015', '李*琳', '常*梅', '17717925118', '132222196702240429',...]
                            print(l_result[j])  # {'CZRYBM': '1015', 'CZRYXM': '李*琳', 'JMXM': '常*梅', 'SJHM': '17717925118', 'SFZH': '132222196702240429'...}

        else:
            print(
                "\n"
                + varType
                + "类型不存在，如：float,money,int,nchar,nvarchar,datetime,timestamp"
            )
        self.conn.close()


if __name__ == "__main__":

    Dm_PO = DmPO("192.168.0.234", "PHUSERS", "Zy123456789", "5236")  # 测试环境

    # result = Dm_PO.execQuery("select * from PHUSERS.SYS_DRUG where id=1")
    # print(result[0])  # (1, '1', '阿莫西林', 'AMXL', '111', '1111', 'QD', '每天一次', '1', '颗', '3', '12:00', '1', '规律', False)

    result = Dm_PO.execQuery("select * from PHUSERS.中医体质辨识 where id=%s" % (1))
    print(result[0])  # (1, 'ok', '2023/10/26 13:16:46', 'r12', 'ABNORMAL_STATUS', 'GY_TZBS01', '体质=平和质', '郭斐', '')


    # print("5 excel导入数据库".center(100, "-"))
    # Dm_PO.xlsx2db('规则db.xlsx', "疾病身份证", "疾病身份证")

    # print("1.1 查询sql".center(100, "-"))
    # a = Sqlserver_PO.execQuery("select * from aaa")
    # print(a)

    # print("1.2 执行sql".center(100, "-"))
    # Sqlserver_PO.execute("aaa", "UPDATE aaa set AGE=20 where ID=4")  # 更新数据
    # Sqlserver_PO.execute("aaa", "drop table aaa")  # 删除表
    # Sqlserver_PO.execute("aaa", "truncate table aaa")  # 删除数据



    # print("2.1.1 获取所有表".center(100, "-"))
    # print(Sqlserver_PO.getTables())  # ['condition_item', 'patient_demographics', 'patient_diagnosis']

    # print("2.1.2 获取所有表和表注释".center(100, "-"))
    # print(Sqlserver_PO.getTableAndComment())  # {'aaa': None, 'bbb': None, 'EMR_ADMISSION_ASSESSMENT': '入院评估记录',...}

    # print("2.1.3 获取所有表结构信息".center(100, "-"))
    # print(Sqlserver_PO.getTableInfor('aaa'))
    # print(Sqlserver_PO.getTableInfor())



    # print("2.2.1 获取字段".center(100, "-"))
    # print(Sqlserver_PO.getFields('aaa'))  # ['ID', 'ADDRESS', 'SALARY', 'NAME', 'AGE', 'time']

    # print("2.2.2 获取字段和字段注释".center(100, "-"))
    # print(Sqlserver_PO.getFieldAndComment('TB_HIS_MZ_Reg'))

    # getFieldAndComment

    # print("2.3 获取记录数 ".center(100, "-"))
    # print(Sqlserver_PO.getQty('aaa'))  # 0

    # print("2.4.1 获取所有字段和类型 ".center(100, "-"))
    # print(Sqlserver_PO.getFieldAndType("aaa"))  # {'ID': 'int', 'NAME': 'text', 'AGE': 'int', 'ADDRESS': 'char', 'SALARY': 'float'}
    #
    # print("2.4.2 获取N个字段和类型 ".center(100, "-"))
    # print(Sqlserver_PO.getMoreFieldAndType("aaa", ["ID"]))  # {'ID': 'int'}
    # print(Sqlserver_PO.getMoreFieldAndType("aaa", ["ID", 'AGE']))  # {'ID': 'int', 'AGE': 'int'}
    #
    # print("2.4.3 获取必填项字段和类型".center(100, "-"))
    # print(Sqlserver_PO.getNotNullFieldAndType('aaa'))  # {'ID': 'int', 'NAME': 'text', 'AGE': 'int', 'ADDRESS': 'char'}
    #
    # print("2.5 获取自增主键".center(100, "-"))
    # print(Sqlserver_PO.getIdentityPrimaryKey('aaa'))  # None // 没有自增主键
    # print(Sqlserver_PO.getIdentityPrimaryKey('bbb'))  # id
    #
    # print("2.6 获取表主键".center(100, "-"))
    # print(Sqlserver_PO.getPrimaryKey('aaa'))  # [{'COLUMN_NAME': 'ADDRESS'}, {'COLUMN_NAME': 'ID'}]
    # print(Sqlserver_PO.getPrimaryKey('bbb'))  # [{'COLUMN_NAME': 'id'}]

    # print("2.7 获取表主键最大值 ".center(100, "-"))
    # print(Sqlserver_PO.getPrimaryKeyMaxValue('aaa'))  # {'ID': 9}
    # print(Sqlserver_PO.getPrimaryKeyMaxValue('bbb'))  # {'id': 4}



    # print("3.1 创建表（自增id主键）".center(100, "-"))
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

    # print("3.2.1 生成类型值".center(100, "-"))
    # print(Sqlserver_PO._genTypeValue("aaa"))  # {'ID': 1, 'NAME': 'a', 'AGE': 1, 'ADDRESS': 'a', 'SALARY': 1.0, 'time': '08:12:23'}

    # print("3.2.2 生成必填项类型值".center(100, "-"))
    # print(Sqlserver_PO._genNotNullTypeValue("aaa"))

    # print("3.2.3 自动生成第一条数据".center(100, "-"))
    # Sqlserver_PO.genFirstRecord('bbb')
    # print("3.2.3(2) 所有表自动生成第一条数据".center(100, "-"))
    # Sqlserver_PO.genFirstRecordByAll()

    # print("3.2.4 自动生成数据".center(100, "-"))
    # Sqlserver_PO.genRecord('aaa')

    # print("3.2.5 自动生成必填项数据".center(100, "-"))
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

