# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-9-5
# Description: 静安社区健康管理中心 创建测试数据
# 测试环境 # http://192.168.0.243:8010/#/login
# 'cs', '12345678'
#***************************************************************

from PO.DataPO import *
Data_PO = DataPO()

from PO.FakePO import *
Fake_PO = FakePO()

from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO(Configparser_PO.DB_SQL("host"), Configparser_PO.DB_SQL("user"), Configparser_PO.DB_SQL("password"), Configparser_PO.DB_SQL("database"), Configparser_PO.DB_SQL("charset"))
Sqlserver_PO2 = SqlServerPO(Configparser_PO.DB_SQL("host"), Configparser_PO.DB_SQL("user"), Configparser_PO.DB_SQL("password"), Configparser_PO.DB_SQL("database2"), Configparser_PO.DB_SQL("charset"))

# 获取随机姓名、地址及电话画面
# print(Fake_PO.genName('Zh_CN', 1))
# print(Fake_PO.genAddress('zh_CN', 1))
# Fake_PO.genPhone_number('Zh_CN', 1)
# 获取身份证和性别字典
varJMXM = Fake_PO.genName('Zh_CN', 1)
varIdcard = Fake_PO.genSsn('Zh_CN', 1)
varSex = Data_PO.getSex(varIdcard)
d_sex = {'男': 1, '女':2, '未知性别':3}

# todo QYYH（签约信息表）
# Sqlserver_PO.desc('QYYH')
# print(Sqlserver_PO.getTableComment('QYYH'))

# 1，获取医院信息表字典（机构）
d_hospital = {}
l_ = Sqlserver_PO2.select("select ORG_CODE,ORG_NAME from SYS_hospital")
for d in l_:
    d_hospital[d['ORG_CODE']]=d['ORG_NAME']
# print(d_hospital)  # {'0000001': '静安精神病院', 'csdm': '彭浦新村街道社区健康管理中心', ...

# 2，当前用户信息
l_ = Sqlserver_PO2.select("select NAME,THIRD_NO,ORG_CODE from SYS_USER where user_name='%s'" % (Configparser_PO.USER("user")))
varNAME = l_[0]['NAME']
# print(varNAME)  # 自动化  //家庭医生
varTHIRD_NO = l_[0]['THIRD_NO']
# print(varTHIRD_NO)  # 1100   //家庭医生的工号
varORG_CODE = l_[0]['ORG_CODE']
# print(varORG_CODE)  # a202020   //机构编号
l_ = Sqlserver_PO2.select("select ORG_NAME from SYS_hospital where org_code='%s'" % (varORG_CODE))
varORG_NAME = l_[0]['ORG_NAME']
# print(varORG_NAME)  # 自动化第六医院   //机构名称

# 3, 随机获取评估状态值(0:预评估；1:评估完成；2:未评估)
evaluationStatus = random.sample([0,1,2], 1)[0]
# print(evaluationStatus)

# 4，随机获取人群分类
l_category = ['0-6岁儿童', '学生（7-17岁）', '普通人群', '老年人', '未分类', '孕妇', '产妇']
d_category = dict(enumerate(l_category, start=1))
# print(d_category)  # {1: '0-6岁儿童', 2: '学生（7-17岁）', 3: '普通人群', 4: '老年人', 5: '未分类', 6: '孕妇', 7: '产妇'}
# print(list(d_category.keys()))  # [1, 2, 3, 4, 5, 6, 7]
randomCategoryKey = random.sample(list(d_category.keys()), 1)[0]
# print(randomCategoryKey, d_category[randomCategoryKey])   # 随机获取字典的key, 如：("2", d_category[2])


# todo HRPERSONBASICINFO(基本信息表)
# Sqlserver_PO.desc('HRPERSONBASICINFO')
# print(Sqlserver_PO.getTableComment('HRPERSONBASICINFO'))

def insert_HRPERSONBASICINFO():
    # 删除记录
    Sqlserver_PO.execute("delete from HRPERSONBASICINFO where ARCHIVENUM = '%s'" % (varIdcard))
    # 插入记录
    Sqlserver_PO.insert("HRPERSONBASICINFO",{"ARCHIVENUM":varIdcard, "NAME":varJMXM, "IDCARD":varIdcard, "CREATETIME":time.strftime("%Y-%m-%d %H:%M:%S")})



varGUID = Data_PO.getFigures(8)

# todo TB_EMPI_INDEX_ROOT(患者主索引表)
# Sqlserver_PO.desc('TB_EMPI_INDEX_ROOT')
# print(Sqlserver_PO.getTableComment('TB_EMPI_INDEX_ROOT'))

