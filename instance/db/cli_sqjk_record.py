# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2019-4-16
# Description: 项目实例
# 查看表结构（字段、类型、大小、可空、注释），注意，表名区分大小写  dbDesc()
# 查找记录  dbRecord('*', 'money', '%34.5%')
# 创建、删除表，插入、删除记录
# *****************************************************************
import sys, os
os.chdir("../")
os.chdir("../")
sys.path.append(os.getcwd())
from PO.SqlserverPO import *


# todo 社区健康平台（静安）
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHC_JINGAN", "GBK")
Sqlserver_PO.dbRecord('*', 'varchar', '%' + sys.argv[1] + '%' )

# todo 社区健康平台（标准版）
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHC", "GBK")
# Sqlserver_PO.dbRecord('*', 'varchar', '140202197610156018')
# Sqlserver_PO.dbDesc()
# Sqlserver_PO.dbDesc('HRCOVER')
# Sqlserver_PO.dbDesc('原始治理规则')
# Sqlserver_PO.dbDesc('HRCOVER',  ['ID', 'NAME'])
# Sqlserver_PO.dbDesc('HRD%')
# Sqlserver_PO.dbDesc('HRD%', ['PID', 'ID', 'NAME'])
# Sqlserver_PO.dbDesc('%', ["ID", "orgCode"])  # 表名中带有UpmsUser字符的表中Birthday字段的结构
# Sqlserver_PO.dbRecord('HRCOVER', 'varchar', '%刘斌龙%')  # 搜索指定表符合条件的记录.
# Sqlserver_PO.dbRecord('HRCOVER', 'varchar', '%张*%')  # 搜索指定表符合条件的记录.
# Sqlserver_PO.dbRecord('*', 'varchar', '%刘斌龙%')  # 搜索所有表符合条件的记录.
# Sqlserver_PO.dbRecord('*', 'money', '%34.5%')



