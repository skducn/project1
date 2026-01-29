# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2025-12-4
# Description   : 患者运营管理平台	Patient Management Operation Platform（PMOP）
# *********************************************************************
from PO.SqlserverPO import *
Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "PMOP_TEST", "GBK")


# print("7.1 查看表结构".center(100, "-"))
# Sqlserver_PO.desc()
# Sqlserver_PO.desc(['id', 'page'])
# Sqlserver_PO.desc('a_c%')
# Sqlserver_PO.desc({'a_%':['id','sql']})

# 患者管理 - 联系患者
# todo PATIENT_CONTACT_TASK_LIST(患者联系任务表)
# Sqlserver_PO.desc('PATIENT_CONTACT_TASK_LIST')
# Sqlserver_PO.desc('PATIENT_CONTACT_DETAIL_LIST')
# PATIENT_DEAL_ID            int      4         None  10    YES    None  患者处理ID
# PATIENT_CONTACT_PERSON_ID  int      4         None  10    YES    None  联系人ID
# Sqlserver_PO.desc('PATIENT_LIST')


# Sqlserver_PO.desc({'a_test':['number', 'rule1']})

# print("7.2 查找记录".center(100, "-"))
# Sqlserver_PO.record('t_upms_user', 'varchar', '%e10adc3949ba59abbe56e057f20f883e')  # 搜索 t_upms_user 表中内容包含 admin 的 varchar 类型记录。
# Sqlserver_PO.record('*', 'int', '68', True)
# Sqlserver_PO.record('*', 'varchar', '%hellokiss%', True)
# Sqlserver_PO.record('*', 'varchar', '%192.168.0.248%')
Sqlserver_PO.record('*', 'varchar', '%2025-12-18 10:40:17%')
# Sqlserver_PO.record('*', 'varchar', u'%ef04737c5b4f4b93be85576e58b97ff2%')
# Sqlserver_PO.record('*', 'varchar', u'%310101195001293595%')
# Sqlserver_PO.record('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
Sqlserver_PO.record('*', 'datetime', u'%2025-12-17 10:40:17%')  # 模糊搜索所有表中带2019-01的timestamp类型。

# print("7.3 插入记录".center(100, "-"))
# Sqlserver_PO.insert("a_test", {'result': str(Fake_PO.genPhone_number('Zh_CN', 1)), 'createDate': Time_PO.getDateTimeByPeriod(0), 'ruleParam': 'param'})


# r = Sqlserver_PO.select("SELECT tags,summary,path,method,query,body FROM %s where summary='%s'" % ('a_phs_auth_app', '登录'))
# print(r[0])  # {'tags': '登录模块', 'summary': '登录', 'path': '/auth/login', 'method': 'post', 'query': None, 'body': "{'password': 'Jinhao123', 'username': '11012'}"}