def insert_TB_EMPI_INDEX_ROOT():
    # 删除记录
    Sqlserver_PO.execute("delete from TB_EMPI_INDEX_ROOT where IDCARDNO = '%s'" % (varIdcard))
    # 插入记录
    Sqlserver_PO.insert("TB_EMPI_INDEX_ROOT", {"GUID":varGUID, "NAME":varJMXM, "IDCARDNO":varIdcard})



# todo TB_DC_CHRONIC_MAIN(慢心病防治随访主表)
# Sqlserver_PO.desc('TB_DC_CHRONIC_MAIN')
# print(Sqlserver_PO.getTableComment('TB_DC_CHRONIC_MAIN'))

def insert_TB_DC_CHRONIC_MAIN():
    # 删除记录
    Sqlserver_PO.execute("delete from TB_DC_CHRONIC_MAIN where EMPIGUID = '%s'" % (varGUID))
    # 插入记录
    varGUID2 = Data_PO.getFigures(11)
    Sqlserver_PO.insert("TB_DC_CHRONIC_MAIN",{"GUID":varGUID2, "MANAGENUM":varIdcard, "ORGCODE":"0000001", "EMPIGUID":varGUID})


# todo T_HIS_DIAGNOSIS(诊断疾病表)
# Sqlserver_PO.desc('T_HIS_DIAGNOSIS')
# print(Sqlserver_PO.getTableComment('T_HIS_DIAGNOSIS'))
def insert_T_HIS_DIAGNOSIS():
    # 删除记录
    Sqlserver_PO.execute("delete from T_HIS_DIAGNOSIS where IDCARD = '%s'" % (varIdcard))
    # 插入记录
    Sqlserver_PO.insert("T_HIS_DIAGNOSIS",{"IDCARD":varIdcard, "DIAGNOSIS_CODE":"G40"})



# todo TB_PREGNANT_MAIN_INFO(孕产妇信息表)
Sqlserver_PO.desc('TB_PREGNANT_MAIN_INFO')
# print(Sqlserver_PO.getTableComment('TB_PREGNANT_MAIN_INFO'))
def insert_TB_PREGNANT_MAIN_INFO(varIdcard):
    # 删除记录
    Sqlserver_PO.execute("delete from TB_PREGNANT_MAIN_INFO where ZJHM = '%s'" % (varIdcard))
    varYCFID = Data_PO.getFigures(8)
    # 插入记录
    Sqlserver_PO.insert("TB_PREGNANT_MAIN_INFO", {"YCFID":varYCFID, "JCH":"13", "XM":varJMXM, "ZJHM":varIdcard})


# todo TB_CHILDBIRTH_RECORD(分娩记录表)
# Sqlserver_PO.desc('TB_CHILDBIRTH_RECORD')
# print(Sqlserver_PO.getTableComment('TB_CHILDBIRTH_RECORD'))
def insert_TB_CHILDBIRTH_RECORD():
    # 删除记录
    Sqlserver_PO.execute("delete from TB_CHILDBIRTH_RECORD where ZJHM = '%s'" % (varIdcard))
    # 插入记录
    # Sqlserver_PO.insert("TB_CHILDBIRTH_RECORD", {"YCFID":?, "ZJHM":varIdcard, "XM":varJMXM})


# todo TB_POSTPARTUM_VISIT_RECORD(产后访视记录表)
# Sqlserver_PO.desc('TB_POSTPARTUM_VISIT_RECORD')
# print(Sqlserver_PO.getTableComment('TB_POSTPARTUM_VISIT_RECORD'))
def insert_TB_POSTPARTUM_VISIT_RECORD():
    # 删除记录
    # Sqlserver_PO.execute("delete from TB_POSTPARTUM_VISIT_RECORD where YCFID = '%s'" % (varYCFID))
    Sqlserver_PO.execute("delete from TB_POSTPARTUM_VISIT_RECORD WHERE YCFID in (SELECT YCFID FROM TB_PREGNANT_MAIN_INFO WHERE ZJHM = '%s'" % (varIdcard))
    # 插入记录
    # Sqlserver_PO.insert("TB_POSTPARTUM_VISIT_RECORD", {"YCFID":?, "JGCODE":"0000001", "XM":varJMXM})



# todo TB_DC_EXAMINATION_INFO(体检信息表)
# Sqlserver_PO.desc('TB_DC_EXAMINATION_INFO')
# print(Sqlserver_PO.getTableComment('TB_DC_EXAMINATION_INFO'))
def insert_TB_DC_EXAMINATION_INFO():
    # 删除记录
    Sqlserver_PO.execute("delete from TB_DC_EXAMINATION_INFO where GUID = '%s'" % (varGUID))
    # 插入记录
    # Sqlserver_PO.insert("TB_DC_EXAMINATION_INFO", {"GUID":varGUID, "ORGCODE":"0000001", "NAME":varJMXM})


