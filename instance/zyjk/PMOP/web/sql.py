# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-10-15
# Description: 专病库（1.2）
# 测试环境 http://192.168.0.243:8083/patient/list
# 账号: jinhao 密码：Jinhao@！@#
#***************************************************************
from PO.SqlserverPO import *
# Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CDRD_TEST", "GBK")
Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CDRD_TEST", "utf8")


# Sqlserver_PO.record('*', 'varchar', '%三枪起搏器%')


# 基础配置 - 标签管理 - 新增标签 - 患者详情/就诊信息 - 人民币
# Sqlserver_PO.record('*', 'varchar', '%人民币%')
# {'TAG_ID': 82, 'CATEGORY_CLASS': 'patient_detail', 'CATEGORY_NAME': '患者详情/就诊信息', 'CATEGORY_KEY': 'cdrd_patient_visit_info', 'TAG_NAME': '人民币', 'TAG_KEY': 'rmb', 'TAG_SORT': 33, 'STATUS': '0', 'CREATE_ID': 26, 'CREATE_TIME': datetime.datetime(2025, 10, 21, 16, 40, 45, 130000), 'UPDATE_ID': None, 'UPDATE_TIME': None, 'REMARK': '4567890'}
# Sqlserver_PO.record('*', 'varchar', '%快乐1%')
# {'TAG_DATA_ID': 152, 'TAG_ID': 82, 'TAG_DATA_NAME': '快乐1', 'TAG_DATA_KEY': 'kl1', 'TAG_DATA_SORT': 4, 'STATUS': '0'}

# 基础配置 - 扩展字段管理 - 新增字段 - 患者详情/就诊信息 - 孔乙己



# 患者列表页 - 王亮玲 patientId=16 (CDRD_PATIENT_INFO)
# 就诊信息 - 就诊详情 patient_visit_id=76 （CDRD_PATIENT_VISIT_INFO）
# 就诊信息 - 就诊详情 - 补充信息 - 孔乙己字段 'EXTEND_FIELD_ID': 47 （SYS_EXTEND_FIELD_MANAGE）
# Sqlserver_PO.record('*', 'varchar', '%孔乙己%')
# {'EXTEND_FIELD_ID': 47, 'CATEGORY_CLASS': 'patient_detail', 'CATEGORY_NAME': '患者详情/就诊信息', 'CATEGORY_KEY': 'cdrd_patient_visit_info', 'EXTEND_FIELD_NAME': '孔乙己', 'EXTEND_FIELD_KEY': 'kyj', 'SORT': 56, 'STATUS': '0', 'REMARK': '4567', 'CREATE_ID': 26, 'CREATE_TIME': datetime.datetime(2025, 10, 21, 16, 7, 22, 573000), 'UPDATE_ID': None, 'UPDATE_TIME': datetime.datetime(2025, 10, 21, 16, 7, 34, 197000)}
# 就诊信息 - 就诊详情 - 补充信息 - 孔乙己字段里的值为"我的上甘岭" 'EXTEND_FIELD_RECORD_ID': 352 （PATIENT_EXTEND_FIELD）
# Sqlserver_PO.record('*', 'varchar', '%我的上甘岭%')
# {'EXTEND_FIELD_RECORD_ID': 352, 'CATEGORY_SOURCE_ID': 16, 'CATEGORY_KEY': 'cdrd_patient_visit_info', 'CATEGORY_ID': 76, 'EXTEND_FIELD_ID': 47, 'EXTEND_FIELD_KEY': 'kyj', 'EXTEND_FIELD_TEXT': '我的上甘岭', 'CREATE_ID': 26, 'CREATE_BY': 'jinhao', 'CREATE_TIME': datetime.datetime(2025, 10, 21, 16, 8, 8, 337000)}
# 就诊信息 - 就诊详情 - 标签 - 标签名称是"测试11" 'TAG_ID': 51
# Sqlserver_PO.record('*', 'varchar', '%测试11%')
# {'TAG_ID': 51, 'CATEGORY_CLASS': 'patient_detail', 'CATEGORY_NAME': '患者详情/就诊信息', 'CATEGORY_KEY': 'cdrd_patient_visit_info', 'TAG_NAME': '测试11', 'TAG_KEY': 'jiuzhenceshi11', 'TAG_SORT': 1, 'STATUS': '0', 'CREATE_ID': 60, 'CREATE_TIME': datetime.datetime(2025, 9, 11, 9, 54, 38), 'UPDATE_ID': 61, 'UPDATE_TIME': datetime.datetime(2025, 10, 20, 13, 37, 1, 73000), 'REMARK': None}
# 就诊信息 - 就诊详情 - 标签 - 标签名称是"测试11" - 标签数据为"就诊测试1102" ，'TAG_DATA_ID': 111
# Sqlserver_PO.record('*', 'varchar', '%就诊测试1102%')
# {'TAG_DATA_ID': 111, 'TAG_ID': 51, 'TAG_DATA_NAME': '就诊测试1102', 'TAG_DATA_KEY': 'jiuzhenceshi1102', 'TAG_DATA_SORT': 2, 'STATUS': '0'}





