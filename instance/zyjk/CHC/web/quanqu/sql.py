# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-10-15
# Description: 社区健康管理中心 - 业务流程
# 测试环境 # http://192.168.0.243:8010/#/login
# 账号: lbl 密码：Qa@123456
# # 在线SM2公钥私钥对生成，加密/解密 https://config.net.cn/tools/sm2.html
public_key = '04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249'
private_key = '124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62'
#***************************************************************
from PO.SqlserverPO import *

# 社区健康平台（全市）
Sqlserver_PO_config = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CHCCONFIG", "GBK")
Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CHC", "GBK")

# todo 'ID': 82, 'THIRD_NO': '1231231','NAME': '小茄子'
# Sqlserver_PO_config.record('sys_user', 'varchar', '%小茄子%')
# 'ID': 82, 'THIRD_NO': '1231231','NAME': '小茄子'
# 'ORG_CODE': '0000001', 'ORG_NAME': '宝山社区卫生服务中心'
# 'CATEGORY_CODE': '4', 'CATEGORY_NAME': '中心主任',
#

# todo 'ID': 132, 'THIRD_NO': '800411', 'NAME': 'jinhao'
# Sqlserver_PO_config.record('sys_user', 'varchar', '%jh123%')
# 'ID': 132, 'THIRD_NO': '800411', 'NAME': 'jinhao'
# 'ORG_CODE': '0000001','ORG_NAME': '宝山社区卫生服务中心',
# ORG_NAME :宝山社区卫生服务中,ORG_CODE:0000001
# 'CATEGORY_CODE': '4', 'CATEGORY_NAME': '中心主任',
#


# todo 健康评估及干预  - QYYH
# select * from TB_EMPI_INDEX_ROOT where name='施*东'
# select * from TB_EMPI_INDEX_ROOT where IDCARDNO='130403195207271821'
# select * from QYYH where sfzh='130403195207271821'

Sqlserver_PO.record('T_ASSESS_INFO', 'varchar', u'%130403195207271821%')  # 施*东
r = Sqlserver_PO.select("SELECT ASSESS_DATE,REPORT_STATUS,UPLOAD_STATUS,UPLOAD_DOC_ID,PDF_REPORT_STATUS,MODEL_CODE FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512646))
print(r[0])  # {'ASSESS_DATE': datetime.date(2025, 10, 16), 'REPORT_STATUS': 1, 'UPLOAD_STATUS': '0', 'UPLOAD_DOC_ID': None, 'PDF_REPORT_STATUS': '0', 'MODEL_CODE': ''}
# 页面：已确认，数据库：REPORT_STATUS：1 ， 报告生成状态（0-预评估，1-评估完成，2-评估中，3-评估失败(取数据)，4-评估失败(执行规则)）
# 确认报告 - REPORT_STATUS：1 （1-评估完成）
# 下载报告 - 'PDF_REPORT_STATUS': '1', 'MODEL_CODE': '014' （老年人）
if r[0]['REPORT_STATUS'] == 3:
    Sqlserver_PO.execute("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512646))




# Sqlserver_PO.desc({'QYYH':['REPORT_STATUS']})  # 评估状态(0:预评估；1:评估完成；2:未评估)
# 页面：待评估， 数据库：未评估
# 页面：报告待审核， 数据库：预评估
# 页面：评估完成， 数据库：评估完成
# Sqlserver_PO.desc('QYYH')

# Sqlserver_PO.record('*', 'int', '68407', False)
# Sqlserver_PO.record('IMPORTANT_CATEGORY', 'int', '68407')
# Sqlserver_PO.desc('IMPORTANT_CATEGORY')  # 重点人群编码


# Sqlserver_PO.record('*', 'varchar', u'%310110194709162023%')

# todo 儿童 - 检查 'MODEL_CODE': '005'
# 006-宝山版成人模板,008-宝山版孕妇模板,005-宝山版儿童模版,010-宝山版产妇模板,012-宝山版学生模板,014-宝山版老年人模板,T001-标准版体重模版,S014-宝山版老年人上传模板
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512492))

# Sqlserver_PO.record('T_ASSESS_INFO', 'varchar', u'%310110195007082023%')
# r = Sqlserver_PO.select("SELECT ASSESS_DATE,REPORT_STATUS,UPLOAD_STATUS,UPLOAD_DOC_ID,PDF_REPORT_STATUS,MODEL_CODE FROM %s where ID='%s'" % ('T_ASSESS_INFO', 511776))
# print(r[0])  # {'ASSESS_DATE': datetime.date(2025, 10, 16), 'REPORT_STATUS': 1, 'UPLOAD_STATUS': '0', 'UPLOAD_DOC_ID': None, 'PDF_REPORT_STATUS': '0', 'MODEL_CODE': ''}
# 页面：已确认，数据库：REPORT_STATUS：1 ， 报告生成状态（0-预评估，1-评估完成，2-评估中，3-评估失败(取数据)，4-评估失败(执行规则)）


# ID_CARD = %310110194709162023% >> T_ASSESS_INFO(评估表) >> 2条