# todo TB_DC_HTN_VISIT(高血压随访表)
# Sqlserver_PO.desc('TB_DC_HTN_VISIT')
# print(Sqlserver_PO.getTableComment('TB_DC_HTN_VISIT'))
def insert_TB_DC_HTN_VISIT():
    # 删除记录
    Sqlserver_PO.execute("delete from TB_DC_HTN_VISIT where GUID = '%s'" % (varGUID))
    # 插入记录
    # Sqlserver_PO.insert("TB_DC_HTN_VISIT", {"GUID":varGUID, "CARDID":varGUID, "ORGCODE":"0000001", "VISITDATE":?, "SBP":?, "DBP":?})



# todo TB_DC_DM_VISIT(糖尿病随访表)
# Sqlserver_PO.desc('TB_DC_DM_VISIT')
# print(Sqlserver_PO.getTableComment('TB_DC_DM_VISIT'))
def insert_TB_DC_DM_VISIT():
    # 删除记录
    Sqlserver_PO.execute("delete from TB_DC_DM_VISIT where GUID = '%s'" % (varGUID))
    # 插入记录
    # Sqlserver_PO.insert("TB_DC_DM_VISIT", {"GUID":varGUID, "CARDID":varGUID, "ORGCODE":"0000001", "VISITDATE":?, "SBP":?, "DBP":?})


# 签约信息表
# # 人群分类 CATEGORY_CODE":'4',"CATEGORY_NAME":d_category[4]
# Sqlserver_PO.insert("QYYH",{"CZRYBM":varTHIRD_NO, "CZRYXM":varNAME, "JMXM":varJMXM, "SJHM":Fake_PO.genPhone_number('Zh_CN',1),
#         "SFZH":varIdcard, "JJDZ":Fake_PO.genAddress('zh_CN', 1),"ARCHIVEUNITCODE":"0000001", "ARCHIVEUNITNAME":d_hospital["0000001"],
#         "SIGNSTATUS":1,"SIGNDATE":"2023-01-01", "CATEGORY_CODE":4,"CATEGORY_NAME":d_category[4],"LAST_SERVICE_DATE":"2023-05-06",
#         "KEY_POPULATION":1, "REPORT_STATUS":0, "LATEST_ASSESS_DATE":"2024-10-10", "LATEST_CONFIRM_DATE":"2024-11-11"})


# Sqlserver_PO.insert("QYYH",{"CZRYBM":varTHIRD_NO, "CZRYXM":varNAME, "JMXM":varJMXM, "SJHM":Fake_PO.genPhone_number('Zh_CN',1),
#         "SFZH":varIdcard, "JJDZ":Fake_PO.genAddress('zh_CN', 1),"ARCHIVEUNITCODE":"0000001", "ARCHIVEUNITNAME":d_hospital["0000001"],
#         "SIGNSTATUS":1,"SIGNDATE":"2023-01-01", "CATEGORY_CODE":7,"CATEGORY_NAME":d_category[7],"LAST_SERVICE_DATE":"2023-05-06",
#         "KEY_POPULATION":1, "REPORT_STATUS":0, "LATEST_ASSESS_DATE":"2024-10-10", "LATEST_CONFIRM_DATE":"2024-11-11"})

# 基本信息表
# insert_HRPERSONBASICINFO()

# 患者主索引表
# insert_TB_EMPI_INDEX_ROOT()

# 慢心病防治随访主表
# insert_TB_DC_CHRONIC_MAIN()

# 诊断疾病表
# insert_T_HIS_DIAGNOSIS()

# 孕产妇信息表
# insert_TB_PREGNANT_MAIN_INFO('150200195611167392')

# print(Sqlserver_PO.select("select * from TB_PREGNANT_MAIN_INFO WHERE ZJHM='150200195611167392'"))


# a = Sqlserver_PO.select("SELECT COLUMN_NAME FROM information_schema.key_column_usage where table_name='TB_PREGNANT_MAIN_INFO'")
# print(a)

# 分娩记录表
# insert_TB_CHILDBIRTH_RECORD()

# 体检信息表
# insert_TB_DC_EXAMINATION_INFO()

# 高血压随访表
# insert_TB_DC_HTN_VISIT()

# 糖尿病随访表
# insert_TB_DC_DM_VISIT()

# Sqlserver_PO.insert('TB_DC_CHRONIC_MAIN',{'GUID': '14449029827','VISITTYPECODE':'31','MANAGENUM':'32070719470820374X','ORGCODE':'0000001','EMPIGUID': '65209815'})


# Sqlserver_PO.desc('HRPERSONBASICINFO')
# print(Sqlserver_PO.getTableComment('HRPERSONBASICINFO'))