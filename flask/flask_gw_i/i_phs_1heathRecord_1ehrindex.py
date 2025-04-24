# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2024-6-18
# Description   : 公卫接口，基本公卫 - 健康档案管理 - 健康档案概况
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
gw_i_PO.curlLogin(encrypt_data)



# # todo 基本公卫 - 健康档案管理 - 健康档案概况（默认无选择, 招远市卫健局）
# 注意：本年度档案更新人数中的未更新人数是通过计算获取，即 未更新人数 = 个人在管理档案 - 已更新人数
params = {"orgCode": ""}
encrypted_params = gw_i_PO.encrypt(json.dumps(params))
url = f"/server/tEhrInfo/getEhrHomeInfo?0={encrypted_params}"
r = gw_i_PO.curl('GET', url)
print(r)

# # 从数据库里获取接口的信息，如名称，参数，url
# l_d_result = Sqlserver_PO.select("select summary, query, url from a_phs_server where path='/tEhrInfo/getEhrHomeInfo'")
# # print(l_d_result[0]['summary'])
# # print(l_d_result[0]['query'])
# print("接口url =>", l_d_result[0]['url'])


# # todo 基本公卫 - 健康档案管理 - 健康档案概况（招远市卫健局 - 大秦家卫生院 - 大秦家镇小杨家村卫生室）
# 注意：本年度档案更新人数中的未更新人数是通过计算获取，即 未更新人数 = 个人在管理档案 - 已更新人数
params = {"orgCode": "370685008001"}
encrypted_params = gw_i_PO.encrypt(json.dumps(params))
url = f"/server/tEhrInfo/getEhrHomeInfo?0={encrypted_params}"
r = gw_i_PO.curl('GET', url)
print(r)


