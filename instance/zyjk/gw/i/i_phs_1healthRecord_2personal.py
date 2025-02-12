# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2024-6-18
# Description   : 公卫接口，基本公卫 - 健康档案管理 - 个人健康档案
# 接口文档：http://192.168.0.203:38080/doc.html
# *****************************************************************
from Gw_i_PO import *
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



