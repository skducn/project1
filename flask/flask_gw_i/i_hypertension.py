# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2024-6-18
# Description   : 公卫接口，高血压专项
# 接口文档：http://192.168.0.203:38080/doc.html
# web：http://192.168.0.203:30080  11012
# 在线SM2公钥私钥对生成，加密/解密 https://config.net.cn/tools/sm2.html
# privateKey = 00c68ee01f14a927dbe7f106ae63608bdb5d2355f18735f7bf1aa9f2e609672681
# publicKey = 047e2c1440d05e86f9677f710ddfd125aaea7f3a390ce0662f9ef9f5ff1fa860d5174251dfa99e922e224a51519a53cd71063d81e64345a0c352c4eb68d88b0cc9
# 【腾讯文档】项目信息表
# https://docs.qq.com/sheet/DYmZMVmFTeXFWRFpQ?tab=BB08J2
# *****************************************************************
from GwPO_i import *
Gw_PO_i = GwPO_i()
from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO(Configparser_PO.DB("host"), Configparser_PO.DB("user"), Configparser_PO.DB("password"), Configparser_PO.DB("database"), Configparser_PO.DB("charset"))  # 测试环境

# 1，登录 - 获取token
login_data = {
        "username": Configparser_PO.ACCOUNT("user"),
        "password": Configparser_PO.ACCOUNT("password"),
        "code": "",
        "uuid": ""
    }
encrypt_data = Gw_PO_i.encrypt(json.dumps(login_data))
Gw_PO_i.curlLogin(encrypt_data)  # {'user': '11012', 'token': 'eyJhbG...



# 新增高血压管理卡(参数：# 确诊日期，管理级别，建卡时间，建卡医生)
Gw_PO_i.newHypertensionManagementCard('{"idCard":"310101195001293595"}', {"qzrq": "2025-03-01" ,"gljbbm": "1", "jksj": "2025-03-03", "jkysxm": "金浩1"})