# Sqlserver_PO.record('PATIENT_EXPORT', 'varchar', '%我的模版1%') # 'MODEL_ID': 7,
# Sqlserver_PO.desc("PATIENT_EXPORT")
# Sqlserver_PO.getTableComment(format="true")
# Sqlserver_PO.desc("PATIENT_EXPORT_FIELD")  # 导出数据表
# Sqlserver_PO.desc("PATIENT_EXPORT_MODULE")  # 导出模块表
# Sqlserver_PO.desc("sys_file_download_record")  # 文件下载记录表
# Sqlserver_PO.desc("sys_file_download")  # 文件下载管理表
# Sqlserver_PO.desc("sys_Tag_authority")  # 文件下载管理表


# todo 'USER_ID': 26, 'JOB_NUM': '1101', 'DEPARTMENT_ID': 32, 'DEPARTMENT_CODE': '0022', 'DEPARTMENT_NAME': '心内科'
# Sqlserver_PO.record('*', 'varchar', '%jinhao%', False)
# Sqlserver_PO.record('sys_user', 'varchar', '%jinhao%')
#
# Sqlserver_PO.record('SYS_USER', 'varchar', '%shuyang%')



# # todo 健康评估及干预  - QYYH
# # select * from TB_EMPI_INDEX_ROOT where name='施*东'
# # select * from TB_EMPI_INDEX_ROOT where IDCARDNO='130403195207271821'
# # select * from QYYH where sfzh='130403195207271821'
#
# Sqlserver_PO.record('T_ASSESS_INFO', 'varchar', u'%130403195207271821%')  # 施*东
# r = Sqlserver_PO.select("SELECT ASSESS_DATE,REPORT_STATUS,UPLOAD_STATUS,UPLOAD_DOC_ID,PDF_REPORT_STATUS,MODEL_CODE FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512646))
# print(r[0])  # {'ASSESS_DATE': datetime.date(2025, 10, 16), 'REPORT_STATUS': 1, 'UPLOAD_STATUS': '0', 'UPLOAD_DOC_ID': None, 'PDF_REPORT_STATUS': '0', 'MODEL_CODE': ''}
# # 页面：已确认，数据库：REPORT_STATUS：1 ， 报告生成状态（0-预评估，1-评估完成，2-评估中，3-评估失败(取数据)，4-评估失败(执行规则)）
# # 确认报告 - REPORT_STATUS：1 （1-评估完成）
# # 下载报告 - 'PDF_REPORT_STATUS': '1', 'MODEL_CODE': '014' （老年人）
# if r[0]['REPORT_STATUS'] == 3:
#     Sqlserver_PO.execute("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512646))
#



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




