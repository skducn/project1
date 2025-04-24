# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2025-4-16
# Description   : 生成数据源
# 将i_gw表格导入db，并转换所有字段类型
# *********************************************************************

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "PHUSERS", "GBK")

def excel2db(tableName, tableSheet):

    # 将表格导入db
    Sqlserver_PO.xlsx2db('i_gw.xlsx', tableName, tableSheet)
    
    # 格式化字段类型
    Sqlserver_PO.setFieldType(tableName, 'status', 'varchar(100)')
    Sqlserver_PO.setFieldType(tableName, 'tags', 'varchar(100)')
    Sqlserver_PO.setFieldType(tableName, 'summary', 'varchar(100)')
    Sqlserver_PO.setFieldType(tableName, 'path', 'varchar(100)')
    Sqlserver_PO.setFieldType(tableName, 'method', 'varchar(10)')
    Sqlserver_PO.setFieldType(tableName, 'rpsStatus', 'varchar(1000)')
    Sqlserver_PO.setFieldType(tableName, 'rpsDetail', 'varchar(5000)')
    Sqlserver_PO.setFieldType(tableName, 'sql', 'varchar(255)')
    Sqlserver_PO.setFieldType(tableName, 'tester', 'varchar(10)')
    Sqlserver_PO.setFieldType(tableName, 'memo', 'varchar(500)')
    Sqlserver_PO.setFieldType(tableName, 'url', 'varchar(255)')
    Sqlserver_PO.setFieldType(tableName, 'updateDate', ' varchar(255)')
    Sqlserver_PO.setFieldType(tableName, 'updateDate', ' DATE')


# excel2db('a_phs_auth_app', '登录')
# excel2db('a_phs_tSignInfo_app', '签约')
# excel2db('a_phs_gxy_app', '高血压')