# r = Sqlserver_PO.select("SELECT ASSESS_DATE,REPORT_STATUS,UPLOAD_STATUS,UPLOAD_DOC_ID,PDF_REPORT_STATUS,MODEL_CODE FROM %s where ID='%s'" % ('T_ASSESS_INFO', 511442))
# print(r[0])  # {'ASSESS_DATE': datetime.date(2025, 6, 11), 'REPORT_STATUS': 0, 'UPLOAD_STATUS': '0', 'UPLOAD_DOC_ID': None, 'PDF_REPORT_STATUS': '0', 'MODEL_CODE': None}
# 页面：待确认，数据库：REPORT_STATUS：0 ， 报告生成状态（0-预评估，1-评估完成，2-评估中，3-评估失败(取数据)，4-评估失败(执行规则)）

# r = Sqlserver_PO.select("SELECT ASSESS_DATE,REPORT_STATUS,UPLOAD_STATUS,UPLOAD_DOC_ID,PDF_REPORT_STATUS,MODEL_CODE FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512571))
# print(r[0])  # {'ASSESS_DATE': datetime.date(2025, 9, 28), 'REPORT_STATUS': 1, 'UPLOAD_STATUS': '0', 'UPLOAD_DOC_ID': None, 'PDF_REPORT_STATUS': '1', 'MODEL_CODE': None}
# 页面：已确认，数据库：REPORT_STATUS：1 ， 报告生成状态（0-预评估，1-评估完成，2-评估中，3-评估失败(取数据)，4-评估失败(执行规则)）

# r = Sqlserver_PO.select("SELECT ASSESS_DATE,REPORT_STATUS,UPLOAD_STATUS,UPLOAD_DOC_ID,PDF_REPORT_STATUS,MODEL_CODE FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512580))
# print(r[0])  # {'ASSESS_DATE': datetime.date(2025, 10, 16), 'REPORT_STATUS': 1, 'UPLOAD_STATUS': '0', 'UPLOAD_DOC_ID': None, 'PDF_REPORT_STATUS': '0', 'MODEL_CODE': '005'}
# 页面：已确认，数据库：REPORT_STATUS：0 ， 报告生成状态（0-预评估，1-评估完成，2-评估中，3-评估失败(取数据)，4-评估失败(执行规则)）


# todo 老年人 - 检查 'MODEL_CODE': '014'
# 006-宝山版成人模板,008-宝山版孕妇模板,005-宝山版儿童模版,010-宝山版产妇模板,012-宝山版学生模板,014-宝山版老年人模板,T001-标准版体重模版,S014-宝山版老年人上传模板
# 老年人
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512455))


# Sqlserver_PO.record('T_ASSESS_INFO', 'varchar', u'%520626198701154673%')
# r = Sqlserver_PO.select("SELECT ASSESS_DATE,REPORT_STATUS,UPLOAD_STATUS,UPLOAD_DOC_ID,PDF_REPORT_STATUS,MODEL_CODE FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512617))
# print(r[0])  # {'ASSESS_DATE': datetime.date(2025, 10, 16), 'REPORT_STATUS': 1, 'UPLOAD_STATUS': '0', 'UPLOAD_DOC_ID': None, 'PDF_REPORT_STATUS': '0', 'MODEL_CODE': ''}
# 页面：已确认，数据库：REPORT_STATUS：1 ， 报告生成状态（0-预评估，1-评估完成，2-评估中，3-评估失败(取数据)，4-评估失败(执行规则)）


# todo 普通人群 - 检查 'MODEL_CODE': '006'
# 006-宝山版成人模板,008-宝山版孕妇模板,005-宝山版儿童模版,010-宝山版产妇模板,012-宝山版学生模板,014-宝山版老年人模板,T001-标准版体重模版,S014-宝山版老年人上传模板
# Sqlserver_PO.record('T_ASSESS_INFO', 'varchar', u'%130102197708161811%')
# r = Sqlserver_PO.select("SELECT ASSESS_DATE,REPORT_STATUS,PDF_REPORT_STATUS,MODEL_CODE FROM %s where ID='%s'" % ('T_ASSESS_INFO', 511220))
# print(r[0])  # {'ASSESS_DATE': datetime.date(2025, 10, 16), 'REPORT_STATUS': 1, 'PDF_REPORT_STATUS': '0', 'MODEL_CODE': ''}
# 页面：已确认，数据库：REPORT_STATUS：1 ， 报告生成状态（0-预评估，1-评估完成，2-评估中，3-评估失败(取数据)，4-评估失败(执行规则)）

