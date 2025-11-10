# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2025-3-27
# Description   : sqlserverApp
# *********************************************************************
from PO.SqlserverPO import *

# 公卫
# Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CDRD_PT", "GBK")

# 社区健康
Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CHC", "GBK")
# Sqlserver_PO.record('*', 'varchar', '%基础服务包（2019版）%')

# c3，新增疾病诊断史
# Sqlserver_PO.record('CDRD_PATIENT_DIAG_INFO', 'varchar', '%古丢丢医院%', False)
# Sqlserver_PO.execute("delete from CDRD_PATIENT_DIAG_INFO where patient_hospital_name='%s'" % ('古丢丢医院'))

# Sqlserver_PO.record('CDRD_PATIENT_SYMPTOM_INFO', 'varchar', '%葫芦娃医院%', False)
# Sqlserver_PO.execute("delete from CDRD_PATIENT_SYMPTOM_INFO where patient_hospital_name='%s'" % ('葫芦娃医院'))

# Sqlserver_PO.record('CDRD_PATIENT_PHYSICAL_SIGN_INFO', 'varchar', '%黑猫警察医院%', False)
# Sqlserver_PO.execute("delete from CDRD_PATIENT_PHYSICAL_SIGN_INFO where patient_hospital_name='%s'" % ('黑猫警察医院'))

# Sqlserver_PO.record('CDRD_PATIENT_OPERATION_INFO', 'int', '%14607%', False)
# Sqlserver_PO.record('CDRD_PATIENT_OPERATION_INFO', 'varchar', '%阿凡达医院1%')

# 实验室检查报告
# Sqlserver_PO.record('CDRD_PATIENT_LAB_EXAMINATION_INFO', 'varchar', '%霹雳医院%')


# todo 社区健康平台（静安）
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHC_JINGAN", "GBK")

# todo 社区健康平台（全市）
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "ZYCONFIG", "GBK")
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "PHS", "GBK")
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "PHS_JOB", "GBK")

# print("7.1 查看表结构".center(100, "-"))
# Sqlserver_PO.desc()
# Sqlserver_PO.desc(['id', 'page'])
# Sqlserver_PO.desc('a_c%')
# Sqlserver_PO.desc({'a_%':['id','sql']})
Sqlserver_PO.desc('WEIGHT_REPORT')  # 体重状态：0-未评估 1-体重偏低 2-正常 3-超重 4-肥胖 5-孕期体重增长过快
# Sqlserver_PO.desc({'a_test':['number', 'rule1']})

# print("7.2 查找记录".center(100, "-"))
# Sqlserver_PO.record('t_upms_user', 'varchar', '%e10adc3949ba59abbe56e057f20f883e')  # 搜索 t_upms_user 表中内容包含 admin 的 varchar 类型记录。
# Sqlserver_PO.record('*', 'varchar', '%13710078886%', False)
# Sqlserver_PO.record('*', 'varchar', '%基础服务包（2019版）%')
# Sqlserver_PO.record('*', 'varchar', '%192.168.0.248%')
# Sqlserver_PO.record('*', 'varchar', '%13710078886%')
# Sqlserver_PO.record('*', 'varchar', u'%ef04737c5b4f4b93be85576e58b97ff2%')
# Sqlserver_PO.record('*', 'varchar', u'%310101195001293595%')
# Sqlserver_PO.record('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
# Sqlserver_PO.record('*', 'datetime', u'%2019-07-17 11:19%')  # 模糊搜索所有表中带2019-01的timestamp类型。

# print("7.3 插入记录".center(100, "-"))
# Sqlserver_PO.insert("a_test", {'result': str(Fake_PO.genPhone_number('Zh_CN', 1)), 'createDate': Time_PO.getDateTimeByPeriod(0), 'ruleParam': 'param'})


# r = Sqlserver_PO.select("SELECT tags,summary,path,method,query,body FROM %s where summary='%s'" % ('a_phs_auth_app', '登录'))
# print(r[0])  # {'tags': '登录模块', 'summary': '登录', 'path': '/auth/login', 'method': 'post', 'query': None, 'body': "{'password': 'Jinhao123', 'username': '11012'}"}




