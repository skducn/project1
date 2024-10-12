# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2019-4-16
# Description: 项目实例
# 7.1 查看表结构（字段、类型、大小、可空、注释），注意，表名区分大小写  desc()
# 7.2 查找记录 record('*', 'money', '%34.5%')
# 7.3 插入记录 insert()
from PO.sqlserverApp import *
# *****************************************************************


from PO.SqlserverPO import *

# todo 社区健康平台
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHC", "GBK")
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHCCONFIG", "GBK")
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHC_JINGAN", "GBK")  # （静安）
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHCCONFIG_JINGAN", "GBK") # （静安）

# Sqlserver_PO.desc('TB_DC_CHRONIC_MAIN')  # 慢性病防治随访主表
# Sqlserver_PO.desc('T_HIS_DIAGNOSIS')  # 诊断疾病表

Sqlserver_PO.record('*', 'varchar', 'jh123')
# Sqlserver_PO.record('*', 'varchar', 'auto', False)
# Sqlserver_PO.record('SYS_USER', 'varchar', 'auto')
# Sqlserver_PO.record('*', 'datetime', '%2024-09-09%')

# print("7.3 插入记录".center(100, "-"))
# Sqlserver_PO.insert("a_test", {'result': str(Fake_PO.genPhone_number('Zh_CN', 1)), 'updateDate': '2010-11-12', 'ruleParam': 'param'})

# a = Sqlserver_PO.select("select ruleParam from a_jiankangganyu_yihuanjibingdanbing where id=6")
# print(a, type(a))
# print(a[0]['ruleParam'], type(a[0]['ruleParam']))
# # Sqlserver_PO.close()






# todo 公卫
# Sqlserver_PO = SqlServerPO("192.168.180.237", "PHUR_TEST", "testPH@2023", "zyconfig_pprod", "GBK")  # 预发布，通过VPN访问
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "PHUSERS", "GBK")
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "ZYCONFIG", "GBK")
# Sqlserver_PO.record('*', 'varchar', 'sj')
# Sqlserver_PO.desc()  # 表名中带有UpmsUser字符的表中Birthday字段的结构
# Sqlserver_PO.desc('a_%')  # 5，查看所有tb开头的表中id字段的结构（通配符*）
# Sqlserver_PO.desc(0, ['ORG_CODE'])  # 5，查看所有tb开头的表中id字段的结构（通配符*）


# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "PHUSERS", "GBK")
# # Sqlserver_PO.record('*', 'varchar', '37068500100100082')
# # Sqlserver_PO.record('*', 'varchar', '卫健委')  # id=72
# Sqlserver_PO.record('*', 'varchar', '招远市卫健局')  # id=72

# 创建表（如存在先删除）
# Sqlserver_PO.execute(""" IF OBJECT_ID('a_test', 'U') IS NOT NULL DROP TABLE a_test
# CREATE TABLE a_test (
#     id INT NOT NULL,
#     name VARCHAR(100),
#     salesrep VARCHAR(100),
#     PRIMARY KEY(id)
# )
# """)

# alter table A_testrule ADD ID2 INT identity(1,1) primary key;

# # 插入多条记录
# Sqlserver_PO.executemany("INSERT INTO a_test VALUES (%d, %s, %s)", [(1, 'John Smith2', 'John Doe3'), (2, 'Jane Doe', 'Joe Dog'), (3, 'Mike T.', 'Sarah H.')])

# # 删除记录
# Sqlserver_PO.execute("DELETE FROM a_test WHERE id = 2")
#
# # 删除表
# Sqlserver_PO.execute("DROP TABLE a_test")


