# -- coding: utf-8 --
# ***************************************************************
# Author     : John
# Data       : 2019-04-16
# Description: get 应用
# ***************************************************************
"""
2.1 获取表结构信息 getStructure(varTable='all')
2.2 获取表 getTables()
2.3 获取表名与表注释 getTableComment(varTable='all')
2.4 获取视图 getViews()
2.5 获取字段 getFields(varTable)
2.6 获取字段名与字段注释 getFieldComment(varTable)
2.7 获取字段名与字段类型 getFieldType(varTable)
2.8 获取非空（必填）字段与类型 getNotNullFieldType（varTable）

2.9 获取自增主键 getIdentityPrimaryKey(varTable)
2.10 获取主键  getPrimaryKey（self, varTable）
2.11 获取主键最大值 getPrimaryKeyMaxValue（self, varTable)
2.12 获取所有外键 getForeignKey()

2.13 获取记录数 getRecordCount(varTable)

"""
from PO.SqlserverPO import *

# todo 社区健康平台（全市）
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHC", "GBK")


# print("2.1 获取表结构信息".center(100, "-"))
# print(Sqlserver_PO.getStructure('a_api_wow_info'))


# # print("2.2 获取表".center(100, "-"))
# print(Sqlserver_PO.getTables())  # ['condition_item', 'patient_demographics', 'patient_diagnosis' ...

# # print("2.3 获取表名与表注释".center(100, "-"))
# print(Sqlserver_PO.getTableComment())  # {'ASSESS_DIAGNOSIS': '门诊数据', 'ASSESS_MEDICATION': '评估用药情况表',...}    #
# print(Sqlserver_PO.getTableComment('a_test%'))
# print(Sqlserver_PO.getTableComment('QYYH'))  # {'QYYH': '1+1+1签约信息表'}

# # print("2.4 获取视图".center(100, "-"))
# print(Sqlserver_PO.getViews())  # ['TB_YFJZ_MYJZJBXX', 'TB_CHSS_GRJKDA', 'TB_CHSS_YWGMS' ...


# print("2.5 获取字段".center(100, "-"))
# print(Sqlserver_PO.getFields('SYS_USER'))  # ['id', 'name', 'age']

# print("2.6 获取字段名与字段注释".center(100, "-"))
# print(Sqlserver_PO.getFieldComment('SYS_USER'))  # {'id': '编号', 'name': None, 'salesrep': None}
#
# print("2.7 获取字段名与字段类型".center(100, "-"))
# print(Sqlserver_PO.getFieldType("a_api_wow_info"))  # {'ID': 'int', 'NAME': 'text', 'AGE': 'int', 'ADDRESS': 'char', 'SALARY': 'float'}
# print(Sqlserver_PO.getFieldType("a_api_wow_info", ["id"]))  # {'ID': 'int', 'NAME': 'text', 'AGE': 'int', 'ADDRESS': 'char', 'SALARY': 'float'}

# print("2.8 获取非空（必填）字段与类型".center(100, "-"))
# print(Sqlserver_PO.getNotNullFieldType('a_test'))  # {'ID': 'int', 'NAME': 'text', 'AGE': 'int', 'ADDRESS': 'char'}

# print("2.9 获取自增主键".center(100, "-"))
# print(Sqlserver_PO.getIdentityPrimaryKey('a_test'))  # None // 没有自增主键
# print(Sqlserver_PO.getIdentityPrimaryKey('a_ceshiguize'))  # ID

# print("2.10 获取主键".center(100, "-"))
# print(Sqlserver_PO.getPrimaryKey('a_api_wow_info'))  # [{'COLUMN_NAME': 'ADDRESS'}, {'COLUMN_NAME': 'ID'}]
# print(Sqlserver_PO.getPrimaryKey('a_test'))  # [{'COLUMN_NAME': 'id'}]

# print("2.11 获取表主键最大值 ".center(100, "-"))
# print(Sqlserver_PO.getPrimaryKeyMaxValue('a_test'))  # {'id': 4}

# print("2.12 获取所有外键 ".center(100, "-"))
# print(Sqlserver_PO.getForeignKey())  # []   //没有返回空列表


# print("2.13 获取记录数".center(100, "-"))
# print(Sqlserver_PO.getRecordCount('a_test'))  # 3

