# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-10-15
# Description: 社区健康管理中心 - 数据流转
# 测试环境 # http://192.168.0.243:8010/#/login
# 账号: lbl 密码：Qa@123456
#***************************************************************
from PO.SqlserverPO import *

# todo 社区健康平台（全市）
Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CHCCONFIG", "GBK")

# Sqlserver_PO.record('sys_user', 'varchar', '%小茄子%')
# id=82,
# NAME:小茄子
# 机构名称, ORG_NAME :宝山社区卫生服务中
# 所属机构编码, ORG_CODE:0000001
# 人员类别编码, CATEGORY_CODE: 4
# 人员类别, CATEGORY_NAME:中心主任
# 第三方工号, THIRD_NO:1231231



Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CHC", "GBK")
Sqlserver_PO.record('*', 'varchar', '%白*均%')




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
# Sqlserver_PO.record('*', 'varchar', '%192.168.0.248%')
# Sqlserver_PO.record('*', 'varchar', u'%ef04737c5b4f4b93be85576e58b97ff2%')
# Sqlserver_PO.record('*', 'varchar', u'%310101195001293595%')
# Sqlserver_PO.record('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
# Sqlserver_PO.record('*', 'datetime', u'%2019-07-17 11:19%')  # 模糊搜索所有表中带2019-01的timestamp类型。

# print("7.3 插入记录".center(100, "-"))
# Sqlserver_PO.insert("a_test", {'result': str(Fake_PO.genPhone_number('Zh_CN', 1)), 'createDate': Time_PO.getDateTimeByPeriod(0), 'ruleParam': 'param'})


# r = Sqlserver_PO.select("SELECT tags,summary,path,method,query,body FROM %s where summary='%s'" % ('a_phs_auth_app', '登录'))
# print(r[0])  # {'tags': '登录模块', 'summary': '登录', 'path': '/auth/login', 'method': 'post', 'query': None, 'body': "{'password': 'Jinhao123', 'username': '11012'}"}