# todo 社区健康平台（标准版）
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHC", "GBK")
# Sqlserver_PO.record('*', 'varchar', '140202197610156018')
# Sqlserver_PO.desc()
# Sqlserver_PO.desc('HRCOVER')
# Sqlserver_PO.desc('原始治理规则')
# Sqlserver_PO.desc('HRCOVER',  ['ID', 'NAME'])
# Sqlserver_PO.desc('HRD%')
# Sqlserver_PO.desc('HRD%', ['PID', 'ID', 'NAME'])
# Sqlserver_PO.desc('%', ["ID", "orgCode"])  # 表名中带有UpmsUser字符的表中Birthday字段的结构
# Sqlserver_PO.record('HRCOVER', 'varchar', '%刘斌龙%')  # 搜索指定表符合条件的记录.
# Sqlserver_PO.record('HRCOVER', 'varchar', '%张*%')  # 搜索指定表符合条件的记录.
# Sqlserver_PO.record('*', 'varchar', '%刘斌龙%')  # 搜索所有表符合条件的记录.
# Sqlserver_PO.record('*', 'money', '%34.5%')






# todo 老年人体检
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "PHS", "GBK")
# Sqlserver_PO.desc()


# todo 重点人群
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "COVID", "GBK")
# Sqlserver_PO.desc()


# todo 家床
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "fsms20", "GBK")
# Sqlserver_PO.desc()

# todo PIM基层健康管理平台
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "pimtest", "GBK")
# Sqlserver_PO.desc()

# todo 区域平台（人名医院）
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "peopleHospital", "utf8")  
# Sqlserver_PO.desc('aaa')

# todo EHR电子健康档案
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "EHRDC", "GBK")  
# Sqlserver_PO.desc()

# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "EHRITF", "GBK")  
# Sqlserver_PO.desc()
# Sqlserver_PO.desc('itf_tb_chronic_main')
# Sqlserver_PO.desc('ITF_TB_EXAMINATION_INFO',  ['registerTypeCode', 'name'])
# Sqlserver_PO.desc('tb_dc_dm_%')
# Sqlserver_PO.desc('tb_dc_dm_%', ['guid', 'drugTypeCodeSystem'])  # # 5，批量输出tb开头表中包含id或page字段的表结构信息
# Sqlserver_PO.desc('%', ["idCardNo", "ehrNum"])  # 表名中带有UpmsUser字符的表中Birthday字段的结构
# Sqlserver_PO.record('CommonDictionary', 'varchar', '%录音%')  # 搜索指定表符合条件的记录.
# Sqlserver_PO.record('*', 'varchar', '%高血压%')  # 搜索所有表符合条件的记录.
# Sqlserver_PO.record('*', 'money', '%34.5%')l
# Sqlserver_PO.record('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
# Sqlserver_PO.record('*', 'datetime', u'%2019-07-17 11:19%')  # 模糊搜索所有表中带2019-01的timestamp类型。
# sqlserver_PO.record('UpmsUser', 'varchar', '%e10adc3949ba59abbe56e057f20f883e')  # 搜索 UpmsUser 表中内容包含 e10adc3949ba59abbe56e057f20f883e 的 varchar 类型记录。
# sqlserver_PO.record('CommonDictionaryType', 'datetime', '2018-10-15 18:21%')  # 模糊搜索所有表中带2018-10-15 18:21%的datetime类型。
# Sqlserver_PO.record('*', 'varchar', '17a7929801e54f1ca8ab69f18c086b00')
# Sqlserver_PO.record('*', 'datetime', '2018-10-15 18:21%')  # 模糊搜索所有表中带2018-10-15 18:21%的datetime类型。
# l = Sqlserver_PO.getAllFields('HrCover')  # 获取表结构字段列表
# print(l)

# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "EHR_CDRINFO", "GBK")  
# r = Sqlserver_PO.execQuery('select * from tb_org where id=%s ' % ('1'))
# print(r)
# tmpList = Sqlserver_PO.execQuery("SELECT convert(nvarchar(255), Categories)  FROM HrRule where RuleId='00081d1c0cce49fd88ac68b7627d6e1c' ")  # 数据库数据自造
# l_result = Sqlserver_PO.execQuery('select top 1 (select sum(live_people_num) from (select live_people_num,org_name from report_qyyh group by org_code,org_name,live_people_num) a)  livePeopleNum from report_qyyh')
# print(l_result)
# l_result = Sqlserver_PO.execQuery('select convert(nvarchar(20), Name) from HrCover where id=%s ' % (1))  # 中文乱码使用 convert(nvarchar(20), 字段)
# l_result = Sqlserver_PO.execQuery('select Name from HrCover where id=%s ' % (1))  # 中文乱码使用 convert(nvarchar(20), 字段)
# print(l_result)