# todo 学生 - 检查 'MODEL_CODE': '012'
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512602))
# Sqlserver_PO.record('T_ASSESS_INFO', 'varchar', u'%310104201109132416%')
# r = Sqlserver_PO.select("SELECT * FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512585))
# r = Sqlserver_PO.select("SELECT ASSESS_DATE,REPORT_STATUS,UPLOAD_STATUS,UPLOAD_DOC_ID,PDF_REPORT_STATUS,MODEL_CODE FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512603))
# print(r[0])  # {'ASSESS_DATE': datetime.date(2025, 10, 16), 'REPORT_STATUS': 1, 'UPLOAD_STATUS': '0', 'UPLOAD_DOC_ID': None, 'PDF_REPORT_STATUS': '0', 'MODEL_CODE': ''}
# 页面：已确认，数据库：REPORT_STATUS：1 ， 报告生成状态（0-预评估，1-评估完成，2-评估中，3-评估失败(取数据)，4-评估失败(执行规则)）



# todo 孕妇 - 检查 'MODEL_CODE': '008'
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512221))
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512560))
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512568))
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512597))

# Sqlserver_PO.record('T_ASSESS_INFO', 'varchar', u'%310110195303082052%')
# r = Sqlserver_PO.select("SELECT ASSESS_DATE,REPORT_STATUS,PDF_REPORT_STATUS,MODEL_CODE FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512615))
# print(r[0])  # {'ASSESS_DATE': datetime.date(2025, 10, 16), 'REPORT_STATUS': 1, 'PDF_REPORT_STATUS': '0', 'MODEL_CODE': ''}
# 页面：已确认，数据库：REPORT_STATUS：1 ， 报告生成状态（0-预评估，1-评估完成，2-评估中，3-评估失败(取数据)，4-评估失败(执行规则)）


# todo 产妇 - 检查 'MODEL_CODE': '010'
# Sqlserver_PO.record('T_ASSESS_INFO', 'varchar', u'%310110195303084226%')
# r = Sqlserver_PO.select("SELECT ASSESS_DATE,REPORT_STATUS,UPLOAD_STATUS,UPLOAD_DOC_ID,PDF_REPORT_STATUS,MODEL_CODE FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512616))
# print(r[0])  # {'ASSESS_DATE': datetime.date(2025, 10, 16), 'REPORT_STATUS': 1, 'UPLOAD_STATUS': '0', 'UPLOAD_DOC_ID': None, 'PDF_REPORT_STATUS': '0', 'MODEL_CODE': ''}
# 页面：已确认，数据库：REPORT_STATUS：1 ， 报告生成状态（0-预评估，1-评估完成，2-评估中，3-评估失败(取数据)，4-评估失败(执行规则)）


# r = Sqlserver_PO.select("SELECT * FROM %s where ID='%s'" % ('QYYH', 68418))
# print(r[0])
#
# r = Sqlserver_PO.select("SELECT * FROM %s where ID='%s'" % ('QYYH', 68419))
# print(r[0])

# Sqlserver_PO.desc('QYYH')
# Sqlserver_PO.desc({'QYYH': 'ASSESS_ORDER'})


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# Sqlserver_PO.desc('QYYH')
# Sqlserver_PO.desc('ORG_MODEL_INFO')

# todo 体重管理
# Sqlserver_PO.execute("update WEIGHT_REPORT set MODEL_CODE='T001'")
# Sqlserver_PO.desc('WEIGHT_REPORT')
# Sqlserver_PO.record('WEIGHT_REPORT', 'varchar', u'%310101195507234066%')
# r = Sqlserver_PO.select("SELECT PDFFILE_STATUS,MODEL_CODE FROM %s where ID='%s'" % ('WEIGHT_REPORT', 1927))
# print(r[0])  # {'ASSESS_DATE': datetime.date(2025, 10, 16), 'REPORT_STATUS': 1, 'UPLOAD_STATUS': '0', 'UPLOAD_DOC_ID': None, 'PDF_REPORT_STATUS': '0', 'MODEL_CODE': ''}
# 页面：已确认，数据库：REPORT_STATUS：1 ， 报告生成状态（0-预评估，1-评估完成，2-评估中，3-评估失败(取数据)，4-评估失败(执行规则)）


# Sqlserver_PO.record('*', 'varchar', '%T002%', False)


# r = Sqlserver_PO.select("SELECT WEIGHT_INTERVENTION,PDFFILE_STATUS FROM %s where SFZH='%s'" % ('QYYH', 310101195507150428))
# print(r[0])






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
# Sqlserver_PO.record('*', 'varchar', u'%310110194709162023%')
# Sqlserver_PO.record('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
# Sqlserver_PO.record('*', 'datetime', u'%2019-07-17 11:19%')  # 模糊搜索所有表中带2019-01的timestamp类型。

# print("7.3 插入记录".center(100, "-"))
# Sqlserver_PO.insert("a_test", {'result': str(Fake_PO.genPhone_number('Zh_CN', 1)), 'createDate': Time_PO.getDateTimeByPeriod(0), 'ruleParam': 'param'})


# r = Sqlserver_PO.select("SELECT tags,summary,path,method,query,body FROM %s where summary='%s'" % ('a_phs_auth_app', '登录'))
# print(r[0])  # {'tags': '登录模块', 'summary': '登录', 'path': '/auth/login', 'method': 'post', 'query': None, 'body': "{'password': 'Jinhao123', 'username': '11012'}"}




