# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2024-6-18
# Description   : 公卫接口，首页
# 接口文档：http://192.168.0.203:38080/doc.html
# web：http://192.168.0.203:30080  testwjw, Qa@123456

# 在线国密SM2加密/解密 https://the-x.cn/zh-cn/cryptography/Sm2.aspx
# 在线SM2公钥私钥对生成，加密/解密 https://config.net.cn/tools/sm2.html
# privateKey = 00c68ee01f14a927dbe7f106ae63608bdb5d2355f18735f7bf1aa9f2e609672681
# publicKey = 047e2c1440d05e86f9677f710ddfd125aaea7f3a390ce0662f9ef9f5ff1fa860d5174251dfa99e922e224a51519a53cd71063d81e64345a0c352c4eb68d88b0cc9

# 【腾讯文档】项目信息表
# https://docs.qq.com/sheet/DYmZMVmFTeXFWRFpQ?tab=BB08J2
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



# todo 首页 - 档案概况，三高概况，重点人群分布情况，健康档案
r = gw_i_PO.curl('GET', "/server/tHome/getHomePageData")
print(r)  # {'code': 200, 'msg': None, 'data': {'total': 129, 'familyTotal': 109, 'signTotal': None, 'currentSignTotal': None, 'threeHighResidents': 1, 'residentsOfLianggao': 6, 'gxyTotal': 19, 'tnbTotal': 11, 'gxzTotal': 11, 'dbtTotal': 4, 'chdTotal': 3, 'tbTotal': 5, 'disTotal': 7, 'smiTotal': 9, 'snrTotal': 16, 'pwTotal': 7, 'childTotal': 20, 'gxyTotalRate': 14.73, 'tnbTotalRate': 8.53, 'gxzTotalRate': 8.53, 'dbtTotalRate': 3.1, 'chdTotalRate': 2.33, 'tbTotalRate': 3.88, 'disTotalRate': 5.43, 'smiTotalRate': 6.98, 'snrTotalRate': 12.4, 'pwTotalRate': 5.43, 'childTotalRate': 15.5, 'transferOutNum': 0, 'switchTeamNum': 0, 'rescindNum': 0, 'deathToll': 14, 'notYetManagedToll': 3}}


# todo 首页 - 任务提醒
# r = gw_i_PO.curl('GET', "/server/tHome/getHomeSumData?0=" + gw_i_PO.encrypt('{"type":"1"}'))
# print(r)  # {'code': 200, 'msg': None, 'data': {'gxyNum': 10, 'tnbNum': 8, 'childNum': 8, 'pwNum': 3, 'tbNum': 6, 'disNum': 2, 'smiNum': 2}}
params = {"type": "1"}
encrypted_params = gw_i_PO.encrypt(json.dumps(params))
url = f"/server/tHome/getHomeSumData?0={encrypted_params}"
r = gw_i_PO.curl('GET', url)
print(r)



