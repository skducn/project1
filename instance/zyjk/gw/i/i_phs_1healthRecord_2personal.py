# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2024-6-18
# Description   : 公卫接口，基本公卫 - 健康档案管理 - 个人健康档案
# 接口文档：http://192.168.0.203:38080/doc.html
# *****************************************************************
from GwPO_i import *
gw_i_PO = Gw_i_PO()
from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO(Configparser_PO.DB("host"), Configparser_PO.DB("user"), Configparser_PO.DB("password"), Configparser_PO.DB("database"), Configparser_PO.DB("charset"))  # 测试环境

# 1，登录 - 获取token
login_data = {
        "username": Configparser_PO.ACCOUNT("user"),
        "password": Configparser_PO.ACCOUNT("password"),
        "code": "",
        "uuid": ""
    }
encrypt_data = gw_i_PO.encrypt(json.dumps(login_data))
gw_i_PO.curlLogin(encrypt_data)  # {'user': '11012', 'token': 'eyJhbG...



# todo 基本公卫 - 健康档案管理 - 个人健康档案 - 查询
params = {"disease":[],"endBirthday":"","startBirthday":"","bloodTypeCode":"","categoryCode":[],"coverType":"0","isOpen":"","createOrgCode":"","creatorName":"","endAge":"","endDate":"","endExamDate":"","endUpdateDate":"","idCard":"","isDisability":"","isExam":"","isHighRisk":"","isSign":"","isUpdate":"","name":"","paymentMethodCode":"","phone":"","presentAddress":"","residenceCode":"","responsibleDocName":"","responsibleDocId":"","selectSource":"","sex":"","startAge":"","startDate":"","startExamDate":"","startUpdateDate":"","current":1,"size":20,"missItem":""}
encrypted_params = gw_i_PO.encrypt(json.dumps(params))
url = f"/server/tEhrInfo/findPage' -d '{encrypted_params}'"
r = gw_i_PO.curl('POST', url)
print(r)

# 列表页数据，匹配登录账号所在机构
# 如：10082账号所属机构（大秦家镇小杨家村卫生室，370685008001）
# select * from PHUSERS.dbo.t_ehr_info where MANAGE_ORG_CODE = (select org_sub_code from ZYCONFIG.dbo.sys_user where USER_NAME ='10082')

# # 从数据库里获取接口的信息，如名称，参数，url
l_d_result = Sqlserver_PO.select("select count(*) from PHUSERS.dbo.t_ehr_info where MANAGE_ORG_CODE = (select org_sub_code from ZYCONFIG.dbo.sys_user where USER_NAME ='10082')")
# print(l_d_result[0]['summary'])
# print(l_d_result[0]['query'])
print("接口url =>", l_d_result)


# todo 基本公卫 - 健康档案管理 - 个人健康档案 - 导出
params = {"disease":[],"endBirthday":"","startBirthday":"","bloodTypeCode":"","categoryCode":[],"coverType":"0","isOpen":"","createOrgCode":"","creatorName":"","endAge":"","endDate":"","endExamDate":"","endUpdateDate":"","idCard":"","isDisability":"","isExam":"","isHighRisk":"","isSign":"","isUpdate":"","name":"","paymentMethodCode":"","phone":"","presentAddress":"","residenceCode":"","responsibleDocName":"","responsibleDocId":"","selectSource":"","sex":"","startAge":"","startDate":"","startExamDate":"","startUpdateDate":"","current":1,"size":20,"missItem":""}
encrypted_params = gw_i_PO.encrypt(json.dumps(params))
url = f"/serverExport/tEhrInfo/exportEhr' -d '{encrypted_params}'"
r = gw_i_PO.curl('POST', url)
print(r)