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


user_name = 'jh'

# 获取医院信息表字典（机构）
d_hospital = {}
l_ = Sqlserver_PO2.select("select ORG_CODE,ORG_NAME from SYS_hospital")
for d in l_:
    d_hospital[d['ORG_CODE']]=d['ORG_NAME']
# print(d_hospital)  # {'0000001': '静安精神病院', 'csdm': '彭浦新村街道社区健康管理中心', ...


l_ = Sqlserver_PO2.select("select THIRD_NO,ORG_CODE from SYS_USER where user_name='%s'" % (user_name))
varTHIRD_NO = l_[0]['THIRD_NO']
print(varTHIRD_NO)  # 2019   //家庭医生的工号
# 获取当前登录家庭医生的机构号
varORG_CODE = l_[0]['ORG_CODE']
print(varORG_CODE)  # 202020   //机构编号
# l_ = Sqlserver_PO2.select("select ORG_NAME from SYS_hospital where org_code='%s'" % (varORG_CODE))
# varORG_NAME = l_[0]['ORG_NAME']
# print(varORG_NAME)  # 自动化第六医院   //机构名

# sys.exit(0)

# 获取随机姓名、地址及电话画面
# print(Fake_PO.genName('Zh_CN', 1))
# print(Fake_PO.genAddress('zh_CN', 1))
# Fake_PO.genPhone_number('Zh_CN', 1)

# 随机获取人群分类
l_category = ['0-6岁儿童', '学生（7-17岁）', '普通人群', '老年人', '未分类', '孕妇', '产妇']
d_category = dict(enumerate(l_category, start=1))
# print(d_category)  # {1: '0-6岁儿童', 2: '学生（7-17岁）', 3: '普通人群', 4: '老年人', 5: '未分类', 6: '孕妇', 7: '产妇'}
# print(list(d_category.keys()))  # [1, 2, 3, 4, 5, 6, 7]  //# 随机获取字典的key
categoryKey = random.sample(list(d_category.keys()), 1)[0]
# print(categoryKey, d_category[categoryKey])
# print("2", d_category[2])  # 2 学生（7-17岁）

# 获取身份证和性别字典
varIdCard = Fake_PO.genSsn('Zh_CN', 1)
varSex = Data_PO.getSex(varIdCard)
d_sex = {'男': 1, '女':2, '未知性别':3}

# 随机获取评估状态值(0:预评估；1:评估完成；2:未评估)
evaluationStatus = random.sample([0,1,2], 1)[0]
# print(evaluationStatus)



def insert(d_param):

    # 插入签约信息表记录

    # 参数：{"ARCHIVEUNITCODE":ORG_CODE, "ARCHIVEUNITNAME":d_hospital[ORG_CODE], "SIGNSTATUS":"1","SIGNDATE":"2024-01-01","CATEGORY_CODE":'2',"CATEGORY_NAME":d_category['2'], "LAST_SERVICE_DATE":"2024-03-03","REPORT_STATUS":"1"}

    Sqlserver_PO.execute('set identity_insert QYYH on')
    # 获取最大ID+1
    l_ = Sqlserver_PO.select('select max(ID) as id from QYYH')
    varID = l_[0]['id'] + 1
    # print(varID)

    varJMXM = Fake_PO.genName('Zh_CN', 1)
    Sqlserver_PO.execute("insert into QYYH(CZRYBM, CZRYXM, JMXM, SJHM, SFZH, JJDZ, SFJD, SIGNORGID, ARCHIVEUNITCODE, "
                         "ARCHIVEUNITNAME, DISTRICTORGCODE, DISTRICTORGNAME, TERTIARYORGCODE, TERTIARYORGNAME, "
                         "PRESENTADDRDIVISIONCODE, PRESENTADDRPROVCODE, PRESENTADDRPROVVALUE, PRESENTADDRCITYCODE, "
                         "PRESENTADDRCITYVALUE, PRESENTADDRDISTCODE, PRESENTADDDISTVALUE, PRESENTADDRTOWNSHIPCODE, "
                         "PRESENTADDRTOWNSHIPVALUE, PRESENTADDRNEIGHBORHOODCODE, PRESENTADDRNEIGHBORHOODVALUE, SIGNSTATUS, "
                         "SIGNDATE, ID, CATEGORY_CODE, CATEGORY_NAME, SEX_CODE, SEX_NAME, LAST_SERVICE_DATE, ASSISTANT_DOC_ID, "
                         "ASSISTANT_DOC_NAME, HEALTH_MANAGER_ID, HEALTH_MANAGER_NAME, ASSISTANT_DOC_PHONE, HEALTH_MANAGER_PHONE, KEY_POPULATION, "
                         "REPORT_STATUS, ASSESS_ORDER, STOP_ASSESS_STATUS, STOP_ASSESS_DATA, STOP_ASSESS_DOC_ID, STOP_ASSESS_DOC_NAME, LATEST_ASSESS_DATE, LATEST_CONFIRM_DATE) "
                         "values "
                         "('%s','令狐冲','%s','%s','%s','%s','','',"
                         "'%s','%s','310118000000','青浦区','111111','上海人民医院','','','','','','','','','','','',"
                         "%s,'%s',%s,'%s','%s','%s','%s','%s',1,'家医助理姓名',2,'健康管理师姓名','%s','%s',%s,%s,2,0,'2029-10-10',-1,'章三','%s','%s')"
                         % (Data_PO.getFigures(6), varJMXM, Fake_PO.genPhone_number('Zh_CN',1), varIdCard,
                            Fake_PO.genAddress('zh_CN', 1), d_param['ARCHIVEUNITCODE'], d_param['ARCHIVEUNITNAME'],
                            d_param["SIGNSTATUS"], d_param["SIGNDATE"], varID, d_param["CATEGORY_CODE"], d_param["CATEGORY_NAME"],
                            d_sex[varSex], varSex, d_param["LAST_SERVICE_DATE"], Fake_PO.genPhone_number('Zh_CN', 1),
                            Fake_PO.genPhone_number('Zh_CN', 1), d_param["KEY_POPULATION"], d_param["REPORT_STATUS"], d_param["LATEST_ASSESS_DATE"], d_param["LATEST_CONFIRM_DATE"]))
    Sqlserver_PO.execute('set identity_insert QYYH off')
    print("QYYH => " + varJMXM + ", " + varIdCard)


insert({"ARCHIVEUNITCODE":varORG_CODE, "ARCHIVEUNITNAME":d_hospital[varORG_CODE],"SIGNSTATUS":1,"SIGNDATE":"2024-01-01",
        "CATEGORY_CODE":'2',"CATEGORY_NAME":d_category[2],"LAST_SERVICE_DATE":"2024-03-03","KEY_POPULATION":1, "REPORT_STATUS":1,
        "LATEST_ASSESS_DATE":"2024-10-10", "LATEST_CONFIRM_DATE":"2024-11-11"})


