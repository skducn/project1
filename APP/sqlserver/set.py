# -- coding: utf-8 --
# ***************************************************************
# Author     : John
# Data       : 2024-10-31
# Description: set 应用
# ***************************************************************
"""
3.1 设置表注释（添加，修改，删除） setTableComment(varTable, varComment)
3.2 设置字段注释（添加、修改、删除） setFieldComment(varTable, varField, varComment)
3.3 设置数据类型 setFieldType(varTable, varField, varType)
3.4 添加自增主键 setIdentityPrimaryKey(varTable, varField)
3.5 删除自增主键 alter column varField drop identity
3.6 删除表的所有外键关系 dropKey(varTable)
3.7 自动生成第一条记录 genFirstRecord()
3.8 所有空表自动生成第一条记录 genFirstRecordByAll()
3.9 自动添加一条记录 genRecord()
3.10 自动生成必填项记录 genRecordByNotNull(self, varTable)

 生成类型值 _genTypeValue(self, varTable)
 生成必填项类型值 _genNotNullTypeValue(self, varTable)
 执行insert _execInsert(self, varTable, d_init,{})

"""
from PO.SqlserverPO import *

# todo 社区健康平台（全市）
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHC", "GBK")

# # print("3.1 设置表注释（添加，修改，删除）".center(100, "-"))
# Sqlserver_PO.setTableComment("a_api_wow_info", "注释")
#
# # print("3.2 设置字段注释（添加、修改、删除）".center(100, "-"))
# Sqlserver_PO.setFieldComment("a_api_wow_info", "id",'编号')

# print("3.3 设置数据类型".center(100, "-"))
# Sqlserver_PO.setFieldType("a_api_wow_info", 'phsField', 'varchar(100)')

# print("3.4 设置自增主键".center(100, "-"))
Sqlserver_PO.setIdentityPrimaryKey("a_api_wow_info", "id")


# print("3.5 自动生成第一条记录".center(100, "-"))
# Sqlserver_PO.genFirstRecord('bbb')

# print("3.6 所有空表自动生成第一条记录".center(100, "-"))
# Sqlserver_PO.genFirstRecordByAll()

# print("3.67自动添加一条记录".center(100, "-"))
# Sqlserver_PO.genRecord('aaa')

# print("3.8 自动生成必填项记录".center(100, "-"))
# Sqlserver_PO.genRecordByNotNull('aaa')



# print("生成类型值".center(100, "-"))
# print(Sqlserver_PO._genTypeValue("aaa"))  # {'ID': 1, 'NAME': 'a', 'AGE': 1, 'ADDRESS': 'a', 'SALARY': 1.0, 'time': '08:12:23'}

# print("生成必填项类型值".center(100, "-"))
# print(Sqlserver_PO._genNotNullTypeValue("aaa"))