# todo 系统用户中心
# Sqlserver_PO = SqlServerPO("192.168.0.195", "ZYDBUser", "qwer123.", "usertest", "GBK")  
# Sqlserver_PO.desc()
# Sqlserver_PO.desc('sys_user')   # 查看myclass表结构
# Sqlserver_PO.desc('b*')  # 查看所有b开头的表结构（通配符*） ???
# Sqlserver_PO.desc('book', 'id,page')   # 查看book表id,page字段的结构
# Sqlserver_PO.desc('b*', 'id,page')  # 查看所有b开头的表中id字段的结构（通配符*）
# Sqlserver_PO.record('t_upms_user', 'varchar', '%e10adc3949ba59abbe56e057f20f883e')  # 搜索 t_upms_user 表中内容包含 admin 的 varchar 类型记录。
# Sqlserver_PO.record('*', 'varchar', '%测试%')
# Sqlserver_PO.record('*', 'money', '%34.5%')
# Sqlserver_PO.record('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
# Sqlserver_PO.record('*','timestamp', u'%2019-01%')  # 模糊搜索所有表中带2019-01的timestamp类型。


# todo 白茅岭 (sqlserver)
# Sqlserver_PO = SqlServerPO("192.168.0.195", "ZYDBUser", "qwer#@!", "bmlpimpro", "GBK")  
# Sqlserver_PO.desc()
# Sqlserver_PO.record('*', 'varchar', '%王维强%')


# todo 白茅岭（注意：234上也存在）
# Sqlserver_PO = SqlServerPO("192.168.0.195", "DBuser", "qwer#@!", "bmlpimpro", "GBK")  
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "bmlpimpro", "GBK")
# Sqlserver_PO.desc()   # 查看所有表结构


# todo fsms家床
# SqlServerPO = SqlServerPO("192.168.0.195", "DBuser", "qwer#@!", "fsms", "GBK")  
# SqlServerPO.desc()  
# sqlserver_PO.record('*', 'varchar', '%测试1%')  # 模糊搜索所有表中带yoy的char类型。
# sqlserver_PO.record('t_upms_user', 'varchar', '%e10adc3949ba59abbe56e057f20f883e')  # 搜索 t_upms_user 表中内容包含 admin 的 varchar 类型记录。
# sqlserver_PO.record('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
# sqlserver_PO.record('*','timestamp', u'%2019-01%')  # 模糊搜索所有表中带2019-01的timestamp类型。
# sqlserver_PO.desc('t_system_patient_basic_info')   # 查看myclass表结构
# sqlserver_PO.desc('b*')  # 查看所有b开头的表结构（通配符*） ???
# sqlserver_PO.desc('book', 'id,page')   # 查看book表id,page字段的结构
# sqlserver_PO.desc('b*', 'id,page')  # 查看所有b开头的表中id字段的结构（通配符*）
# sqlserver_PO.record('t_upms_user', 'varchar', '%e10adc3949ba59abbe56e057f20f883e')  # 搜索 t_upms_user 表中内容包含 admin 的 varchar 类型记录。
# sqlserver_PO.record('*', 'varchar', '%海鹰居委会%')
# sqlserver_PO.record('*', 'money', '%34.5%')
# sqlserver_PO.record('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
# sqlserver_PO.record('*', 'datetime', u'%2019-07-17 11:19%')  # 模糊搜索所有表中带2019-01的timestamp类型。


# todo BI集成平台
# SqlServerPO = SqlServerPO("192.168.0.195", "DBuser", "qwer#@!", "bidev", "GBK")  
# SqlServerPO.desc()  



