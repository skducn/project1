# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2025-3-27
# Description   : sqlserverApp
# *********************************************************************

from PO.SqlserverPO import *


# todo 社区健康平台（静安）
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHC_JINGAN", "GBK")

# todo 社区健康平台（全市）
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "PHUSERS", "GBK")
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "ZYCONFIG", "GBK")
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "PHS", "GBK")
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "PHS_JOB", "GBK")

# print("7.1 查看表结构".center(100, "-"))
# Sqlserver_PO.desc()
# Sqlserver_PO.desc(['id', 'page'])
# Sqlserver_PO.desc('a_c%')
# Sqlserver_PO.desc({'a_%':['id','sql']})
# Sqlserver_PO.desc('QYYH')
# Sqlserver_PO.desc({'a_test':['number', 'rule1']})

# print("7.2 查找记录".center(100, "-"))
# Sqlserver_PO.record('t_upms_user', 'varchar', '%e10adc3949ba59abbe56e057f20f883e')  # 搜索 t_upms_user 表中内容包含 admin 的 varchar 类型记录。
# Sqlserver_PO.record('*', 'varchar', '%13710078886%', False)
# Sqlserver_PO.record('*', 'varchar', '%基础服务包（2019版）%')
Sqlserver_PO.record('*', 'varchar', '%192.168.0.248%')
# Sqlserver_PO.record('*', 'varchar', '%13710078886%')
# Sqlserver_PO.record('*', 'varchar', u'%ef04737c5b4f4b93be85576e58b97ff2%')
# Sqlserver_PO.record('*', 'varchar', u'%310101195001293595%')
# Sqlserver_PO.record('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
# Sqlserver_PO.record('*', 'datetime', u'%2019-07-17 11:19%')  # 模糊搜索所有表中带2019-01的timestamp类型。

# print("7.3 插入记录".center(100, "-"))
# Sqlserver_PO.insert("a_test", {'result': str(Fake_PO.genPhone_number('Zh_CN', 1)), 'createDate': Time_PO.getDateTimeByPeriod(0), 'ruleParam': 'param'})


